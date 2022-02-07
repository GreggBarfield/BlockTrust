import json

from ..no_value import NoValue

NO_VALUE = NoValue()

class Sustainability:
    def __init__(self, db):
        self._db = db

    def insert(self, account, response, sectorScoreCounterJSON):
        sectorScoreCounter = json.loads(sectorScoreCounterJSON)
        # First Score = Excellent
        # Second Score = Acceptable
        # Third Score = Needs Work

        air_first_score = None
        air_second_score = None
        air_third_score = None
        land_first_score = None
        land_second_score = None
        land_third_score = None
        water_first_score = None
        water_second_score = None
        water_third_score = None
        animal_first_score = None
        animal_second_score = None
        animal_third_score = None
        safety_first_score = None
        safety_second_score = None
        safety_third_score = None
        efficiency_first_score = None
        efficiency_second_score = None
        efficiency_third_score = None

        for section in sectorScoreCounter:
            if section == 'air':
                air_first_score = sectorScoreCounter[section]["excellent"]
                air_second_score = sectorScoreCounter[section]["acceptable"]
                air_third_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'land':
                land_first_score = sectorScoreCounter[section]["excellent"]
                land_second_score = sectorScoreCounter[section]["acceptable"]
                land_third_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'water':
                water_first_score = sectorScoreCounter[section]["excellent"]
                water_second_score = sectorScoreCounter[section]["acceptable"]
                water_third_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'animal':
                animal_first_score = sectorScoreCounter[section]["excellent"]
                animal_second_score = sectorScoreCounter[section]["acceptable"]
                animal_third_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'safety':
                safety_first_score = sectorScoreCounter[section]["excellent"]
                safety_second_score = sectorScoreCounter[section]["acceptable"]
                safety_third_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'efficiency':
                efficiency_first_score = sectorScoreCounter[section]["excellent"]
                efficiency_second_score = sectorScoreCounter[section]["acceptable"]
                efficiency_third_score = sectorScoreCounter[section]["needsWork"]

        self._db.execute(
            """INSERT INTO sustainability
                (account, air_first_score, air_second_score, air_third_score, 
                land_first_score, land_second_score, land_third_score, 
                water_first_score, water_second_score, water_third_score, 
                animal_first_score, animal_second_score, animal_third_score, 
                safety_first_score, safety_second_score, safety_third_score, 
                efficiency_first_score, efficiency_second_score, 
                efficiency_third_score, response)
                VALUES (%(account)s, %(air_first_score)s, %(air_second_score)s, 
                        %(air_third_score)s, %(land_first_score)s, %(land_second_score)s,
                        %(land_third_score)s, %(water_first_score)s, 
                        %(water_second_score)s, %(water_third_score)s,
                        %(animal_first_score)s, %(animal_second_score)s,
                        %(animal_third_score)s, %(safety_first_score)s,
                        %(safety_second_score)s, %(safety_third_score)s,
                        %(efficiency_first_score)s, %(efficiency_second_score)s,
                        %(efficiency_third_score)s, %(response)s)
            """,
            {
                "account": account,
                "air_first_score": air_first_score,
                "air_third_score": air_third_score,
                "air_second_score": air_second_score,
                "land_first_score": land_first_score,
                "land_third_score": land_third_score,
                "land_second_score": land_second_score,
                "water_first_score": water_first_score,
                "water_third_score": water_third_score,
                "water_second_score": water_second_score,
                "animal_first_score": animal_first_score,
                "animal_third_score": animal_third_score,
                "animal_second_score": animal_second_score,
                "safety_first_score": safety_first_score,
                "safety_third_score": safety_third_score,
                "safety_second_score": safety_second_score,
                "efficiency_first_score": efficiency_first_score,
                "efficiency_third_score": efficiency_third_score,
                "efficiency_second_score": efficiency_second_score,
                "response": json.dumps(response),
            }
        )

    def get_sustainability_by_account(self, account, withAccountDetails=False):
        if withAccountDetails:
            data = self._db.execute_d(
                """SELECT a.id, a.name, a.sector, s.*,
                (air_first_score + land_first_score + water_first_score 
                + animal_first_score + safety_first_score 
                + efficiency_first_score) as "total_first_score",
                (air_second_score + land_second_score + water_second_score 
                + animal_second_score + safety_second_score 
                + efficiency_second_score) as "total_second_score",
                (air_third_score + land_third_score + water_third_score 
                + animal_third_score + safety_third_score 
                + efficiency_third_score) as "total_third_score"
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
                """SELECT *, 
                (air_first_score + land_first_score + water_first_score 
                + animal_first_score + safety_first_score 
                + efficiency_first_score) as "total_first_score",
                (air_second_score + land_second_score + water_second_score 
                + animal_second_score + safety_second_score 
                + efficiency_second_score) as "total_second_score",
                (air_third_score + land_third_score + water_third_score 
                + animal_third_score + safety_third_score 
                + efficiency_third_score) as "total_third_score"
                FROM sustainability 
                WHERE account=%(account)s 
                ORDER BY created_timestamp DESC
                """, 
                {
                    "account": account
                })

            return data

    def get_sustainability_totals_by_sector(self, sectorID):
        data = self._db.execute_d(
            """SELECT 
               SUM(air_first_score + land_first_score + water_first_score 
               + animal_first_score + safety_first_score + efficiency_first_score) AS "total_first_score",
               SUM(air_second_score + land_second_score + water_second_score 
               + animal_second_score + safety_second_score + efficiency_second_score) AS "total_second_score",
               SUM(air_third_score + land_third_score + water_third_score 
               + animal_third_score + safety_third_score + efficiency_third_score) AS "total_third_score"
               FROM sustainability AS s
               INNER JOIN accounts AS a ON s.account=a.id
               WHERE a.sector = %(sector)s
               ORDER BY s.created_timestamp DESC LIMIT 1;
            """,
            {
                "sector": sectorID,
            })

        return data

    def get_sustainability(self, account=NO_VALUE, response=NO_VALUE, created_timestamp=NO_VALUE):
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

        #ordering it by the latest first
        order_condition = " ORDER BY ID DESC"

        query = base_query + combined_query_condition + order_condition

        sustainability_rows = self._db.execute_d(query, query_values)
        if len(sustainability_rows) > 0:
            return sustainability_rows
        else:
            return []
