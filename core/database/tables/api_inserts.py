import json
import datetime
from ...utilities.email import send_email
from ...config import ADMIN_EMAIL


HEALTH_TRACK_PARTNER_NAME = "MFA Health Track"
RED_ANGUS_PARTNER_NAME = "Red Angus Assoc"


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
        Checks for API inserts
        """
        partners = [HEALTH_TRACK_PARTNER_NAME, RED_ANGUS_PARTNER_NAME]
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
                api_insert_datetime = api_insert["created"]
                days_since_last_api_insert_datetime = datetime.datetime.now() - api_insert_datetime
                days_since_last_api_insert = days_since_last_api_insert_datetime.days
                weeks_since_last_api_insert = days_since_last_api_insert / 7
                if weeks_since_last_api_insert >= 1 and days_since_last_api_insert % 7 == 0:
                    email_subject = "API Update"
                    email_body = "No API insert in the last " + str(int(weeks_since_last_api_insert)) + " week(s) for account: " + partner
                    send_email(email_subject, email_body, ADMIN_EMAIL)

