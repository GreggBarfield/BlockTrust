import json


class RejectedRegistrations:

    def __init__(self, db):
        self._db = db

    def insert_rejected_registration(self, details, recaptcha_response):
        """Inserts registration rejected.
        """
        try:
            self._db.execute(
                """INSERT INTO rejected_registrations
                    (details, recaptcha_response)
                    VALUES
                        (%(details)s, %(recaptcha_response)s)
                """,
                {
                    "details": json.dumps(details),
                    "recaptcha_response": json.dumps(recaptcha_response)      
                }
            )
        except Exception as e:
            print(e)