from ...sectors import sectors_by_id
from ..objects.account import Account, AccountException


class AccountsException(Exception):
    """Account generic exception."""

    def __init__(self, reason):
        """Constructor for AccountException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class Accounts:

    def __init__(self, db):
        self._db = db

    def get_by_id(self, account_id):
        """Gets an account by an ID.

        Params:
            id: the account id
        
        Returns:
            An Account() object

        Raises:
            AccountsException on ID not found
        """
        # TODO: Add account_links caching option
        account_rows = self._db.execute_d(
            """SELECT * FROM accounts
                WHERE id=%(id)s
            """,
            {
                "id": account_id
            }
        )
        if len(account_rows) != 1:
            raise AccountsException("No account found with that ID.")
        return Account(self._db, account_rows[0])


    def get_by_account_user(self, account_user):
        """Gets an account by an AccountUser object.

        Params:
            account_user: the AccountUser object
        
        Returns:
            An Account() object
        
        Raises:
            AccountsException
        """
        return self.get_by_id(account_user.account_id())
    

    def get_by_user(self, user):
        """Gets a user's accounts.

        Params:
            user: The User object
        
        Returns:
            A possibly empty list of Account() objects.
        """
        account_rows = self._db.execute_d(
            """SELECT accounts.* FROM accounts
                INNER JOIN account_users ON accounts.id = account_users.account
                WHERE account_users.user = %(user_id)s
            """,
            {
                "user_id": user.id()
            }
        )

        return [
            Account(self._db, account_row)
            for account_row in account_rows
        ]
    
    
    def get_by_stripe_customer_id(self, stripe_customer_id):
        """Gets an account by an ID.

        Params:
            stripe_customer_id: the stripe_customer_id of the account
        
        Returns:
            An Account() object

        Raises:
            AccountsException on ID not found
        """
        account_rows = self._db.execute_d(
            """SELECT * FROM accounts
                WHERE stripe_customer_id=%(stripe_customer_id)s
            """,
            {
                "stripe_customer_id": stripe_customer_id
            }
        )
        if len(account_rows) != 1:
            raise AccountsException("No account found with that Stripe Customer ID.")
        return Account(self._db, account_rows[0])


    def create_account(self, user, name, company, sector):
        """Creates a new account with the user automatically added.

        Params:
            user: a User object (assumed to be safe)
            name: the account name
            company: the company name
            sector: the sector number
        
        Returns:
            An Account object

        Raises:
            AccountsException
        """
        try:
            sector = int(sector)
        except Exception as e:
            raise AccountsException("Sector number is invalid.")

        if sector not in sectors_by_id:
            raise AccountsException("Sector number is not listed internally.")

        self._db.execute(
            """INSERT INTO accounts
                (name, company, sector)
                VALUES
                    (%(name)s, %(company)s, %(sector)s)
            """,
            {
                "name": name,
                "company": company,
                "sector": sector
            }
        )

        try:
            account = self.get_by_id(self._db.last_row_id())
            account.add_user(user)
            return account
        except AccountException as e:
            raise AccountsException("Account exception: " + str(e))


    def update_account(self, account_id, name, company, sector_id, token, paid, manual_paid, stripe_customer_id):
        """Updates an account.

        Params:
            account_id: id of the account to update
            name: the account name
            company: the company name
            sector: the sector number
            token: token that we give the customer to use our apis
            paid: indicates if it is a paid account (this should be synced with stripe subscription)
            manual_paid: indicates if it is a manually marked paid account
            stripe_customer_id: the id for the corresponding customer object in stripe
        """
        self._db.execute("""
            UPDATE accounts
                SET name=%(name)s, company=%(company)s, sector=%(sector_id)s,
                    token=%(token)s, paid=%(paid)s, manual_paid=%(manual_paid)s,
                    stripe_customer_id=%(stripe_customer_id)s
                WHERE id=%(account_id)s
            """,
            {
                "account_id": account_id,
                "name": name,
                "company": company,
                "sector_id": sector_id,
                "token": token,
                "paid": paid,
                "manual_paid": manual_paid,
                "stripe_customer_id": stripe_customer_id
            }
        )