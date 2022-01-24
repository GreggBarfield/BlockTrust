import json

from ..no_value import NoValue

NO_VALUE = NoValue()

class Sustainability:
    def __init__(self, db):
        self._db = db

    def insert(self, account, response, sectorScoreCounterJSON):
        sectorScoreCounter = json.loads(sectorScoreCounterJSON)

        air_score = None
        land_score = None
        water_score = None
        animal_score = None
        safety_score = None
        efficiency_score = None
        total_score = None

        for section in sectorScoreCounter:
            if section == 'air':
                air_score = json.dumps(sectorScoreCounter[section])
            elif section == 'land':
                land_score = json.dumps(sectorScoreCounter[section])
            elif section == 'water':
                water_score = json.dumps(sectorScoreCounter[section])
            elif section == 'animal':
                animal_score = json.dumps(sectorScoreCounter[section])
            elif section == 'safety':
                safety_score = json.dumps(sectorScoreCounter[section])
            elif section == 'efficiency':
                efficiency_score = json.dumps(sectorScoreCounter[section])
            elif section == 'allSections':
                total_score = json.dumps(sectorScoreCounter[section])

        self._db.execute(
            """INSERT INTO sustainability
                (account, total_score, air_score, land_score, water_score, 
                    animal_score, safety_score, efficiency_score, response)
                VALUES (%(account)s, %(total_score)s, %(air_score)s, %(land_score)s, 
                        %(water_score)s, %(animal_score)s, %(safety_score)s, 
                        %(efficiency_score)s, %(response)s)
            """,
            {
                "account": account,
                "total_score": total_score,
                "air_score": air_score,
                "land_score": land_score,
                "water_score": water_score,
                "animal_score": animal_score,
                "safety_score": safety_score,
                "efficiency_score": efficiency_score,
                "response": json.dumps(response),
            }
        )

    def get_sustainability_by_account(self, account, withAccountDetails=False):
        if withAccountDetails:
            data = self._db.execute_d(
                """SELECT a.id, a.name, a.sector, s.response
                FROM sustainability AS s
                INNER JOIN accounts AS a ON s.account=a.id
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
                    "account": account
                })

            return data

    def get_sustainability_by_sector(self, sectorID):
        data = self._db.execute_d(
            """SELECT s.*, a.sector, a.company FROM sustainability AS s
               INNER JOIN accounts AS a ON s.account=a.id
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

    def get_sustainability(self, account=NO_VALUE, response=NO_VALUE, 
                                created_timestamp=NO_VALUE, order_by_column=NO_VALUE,
                                order_desc=False):
        """
        Get sustainability by the values specified.

        Returns:
            A list of sustainability(s) record if found else []
        """

        # base query
        base_query = "SELECT * FROM sustainability"

        query_conditions = []
        query_values = {}

        if account is not NO_VALUE:
            query_conditions.append(" account = %(account)s")
            query_values["account"] = account

        if response is not NO_VALUE:
            query_conditions.append(" response = %(response)s")
            query_values["response"] = response

        if created_timestamp is not NO_VALUE:
            query_conditions.append(" created_timestamp = %(created_timestamp)s")
            query_values["created_timestamp"] = created_timestamp

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        order_condition = ""

        if order_by_column is not NO_VALUE:
            order_condition = " ORDER BY %(order_by_column)s"
            query_values["order_by_column"] = order_by_column
            if order_desc:
                order_condition += " DESC"

        query = base_query + combined_query_condition + order_condition

        sustainability_rows = self._db.execute_d(query, query_values)
        if len(sustainability_rows) > 0:
            return sustainability_rows
        else:
            return []
