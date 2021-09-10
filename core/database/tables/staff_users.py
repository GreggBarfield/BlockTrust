from ..objects.staff_user import StaffUser
import bcrypt


class StaffUsersException(Exception):
    """Generic user exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for UsersException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class StaffUsers:

    def __init__(self, db):
        self._db = db

    @staticmethod
    def _format_field(field):
        """Format a staff user info field.

        Params:
            field: The staff user's field (str)
        """
        if field is None:
            raise ValueError("field can't be None")
        if b'\x00' in field.encode("utf-8"):
            raise ValueError("Null bytes in the field??? Stop whatever is going on")
        field.strip(" \n\r\t")
        return field if field != '' else None

    def get(self, staff_id):
        """Gets a staff user by their ID.

        Params:
            staff_id: Staff's user ID

        Returns:
            A StaffUser object on success, or None on no match.
        """
        matching_users = self._db.execute_d(
            """
                SELECT * FROM staff
                WHERE
                    id=%(id)s
            """,
            {
                "id": staff_id
            }
        )

        if len(matching_users) != 1:
            raise StaffUsersException()

        return StaffUser(self._db, matching_users[0])

    def get_by_email(self, email):
        """Get a staff user by email.

        Params:
            email: The staff user's email

        Returns:
            A StaffUser object on success, or None on no match.
        """
        matching_users = self._db.execute_d(
            """
                SELECT * FROM staff
                WHERE
                    email=%(email)s
            """,
            {
                "email": StaffUsers._format_field(email)
            }
        )

        if len(matching_users) == 0:
            return None
        return StaffUser(self._db, matching_users[0])

    def get_by_username(self, username):
        """Get a staff user by username.

        Params:
            username: The staff user's username

        Returns:
            A StaffUser object on success, or None on no match.
        """
        matching_users = self._db.execute_d(
            """
                SELECT * FROM staff
                WHERE
                    username=%(username)s
            """,
            {
                "username": StaffUsers._format_field(username)
            }
        )

        if len(matching_users) != 1:
            return None
        return StaffUser(self._db, matching_users[0])

    def create_staff_user(self, username, password, email, first_name, last_name, phone, is_admin):
        """Creates a new user

        Params:
            username: username to login
            password: password to login
            email: email of the staff user
            first_name: first name of the staff user
            last_name: last name of the staff user
            phone: phone of the staff user
            is_admin: Specifies whether the staff user is an admin(1 for yes, 0 for no)

        Returns:
            A User object

        Raises:
            StaffUsersException
        """

        # Email must exist and contain an '@'
        if len(email) == 0:
            raise StaffUsersException("Email is blank.")
        if '@' not in email or '.' not in email or len(email) < 5:
            raise StaffUsersException("The email you entered is incomplete.")
        if ' ' in email:
            raise StaffUsersException("Spaces cannot be in the email.")
        # Double-usage
        user = self.get_by_email(email)
        if user is not None:
            raise StaffUsersException("Email is already being used.")

        # Double-usage. This should never happen since if email doesn't exist, username shouldn't as well.
        user = self.get_by_username(username)
        if user is not None:
            raise StaffUsersException("Username is already being used.")

        # Password must be at least 10 characters in unicode
        # and be no more than 60 characters in UTF-8
        # and can't contain the null byte when in UTF-8

        if len(password) < 10:
            raise StaffUsersException("Password must be at least 10 characters.")

        if len(password.encode("utf-8")) > 60:
            raise StaffUsersException("Your password is too long. (Can't be longer than 60 bytes when in UTF-8 formatting.)")

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
                INSERT INTO staff
                    (password, username, email, phone, first_name, last_name, is_admin)
                    VALUES
                        (%(password)s, %(username)s, %(email)s, %(phone)s, %(first_name)s, %(last_name)s, %(is_admin)s)
            """,
            {
                "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                "username": username,
                "phone": phone,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "is_admin": is_admin
            }
        )
        staff_user = self.get_by_username(username)
        return staff_user
