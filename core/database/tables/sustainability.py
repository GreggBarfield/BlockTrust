import json
class Sustainability:
    def __init__(self, db):
        self._db = db
    def insert(self,account, response):
        self._db.execute(
            """INSERT INTO sustainability
                (account, response)
                VALUES (%(account)s, %(response)s)
            """,
            {
                "account": account,
                "response": json.dumps(response),  # Does this need to be converted to a string first?
            }
        )
