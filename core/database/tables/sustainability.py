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

        air_first_score_points = None
        air_second_score_points = None
        air_third_score_points = None
        land_first_score_points = None
        land_second_score_points = None
        land_third_score_points = None
        water_first_score_points = None
        water_second_score_points = None
        water_third_score_points = None
        animal_first_score_points = None
        animal_second_score_points = None
        animal_third_score_points = None
        safety_first_score_points = None
        safety_second_score_points = None
        safety_third_score_points = None
        efficiency_first_score_points = None
        efficiency_second_score_points = None
        efficiency_third_score_points = None

        for section in sectorScoreCounter:
            if section == 'air':
                air_first_score_points = sectorScoreCounter[section]["excellent"]
                air_second_score_points = sectorScoreCounter[section]["acceptable"]
                air_third_score_points = sectorScoreCounter[section]["needsWork"]
            elif section == 'land':
                land_first_score_points = sectorScoreCounter[section]["excellent"]
                land_second_score_points = sectorScoreCounter[section]["acceptable"]
                land_third_score_points = sectorScoreCounter[section]["needsWork"]
            elif section == 'water':
                water_first_score_points = sectorScoreCounter[section]["excellent"]
                water_second_score_points = sectorScoreCounter[section]["acceptable"]
                water_third_score_points = sectorScoreCounter[section]["needsWork"]
            elif section == 'animal':
                animal_first_score_points = sectorScoreCounter[section]["excellent"]
                animal_second_score_points = sectorScoreCounter[section]["acceptable"]
                animal_third_score_points = sectorScoreCounter[section]["needsWork"]
            elif section == 'safety':
                safety_first_score_points = sectorScoreCounter[section]["excellent"]
                safety_second_score_points = sectorScoreCounter[section]["acceptable"]
                safety_third_score_points = sectorScoreCounter[section]["needsWork"]
            elif section == 'efficiency':
                efficiency_first_score_points = sectorScoreCounter[section]["excellent"]
                efficiency_second_score_points = sectorScoreCounter[section]["acceptable"]
                efficiency_third_score_points = sectorScoreCounter[section]["needsWork"]

        self._db.execute(
            """INSERT INTO sustainability
                (account, air_first_score_points, air_second_score_points, air_third_score_points, 
                land_first_score_points, land_second_score_points, land_third_score_points, 
                water_first_score_points, water_second_score_points, water_third_score_points, 
                animal_first_score_points, animal_second_score_points, animal_third_score_points, 
                safety_first_score_points, safety_second_score_points, safety_third_score_points, 
                efficiency_first_score_points, efficiency_second_score_points, 
                efficiency_third_score_points, response)
                VALUES (%(account)s, %(air_first_score_points)s, %(air_second_score_points)s, 
                        %(air_third_score_points)s, %(land_first_score_points)s, %(land_second_score_points)s,
                        %(land_third_score_points)s, %(water_first_score_points)s, 
                        %(water_second_score_points)s, %(water_third_score_points)s,
                        %(animal_first_score_points)s, %(animal_second_score_points)s,
                        %(animal_third_score_points)s, %(safety_first_score_points)s,
                        %(safety_second_score_points)s, %(safety_third_score_points)s,
                        %(efficiency_first_score_points)s, %(efficiency_second_score_points)s,
                        %(efficiency_third_score_points)s, %(response)s)
            """,
            {
                "account": account,
                "air_first_score_points": air_first_score_points,
                "air_third_score_points": air_third_score_points,
                "air_second_score_points": air_second_score_points,
                "land_first_score_points": land_first_score_points,
                "land_third_score_points": land_third_score_points,
                "land_second_score_points": land_second_score_points,
                "water_first_score_points": water_first_score_points,
                "water_third_score_points": water_third_score_points,
                "water_second_score_points": water_second_score_points,
                "animal_first_score_points": animal_first_score_points,
                "animal_third_score_points": animal_third_score_points,
                "animal_second_score_points": animal_second_score_points,
                "safety_first_score_points": safety_first_score_points,
                "safety_third_score_points": safety_third_score_points,
                "safety_second_score_points": safety_second_score_points,
                "efficiency_first_score_points": efficiency_first_score_points,
                "efficiency_third_score_points": efficiency_third_score_points,
                "efficiency_second_score_points": efficiency_second_score_points,
                "response": json.dumps(response),
            }
        )

    def get_sustainability_by_account(self, account, withAccountDetails=False):
        if withAccountDetails:
            data = self._db.execute_d(
                """SELECT a.id, a.name, a.sector, s.*,
                (air_first_score_points + land_first_score_points + water_first_score_points 
                + animal_first_score_points + safety_first_score_points 
                + efficiency_first_score_points) AS "total_first_score_points",
                (air_second_score_points + land_second_score_points + water_second_score_points 
                + animal_second_score_points + safety_second_score_points 
                + efficiency_second_score_points) AS "total_second_score_points",
                (air_third_score_points + land_third_score_points + water_third_score_points 
                + animal_third_score_points + safety_third_score_points 
                + efficiency_third_score_points) AS "total_third_score_points"
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
                (air_first_score_points + land_first_score_points + water_first_score_points 
                + animal_first_score_points + safety_first_score_points 
                + efficiency_first_score_points) AS "total_first_score_points",
                (air_second_score_points + land_second_score_points + water_second_score_points 
                + animal_second_score_points + safety_second_score_points 
                + efficiency_second_score_points) AS "total_second_score_points",
                (air_third_score_points + land_third_score_points + water_third_score_points 
                + animal_third_score_points + safety_third_score_points 
                + efficiency_third_score_points) AS "total_third_score_points"
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
               SUM(air_first_score_points + land_first_score_points + water_first_score_points 
               + animal_first_score_points + safety_first_score_points + efficiency_first_score_points) AS "total_first_score_points",
               SUM(air_second_score_points + land_second_score_points + water_second_score_points 
               + animal_second_score_points + safety_second_score_points + efficiency_second_score_points) AS "total_second_score_points",
               SUM(air_third_score_points + land_third_score_points + water_third_score_points 
               + animal_third_score_points + safety_third_score_points + efficiency_third_score_points) AS "total_third_score_points"
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
