from enum import Enum
import json
import mysql.connector as mysql
from core.database.database import Database


statuses_by_id = {
    0: "Pending",
    1: "Done",
    2: "Blocked",
    3: "Running",
    4: "Bad Namespace",
    5: "Bad Type",
    6: "Exception"
}
statuses_by_name = {b: a for a, b in statuses_by_id.items()}


priority = {
    0: "Low",
    1: "High"
}

# Note that the blocking system is currently limited to a single block per insert


class BlockNotAvailable(Exception):
    pass


class InsertsModel:

    def __init__(self, mysql_config):
        """Construct the InsertsModel.

        Params:
            mysql_config: The configuration to pass to MySQL
        """
        self._connection = mysql.connect(**mysql_config)
        self._cur = self._connection.cursor(dictionary=True)

    @staticmethod
    def _process_row(row):
        json_fields = ['api_blocks.value', 'fields', 'row']
        for f in json_fields:
            if row[f] is not None and row[f] != "":
                row[f] = json.loads(row[f])
            else:
                row[f] = None

        # Legacy support: fields is now dictionary
        if (
            not isinstance(row['fields'], dict)
        ):
            if row['fields'] is None:
                row['fields'] = {}
            else:
                row['fields'] = {a[0]: a[1] for a in zip(row['fields'], row['row'])}
        return row

    def get_next(self):
        """Get the next insert.

        Returns:
            None if none are available, or a dictionary of the insert
        """
        results = Database._expand_multi(self._cur.execute(
            """
                LOCK TABLES api_inserts WRITE, api_blocks WRITE;
                SET @insert_id = (
                    SELECT id FROM api_inserts WHERE status=%(pending_status)s
                    ORDER BY priority DESC, id ASC
                    LIMIT 1
                );
                UPDATE api_inserts SET status=%(running_status)s WHERE id=@insert_id;
                SELECT api_inserts.*, api_blocks.value AS 'api_blocks.value',
                    api_blocks.resolved AS 'api_blocks.resolved'
                    FROM api_inserts
                    LEFT JOIN api_blocks ON api_blocks.id=api_inserts.block
                    WHERE api_inserts.id=@insert_id;
                UNLOCK TABLES;
            """,
            {
                'pending_status': statuses_by_name['Pending'],
                'running_status': statuses_by_name['Running']
            },
            multi=True
        ))
        rows = results[3]
        return InsertsModel._process_row(rows[0]) if rows else None

    def set_status(self, insert_id, status_name):
        """Sets the status.

        Params:
            insert_id: The insert's ID
            status_name: The status to apply
        """
        self._cur.execute(
            """
                UPDATE api_inserts SET status=%(status)s WHERE id=%(insert_id)s;
            """,
            {
                'status': statuses_by_name[status_name],
                'insert_id': insert_id
            }
        )

    def emit_block(self, key, value):
        """Ensures that a block exists with the matching key value.

        Params:
            key: A string less than 200 characters
            value: A json-serializable value
        """
        if len(key) > 200:
            raise RuntimeError("Key is too long for emitted block")
        # Is this just splitting it by semicolon and then running them individually?
        # If so, using the multi thing is pointless... need to look into why expand
        # needs to be fed
        Database._expand_multi(self._cur.execute(
            """
                LOCK TABLES api_inserts WRITE, api_blocks WRITE;
                INSERT INTO api_blocks (`key`, resolved, value)
                    VALUES (%(key)s, 1, %(value)s)
                    ON DUPLICATE KEY UPDATE value=%(value)s, resolved=1;
                UPDATE api_inserts SET api_inserts.status=%(status_pending)s
                    WHERE api_inserts.status=%(status_blocked)s AND api_inserts.block=(
                        SELECT api_blocks.id FROM api_blocks WHERE api_blocks.`key`=%(key)s
                    );
                UNLOCK TABLES;
            """,
            {
                'key': key,
                'value': json.dumps(value),
                'status_pending': statuses_by_name['Pending'],
                'status_blocked': statuses_by_name['Blocked']
            },
            multi=True
        ))

    def blocked_on(self, key, insert_id):
        """Gets the value for a block.

        Inserts a new block and/or marks the insert as blocked in cases.

        Returns:
            The block value

        Raises:
            BlockNotAvailable on the block being unresolved
        """
        if len(key) > 200:
            raise RuntimeError("Key is too long for block")

        # bad code but needs to be concurrent
        # the plan is soon to not be using this system anyways so whatever

        # barely avoiding using functions/procedures for if statements

        results = Database._expand_multi(self._cur.execute(
            """
                SET @block_key = %(key)s;
                SET @block_id = NULL;
                SET @block_resolved = NULL;
                SET @block_value = NULL;
                LOCK TABLES api_inserts WRITE, api_blocks WRITE;
                INSERT INTO api_blocks (`key`, resolved)
                    VALUES (@block_key, 0)
                    ON DUPLICATE KEY UPDATE resolved=resolved;
                SELECT @block_value:=value, @block_id:=id, @block_resolved:=resolved
                    FROM api_blocks
                    WHERE `key`=@block_key;
                SELECT @block_value AS value, @block_resolved AS resolved;
                UPDATE api_inserts SET status=%(blocked_status)s, block=@block_id
                    WHERE (@block_value IS NULL) AND api_inserts.id=%(id)s;
                UNLOCK TABLES;
            """,
            {
                'key': key,
                'id': insert_id,
                'blocked_status': statuses_by_name['Blocked']
            },
            multi=True
        ))

        result = results[7][0]
        value = result['value']
        resolved = result['resolved']
        if resolved is None or resolved == 0:
            raise BlockNotAvailable()
        return value
