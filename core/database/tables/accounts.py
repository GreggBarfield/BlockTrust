from ...sectors import sectors_by_id
from ..objects.account import Account, AccountException
from ..no_value import NoValue
from ..frag import frag

NO_VALUE = NoValue()

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
        
    def get_partners_by_sector_id(self, sector_id):
        """Gets an partners in the accounts table using sector ID.

        Params:
            id: the sector id
        
        Returns:
            One or more partner Account() object

        Raises:
            AccountsException on ID not found
        """
        partner_rows = self._db.execute_d(
            """SELECT * FROM accounts
                WHERE sector=%(id)s AND is_partner=1
            """,
            {
                "id": sector_id
            }
        )
        return [
            Account(self._db, partner_row)
            for partner_row in partner_rows
        ]


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


    def create_account(self, user, name, company, sector, partner, affiliate_id, address, city, state, zip, phone):
        """Creates a new account with the user automatically added.

        Params:
            user: a User object (assumed to be safe)
            name: the account name
            company: the company name
            sector: the sector number
            partner: partner id
            affiliate_id: account number in our partners system
            address: company's address
            city: company's city
            state: company's state
            zip: company's zip
            phone: company's phone

        Returns:
            An Account object

        Raises:
            AccountsException
        """
        try:
            sector = int(sector)
        except Exception as e:
            raise AccountsException("Sector number (" + str(sector) + ") is invalid.")

        if sector not in sectors_by_id:
            raise AccountsException("Sector number is not listed internally.")

        # Process phone number
        if phone != None:
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
            """INSERT INTO accounts
                (name, company, sector, partner_account, affiliate_id, address, city, state, zip, phone)
                VALUES
                    (%(name)s, %(company)s, %(sector)s, %(partner)s, %(affiliate_id)s, %(address)s, %(city)s, %(state)s, %(zip)s, %(phone)s)
            """,
            {
                "name": name,
                "company": company,
                "sector": sector,
                "partner": partner,
                "affiliate_id": affiliate_id,
                "address": address,
                "city": city,
                "state": state,
                "zip": zip,
                "phone": phone
            }
        )
        account = self.get_by_id(self._db.last_row_id())
        # make the first user the account admin
        account.add_user(user, 1)
        # Link the account appropriately in the database
        account.update_account_links()
        return account


    def update_account(self, account_id, name=NO_VALUE, company=NO_VALUE, sector_id=NO_VALUE, affiliate_id=NO_VALUE, city=NO_VALUE, state=NO_VALUE, zip=NO_VALUE, 
        phone = NO_VALUE, token=NO_VALUE, stripe_paid=NO_VALUE, manual_paid=NO_VALUE, stripe_customer_id=NO_VALUE):
        """Updates an account.

        Params:
            account_id: id of the account to update
            name: the account name
            company: the company name
            sector: the sector number
            token: token that we give the customer to use our apis
            stripe_paid: indicates if this account has an active subscription in stripe
            manual_paid: indicates if it is a manually marked paid account
            stripe_customer_id: the id for the corresponding customer object in stripe
        """
        set_frags = frag()
        if name is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "name=:name,",
                            name=name
                        )
        if company is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "company=:company,",
                            company=company
                        )
        if sector_id is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "sector_id=:sector_id,",
                            sector_id=sector_id
                        )
        if affiliate_id is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "affiliate_id=:affiliate_id,",
                            affiliate_id=affiliate_id
                        )
        if city is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "city=:city,",
                            city=city
                        )
        if state is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "state=:state,",
                            state=state
                        )
        if zip is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "zip=:zip,",
                            zip=zip
                        )
        if phone is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "phone=:phone,",
                            phone=phone
                        )
        if token is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "token=:token,",
                            token=token
                        )
        if stripe_paid is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "stripe_paid=:stripe_paid,",
                            stripe_paid=stripe_paid
                        )
        if manual_paid is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "manual_paid=:manual_paid,",
                            manual_paid=manual_paid
                        )
        if stripe_customer_id is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "stripe_customer_id=:stripe_customer_id",
                            stripe_customer_id=stripe_customer_id
                        )

        if len(set_frags[0]) > 0 and len(set_frags[1]) > 0:
            #  check if last character in SQL is , and remove it if so
            if set_frags[0][-1] == ",":
                set_frags = (set_frags[0][:-1], set_frags[1])

            self._db.exec_frag(
                frag(
                    "UPDATE accounts SET",
                    set_frags,
                    frag(
                        "WHERE id=:id",
                        id=account_id
                    )
                )
            )

    def get_accounts_list(self):
        """Gets a list of all account numbers and account names.

        Params:

        Returns:
            An Array of registered accounts
        """
        # TODO: Add account_links caching option
        account_rows = self._db.execute_d(
            """SELECT id, company, sector FROM accounts
            """,
            {}
        )
        return account_rows
