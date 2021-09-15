from core.database.objects.employee import Employee
from .. import database
import bcrypt
from ..no_value import NoValue
from ..frag import frag

NO_VALUE = NoValue()


class EmployeesException(Exception):
    """Generic user exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for UsersException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Employees:

    def __init__(self, db: 'database.Database'):
        self._db = db

    def get(self, user_id):
        """Gets a employee by their ID.

        Params:
            employee_id: employee's ID

        Returns:
            A employee object on success, or None on no match.
        """
        matching_users = self._db.execute_d(
            """
                SELECT * FROM employees
                WHERE
                    id=%(id)s
            """,
            {
                "id": user_id
            }
        )

        if len(matching_users) != 1:
            return None

        return Employee(matching_users[0])

    def get_by_email(self, email):
        """Get a employee by email.

        Params:
            email: The employee's email

        Returns:
            A employee object on success, or None on no match.
        """
        matching_employee = self._db.execute_d(
            """
                SELECT * FROM employees
                WHERE
                    email=%(email)s
            """,
            {
                "email": self._format_field(email)
            }
        )

        if len(matching_employee) == 0:
            return None
        return Employee(matching_employee[0])

    def get_by_username(self, username):
        """Get a employee by username.

        Params:
            username: The employee's username

        Returns:
            A employee object on success, or None on no match.
        """
        matching_employee = self._db.execute_d(
            """
                SELECT * FROM employees
                WHERE
                    username=%(username)s
            """,
            {
                "username": username
            }
        )

        if len(matching_employee) != 1:
            return None
        return Employee(matching_employee[0])

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