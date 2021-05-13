from ..objects.user import User


class UsersException(Exception):
    """Generic user exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for UsersException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class NoUserFoundException(UsersException):
    """User was not found."""
    pass


class Users:

    def __init__(self, db):
        self._db = db

    def get(self, user_id):
        """Gets a user by their ID.

        Params:
            user_id: User's ID

        Returns:
            A User object on success, or None on no match.
        """
        matching_users = self._db.execute_d(
            """
                SELECT * FROM users
                WHERE
                    id=%(id)s
            """,
            {
                "id": user_id
            }
        )

        if len(matching_users) != 1:
            raise UsersException()

        return User(self._db, matching_users[0])

    def get_by_email(self, email):
        """Get a user by email.

        Params:
            email: The user's email

        Returns:
            A User object on success, or None on no match.
        """
        matching_users = self._db.execute_d(
            """
                SELECT * FROM users
                WHERE
                    email=%(email)s
            """,
            {
                "email": Users._format_field(email)
            }
        )

        if len(matching_users) != 1:
            raise NoUserFoundException()
        return User(self._db, matching_users[0])

    def get_by_username(self, username):
        """Get a user by username.

        Params:
            username: The user's username

        Returns:
            A User object on success, or None on no match.
        """
        matching_users = self._db.execute_d(
            """
                SELECT * FROM users
                WHERE
                    username=%(username)s
            """,
            {
                "username": Users._format_field(username)
            }
        )

        if len(matching_users) != 1:
            raise NoUserFoundException()
        return User(self._db, matching_users[0])

    def get_rows_by_account(self, account_id):
        """Gets user rows by account ID.

        Params:
            account_id: The account ID

        Returns:
            The rows

            Enhanced with account_name
        """
        rows = self._db.execute_d(
            """
            SELECT users.*, accounts.name AS account_name FROM users
                INNER JOIN account_users
                    ON account_users.user=users.id
                INNER JOIN accounts
                    ON account_users.account=accounts.id
                WHERE account_users.account=%(account)s
            """,
            {
                "account": account_id
            }
        )
        return rows

    def verify_email(self, email):
        """
            Confirms a user profile and marks it as verified

            Params:
            email: User email to be verified

            Returns:
            None
            """

        self._db.execute_d(
                """
                UPDATE users
                SET email_verified="Y"
                WHERE users.email=%(email)s
                """,
                {
                    "email": email
                }
                )

    def get_email_verified_status(self, email):
        """
        Confirms if the user email is verified

        Params:
            email:User email which needs to be looked up for verification status

        Returns:
            True if user is verified. False if not verified.
        """
        matching_user = self._db.execute_d(
            """
                SELECT * FROM users
                WHERE
                    email=%(email)s
            """,
            {
                "email": Users._format_field(email)
            }
        )
        if len(matching_user) != 1:
            raise NoUserFoundException()
        if matching_user[0]['email_verified'] == "Y":
            return True
        else:
            return False

    @staticmethod
    def _format_field(field):
        """Format a user info field.

        Params:
            field: The user's field (str)
        """
        if field is None:
            raise ValueError("field can't be None")
        if b'\x00' in field.encode("utf-8"):
            raise ValueError("Null bytes in the field??? Stop whatever is going on")
        return field.strip(" \n\r\t")
