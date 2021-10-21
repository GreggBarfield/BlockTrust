class UserLoginsByEmployee:

    def __init__(self, db):
        self._db = db

    def insert_user_logins_by_employee(self, user_id, employee_id):
        """Inserts Error Log.
        """
        self._db.execute(
            """INSERT INTO user_logins_by_employee
                (user_id, employee_id)
                VALUES
                    (%(user_id)s, %(employee_id)s)
            """,
            {
                "user_id": user_id,
                "employee_id": employee_id           
            }
        )