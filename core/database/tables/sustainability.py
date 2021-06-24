import json
class Sustainability:
    def __init__(self, db):
        self._db = db
    def insert(self,username, response):
        self._db.execute(
            """INSERT INTO sustainability
                (username, response)
                VALUES (%(username)s, %(response)s)
            """,
            {
                "username": username,
                "response": json.dumps(response),  # Does this need to be converted to a string first?
            }
        )
