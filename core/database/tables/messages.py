import time
from ...common_exceptions import ExportException

class MessagesException(Exception):
    """Messages generic exception."""

    def __init__(self, reason):
        """Constructor for MessagesException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class Messages:

    def __init__(self, db):
        self._db = db

    def insert_message(self, from_account, to_account, data):
        """Inserts a message.

        Params:
            from_account: The account the message is from (id)
            to_account: The account the message is to (id)
            data: The data in the message

        Returns:
            The ID of the message inserted
        """
        self._db.execute("""
            INSERT INTO messages (from_account, to_account, data, time_sent)
                VALUES (%(from_account)s, %(to_account)s, %(data)s, %(time_sent)s)
        """,
            {
                "from_account": from_account,
                "to_account": to_account,
                "data": data,
                "time_sent": int(time.time())
            }
        )
        return self._db.last_row_id()

    def get(self, from_account, to_account):
        """Gets all messages where...

        Params:
            from_account: Where from_account is this
            to_account: Where to_account is this
        
        Returns:
            A list of dictionaries (rows)

            The rows are also enhanced with "from_name" and "to_name"
                (could be null!)
        """
        where_clauses = []
        values = []

        if from_account is not None:
            where_clauses += ["from_account=%s"]
            values += [from_account]

        if to_account is not None:
            where_clauses += ["to_account=%s"]
            values += [to_account]

        if len(where_clauses) == 0:
            raise ValueError("from_account and to_account None")

        where_clause_total = ' OR '.join(where_clauses)

        rows = self._db.execute_d("""
            SELECT messages.*,
                    from_account_table.name AS from_name,
                    to_account_table.name AS to_name
                FROM messages
				LEFT JOIN accounts AS from_account_table
					ON messages.from_account=from_account_table.id
				LEFT JOIN accounts AS to_account_table
					ON messages.to_account=to_account_table.id
                WHERE """ + where_clause_total + """
                ORDER BY id DESC
        """,
            values
        )
        return rows
