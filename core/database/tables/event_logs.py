from ..no_value import NoValue
from json import dumps

NO_VALUE = NoValue()

event_type_by_name = {
    "Signup": 1,
    "Tag Upload": 2,
    "Account Info Edit": 3,
    "User Info Edit": 4,
    "Email Verified": 5,
    "Invited Signup": 6,
    "Sales Group Purchase": 7,
    "Account Created By Employee": 8,
    "Bulk Account And User Signup By Employee": 9
}
event_type_by_id = {
    value: key
    for key, value in event_type_by_name.items()
}


class EventLogs:

    def __init__(self, db):
        self._db = db

    def get(self, id=NO_VALUE, account_id=NO_VALUE, user_id=NO_VALUE, event_type_id=NO_VALUE,
                       details=NO_VALUE):
        """
        Gets the event logs based on provided parameters

        Params:
            id: Event log ID
            account_id: Account ID associated with event log
            user_id: User ID associated with event log
            event_type_id: Event type ID
            details: Additional details about event

        Returns:
            A list of event logs or an empty list
        """
        base_query = "SELECT * FROM event_logs"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if account_id is not NO_VALUE:
            query_conditions.append(" account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if user_id is not NO_VALUE:
            query_conditions.append(" user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if event_type_id is not NO_VALUE:
            query_conditions.append(" event_type_id = %(event_type_id)s")
            query_values["event_type_id"] = event_type_id
        if details is not NO_VALUE:
            query_conditions.append(" event_details = %(event_details)s")
            query_values["event_details"] = details

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        event_rows = self._db.execute_d(query, query_values)
        if len(event_rows) > 0:
            return event_rows
        else:
            return []

    def insert_event_log(self, event_type_id=None, account_id=None, user_id=None, details=None):
        """
        Inserts an event log

        Params:
            account_id: Account ID associated with event
            user_id: User ID associated with event
            event_type_id: Event type ID
            details: Additional details about event
        """
        self._db.execute(
            """
            INSERT INTO event_logs (account_id, user_id, event_type_id, details)
            VALUES (%(account_id)s, %(user_id)s, %(event_type_id)s, %(details)s)
            """,
            {
                "account_id": account_id,
                "user_id": user_id,
                "event_type_id": event_type_id,
                "details": dumps(details) if details else None
            }
        )
