from ..no_value import NoValue
from json import dumps, loads

NO_VALUE = NoValue()

event_log_cols = ("id", "account_id", "user_id", "event_type_id", "details", "created_timestamp", "last_updated_timestamp")

class APIInsertsUnknownFields:

    def __init__(self, db):
        self._db = db

    
    def insert(self, account_id=None, api_action=None, api_action_type=None, unknown_field_name=None,
               unknown_field_data=None):
        """
        Inserts an API Insert unknown field

        Params:
            account_id: Account ID associated with event
            api_action: API action being performed
            api_action_type: API Action Type
            unknown_field_name: Unknown field name
            unknown_field_data: Value present for unknown field
        """
        
        self._db.execute(
            """
            INSERT INTO api_inserts_unknown_fields (account_id, api_action, api_action_type, unknown_field_name, unknown_field_data)
            VALUES (%(account_id)s, %(api_action)s, %(api_action_type)s, %(unknown_field_name)s, %(unknown_field_data)s)
            """,
            {
                "account_id": account_id,
                "api_action": api_action,
                "api_action_type": api_action_type,
                "unknown_field_name": unknown_field_name,
                "unknown_field_data": unknown_field_data
            }
        )


    def get(self, id=NO_VALUE, account_id=None, api_action=None, api_action_type=None, unknown_field_name=None,
            unknown_field_data=None):
        """
        Gets the API Insert unknown fields based on provided parameters

        Params:
            account_id: Account ID associated with event
            api_action: API action being performed
            api_action_type: API Action Type
            unknown_field_name: Unknown field name
            unknown_field_data: Value present for unknown field

        Returns:
            A list of API Insert unknown fields or an empty list
        """
        base_query = "SELECT * FROM api_inserts_unknown_fields"

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if api_action is not NO_VALUE:
            query_conditions.append(" api_action = %(api_action)s")
            query_values["api_action"] = api_action
        if api_action_type is not NO_VALUE:
            query_conditions.append(" api_action_type = %(api_action_type)s")
            query_values["api_action_type"] = api_action_type
        if unknown_field_name is not NO_VALUE:
            query_conditions.append(" unknown_field_name = %(unknown_field_name)s")
            query_values["unknown_field_name"] = unknown_field_name
        if unknown_field_data is not NO_VALUE:
            query_conditions.append(" unknown_field_data = %(unknown_field_data)s")
            query_values["unknown_field_data"] = unknown_field_data

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        api_inserts_unknown_fields_rows = self._db.execute_d(query, query_values)
        if len(api_inserts_unknown_fields_rows) > 0:
            return api_inserts_unknown_fields_rows
        else:
            return []