from ..no_value import NoValue

NO_VALUE = NoValue()

TABLE_COLUMNS = ("id", "owner_account_id", "viewer_account_id", "viewer_account_name", "viewer_user_id", "data_type_id",
                 "created_timestamp", "last_updated_timestamp")

DATA_TYPE_NAME_TO_ID = {
    "EID": 1,
    "Sustainability": 2
}


class ViewLogs:

    def __init__(self, db):
        self._db = db

    def insert_view_logs(self, owner_account_id, viewer_account_id, viewer_account_display_name, data_type_id, viewer_user_id=None, 
                         eid=None, sustainability_response_id=None):
        """
        Inserts a new view_log record
        
        Returns:
            id of row inserted
        """
        
        self._db.execute(
            """
                INSERT INTO view_logs (owner_account_id, viewer_account_id, viewer_account_display_name, viewer_user_id, data_type_id, 
                eid, sustainability_response_id)
                VALUES (%(owner_account_id)s, %(viewer_account_id)s, %(viewer_account_display_name)s, %(viewer_user_id)s, %(data_type_id)s, 
                %(eid)s, %(sustainability_response_id)s)
            """,
            {
                "owner_account_id": owner_account_id,
                "viewer_account_id": viewer_account_id,
                "viewer_account_display_name": viewer_account_display_name,
                "viewer_user_id": viewer_user_id,
                "data_type_id": data_type_id,
                "eid": eid,
                "sustainability_response_id":sustainability_response_id
            }
        )
        return self._db.last_row_id()

    def get_view_logs(self, id=NO_VALUE, owner_account_id=NO_VALUE, viewer_account_id=NO_VALUE, data_type_id=NO_VALUE):
        """
        Gets the view logs based on the provided parameters

        Returns:
            A list of view logs or an empty array
        """
        base_query = "SELECT * FROM view_logs"

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if owner_account_id is not NO_VALUE:
            query_conditions.append("owner_account_id = %(owner_account_id)s")
            query_values["owner_account_id"] = owner_account_id
        if viewer_account_id is not NO_VALUE:
            query_conditions.append("viewer_account_id = %(viewer_account_id)s")
            query_values["viewer_account_id"] = viewer_account_id
        if data_type_id is not NO_VALUE:
            query_conditions.append("data_type_id = %(data_type_id)s")
            query_values["data_type_id"] = data_type_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition
        view_log_rows = self._db.execute_d(query, query_values)

        if len(view_log_rows) > 0:
            return view_log_rows
        else:
            return []
