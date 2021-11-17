import json

class Sustainability:
    def __init__(self, db):
        self._db = db

    def insert(self, account, response):
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

    def get_by_account(self, account, withAccountDetails=False):
        if withAccountDetails:
            data = self._db.execute_d(
                """SELECT a.id, a.name, a.sector, s.response
                FROM sustainability AS s
                JOIN accounts AS a ON s.account=a.id
                WHERE account=%(account)s
                ORDER BY s.created_timestamp DESC
                """,
                {
                    "account": account,
                })

            return data
        else:
            data = self._db.execute_d(
                """SELECT * FROM sustainability 
                WHERE account=%(account)s
                ORDER BY created_timestamp DESC
                """,
                {
                    "account": account,
                })

            return data

    def get_by_sector(self, sectorID):
        data = self._db.execute_d(
            """SELECT s.*, a.sector, a.company FROM sustainability AS s
               join accounts AS a ON s.account=a.id
               WHERE s.created_timestamp = ANY (
		        SELECT MAX(created_timestamp) AS most_recent FROM sustainability
		        GROUP BY account
	           )
               AND a.sector = %(sector)s;
            """,
            {
                "sector": sectorID,
            })

        return data