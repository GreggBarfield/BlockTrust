import traceback
import bcrypt

from flask import session, g

from ..objects.user import User

class UsersException(Exception):
    """Generic user exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for UsersException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class LoginException(UsersException):
    """Generic user exception."""

    def __init__(self, reason):
        """Constructor for LoginException.

        Params:
            reason: The reason it failed.
                This will likely end up getting printed to the user,
                so be careful.
        """
        super().__init__(reason)


class NoUserFoundException(UsersException):
    """User was not found."""
    pass


class SignupFailedException(UsersException):
    """Signup failed."""

    def __init__(self, reason):
        """Constructor for SignupFailedException.

        Params:
            reason: The reason signup failed.
                This will likely end up getting printed to the user,
                so be careful.
        """
        super().__init__(reason)


class Users:

    SESSION_USER_ID_VAR = "user_id"


    def __init__(self, db):
        self._db = db
    
    def login(self, identifier, password="", override=False):
        """Performs a login.

        Params:
            identifier: Username, email, or user ID.
            password: Plaintext password (default "")
            override: True to override default login
        
        Raises:
            UsersException, LoginException

        Returns:
            An User object on success.
        """

        try:
            if password is None and override is not True:
                raise UsersException("password is None")
            
            if override is not True and override is not False:
                raise UsersException("override is bad")

            identifier = self._format_field(identifier)
            password = self._format_field(password)

            if identifier == "" or password == "":
                raise LoginException("Identifier or password is blank.")

            user_row = None

            # Try ID first for security purposes
            
            all_digits = True
            
            for c in identifier:
                if c not in "0123456789":  # ASCII digits ONLY
                    all_digits = False
            
            if user_row is None and all_digits:
                id_results = self._db.execute_d(
                    """
                        SELECT * FROM users
                        WHERE
                            id=%(id)s
                    """,
                    {
                        "id": identifier
                    }
                )
                if len(id_results) == 1:
                    user_row = id_results[0]
        
            # Try username

            if user_row is None:
                username_results = self._db.execute_d(
                    """
                        SELECT * FROM users
                        WHERE
                            username=%(username)s
                    """,
                    {
                        "username": identifier
                    }
                )
                if len(username_results) == 1:
                    user_row = username_results[0]

            # Try email

            if user_row is None and '@' in identifier:
                email_results = self._db.execute_d(
                    """
                        SELECT * FROM users
                        WHERE
                            email=%(email)s
                    """,
                    {
                        "email": identifier
                    }
                )
                if len(email_results) == 1:
                    user_row = email_results[0]

            # End of tries

            generic_error = "Sorry, that didn't match any of our records. Try again, or contact us if you're having issues."

            if user_row is None:
                raise LoginException(generic_error)

            if override is not True and not bcrypt.checkpw(password.encode("utf-8"), user_row["password"].encode("utf-8")):
                raise LoginException(generic_error)

            g.user = User(self._db, user_row)
            session.clear()
            session[Users.SESSION_USER_ID_VAR] = g.user.id()

            return g.user
        except LoginException as e:
            raise e
        except UsersException as e:
            raise e
        except Exception as e:
            raise UsersException("other exception")
    
    def logout(self):
        """Clear session of user info and remove g user."""
        g.user = None
        session[Users.SESSION_USER_ID_VAR] = ""
        session.clear()

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
                "email": self._format_field(email)
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
                "username": self._format_field(username)
            }
        )

        if len(matching_users) != 1:
            raise NoUserFoundException()
        return User(self._db, matching_users[0])

    def signup(self, username, email, phone, first, last, password, confirm_password):
        """Create new user account.

        Params:
            username: new username
            email: new email
            phone: new phone number (must be at least blank string)
            first: first name
            last: last name (must be at least blank string)
            password: password
            confirm_password: the confirmed password
                (if password comes from a user field, confirm_password should too;
                don't just duplicate password)
        
        Returns:
            Nothing
        
        Raises:
            SignupFailedException on failure with the reason.
        """
        username = self._format_field(username)
        email = self._format_field(email)
        phone = self._format_field(phone)
        first = self._format_field(first)
        last = self._format_field(last)
        password = self._format_field(password)
        confirm_password = self._format_field(confirm_password)

        # Double-usage
        
        try:
            self.get_by_email(email)
            raise SignupFailedException("Email is already being used.")
        except NoUserFoundException:
            pass

        try:
            self.get_by_username(username)
            raise SignupFailedException("Username is already being used.")
        except NoUserFoundException:
            pass

        # We don't really care whether or not the phone is being used more than once

        # Correct symbols
        # This is VERY IMPORTANT, otherwise login() could have difficulties
        # if someone uses an integer for a username for example.

        # Username must exist, not be all digits (so it does't look like an ID),
        # be in proper char set
        # and not contain an '@' (so it doesn't look like an email)
        # (the '@' is just an explicit check)

        if '@' in username:
            raise SignupFailedException("'@' cannot be in the username.")

        # Confusing when a user gets ' ' cannot be in username, so be more specific with spaces
        if ' ' in username:
            raise SignupFailedException("Spaces cannot be in the username.")

        if len(username) == 0:
            raise SignupFailedException("Username is blank.")


        # .isdigit and .isalpha is NOT safe (subscripts and stuff can count as digit)
        digits = ''.join(chr(ord('0') + i) for i in range(10))
        all_digits = True
        for c in username:
            if c not in digits:
                all_digits = False

        if all_digits:
            raise SignupFailedException("Username cannot be all digits.")

        valid_chars = (
            digits +  # Digits
            ''.join(chr(ord('a') + i) for i in range(26)) +  # Lowercase chars
            ''.join(chr(ord('A') + i) for i in range(26)) +  # Uppercase chars
            '_'  # Other
        )

        for c in username:
            if c not in valid_chars:
                raise SignupFailedException("Invalid character '" + c + "' in username.")
        
        # Email must exist and contain an '@'

        if len(email) == 0:
            raise SignupFailedException("Email is blank.")

        if '@' not in email or '.' not in email or len(email) < 5:
            raise SignupFailedException("The email you entered is incomplete.")

        # Password must be at least 10 characters in unicode
        # and be no more than 60 characters in UTF-8
        # and can't contain the null byte when in UTF-8

        if len(password) < 10:
            raise SignupFailedException("Password must be at least 10 characters.")
    
        if len(password.encode("utf-8")) > 60:
            raise SignupFailedException("Your password is too long. (Can't be longer than 60 bytes when in UTF-8 formatting.)")

        # Password should equal confirm_password

        if password != confirm_password:
            raise SignupFailedException("The passwords you entered were not identical.")

        # Process phone number

        temp_phone = ""
        for c in phone:
            if c in digits:
                temp_phone += c
        phone = temp_phone

        # If phone is empty it is -1
        if phone == "":
            phone = "-1"

        self._db.execute_d(
            """
                INSERT INTO users
                    (password, username, email, phone, first, last, email_verified)
                    VALUES
                        (%(password)s, %(username)s, %(email)s, %(phone)s, %(first)s, %(last)s, %(email_verified)s)
            """,
            {
                "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                "username": username,
                "email": email,
                "phone": phone,
                "first": first,
                "last": last,
                "email_verified": ""
            }
        )


    def session_open(self):
        """Load session into app context."""
        g.user = None
        if Users.SESSION_USER_ID_VAR in session and session[Users.SESSION_USER_ID_VAR] != "":
            g.user = self.get(session[Users.SESSION_USER_ID_VAR])
        else:
            session[Users.SESSION_USER_ID_VAR] = ""
            # TODO: if this fails, abort request and redirect to issue opening session screen


    def _format_field(self, field):
        """Format a user info field.

        Params:
            field: The user's field (str)
        """
        if field is None:
            raise ValueError("field can't be None")
        if b'\x00' in field.encode("utf-8"):
            raise ValueError("Null bytes in the field??? Stop whatever is going on")
        return field.strip(" \n\r\t")
