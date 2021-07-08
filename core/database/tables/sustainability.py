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

    def check(self, account, response):
        row = self._db.execute_d(
            """SELECT * FROM sustainability 
            WHERE account=%(account)s
            """,
            {
                "account": account,
            })
        
        if(row is None):
            self.insert(account,response)
        else:
            self.update(account,response)

    def update(self,account, response):
        self._db.execute(
             """
             UPDATE
                `sustainability`
                SET
                `response` =  %(response)s
                WHERE
                (`account` = %(account)s);
            """,
            {
                "account": account,
                "response": json.dumps(response),  # Does this need to be converted to a string first?
            }
        )
