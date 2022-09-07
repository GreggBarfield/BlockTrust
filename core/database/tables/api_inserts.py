import json
import datetime
from ...utilities.email import send_email
from ...config import ADMIN_EMAIL

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
                api_insert_datetime = api_insert["created"]
                earliest_date = datetime.datetime.now() - datetime.timedelta(days=7)
                if api_insert_datetime < earliest_date:
                    print("More than a week old insert")
                    print(ADMIN_EMAIL)
                    email_subject = "No API Insert in past 7+ days"
                    email_body = "No API insert in the last 7+ days for account: " + partner
                    send_email(email_subject, email_body, ADMIN_EMAIL)

