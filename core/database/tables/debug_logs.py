from ..no_value import NoValue
import json

NO_VALUE = NoValue()

class DebugLogs:

    def __init__(self, db):
        self._db = db

    def insert_debug_log(self, component, short_info=None, long_info=None, details=None):
        """Inserts Error Log.
        """
        try:
            self._db.execute(
                """INSERT INTO debug_logs
                    (component, short_info, long_info, details)
                    VALUES
                        (%(component)s, %(short_info)s, %(long_info)s, %(details)s)
                """,
                {
                    "component": component,
                    "short_info": short_info,
                    "long_info": long_info,
                    "details": None if details is None else json.dumps(details)              
                }
            )
        except Exception as e:
            print(e)
    
    def get(self, component=NO_VALUE, short_info=NO_VALUE, details_owner_account_id=NO_VALUE, details_eid=NO_VALUE):
        """
        Gets the debug logs based on provided parameters
        
        Params:
            component: Component name to debug
            short_info: Short definition of debug log
            details_json_key: JSON key to be checked in details column
            details_json_value: JSON value to be checked in details column
        
        Returns:
            Debug logs rows based on provided parameters
        """
        try:
            base_query = "SELECT * FROM debug_logs"
            query_conditions = []
            query_values = {}
            order_by_clause = ""

            if component is not NO_VALUE:
                query_conditions.append(" component = %(component)s")
                query_values["component"] = component
            if short_info is not NO_VALUE:
                query_conditions.append(" short_info = %(short_info)s")
                query_values["short_info"] = short_info
            if details_owner_account_id is not NO_VALUE:
                query_conditions.append(" JSON_EXTRACT(details, $.owner_account_id) = %(details_owner_account_id)s ")
                query_values["details_owner_account_id"] = details_owner_account_id
            if details_eid is not NO_VALUE:
                query_conditions.append(" JSON_EXTRACT(details, $.eid) = %(details_eid)s ")
                query_values["details_eid"] = details_eid

            if len(query_conditions) >= 1:
                combined_query_condition = " WHERE" + " AND ".join(query_conditions) + " " + order_by_clause
            else:
                combined_query_condition = ""
            query = base_query + combined_query_condition
            debug_logs_rows = self._db.execute_d(query, query_values)
            if len(debug_logs_rows) > 0:
                return debug_logs_rows
            return []
        except Exception as e:
            print(str(e))