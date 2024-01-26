import bcrypt
from flask import g, session
from ..database.tables.auction_markets import AuctionMarkets
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
from ..config import SUPPORT_GENERAL_EMAIL, ADMIN_EMAIL
from ..sectors import SECTORS_ID_TO_NAME

from json import loads

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


def load_app_context():
    load_user_to_context()
    if "user" in g:
        load_account_to_context()
    else:
        load_employee_to_context()


def load_employee(employee_id):
    session.clear()
    session[SESSION_EMPLOYEE_ID_VAR] = employee_id
    load_employee_to_context()


def load_employee_to_context():
    if SESSION_EMPLOYEE_ID_VAR in session:
        g.employee = Employees(g.db).get_by_id(session[SESSION_EMPLOYEE_ID_VAR])


def load_account(account_id):
    """Start a session with this account.

    Note that g.user should already be set to allow this to work.

    Params:
        account: Account to set as active

    Raises:
        NoAccountUserFound on user not found
    """
    account_user = g.db.account_users.get_by_user_and_account_id(g.user, account_id)
    session[SESSION_ACCOUNT_ID_VAR] = account_id
    session[SESSION_IS_ADMIN_VAR] = account_user.is_admin()
    load_account_to_context()


def load_user(user_id, employee_id=0):
    session.clear()
    session[SESSION_USER_ID_VAR] = user_id
    if employee_id:
        session[SESSION_EMPLOYEE_ID_VAR] = employee_id
    load_user_to_context()


def load_user_to_context():
    if SESSION_USER_ID_VAR in session:
        g.user = g.db.users.get_user_by_id(session[SESSION_USER_ID_VAR])
        if SESSION_EMPLOYEE_ID_VAR in session:
            g.employee_id = session[SESSION_EMPLOYEE_ID_VAR]


def load_account_to_context():
    if SESSION_ACCOUNT_ID_VAR in session:
        g.account = g.db.accounts.get_account_by_id(session[SESSION_ACCOUNT_ID_VAR])
        if SESSION_IS_ADMIN_VAR in session:
            g.is_admin = session[SESSION_IS_ADMIN_VAR]


def signup(username, email, phone, first_name, last_name, password, confirm_password, company, partner, affiliate_id,
           sector, address, city, state, zip_code, personal_phone, recaptcha_score, ip_address, ip_country,
           auction_markets_used, preconditioning_programs, pvp_programs):
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
    optional_fields = {}
    if len(auction_markets_used) > 0:
        optional_fields["auction_market_ids"] = auction_markets_used
    if len(preconditioning_programs) > 0:
        optional_fields["preconditioning_programs"] = preconditioning_programs
    if len(pvp_programs) > 0:
        optional_fields["pvp_programs"] = pvp_programs
    if len(auction_markets_used) == 0 and len(preconditioning_programs) == 0 and len(pvp_programs) == 0:
        optional_fields = None

    sector, phone, affiliate_id = g.db.accounts.validate_new_account(sector, partner, affiliate_id, phone)

    user = g.db.users.validate_and_insert_user(
        username=username,
        password=password,
        confirm_password=confirm_password,
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
            phone=phone,
            optional_fields=optional_fields
        )

        perform_new_account_actions(
            db=g.db, account_id=account_obj.id(), user_id=user.id(), event_type_id=event_type_by_name["Signup"],
            sector_id=account_obj.sector_id(), partner_id=partner, email=email
        )

        are_auction_markets_used_by_account = False
        auction_market_names = []
        preconditioning_programs = []
        pvp_programs = []
        if account_obj.optional_fields() is not None:
            optional_fields = loads(account_obj.optional_fields())
            if "auction_market_ids" in optional_fields:
                are_auction_markets_used_by_account = True
                auction_market_ids = optional_fields["auction_market_ids"]
                for auction_market_id in auction_market_ids:
                    auction_market_data = AuctionMarkets(g.db).get_auction_markets(id=auction_market_id)
                    if len(auction_market_data) > 0:
                        auction_market_names.append(auction_market_data[0]["name"])
            if "preconditioning_programs" in optional_fields:
                preconditioning_programs = optional_fields["preconditioning_programs"]
            if "pvp_programs" in optional_fields:
                pvp_programs = optional_fields["pvp_programs"]

        partner_account_company = ""
        if account_obj.partner_account_id() is not None:
            partner_account = g.db.accounts.get_account_by_id(account_id=account_obj.partner_account_id())
            partner_account_company = partner_account.company()
        send_email(
            "BlockTrust Network New Account Signup",
            render_email("new_account_info.html", {
                'user_account': account_obj,
                'partner_account_company': partner_account_company,
                'sectors_id_to_name': SECTORS_ID_TO_NAME,
                'user': user,
                "are_auction_markets_used_by_account": are_auction_markets_used_by_account,
                "account_auction_market_names": auction_market_names,
                "preconditioning_programs": preconditioning_programs,
                "pvp_programs": pvp_programs
            }), ADMIN_EMAIL
        )

    except Exception as e:
        raise e


def logout():
    """Clear session"""
    session.clear()
    g.pop("user", None)
    g.pop("employee", None)


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
            password=new_password
        )
    except Exception as e:
        raise e


def confirm(email):
    """Confirms that the user email is verified"""
    user_account = g.db.users.get_users_and_accounts(user_email=email)[0]
    g.db.users.modify_user(id=user_account["user_id"], is_email_verified=1)
    EventLogs(g.db).insert_event_log(user_id=user_account["user_id"], event_type_id=event_type_by_name["Email Verified"])


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
        generic_error = "Sorry, that didn't match any of our records. Try again, or contact us if you're having issues"

        if user_row is None:
            raise LoginException(generic_error)

        # To check if the user profile being accessed has a verified email
        if user_row['is_email_verified'] == 0:
            email_not_verified_error = "Your email is not verified. Please verify your email and try to login again"
            raise EmailNotVerifiedException(email_not_verified_error)

        # Retained for future 5/30/23
        # locked_account_error = "Your account (" + user_row["username"] + ") is locked for 24 hours due to reaching the maximum 3 consecutive failed login attempts. Contact us if you're having issues"
        # if int(user_row["is_user_locked"]) == 1:
        #     # If the user is currently locked, check whether the user has waited for one day. If not, throw error.
        #     if (user_row["locked_time"] + SECONDS_IN_ONE_DAY) > int(round(time.time())):
        #         raise LoginException(locked_account_error)
        #     else:
        #         g.db.execute(
        #         """
        #             UPDATE users
        #             SET failed_attempts =  %(failed_attempts)s,
        #             is_user_locked = %(is_user_locked)s,
        #             locked_time = %(locked_time)s
        #             WHERE
        #                 users.id=%(id)s
        #         """,
        #             {
        #                 "id": user_row["id"],
        #                 "failed_attempts": 0,
        #                 "is_user_locked": 0,
        #                 "locked_time": None
        #             }
        #         )

        if not bcrypt.checkpw(password.encode("utf-8"), user_row["password"].encode("utf-8")):
            g.db.execute_d(
                """
                    UPDATE users
                    SET failed_attempts =  failed_attempts + 1
                    WHERE
                        users.id=%(id)s
                """,
                {
                    "id": user_row["id"]
                }
            )

            # Retained for future 5/30/23
            # if failed_attempts == 3:
            #     g.db.execute(
            #     """
            #         UPDATE users
            #         SET is_user_locked = %(is_user_locked)s, locked_time = %(locked_time)s
            #         WHERE
            #             users.id=%(id)s
            #     """,
            #         {
            #             "id": user_row["id"],
            #             "is_user_locked": 1,
            #             "locked_time": int(round(time.time()))
            #         }
            #     )
            #     raise LoginException(locked_account_error)

            raise LoginException(generic_error)

        if user_row["failed_attempts"] > 0:
            g.db.execute(
                """
                    UPDATE users
                    SET failed_attempts =  0
                    WHERE
                        users.id=%(id)s
                """,
                {
                    "id": user_row["id"]
                }
            )
        return user_row["id"]
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

        load_employee(employee_row["id"])
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
        user = g.db.users.validate_and_insert_user(
            username=username,
            password=password,
            confirm_password=confirm_password,
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


def employee_login_as_user(account_id, user_id, employee_id, is_admin):
    """
    Params:
        account_id: Account's ID
        user_id: User Id of the user for logging in
        employee_id: Employee Id using the user to log in

    Returns:
        Nothing.

    Raises:
        Exception
    """
    account_user = g.db.account_users.get_account_users(account=account_id, user=user_id, is_admin=is_admin)
    if account_user:
        logout()
        load_user(user_id, employee_id)
        load_account(account_id)
    else:
        raise Exception("No user found")


def login_as_employee(employee_id):
    """
    Params:
        employee_id: Employee Id to log in
    Returns:
        Nothing.
    """
    logout()
    load_employee(employee_id)


def verified_signup(username, email, phone, first_name, last_name, password, confirm_password, company, partner,
                    affiliate_id, sector, address, city, state, zip_code, personal_phone,auction_markets_used,
                    preconditioning_programs, pvp_programs):
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
    optional_fields = {}
    if len(auction_markets_used) > 0:
        optional_fields["auction_market_ids"] = auction_markets_used
    if len(preconditioning_programs) > 0:
        optional_fields["preconditioning_programs"] = preconditioning_programs
    if len(pvp_programs) > 0:
        optional_fields["pvp_programs"] = pvp_programs
    if len(auction_markets_used) == 0 and len(preconditioning_programs) == 0 and len(pvp_programs) == 0:
        optional_fields = None

    sector, phone, affiliate_id = g.db.accounts.validate_new_account(sector, partner, affiliate_id, phone)

    user = g.db.users.validate_and_insert_user(
        username=username,
        password=password,
        confirm_password=confirm_password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=personal_phone,
        email_verified=1
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
            phone=phone,
            optional_fields=optional_fields
        )
        perform_new_account_actions(
            db=g.db, account_id=account_obj.id(), user_id=user.id(),
            event_type_id=event_type_by_name["API Signup"], sector_id=account_obj.sector_id(),
            partner_id=partner, email=email
        )

    except Exception as e:
        raise e