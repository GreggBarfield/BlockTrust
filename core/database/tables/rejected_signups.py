import json


class RejectedSignups:

    def __init__(self, db):
        self._db = db

    def insert_rejected_signup(self, details, recaptcha_score):
        """Inserts Error Log.
        """
        try:
            self._db.execute(
                """INSERT INTO rejected_signups
                    (details, recaptcha_score)
                    VALUES
                        (%(details)s, %(recaptcha_score)s)
                """,
                {
                    "details": json.dumps(details),
                    "recaptcha_score": recaptcha_score      
                }
            )
        except Exception as e:
            print(e)