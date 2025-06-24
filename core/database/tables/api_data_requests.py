from json import dumps
from ..no_value import NoValue

NO_VALUE = NoValue()

class APIDataRequests:

    def __init__(self, db):
        self._db = db

    def insert_api_data_request(self, api_route, request_data=None, account_id=None, employee_id=None, user_id=None):
        """Inserts an api data request received.
        """
        self._db.execute(
            """INSERT INTO api_data_requests
                (account_id, api_route, request_data, employee_id, user_id)
                VALUES
                    (%(account_id)s, %(api_route)s , %(request_data)s, %(employee_id)s, %(user_id)s)
            """,
            {
                "account_id": account_id,
                "api_route": api_route,
                "request_data": dumps(request_data) if request_data else None,
                "employee_id": employee_id,
                "user_id": user_id
            }
        )

    def get(self, id=NO_VALUE, account_id=NO_VALUE, employee_id=NO_VALUE, api_route=NO_VALUE, request_data=NO_VALUE):
        """
        Gets the API data requests data based on provided parameters

        Params:
            id: API Data request ID
            account_id: Account ID associated with API data request
            employee_id: Employee ID associated with API data request
            api_route: API Route requested
            request_data: Additional details about data request

        Returns:
            A list of API data requests or an empty list
        """
        base_query = "SELECT * FROM api_data_requests"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if employee_id is not NO_VALUE:
            query_conditions.append(" employee_id = %(employee_id)s")
            query_values["employee_id"] = employee_id
        if api_route is not NO_VALUE:
            query_conditions.append(" api_route = %(api_route)s")
            query_values["api_route"] = api_route
        if request_data is not NO_VALUE:
            query_conditions.append(" request_data = %(request_data)s")
            query_values["request_data"] = dumps(request_data)
        
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition + " ORDER BY ID DESC"
        rows = self._db.execute_d(query, query_values)

        if len(rows) > 0:
            return rows
        else:
            return []