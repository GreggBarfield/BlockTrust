import json
from ..no_value import NoValue

NO_VALUE = NoValue()

QUESTIONNAIRE_STATUS_NAMES_TO_IDS = {
    "Pending": 0,
    "Completed": 1
}


class SustainabilityResponses:

    def __init__(self, db):
        self._db = db
        self.sustainability_responses_cols = ()

    def get_sustainability_responses(self, id=NO_VALUE, account_id=NO_VALUE, user_id=NO_VALUE, air_points=NO_VALUE,
                                     land_points=NO_VALUE, water_points=NO_VALUE, animal_points=NO_VALUE,
                                     safety_points=NO_VALUE, efficiency_points=NO_VALUE, improvement_points=NO_VALUE,
                                     score=NO_VALUE, sector_id=NO_VALUE, questionnaire_status_id=NO_VALUE):
        """
        Gets the sustainability responses based on the attributes provided

        Params:
            id: ID of the sustainability response
            account_id: Account ID of account submitting the response
            user_id: User ID of user submitting the response
            air_points: Air & Greenhouse Gas Emissions points
            land_points: Land points
            water_points: Water points
            animal_points:  Animal Health and Well Being points
            safety_points: Employee Safety and Well Bring points
            efficiency_points: Efficiency and Yield points
            improvement_points: Improvement points
            score: Total Score
            sector_id: Account sector
            questionnaire_status_id: Submission status of questionnaire

        Returns:
            A list of sustainability response rows or an empty list
        """
        base_query = "SELECT * FROM sustainability_responses"

        query_conditions = []
        query_values = {}
        order_by_clause = ""

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if air_points is not NO_VALUE:
            query_conditions.append(" air_points = %(air_points)s")
            query_values["air_points"] = air_points
        if land_points is not NO_VALUE:
            query_conditions.append(" land_points = %(land_points)s")
            query_values["land_points"] = land_points
        if water_points is not NO_VALUE:
            query_conditions.append(" water_points = %(water_points)s")
            query_values["water_points"] = water_points
        if animal_points is not NO_VALUE:
            query_conditions.append(" animal_points = %(animal_points)s")
            query_values["animal_points"] = animal_points
        if safety_points is not NO_VALUE:
            query_conditions.append(" safety_points = %(safety_points)s")
            query_values["safety_points"] = safety_points
        if efficiency_points is not NO_VALUE:
            query_conditions.append(" efficiency_points = %(efficiency_points)s")
            query_values["efficiency_points"] = efficiency_points
        if improvement_points is not NO_VALUE:
            query_conditions.append(" improvement_points = %(improvement_points)s")
            query_values["improvement_points"] = improvement_points
        if score is not NO_VALUE:
            query_conditions.append(" score = %(score)s")
            query_values["score"] = score
        if sector_id is not NO_VALUE:
            query_conditions.append(" sector_id = %(sector_id)s")
            query_values["sector_id"] = sector_id
        if questionnaire_status_id is not NO_VALUE:
            query_conditions.append(" questionnaire_status_id = %(questionnaire_status_id)s")
            query_values["questionnaire_status_id"] = questionnaire_status_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition + " ORDER BY ID DESC"

        sustainability_response_rows = self._db.execute_d(query, query_values)
        if len(sustainability_response_rows) > 0:
            return sustainability_response_rows
        else:
            return []

    def insert_sustainabilty_response(self, account_id, user_id, air_points, land_points, water_points, animal_points,
                                      safety_points, efficiency_points, improvement_points, score, response,
                                      sector_id, questionnaire_status_id):
        """
        Insert a sustainability response

        Params: 
            account_id: Account ID of account submitting the response
            user_id: User ID of user submitting the response
            air_points: Air & Greenhouse Gas Emissions points
            land_points: Land points
            water_points: Water points
            animal_points:  Animal Health and Well Being points
            safety_points: Employee Safety and Well Bring points
            efficiency_points: Efficiency and Yield points
            improvement_points: Improvement points
            score: Total Score
            response: Response provided by the user
            sector_id: Account sector
            questionnaire_status_id: Submission status of questionnaire
        """
        self._db.execute(
            """
            INSERT INTO sustainability_responses (account_id, user_id, air_points, land_points, water_points, animal_points,
            safety_points, efficiency_points, improvement_points, score, response, sector_id, questionnaire_status_id)
            VALUES (%(account_id)s, %(user_id)s, %(air_points)s, %(land_points)s, %(water_points)s, %(animal_points)s,
            %(safety_points)s, %(efficiency_points)s, %(improvement_points)s, %(score)s, %(response)s, %(sector_id)s, %(questionnaire_status_id)s)
            """,
            {
                "account_id": account_id,
                "user_id": user_id,
                "air_points": air_points,
                "land_points": land_points,
                "water_points": water_points,
                "animal_points": animal_points,
                "safety_points": safety_points,
                "efficiency_points": efficiency_points,
                "improvement_points": improvement_points,
                "score": score,
                "response": json.dumps(response) if response is not None else None,
                "sector_id": sector_id,
                "questionnaire_status_id": questionnaire_status_id
            }
        )
        sustainability_response_id = self._db.last_row_id()
        return sustainability_response_id

    def update_sustainability_response(self, id, account_id=NO_VALUE, user_id=NO_VALUE, air_points=NO_VALUE,
                                       land_points=NO_VALUE, water_points=NO_VALUE, animal_points=NO_VALUE,
                                       safety_points=NO_VALUE, efficiency_points=NO_VALUE, improvement_points=NO_VALUE,
                                       score=NO_VALUE, response=NO_VALUE, sector_id=NO_VALUE, questionnaire_status_id=NO_VALUE):
        """
        Updates a sustainability response

        Params:
            id: ID of the sustainability response
            account_id: Account Id of account submitting the response
            user_id: User ID of user submitting the response
            air_points: Air & Greenhouse Gas Emissions points
            land_points: Land points
            water_points: Water points
            animal_points:  Animal Health and Well Being points
            safety_points: Employee Safety and Well Bring points
            efficiency_points: Efficiency and Yield points
            improvement_points: Improvement points
            score: Total Score
            response: Response provided by the user
            sector_id: Account sector
            questionnaire_status_id: Submission status of questionnaire
        """
        base_query = "UPDATE sustainability_responses "

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if air_points is not NO_VALUE:
            query_conditions.append(" air_points = %(air_points)s")
            query_values["air_points"] = air_points
        if land_points is not NO_VALUE:
            query_conditions.append(" land_points = %(land_points)s")
            query_values["land_points"] = land_points
        if water_points is not NO_VALUE:
            query_conditions.append(" water_points = %(water_points)s")
            query_values["water_points"] = water_points
        if animal_points is not NO_VALUE:
            query_conditions.append(" animal_points = %(animal_points)s")
            query_values["animal_points"] = animal_points
        if safety_points is not NO_VALUE:
            query_conditions.append(" safety_points = %(safety_points)s")
            query_values["safety_points"] = safety_points
        if efficiency_points is not NO_VALUE:
            query_conditions.append(" efficiency_points = %(efficiency_points)s")
            query_values["efficiency_points"] = efficiency_points
        if improvement_points is not NO_VALUE:
            query_conditions.append(" improvement_points = %(improvement_points)s")
            query_values["improvement_points"] = improvement_points
        if score is not NO_VALUE:
            query_conditions.append(" score = %(score)s")
            query_values["score"] = score
        if response is not NO_VALUE:
            query_conditions.append(" response = %(response)s")
            query_values["response"] = json.dumps(response)
        if sector_id is not NO_VALUE:
            query_conditions.append(" sector_id = %(sector_id)s")
            query_values["sector_id"] = sector_id
        if questionnaire_status_id is not NO_VALUE:
            query_conditions.append(" questionnaire_status_id = %(questionnaire_status_id)s")
            query_values["questionnaire_status_id"] = questionnaire_status_id

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Sustainability responses")

    def get_sustainability_response_averages(self, account_id=NO_VALUE, sector_id=NO_VALUE):
        """
        Returns the sustainability average points for each sectiona and also by account if account_id is specififed

        Params:
            account_id: Account ID for which averages are required

        Returns:
            Sustainability point averages by section (A dictionary). Will return a dictionary with None for the AVG(column) if no data exists.
        """
        base_query = """SELECT AVG(air_points) as air_average, AVG(land_points) as land_average, AVG(water_points) as water_average,
                   AVG(animal_points) as animal_average, AVG(safety_points) as safety_average, AVG(efficiency_points) as efficiency_average,
                   AVG(improvement_points) as improvement_average, AVG(score) as score_average FROM sustainability_responses"""
        query_conditions = []
        query_value = {}
        if account_id is not NO_VALUE:
            query_conditions.append("account_id = %(account_id)s")
            query_value["account_id"] = account_id
        if sector_id is not NO_VALUE:
            query_conditions.append("sector_id = %(sector_id)s")
            query_value["sector_id"] = sector_id

        if len(query_conditions) >= 1:
            query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            query_condition = ""

        query = base_query + query_condition

        sustainability_averages = self._db.execute_d(query, query_value)
        return sustainability_averages[0]