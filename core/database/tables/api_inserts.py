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

    def check_for_partner_api_inserts(self, number_of_days=1):
        """
        Checks for API inserts for the specified number of days
        """
        partners = ["MFA Health Track", "RED ANGUS"]
        for partner in partners:
            self._db.execute_d(
                """
                SELECT count(*) as inserts_count FROM api_inserts
                WHERE account in (SELECT id FROM accounts WHERE company = %(company)s)
                AND DAY(created) > DAY(current_date())-%(number_of_days)s
                """, {
                    "company": partner,
                    "number of days": number_of_days
                }
            )
