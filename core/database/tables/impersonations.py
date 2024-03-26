class Impersonations:

    def __init__(self, db):
        self._db = db

    def insert(self, user_id, employee_id=None, impersonated_by_user_id=None):
        """Inserts Error Log.
        """
        self._db.execute(
            """INSERT INTO impersonations
                (user_id, employee_id, impersonated_by_user_id)
                VALUES
                    (%(user_id)s, %(employee_id)s, %(impersonated_by_user_id)s)
            """,
            {
                "user_id": user_id,
                "employee_id": employee_id,
                "impersonated_by_user_id": impersonated_by_user_id
            }
        )