import json

class ApiInserts:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id, namespace, type, data):
        """Inserts data into table.

        Params:
            data: the data to be added
        """
        self._db.execute(
            """INSERT INTO api_inserts
                (account, namespace, type, fields)
                VALUES
                    (%(account)s, %(namespace)s, %(type)s, %(fields)s)
            """,
            {
                "account": account_id,
                "namespace": namespace,
                "type": type,
                "fields": json.dumps(data)
            }
        )
