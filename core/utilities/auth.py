import bcrypt
from flask import g, session
from ..database.tables.users import Users
from ..database.objects.user import User
from ..database.tables.users import UsersException
from ..database.objects.employee import Employee
from ..database.tables.employees import Employees, EmployeesException
from ..database.tables.event_logs import EventLogs, event_type_by_name
import time
from ..database.tables.connection_invites import ConnectionInvites
from ..database.tables.account_links import AccountLinks
from ..database.combinations import create_connections_for_supply_chain, perform_new_account_actions
from ..renderers.email import render_email

from ..utilities.general_utilities import validate_email, format_field
from ..utilities.email import send_email
from .constants import SECONDS_IN_ONE_DAY
from ..config import SUPPORT_GENERAL_EMAIL
from ..sectors import SECTORS_ID_TO_NAME

# since session objects are easily decoded, we use key names which make no sense
SESSION_USER_ID_VAR = "abc"
SESSION_ACCOUNT_ID_VAR = "def"
SESSION_IS_ADMIN_VAR = "ghi"
SESSION_EMPLOYEE_ID_VAR = "jkl"
SESSION_STRIPE_ACCOUNT_ID_VAR = "mno"


class AuthException(Exception):
    """Generic auth exception."""
    pass


class LoginException(AuthException):
    """Generic auth login exception."""

    def __init__(self, reason):
        """Constructor for LoginException.

        Params:
            reason: The reason it failed.
                This will likely end up getting printed to the user,
                so be careful.
        """
        super().__init__(reason)


class EmailNotVerifiedException(AuthException):
    """Exception raised when a user with an unverified email tries to login"""
    def __init__(self, reason):
        """Constructor for EmailNotVerifiedException
        Params:
            reason: The reason why login failed. (Unverified email)
        """
        super().__init__(reason)


class SignupFailedException(AuthException):
    """Signup failed."""

    def __init__(self, reason):
        """Constructor for SignupFailedException.

        Params:
            reason: The reason signup failed.
                This will likely end up getting printed to the user,
                so be careful.
        """
        super().__init__(reason)


def session_open():
    """Load session into app context."""
    session_open_user()
    if g.user is not None:
        session_open_account()
    else:
        session_open_employee()


def session_open_employee():
    """"Load employee session into app context."""
    if SESSION_EMPLOYEE_ID_VAR in session and session[SESSION_EMPLOYEE_ID_VAR] != "":
        g.employee = Employees(g.db).get(session[SESSION_EMPLOYEE_ID_VAR])
    else:
        session[SESSION_EMPLOYEE_ID_VAR] = ""


def session_start_account(account_id):
    """Start a session with this account.

    Note that g.user should already be set to allow this to work.

    Params:
        account: Account to set as active

    Raises:
        NoAccountUserFound on user not found
    """
    g.account = None
    session[SESSION_ACCOUNT_ID_VAR] = ""
    session[SESSION_IS_ADMIN_VAR] = ""
    attempt_login = g.db.account_users.get_by_user_and_account_id(g.user, account_id)
    if attempt_login.account_id() == account_id and attempt_login.user_id() == g.user.id():
        session[SESSION_ACCOUNT_ID_VAR] = account_id
        session[SESSION_IS_ADMIN_VAR] = attempt_login.is_admin()
        session_open_account()


def session_open_user():
    """Load user session into app context."""
    g.user = None
    if SESSION_USER_ID_VAR in session and session[SESSION_USER_ID_VAR] != "":
        g.user = g.db.users.get_user_by_id(session[SESSION_USER_ID_VAR])
        if SESSION_EMPLOYEE_ID_VAR in session and session[SESSION_EMPLOYEE_ID_VAR] != "":
            g.is_employee_impersonating = 1
        else:
            g.is_employee_impersonating = 0
    else:
        session[SESSION_USER_ID_VAR] = ""
        # TODO: if this fails, abort request and redirect to issue opening session screen


def session_open_account():
    """Load account session into app context."""
    g.account = None
    if SESSION_ACCOUNT_ID_VAR in session and session[SESSION_ACCOUNT_ID_VAR] != "":
        g.account = g.db.accounts.get_account_by_id(session[SESSION_ACCOUNT_ID_VAR])
        if SESSION_IS_ADMIN_VAR in session and session[SESSION_IS_ADMIN_VAR] != "":
            # Not bothering to get the account_user from db again on each request, since we don't let users change anyone's
            # role and therefore assuming is_admin will not change during an active session
            g.is_admin = session[SESSION_IS_ADMIN_VAR]
    else:
        session[SESSION_ACCOUNT_ID_VAR] = ""


def signup(username, email, phone, first_name, last_name, password, confirm_password, company, partner, affiliate_id, sector, address, city, state, zip_code, 
            personal_phone, recaptcha_score, ip_address, ip_country):
    """Create new user account.

    Params:
        username: new username
        email: new email
        phone: company phone number (must be at least blank string)
        first: first name
        last: last name (must be at least blank string)
        password: password
        confirm_password: the confirmed password
            (if password comes from a user field, confirm_password should too;
            don't just duplicate password)
        company: company name
        affiliate_id: affliate id
        city: city
        state: state
        zip: zip
    Returns:
        Nothing

    Raises:
        SignupFailedException on failure with the reason.
    """
    username = format_field(username)
    email = format_field(email)
    phone = format_field(phone)
    first_name = format_field(first_name)
    last_name = format_field(last_name)
    password = format_field(password)
    confirm_password = format_field(confirm_password)
    company = format_field(company)
    partner = format_field(partner)
    affiliate_id = format_field(affiliate_id)
    sector = format_field(sector)
    address = format_field(address)
    city = format_field(city)
    state = format_field(state)
    zip_code = format_field(zip_code)
    personal_phone = format_field(personal_phone)
    ip_address = format_field(ip_address)
    ip_country = format_field(ip_country)

    # Password should equal confirm_password

    if password != confirm_password:
        raise SignupFailedException("The passwords you entered were not identical.")

    if affiliate_id and affiliate_id.isdigit():
        affiliate_id = int(affiliate_id)
    sector, phone = g.db.accounts.validate_new_account(sector, partner, affiliate_id, phone)

    user = g.db.users.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=personal_phone,
        email_verified=0,
        recaptcha_score=recaptcha_score,
        ip_address=ip_address,
        ip_country=ip_country
    )

    try:
        account_obj = g.db.accounts.create_account_with_admin(
            user=user,
            company=company,
            sector=sector,
            partner=partner,
            affiliate_id=affiliate_id,
            address=address,
            city=city,
            state=state,
            zip=zip_code,
            phone=phone
        )
        ConnectionInvites(g.db).convert_invites_to_connections(email, account_obj)

        perform_new_account_actions(db=g.db, account_id=account_obj.id(), user_id=user.id(),
                                    event_type_id=event_type_by_name["Signup"], sector_id=account_obj.sector_id())

    except Exception as e:
        raise e


def logout():
    """Clear session of user info and remove g user."""
    session.clear()
    g.user=None
    g.employee=None


def reset_user_password(email, new_password, confirm_password):
    """
    Changing the password in the user database

    Params:
        email: The user email for which the password needs to be updated
        new_password: The new password which needs to be set

    Returns: None

    Raises:
        Exception on failure with the reason.
    """
    try:
        # Check if password reset link is valid. As token.py returns false if link is Invalid
        if email is False:
            raise Exception("Password reset link is Invalid")
        user = Users(g.db).get_users(email=email)[0]
        Users(g.db).validate_user(email, new_password, confirm_password)
        Users(g.db).modify_user(
            id=user["id"],
            password=new_password,
            confirm_password=confirm_password
        )
    except Exception as e:
        raise e


def confirm(email):
    """Confirms that the user email is verified"""
    user_account = g.db.users.get_users_and_accounts(user_email=email)[0]
    g.db.users.modify_user(id=user_account["user_id"], is_email_verified=1)
    EventLogs(g.db).insert_event_log(user_id=user_account["user_id"], event_type_id=event_type_by_name["Email Verified"])
    partner_account_company = ""
    if user_account["partner_account"] is not None:
        partner_account = g.db.accounts.get_account_by_id(account_id=user_account["partner_account"])
        partner_account_company = partner_account.company()
    send_email(
        "BlockTrust Network New Registration Information",
        render_email("new_account_info.html", {
            'user_account': user_account,
            'partner_account_company': partner_account_company,
            'sectors_id_to_name': SECTORS_ID_TO_NAME
        }), SUPPORT_GENERAL_EMAIL
    )


def login(identifier, password=""):
    """Performs a login.

    Params:
        identifier: Username, email, or user ID.
        password: Plaintext password (default "")

    Raises:
        UsersException, LoginException

    Returns:
        An User object on success.
    """

    try:

        if password is None:
            raise LoginException("password is None")

        identifier = Users._format_field(identifier)
        password = Users._format_field(password)

        if identifier == "" or password == "":
            raise LoginException("Identifier or password is blank.")

        user_row = None

        # Try ID first for security purposes
        all_digits = True
        for c in identifier:
            if c not in "0123456789":  # ASCII digits ONLY
                all_digits = False
        if user_row is None and all_digits:
            id_results = g.db.execute_d(
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
            username_results = g.db.execute_d(
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
            email_results = g.db.execute_d(
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
        generic_error = "Sorry, that didn't match any of our records. Try again, or contact us if you're having issues. Note that after 3 consecutive incorrect attempts, your account will be locked for 24 hours"

        if user_row is None:
            raise LoginException(generic_error)

        # To check if the user profile being accessed has a verified email
        if user_row['is_email_verified'] == 0:
            email_not_verified_error = "Your email is not verified. Please verify your email and try to login again"
            raise EmailNotVerifiedException(email_not_verified_error)

        locked_account_error = "Your account (" + user_row["username"] + ") is locked for 24 hours due to reaching the maximum 3 consecutive failed login attempts. Contact us if you're having issues"
        if int(user_row["is_user_locked"]) == 1:
            
            # If the user is currently locked, check whether the user has waited for one day. If not, throw error.
            
            if (user_row["locked_time"] + SECONDS_IN_ONE_DAY) > int(round(time.time())):
                raise LoginException(locked_account_error)
            else:
                g.db.execute(
                """
                    UPDATE users
                    SET failed_attempts =  %(failed_attempts)s, 
                    is_user_locked = %(is_user_locked)s, 
                    locked_time = %(locked_time)s
                    WHERE
                        users.id=%(id)s
                """,
                    {
                        "id": user_row["id"],
                        "failed_attempts": 0,
                        "is_user_locked": 0,
                        "locked_time": None
                    }
                )

        if not bcrypt.checkpw(password.encode("utf-8"), user_row["password"].encode("utf-8")):
            failed_attempts = user_row["failed_attempts"] + 1
            g.db.execute_d(
                    """
                        UPDATE users
                        SET failed_attempts =  %(failed_attempts)s
                        WHERE
                            users.id=%(id)s
                    """,
                    {
                        "id": user_row["id"],
                        "failed_attempts":  failed_attempts
                    }
            )
 
            if failed_attempts == 3:
                g.db.execute(
                """
                    UPDATE users
                    SET is_user_locked = %(is_user_locked)s, locked_time = %(locked_time)s
                    WHERE
                        users.id=%(id)s
                """,
                    {
                        "id": user_row["id"],
                        "is_user_locked": 1,
                        "locked_time": int(round(time.time()))
                    }
                )
                raise LoginException(locked_account_error)
         
            raise LoginException(generic_error)


        if  user_row["failed_attempts"] > 0:
            g.db.execute(
            """
                UPDATE users
                SET failed_attempts =  %(failed_attempts)s
                WHERE
                    users.id=%(id)s
            """,
                {
                    "id": user_row["id"],
                    "failed_attempts": 0
                }
            )      
        g.user = User(g.db, user_row)
        session.clear()
        session[SESSION_USER_ID_VAR] = g.user.id()
        return g.user
    except LoginException as e:
        raise e
    except EmailNotVerifiedException as e:
        raise e
    except UsersException as e:
        raise e
    except Exception as e:
        raise LoginException("other exception")


def employee_login(identifier, password=""):
    """Performs a employee login.

    Params:
        identifier: Username, or email.
        password: Plaintext password (default "")

    Raises:
        UsersException, LoginException

    Returns:
        An User object on success.
    """

    try:
        if password is None:
            raise LoginException("password is None")

        identifier = Users._format_field(identifier)
        password = Users._format_field(password)

        if identifier == "" or password == "":
            raise LoginException("Identifier or password is blank.")

        employee_row = None

        # Try username

        if employee_row is None:
            username_results = g.db.execute_d(
                """
                    SELECT * FROM employees
                    WHERE
                        username=%(username)s
                """,
                {
                    "username": identifier
                }
            )
            if len(username_results) == 1:
                employee_row = username_results[0]

        # Try email

        if employee_row is None and '@' in identifier:
            email_results = g.db.execute_d(
                """
                    SELECT * FROM employees
                    WHERE
                        email=%(email)s
                """,
                {
                    "email": identifier
                }
            )
            if len(email_results) == 1:
                employee_row = email_results[0]

        # End of tries

        generic_error = "Sorry, that didn't match any of our records. Try again, or contact us if you're having issues."

        if employee_row is None:
            raise LoginException(generic_error)

        if not bcrypt.checkpw(password.encode("utf-8"), employee_row["password"].encode("utf-8")):
            raise LoginException(generic_error)

        g.employee = Employee(employee_row)
        session.clear()
        session[SESSION_EMPLOYEE_ID_VAR] = g.employee.id()
    except LoginException as e:
        raise e
    except Exception as e:
        raise LoginException(str(e))


def get_email_verified_value(email):
    """
    Gets the verification status of the email provided
    Params:
        email: Email of the user to check verification status


    Returns:
       True if user email is verified. False if user is unverified.
    """
    return g.db.users.get_email_verified_status(email)


def invited_signup(username, email, first_name, last_name, password, confirm_password, account_id, is_admin):
    """Add a user to an existing account.

    Params:
        username: new username
        email: new email
        phone: company phone number (must be at least blank string)
        first: first name
        last: last name (must be at least blank string)
        password: password
        confirm_password: the confirmed password
            (if password comes from a user field, confirm_password should too;
            don't just duplicate password)
        account: Account object
        is_admin: Indicates whether the new user is an admin user
    Returns:
        Nothing

    Raises:
        SignupFailedException on failure with the reason.
    """
    username = Users._format_field(username)
    email = Users._format_field(email)
    first_name = Users._format_field(first_name)
    last_name = Users._format_field(last_name)
    password = Users._format_field(password)
    confirm_password = Users._format_field(confirm_password)
    email_validation = validate_email(email)
    if email_validation["success"]:
        # Password should equal confirm_password
        if password != confirm_password:
            raise SignupFailedException("The passwords you entered were not identical.")
        user = g.db.users.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=None,
            email_verified=1
        )
        account = g.db.accounts.get_account_by_id(account_id)
        if is_admin == 0:
            g.db.account_users.add_user_to_account(user, account)
        else:
            g.db.account_users.add_user_to_account(user, account, 1)
        EventLogs(g.db).insert_event_log(account_id=account.id(), user_id=user.id(), event_type_id=event_type_by_name["Invited Signup"])
        user_accounts = g.db.users.get_users_and_accounts(user_email=email)
        if len(user_accounts) > 1:
            user_account = user_accounts[0]
            partner_account_company = ""
            if account.partner_account_id() is not None:
                partner_account = g.db.accounts.get_account_by_id(account_id=account.partner_account_id())
                partner_account_company = partner_account.company()
            send_email(
                "BlockTrust Network New Invited User Registration Information",
                render_email("new_account_info.html", {
                    'user_account': user_account,
                    'partner_account_company': partner_account_company,
                    'sectors_id_to_name': SECTORS_ID_TO_NAME
                }), SUPPORT_GENERAL_EMAIL
            )
    else:
        raise Exception(email_validation["message"])


def employee_signup(first_name, last_name, email, phone, username, password, confirm_password):
    """
    Params:
        first_name: Employee first name
        last_name: Employee last name
        email: Employee email
        phone: Employee phone number
        username: Employee username
        password: Password
        confirm_password: Confirmed password

    Returns:
        Nothing

    Raises:
        SignupFailedException on failure with the reason
    """
    first_name = Employees._format_field(first_name)
    last_name = Employees._format_field(last_name)
    email = Employees._format_field(email)
    phone = Employees._format_field(phone)
    username = Employees._format_field(username)
    password = Employees._format_field(password)
    confirm_password = Employees._format_field(confirm_password)

    if password != confirm_password:
        raise SignupFailedException("The passwords you entered were not identical.")

    try:
        Employees(g.db).create_employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            username=username,
            password=password
        )
    except EmployeesException as e:
        raise e


def employee_login_as_user(user_id, employee_id):
    """
    Params:
        user_id: User Id of the user for logging in

    Returns:
        Nothing
    """
    id_results = g.db.execute_d(
                """
                    SELECT * FROM users
                    WHERE
                        id=%(id)s
                """,
                {
                    "id": user_id
                }
            )
    if len(id_results) == 1:
        user_row = id_results[0]
        session.clear()
        session[SESSION_USER_ID_VAR] = user_row["id"]
        session[SESSION_EMPLOYEE_ID_VAR] = employee_id
    else:
        raise Exception("No user found")
