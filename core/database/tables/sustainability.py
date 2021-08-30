import json
import datetime

class Sustainability:
    def __init__(self, db):
        self._db = db

    def insert(self, account, response):
        self._db.execute(
            """INSERT INTO sustainability
                (account, response, created_timestamp)
                VALUES (%(account)s, %(response)s, %(timeStamp)s)
            """,
            {
                "account": account,
                "response": json.dumps(response),  # Does this need to be converted to a string first?
                "timeStamp": datetime.datetime.now()
            }
        )

    def get_by_account(self, account):
        data = self._db.execute_d(
            """SELECT * FROM sustainability 
            WHERE account=%(account)s
            ORDER BY created_timestamp DESC
            """,
            {
                "account": account,
            })

        return data