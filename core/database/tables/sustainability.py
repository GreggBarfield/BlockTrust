import json

from ..no_value import NoValue

NO_VALUE = NoValue()

class Sustainability:
    def __init__(self, db):
        self._db = db

    def insert(self, account, response, sectorScoreCounterJSON):
        sectorScoreCounter = json.loads(sectorScoreCounterJSON)

        air_excellent_score = None
        air_acceptable_score = None
        air_needsWork_score = None
        land_excellent_score = None
        land_acceptable_score = None
        land_needsWork_score = None
        water_excellent_score = None
        water_acceptable_score = None
        water_needsWork_score = None
        animal_excellent_score = None
        animal_acceptable_score = None
        animal_needsWork_score = None
        safety_excellent_score = None
        safety_acceptable_score = None
        safety_needsWork_score = None
        efficiency_excellent_score = None
        efficiency_acceptable_score = None
        efficiency_needsWork_score = None

        for section in sectorScoreCounter:
            if section == 'air':
                air_excellent_score = sectorScoreCounter[section]["excellent"]
                air_acceptable_score = sectorScoreCounter[section]["acceptable"]
                air_needsWork_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'land':
                land_excellent_score = sectorScoreCounter[section]["excellent"]
                land_acceptable_score = sectorScoreCounter[section]["acceptable"]
                land_needsWork_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'water':
                water_excellent_score = sectorScoreCounter[section]["excellent"]
                water_acceptable_score = sectorScoreCounter[section]["acceptable"]
                water_needsWork_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'animal':
                animal_excellent_score = sectorScoreCounter[section]["excellent"]
                animal_acceptable_score = sectorScoreCounter[section]["acceptable"]
                animal_needsWork_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'safety':
                safety_excellent_score = sectorScoreCounter[section]["excellent"]
                safety_acceptable_score = sectorScoreCounter[section]["acceptable"]
                safety_needsWork_score = sectorScoreCounter[section]["needsWork"]
            elif section == 'efficiency':
                efficiency_excellent_score = sectorScoreCounter[section]["excellent"]
                efficiency_acceptable_score = sectorScoreCounter[section]["acceptable"]
                efficiency_needsWork_score = sectorScoreCounter[section]["needsWork"]

        self._db.execute(
            """INSERT INTO sustainability
                (account, air_excellent_score, air_acceptable_score, air_needsWork_score, 
                land_excellent_score, land_acceptable_score, land_needsWork_score, 
                water_excellent_score, water_acceptable_score, water_needsWork_score, 
                animal_excellent_score, animal_acceptable_score, animal_needsWork_score, 
                safety_excellent_score, safety_acceptable_score, safety_needsWork_score, 
                efficiency_excellent_score, efficiency_acceptable_score, 
                efficiency_needsWork_score, response)
                VALUES (%(account)s, %(air_excellent_score)s, %(air_acceptable_score)s, 
                        %(air_needsWork_score)s, %(land_excellent_score)s, %(land_acceptable_score)s,
                        %(land_needsWork_score)s, %(water_excellent_score)s, 
                        %(water_acceptable_score)s, %(water_needsWork_score)s,
                        %(animal_excellent_score)s, %(animal_acceptable_score)s,
                        %(animal_needsWork_score)s, %(safety_excellent_score)s,
                        %(safety_acceptable_score)s, %(safety_needsWork_score)s,
                        %(efficiency_excellent_score)s, %(efficiency_acceptable_score)s,
                        %(efficiency_needsWork_score)s, %(response)s)
            """,
            {
                "account": account,
                "air_excellent_score": air_excellent_score,
                "air_needsWork_score": air_needsWork_score,
                "air_acceptable_score": air_acceptable_score,
                "land_excellent_score": land_excellent_score,
                "land_needsWork_score": land_needsWork_score,
                "land_acceptable_score": land_acceptable_score,
                "water_excellent_score": water_excellent_score,
                "water_needsWork_score": water_needsWork_score,
                "water_acceptable_score": water_acceptable_score,
                "animal_excellent_score": animal_excellent_score,
                "animal_needsWork_score": animal_needsWork_score,
                "animal_acceptable_score": animal_acceptable_score,
                "safety_excellent_score": safety_excellent_score,
                "safety_needsWork_score": safety_needsWork_score,
                "safety_acceptable_score": safety_acceptable_score,
                "efficiency_excellent_score": efficiency_excellent_score,
                "efficiency_needsWork_score": efficiency_needsWork_score,
                "efficiency_acceptable_score": efficiency_acceptable_score,
                "response": json.dumps(response),
            }
        )

    def get_sustainability_by_account(self, account, withAccountDetails=False):
        if withAccountDetails:
            data = self._db.execute_d(
                """SELECT a.id, a.name, a.sector, s.*,
                (air_excellent_score + land_excellent_score + water_excellent_score 
                + animal_excellent_score + safety_excellent_score 
                + efficiency_excellent_score) as "total_excellent_score",
                (air_acceptable_score + land_acceptable_score + water_acceptable_score 
                + animal_acceptable_score + safety_acceptable_score 
                + efficiency_acceptable_score) as "total_acceptable_score",
                (air_needsWork_score + land_needsWork_score + water_needsWork_score 
                + animal_needsWork_score + safety_needsWork_score 
                + efficiency_needsWork_score) as "total_needsWork_score"
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
                (air_excellent_score + land_excellent_score + water_excellent_score 
                + animal_excellent_score + safety_excellent_score 
                + efficiency_excellent_score) as "total_excellent_score",
                (air_acceptable_score + land_acceptable_score + water_acceptable_score 
                + animal_acceptable_score + safety_acceptable_score 
                + efficiency_acceptable_score) as "total_acceptable_score",
                (air_needsWork_score + land_needsWork_score + water_needsWork_score 
                + animal_needsWork_score + safety_needsWork_score 
                + efficiency_needsWork_score) as "total_needsWork_score"
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
               SUM(air_excellent_score + land_excellent_score + water_excellent_score 
               + animal_excellent_score + safety_excellent_score + efficiency_excellent_score) AS "total_excellent_score",
               SUM(air_acceptable_score + land_acceptable_score + water_acceptable_score 
               + animal_acceptable_score + safety_acceptable_score + efficiency_acceptable_score) AS "total_acceptable_score",
               SUM(air_needsWork_score + land_needsWork_score + water_needsWork_score 
               + animal_needsWork_score + safety_needsWork_score + efficiency_needsWork_score) AS "total_needsWork_score"
               FROM sustainability AS s
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
