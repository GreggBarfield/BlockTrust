class InvitedUsers:

    def __init__(self, db):
        self._db = db

    def insert_invited_user(self, email, invited_by_user_id=None, invited_by_employee_id=None,
                            is_invited_as_admin=int(False)):
        """Inserts a new row.

        Returns:
            The invited user ID inserted
        """
        self._db.execute(
            """INSERT INTO invited_users
                (email, invited_by_user_id, invited_by_employee_id, is_invited_as_admin)
                VALUES (%(email)s, %(invited_by_user_id)s, %(invited_by_employee_id)s, %(is_invited_as_admin)s)
            """,
            {
                "email": email,
                "invited_by_user_id": invited_by_user_id,
                "invited_by_employee_id": invited_by_employee_id,
                "is_invited_as_admin": is_invited_as_admin
            }
        )
        return self._db.last_row_id()
