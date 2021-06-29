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
                "response": json.dumps(response),  
            }
        )
    
    # Get the last questionnaire the user submit
    def getResponse(self,account):
        response= self._db.execute_d(
            """
            SELECT sustainability.response AS response
            FROM sustainability WHERE account=%(account)s ORDER BY (id) DESC LIMIT 1
            """,
            {
                "account": account,
            }
        )
        return response[0]
