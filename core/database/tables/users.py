from ..objects.user import User
import bcrypt
from ..no_value import NoValue

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

    def get_user_by_id(self, user_id):
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
            return None

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

    def create_user(self, username, password, email, first_name, last_name, phone, email_verified, recaptcha_score=None, ip_address=None, ip_country=None):
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

        # Password must be at least 8 characters in unicode
        # and be no more than 60 characters in UTF-8
        # and can't contain the null byte when in UTF-8

        if len(password) < 8:
            raise UsersException("Password must be at least 8 characters.")

        if len(password.encode("utf-8")) > 60:
            raise UsersException("Your password is too long. (Can't be longer than 60 bytes when in UTF-8 formatting.)")

        # Process phone number
        if phone is not None:
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
                    (password, username, email, phone, first_name, last_name, is_email_verified, recaptcha_score, ip_address, ip_country)
                    VALUES
                        (%(password)s, %(username)s, %(email)s, %(phone)s, %(first_name)s, %(last_name)s, %(email_verified)s, %(recaptcha_score)s, %(ip_address)s, %(ip_country)s)
            """,
            {
                "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                "username": username,
                "phone": phone,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "email_verified": email_verified,
                "recaptcha_score": recaptcha_score,
                "ip_address": ip_address,
                "ip_country": ip_country
            }
        )
        user = self.get_by_username(username)
        return user

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

    def create_pseudo_user(self, username, password, first_name, last_name):
        """Inserts an entry to user table. Routine is created for system generated users 

        Params:
            username: username to login
            password: password to login
            first_name: first name of the user
            last_name: last name of the user

        Returns:
            An User object

        Raises:
            UsersException
        """
        user = self.get_by_username(username)
        if user is not None:
            raise UsersException("Username is already being used.")

        # Password must be at least 8 characters in unicode
        # and be no more than 60 characters in UTF-8
        # and can't contain the null byte when in UTF-8

        if len(password) < 8:
            raise UsersException("Password must be at least 8 characters.")

        if len(password.encode("utf-8")) > 60:
            raise UsersException("Password is too long. (Can't be longer than 60 bytes when in UTF-8 formatting.)")

        self._db.execute(
            """
                INSERT INTO users
                    (password, username, first_name, last_name, is_system_generated)
                    VALUES
                        (%(password)s, %(username)s, %(first_name)s, %(last_name)s, %(is_system_generated)s)
            """,
            {
                "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "is_system_generated": 1
            }
        )
        user = self.get_by_username(username)
        return user

    def get_users(self, id=NO_VALUE, username=NO_VALUE, email=NO_VALUE, phone=NO_VALUE, first_name=NO_VALUE, last_name=NO_VALUE,
                  is_email_verified=NO_VALUE, failed_attempts=NO_VALUE, is_user_locked=NO_VALUE, locked_time=NO_VALUE,
                  is_system_generated=NO_VALUE, recaptcha_score=NO_VALUE):
        """
        Returns the users based on provided attributes

        Params:
            id: USer ID
            username: username to login
            email: email to login
            phone: phone number of user
            first_name: first name of the user
            last_name: last name of the user
            is_email_verified: email verification status
            failed_attempts: failed login attempts
            is_user_locked: user account locked status
            is_system_generated: indicates if user is system generated

        Returns:
            A list of users or None

        """
        base_query = "SELECT * FROM users"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if username is not NO_VALUE:
            query_conditions.append("username = %(username)s")
            query_values["username"] = username
        if email is not NO_VALUE:
            query_conditions.append("email = %(email)s")
            query_values["email"] = email
        if phone is not NO_VALUE:
            query_conditions.append("phone = %(phone)s")
            query_values["phone"] = phone
        if first_name is not NO_VALUE:
            query_conditions.append("first_name = %(first_name)s")
            query_values["first_name"] = first_name
        if last_name is not NO_VALUE:
            query_conditions.append("last_name = %(last_name)s")
            query_values["last_name"] = last_name
        if is_email_verified is not NO_VALUE:
            query_conditions.append("is_email_verified = %(is_email_verified)s")
            query_values["is_email_verified"] = is_email_verified
        if failed_attempts is not NO_VALUE:
            query_conditions.append("failed_attempts = %(failed_attempts)s")
            query_values["failed_attempts"] = failed_attempts
        if is_user_locked is not NO_VALUE:
            query_conditions.append("is_user_locked = %(is_user_locked)s")
            query_values["is_user_locked"] = is_user_locked
        if locked_time is not NO_VALUE:
            query_conditions.append("locked_time = %(locked_time)s")
            query_values["locked_time"] = locked_time
        if is_system_generated is not NO_VALUE:
            query_conditions.append("is_system_generated = %(is_system_generated)s")
            query_values["is_system_generated"] = is_system_generated
        if recaptcha_score is not NO_VALUE:
            query_conditions.append("recaptcha_score = %(recaptcha_score)s")
            query_values["recaptcha_score"] = recaptcha_score
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        user_rows = self._db.execute_d(query, query_values)
        if len(user_rows) > 0:
            return user_rows
        else:
            return []

    def get_users_and_accounts(self, user_id=NO_VALUE, user_email=NO_VALUE):
        """
        Gets the user and accounts based on parameters

        Params:
            user_id: user id

        Returns:
            A list of user and account rows joined or an empty list
        """

        base_query = """
            SELECT *, u.id as user_id, a.id as account_id, u.phone as user_phone, a.phone as account_phone FROM users u
            INNER JOIN account_users au on au.user = u.id
            INNER JOIN accounts a on a.id = au.account 
        """
        query_conditions = []
        query_values = {}

        if user_id is not NO_VALUE:
            query_conditions.append("u.id = %(user_id)s")
            query_values["user_id"] = user_id

        if user_email is not NO_VALUE:
            query_conditions.append("u.email = %(user_email)s")
            query_values["user_email"] = user_email

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        result_rows = self._db.execute_d(query, query_values)
        if len(result_rows) > 0:
            return result_rows
        else:
            return []

    def modify_user(self, id, email=NO_VALUE, first_name=NO_VALUE, last_name=NO_VALUE,
                    phone=NO_VALUE, password=NO_VALUE, confirm_password=NO_VALUE, is_email_verified=NO_VALUE):
        """
        Transform, validates and updates an user record.
        """
        # username = Users._format_field(username)
 
        # # Email must exist and contain an '@'
        if email is not NO_VALUE:
            if len(email) == 0:
                raise UsersException("Email is blank.")
            if '@' not in email or '.' not in email or len(email) < 5:
                raise UsersException("The email you entered is incomplete.")
            if ' ' in email:
                raise UsersException("Spaces cannot be in the email.")
            existing_row = self.get_users(id=id)[0]
            if existing_row["email"] != email:
                # Double-usage. 
                existing_user = self.get_users(email=email)
                if len(existing_user) > 0:
                    raise UsersException("Email is already being used.")
                else:
                    # email will be updated 
                    is_email_verified = 0
            else:
                #don't update since email is same
                email = NO_VALUE

        if password is not NO_VALUE:
            if password is None:
                password = NO_VALUE
            else:
                password = Users._format_field(password)
                if len(password) < 8:
                    raise UsersException("Password must be at least 8 characters.")

                if len(password.encode("utf-8")) > 60:
                    raise UsersException("Your password is too long.")

                if (password != confirm_password):
                    raise UsersException("Password and Confirm password are not the same!")

        # Process phone number
        if phone is not NO_VALUE:
            digits = ''.join(chr(ord('0') + i) for i in range(10))
            temp_phone = ""
            for c in phone:
                if c in digits:
                    temp_phone += c
            phone = temp_phone
            # If phone is empty it is NULL
            if phone == "":
                phone = None
        
        self.update_user(id, email, first_name, last_name, phone, password, is_email_verified)

    def update_user(self, id, email=NO_VALUE, first_name=NO_VALUE, last_name=NO_VALUE,
                       phone=NO_VALUE, password=NO_VALUE, is_email_verified=NO_VALUE):
        """
        Updates an user.

        Params:
            username: This is the user id, just the user can see it
            email: email address of user,just the user can see it
            password: This is corresponding password used to login
            phone: phone number of user
            first: first name of the user.
            last: last name of the user.
        """
        base_query = "UPDATE users"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if email is not NO_VALUE:
            query_conditions.append("email = %(email)s")
            query_values["email"] = email
            query_conditions.append("username = %(username)s")
            query_values["username"] = email
        if first_name is not NO_VALUE:
            query_conditions.append("first_name = %(first_name)s")
            query_values["first_name"] = first_name
        if first_name is not NO_VALUE:
            query_conditions.append("first_name = %(first_name)s")
            query_values["first_name"] = first_name
        if last_name is not NO_VALUE:
            query_conditions.append("last_name = %(last_name)s")
            query_values["last_name"] = last_name
        if phone is not NO_VALUE:
            query_conditions.append("phone = %(phone)s")
            query_values["phone"] = phone
        if password is not NO_VALUE:
            query_conditions.append("password = %(password)s")
            query_values["password"] = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        if is_email_verified is not NO_VALUE:
            query_conditions.append("is_email_verified = %(is_email_verified)s")
            query_values["is_email_verified"] = is_email_verified
        if phone is not NO_VALUE:
            query_conditions.append("phone = %(phone)s")
            query_values["phone"] = phone
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update user record")

    # def update_user(self, username, first_name=NO_VALUE, last_name=NO_VALUE, phone=NO_VALUE, password=None, confirm_password=None, is_email_verified=NO_VALUE):
    #     """Updates user information.

    #     Params:
    #         username: This is the user id, just the user can see it
    #         email: email address of user,just the user can see it
    #         password: This is corresponding password used to login
    #         phone: phone number of user
    #         first: first name of the user.
    #         last: last name of the user.
    #     Returns:
    #         None

    #     Raises:
    #         UsersException

    #     """
    #     username = Users._format_field(username)

    #     if password is not None:
    #         password = Users._format_field(password)
    #         if len(password) < 8:
    #             raise UsersException("Password must be at least 8 characters.")

    #         if len(password.encode("utf-8")) > 60:
    #             raise UsersException("Your password is too long.")

    #         if (password != confirm_password):
    #             raise UsersException("Password and Confirm password are not the same!")

    #     # Process phone number
    #     if phone is not NO_VALUE:
    #         digits = ''.join(chr(ord('0') + i) for i in range(10))
    #         temp_phone = ""
    #         for c in phone:
    #             if c in digits:
    #                 temp_phone += c
    #         phone = temp_phone
    #         # If phone is empty it is NULL
    #         if phone == "":
    #             phone = None

    #     set_frags = frag()
    #     if first_name is not NO_VALUE:
    #         set_frags = frag(
    #                         set_frags,
    #                         "first_name=:first_name,",
    #                         first_name=first_name
    #                     )
    #     if last_name is not NO_VALUE:
    #         set_frags = frag(
    #                         set_frags,
    #                         "last_name=:last_name,",
    #                         last_name=last_name
    #                     )
    #     if phone is not NO_VALUE:
    #         set_frags = frag(
    #                         set_frags,
    #                         "phone=:phone,",
    #                         phone=phone
    #                     )
    #     #password should never be none
    #     if password is not None:
    #         set_frags = frag(
    #                         set_frags,
    #                         "password=:password,",
    #                         password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    #                     )
    #     if is_email_verified is not NO_VALUE:
    #         set_frags = frag(
    #                         set_frags,
    #                         "is_email_verified=:is_email_verified,",
    #                         is_email_verified=is_email_verified
    #                     )

    #     if len(set_frags[0]) > 0 and len(set_frags[1]) > 0:
    #         # check if last character in SQL is , and remove it if so
    #         if set_frags[0][-1] == ",":
    #             set_frags = (set_frags[0][:-1], set_frags[1])

    #         self._db.exec_frag(
    #             frag(
    #                 "UPDATE users SET",
    #                 set_frags,
    #                 frag(
    #                     "WHERE username=:username",
    #                     username=username
    #                 )
    #             )
    #         )