from ..objects.user import User
import bcrypt
from ..no_value import NoValue
from ..frag import frag

NO_VALUE = NoValue()


class UsersException(Exception):
    """Generic user exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for UsersException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


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

        if len(matching_users) == 0:
            return None
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
            return None
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
            SELECT users.*, accounts.company AS account_name FROM users
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
                SET is_email_verified=1
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
        if len(matching_user) > 0:
            return matching_user[0]['is_email_verified']
        else:
            return 0

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
        field.strip(" \n\r\t")
        return field if field != '' else None

    def create_user(self, username, password, email, first_name, last_name, phone, email_verified):
        """Creates a new user

        Params:
            username: username to login
            password: password to login
            email: email of the user
            first_name: first name of the user
            last_name: last name of the user
            phone: phone of the user
            email_verified: is email verified

        Returns:
            An User object

        Raises:
            UsersException
        """

        # Email must exist and contain an '@'
        if len(email) == 0:
            raise UsersException("Email is blank.")
        if '@' not in email or '.' not in email or len(email) < 5:
            raise UsersException("The email you entered is incomplete.")
        if ' ' in email:
            raise UsersException("Spaces cannot be in the email.")
        # Double-usage
        user = self.get_by_email(email)
        if user is not None:
            raise UsersException("Email is already being used.")


        # Double-usage. This should never happen since if email doesn't exist, username shouldn't as well. But to be absolutely sure.
        user = self.get_by_username(username)
        if user is not None:
            raise UsersException("Username is already being used.")

        # Password must be at least 10 characters in unicode
        # and be no more than 60 characters in UTF-8
        # and can't contain the null byte when in UTF-8

        if len(password) < 8:
            raise UsersException("Password must be at least 8 characters.")

        if len(password.encode("utf-8")) > 60:
            raise UsersException("Your password is too long. (Can't be longer than 60 bytes when in UTF-8 formatting.)")

        # Process phone number
        
        digits = ''.join(chr(ord('0') + i) for i in range(10))
        temp_phone = ""
        for c in phone:
            if c in digits:
                temp_phone += c
        phone = temp_phone

        # If phone is empty it is NULL
        if phone == "":
            phone = None

        # We don't really care whether or not the phone is being used more than once

        self._db.execute(
            """
                INSERT INTO users
                    (password, username, email, phone, first_name, last_name, is_email_verified)
                    VALUES
                        (%(password)s, %(username)s, %(email)s, %(phone)s, %(first_name)s, %(last_name)s, %(email_verified)s)
            """,
            {
                "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                "username": username,
                "phone": phone,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "email_verified": email_verified
            }
        )
        user = self.get_by_username(username)
        return user

    def update_user(self, username, first=NO_VALUE, last=NO_VALUE, phone=NO_VALUE, password=NO_VALUE, confirm_password=NO_VALUE):
        """Updates user information.

        Params:
            username: This is the user id, just the user can see it
            email: email address of user,just the user can see it
            password: This is corresponding password used to login
            phone: phone number of user
            first: first name of the user.
            last: last name of the user.
        Returns:
            None

        Raises:
            UsersException

        """
        username = Users._format_field(username)

        password = Users._format_field(password)
        if password != None and len(password) > 0:
            if len(password) < 10:
                raise UsersException("Password must be at least 10 characters.")

            if len(password.encode("utf-8")) > 60:
                raise UsersException("Your password is too long.")

            if (password != confirm_password):
                raise UsersException("Password and Confirm password are not the same!")
        else:
            password = NO_VALUE

        # Process phone number
        digits = ''.join(chr(ord('0') + i) for i in range(10))
        temp_phone = ""
        for c in phone:
            if c in digits:
                temp_phone += c
        phone = temp_phone

        # If phone is empty it is NULL
        if phone == "":
            phone = None

        set_frags = frag()
        if first is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "first=:first,",
                             first = first
                        )
        if last is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "last=:last,",
                             last = last
                        )
        if phone is not NO_VALUE:
            set_frags = frag(
                            set_frags, 
                            "phone=:phone,",
                             phone = phone
                        )
        if password is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "password=:password,",
                            password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                        )

        if len(set_frags[0]) > 0 and len(set_frags[1]) > 0:
            # check if last character in SQL is , and remove it if so
            if set_frags[0][-1] == ",":
                set_frags = (set_frags[0][:-1], set_frags[1])

            self._db.exec_frag(   
                frag(
                    "UPDATE users SET",
                    set_frags,
                    frag(
                        "WHERE username=:username",
                         username = username
                    )
                )
            )

    def is_user_deletable(self, user):
        """This runs checks to find if a user record is deletable.

        Params:
            id: The user object

        Returns:
            True Or False
        """
        account_users = self._db.account_users.get_by_user(user)
        if len(account_users) > 0:
            return False
        else:
            return True

    def delete_by_user(self, user):
        """Delete a user record if it is deletable

        Params:
            user: The user's object

        Returns:
            True if success else False
        """
        if self.is_user_deletable(user):
            self._db.execute_d(
                """
                    DELETE FROM users
                    WHERE
                        id=%(id)s
                """,
                {
                    "id": user.id()
                }
            )
