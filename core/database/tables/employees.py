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

    def get_by_id(self, user_id):
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

    def create_employee(self, username, password, email, first_name, last_name, phone=None):
        """Creates a new employee

        Params:
            username: username to login
            password: password to login
            email: email of the employee
            first_name: first name of the employee
            last_name: last name of the employee
            phone: phone of the employee
            is_admin: Specifies whether the employee is an admin(1 for yes, 0 for no) (Add in future)

        Returns:
            An employee object

        Raises:
            EmployeesException
        """

        # Email must exist and contain an '@'
        if len(email) == 0:
            raise EmployeesException("Email is blank.")
        if '@' not in email or '.' not in email or len(email) < 5:
            raise EmployeesException("The email you entered is incomplete.")
        if ' ' in email:
            raise EmployeesException("Spaces cannot be in the email.")
        # Double-usage
        user = self.get_by_email(email)
        if user is not None:
            raise EmployeesException("Email is already being used.")

        # Double-usage. This should never happen since if email doesn't exist, username shouldn't as well.
        user = self.get_by_username(username)
        if user is not None:
            raise EmployeesException("Username is already being used.")

        # Password must be at least 10 characters in unicode
        # and be no more than 60 characters in UTF-8
        # and can't contain the null byte when in UTF-8

        if len(password) < 8:
            raise EmployeesException("Password must be at least 8 characters.")

        if len(password.encode("utf-8")) > 60:
            raise EmployeesException("Your password is too long. (Can't be longer than 60 bytes when in UTF-8 formatting.)")

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

        self._db.execute(
            """
                INSERT INTO employees
                    (password, username, email, phone, first_name, last_name)
                    VALUES
                        (%(password)s, %(username)s, %(email)s, %(phone)s, %(first_name)s, %(last_name)s)
            """,
            {
                "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                "username": username,
                "phone": phone,
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
        )
        employee = self.get_by_username(username)
        return employee

    def get(self, id=NO_VALUE):
        """
        Returns the employee based on provided attributes
        """
        base_query = "SELECT * FROM employees"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        employee_rows = self._db.execute_d(query, query_values)
        if len(employee_rows) > 0:
            return employee_rows
        else:
            return []

    def update(self, id, impersonating_as_user_id=NO_VALUE):
        """
        Updates an employee.
        """
        base_query = "UPDATE employees"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if impersonating_as_user_id is not NO_VALUE:
            query_conditions.append("impersonating_as_user_id = %(impersonating_as_user_id)s")
            query_values["impersonating_as_user_id"] = impersonating_as_user_id
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Values for fields to update employee record not given")
        return self._db.row_count()
