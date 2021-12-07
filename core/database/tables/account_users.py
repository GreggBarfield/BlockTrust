from core.database.tables.job_runs import NO_VALUE
from ..objects.account_user import AccountUser
from ..no_value import NoValue

NO_VALUE = NoValue()

class AccountUsersException(Exception):
    """account users generic exception."""

    def __init__(self, reason="no reason given"):
        """Constructor for AccountUsersException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


class NoAccountUserFound(AccountUsersException):
    """No account user found (or multiple found)."""
    pass


class AccountUsers:

    def __init__(self, db):
        self._db = db

    def get_by_user_and_account_id(self, user, account_id):
        """Get an account user by a user and an account ID.

        Params:
            user: User object
            account: Account ID

        Returns:
            An AccountUser object

        Raises:
            NoAccountUserFound
        """
        account_users = self._db.execute_d(
            """
                SELECT * FROM account_users
                    WHERE user=%(user)s
                        AND account=%(account)s
            """,
            {
                "user": user.id(),
                "account": account_id
            }
        )

        if len(account_users) == 1:
            return AccountUser(self._db, account_users[0])
        raise NoAccountUserFound()

    def get_by_user_and_account(self, user, account):
        """Get an account user by a user and an account.

        Params:
            user: User object
            account: Account object

        Returns:
            An AccountUser object

        Raises:
            NoAccountUserFound
        """
        return self.get_by_user_and_account_id(user, account.id())

    def get_by_user(self, user):
        """Get a user's linked accounts.

        Params:
            user: User object

        Returns:
            A list of AccountUser objects. This list can be blank
                (exceptions are not raised on no accounts found)
        """
        account_users = self._db.execute_d(
            """
                SELECT * FROM account_users
                    WHERE user=%(user)s
            """,
            {
                "user": user.id()
            }
        )
        return [AccountUser(self._db, account_user) for account_user in account_users]

    def add_user_to_account(self, user, account, is_admin=0):
        """Add a user to an account.

        Params:
            user: a User object to add to account
            account: an Account object to add the user to

        Raises:
            AccountUsersException
        """

        # Check if link already exists
        try:
            self.get_by_user_and_account(user, account)
            raise AccountUsersException("account user already exists")
        except NoAccountUserFound as e:
            pass

        # add new link

        self._db.execute(
            """
                INSERT INTO account_users
                    (user, account, is_admin)
                    VALUES
                        (%(user)s, %(account)s, %(is_admin)s)
            """,
            {
                "user": user.id(),
                "account": account.id(),
                "is_admin": is_admin
            }
        )

    def get_account_users(self, account=NO_VALUE, user=NO_VALUE, is_admin=NO_VALUE, selectColumns=[]):
        """
        Gets the account records based on conditions provided

        Params:
            account: Account ID
            user: User ID
            is_admin: (1 or 0) Based on whether admin or not admin

        Return:
            Results based on conditions provided or None
        """
        if len(selectColumns) > 0:
            selectColumns = ",".join(selectColumns)
        else:
            selectColumns = "*"

        # Base query
        query = "SELECT " + selectColumns + " FROM account_users"

        query_condition_list = []
        query_values = {}

        if account is not NO_VALUE:
            query_condition_list.append(" account = %(account)s")
            query_values["account"] = account

        if user is not NO_VALUE:
            query_condition_list.append(" user = %(user)s")
            query_values["user"] = user

        if is_admin is not NO_VALUE:
            query_condition_list.append(" is_admin = %(is_admin)s")
            query_values["is_admin"] = is_admin

        if len(query_condition_list) >= 1:
            query_condition = " WHERE" + " AND ".join(query_condition_list)
        else:
            query_condition = ""

        query = query + query_condition

        account_user_rows = self._db.execute_d(query, query_values)
        if len(account_user_rows) > 0:
            return account_user_rows
        else:
            return []
