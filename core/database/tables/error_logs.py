import json


class ErrorLogs:

    def __init__(self, db):
        self._db = db

    def insert_error_log(self, component, short_error, long_error=None, details=None):
        """Inserts Error Log.
        """
        try:
            self._db.execute(
                """INSERT INTO error_logs
                    (component, short_error, long_error, column_name, column_value)
                    VALUES
                        (%(component)s, %(short_error)s, %(long_error)s, %(details)s)
                """,
                {
                    "component": component,
                    "short_error": short_error,
                    "long_error": long_error,
                    "details": None if details is None else json.dumps(details)              
                }
            )
        except Exception as e:
            print(e)