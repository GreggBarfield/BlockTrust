import bcrypt
from flask import g, session
from ..database.tables.users import Users, NoUserFoundException
from ..database.objects.user import User
from ..database.objects.account import Account


SESSION_USER_ID_VAR = "user_id"
SESSION_ACCOUNT_ID_VAR = "account_id"


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
    session_open_account()


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
    attempt_login = g.db.account_users.get_by_user_and_account_id(g.user, account_id)
    if attempt_login.account_id() == account_id and attempt_login.user_id() == g.user.id():
        session[SESSION_ACCOUNT_ID_VAR] = account_id
        session_open_account()


def session_open_user():
    """Load user session into app context."""
    g.user = None
    if SESSION_USER_ID_VAR in session and session[SESSION_USER_ID_VAR] != "":
        g.user = g.db.users.get(session[SESSION_USER_ID_VAR])
    else:
        session[SESSION_USER_ID_VAR] = ""
        # TODO: if this fails, abort request and redirect to issue opening session screen


def session_open_account():
    """Load account session into app context."""
    g.account = None
    if SESSION_ACCOUNT_ID_VAR in session and session[SESSION_ACCOUNT_ID_VAR] != "":
        g.account = g.db.accounts.get_by_id(session[SESSION_ACCOUNT_ID_VAR])
    else:
        session[SESSION_ACCOUNT_ID_VAR] = ""


def signup(username, email, phone, first_name, last_name, password, confirm_password, company, affiliate_id, sector, city, state, zip_code):
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
    username = Users._format_field(username)
    email = Users._format_field(email)
    phone = Users._format_field(phone)
    first_name = Users._format_field(first_name)
    last_name = Users._format_field(last_name)
    password = Users._format_field(password)
    confirm_password = Users._format_field(confirm_password)
    company = Users._format_field(company)
    affiliate_id = Users._format_field(affiliate_id)
    sector = Users._format_field(sector)
    city = Users._format_field(city)
    state = Users._format_field(state)
    zip_code = Users._format_field(zip_code)


    # Password should equal confirm_password

    if password != confirm_password:
        raise SignupFailedException("The passwords you entered were not identical.")

    user = g.db.users.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone="",
        email_verified="N"
    )

    g.db.accounts.create_account(
        user=user,
        name="",
        company=company,
        sector=sector,
        affiliate_id=affiliate_id,
        city=city,
        state=state,
        zip=zip_code,
        phone=phone
    )


def logout():
    """Clear session of user info and remove g user."""
    g.user = None
    session[SESSION_USER_ID_VAR] = ""
    session.clear()


def confirm(email):
    """Confirms that the user email is verified"""
    g.db.users.verify_email(email)


def login(identifier, password="", override=False):
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
            raise LoginException("password is None")
        if override is not True and override is not False:
            raise LoginException("override is bad")

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

        generic_error = "Sorry, that didn't match any of our records. Try again, or contact us if you're having issues."

        if user_row is None:
            raise LoginException(generic_error)

        if override is not True and not bcrypt.checkpw(password.encode("utf-8"), user_row["password"].encode("utf-8")):
            raise LoginException(generic_error)
        # To check if the user profile being accessed has a verified email

        if user_row['email_verified'] == 'N':
            email_not_verified_error = "Your email is not verified. Please verify your email and try to login again"
            raise EmailNotVerifiedException(email_not_verified_error)

        g.user = User(g.db, user_row)
        session.clear()
        session[SESSION_USER_ID_VAR] = g.user.id()

        return g.user
    except LoginException as e:
        raise e
    except EmailNotVerifiedException as e:
        raise e
    except Users.UsersException as e:
        raise e
    except Exception as e:
        raise LoginException("other exception")


def get_email_verified_value(email):
    """
    Gets the verification status of the email provided
    Params:
        email: Email of the user to check verification status


    Returns:
       True if user email is verified. False if user is unverified.
    """
    return g.db.users.get_email_verified_status(email)
