import json


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