import json
import datetime

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

    def check_for_partner_api_inserts(self):
        """
        Checks for API inserts for the specified number of days
        """
        # partners = ["MFA Health Track", "RED ANGUS"]
        partners = ["ABCD"]
        for partner in partners:
            latest_api_insert = self._db.execute_d(
                """
                SELECT * FROM api_inserts
                WHERE account in (SELECT id FROM accounts WHERE company = %(company)s)
                ORDER BY created DESC LIMIT 1
                """, {
                    "company": partner
                }
            )
            if len(latest_api_insert) > 0:
                api_insert = latest_api_insert[0]
                f = '%Y-%m-%d %H:%M:%S'
                api_insert_timestamp = api_insert["created"]
                api_insert_datetime = datetime.datetime.strptime(api_insert_timestamp, f)
                print(api_insert_datetime)
