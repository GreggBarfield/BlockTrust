class InvitedUsers:

    def __init__(self, db):
        self._db = db

    def insert_invited_user(self, email, invited_by_id, is_invited_by_employee, is_invited_as_admin):
        """Inserts a new row.

        Returns:
            The invited user ID inserted
        """
        self._db.execute(
            """INSERT INTO invited_users
                (email, invited_by_id, is_invited_by_employee, is_invited_as_admin)
                VALUES (%(email)s, %(invited_by_id)s, %(is_invited_by_employee)s, %(is_invited_as_admin)s)
            """,
            {
                "email": email,
                "invited_by_id": invited_by_id,
                "is_invited_by_employee": is_invited_by_employee, 
                "is_invited_as_admin": is_invited_as_admin
            }
        )
        return self._db.last_row_id()
