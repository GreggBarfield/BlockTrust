from ...sectors import sectors_by_id, sectors_by_name
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
   
    def get_by_partner_affiliate_id(self, partner_id, affiliate_id):
        """Gets an account using the partner and affiliate id.

        Params:
            stripe_customer_id: the stripe_customer_id of the account
        
        Returns:
            An Account() object
        """
        account_rows = self._db.execute_d(
            """SELECT * FROM accounts
                WHERE partner_account=%(partner_id)s AND affiliate_id=%(affiliate_id)s
            """,
            {
                "partner_id": partner_id,
                "affiliate_id": affiliate_id
            }
        )
        if len(account_rows) == 0:
            return None
        return Account(self._db, account_rows[0])


    def create_account(self, user, company, sector, partner, affiliate_id, address, city, state, zip, phone):
        """Creates a new account with the user automatically added.

        Params:
            user: a User object (assumed to be safe)
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

        # Validations
        
        if partner is not None:
            accounts = self.get_accounts(affiliate_id=affiliate_id, partner_account=partner)
            if len(accounts) > 0:
                raise AccountsException("This partner id has already been taken by another account.")

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
                (company, sector, partner_account, affiliate_id, address, city, state, zip, phone)
                VALUES
                    (%(company)s, %(sector)s, %(partner)s, %(affiliate_id)s, %(address)s, %(city)s, %(state)s, %(zip)s, %(phone)s)
            """,
            {
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
        
        # update account name
        name = company
        if sector == sectors_by_name["Cow-Calf"]:
            name = "Ranch "+ str(account.id())
        self.update_account(account.id(), name=name)

        # make the first user the account admin
        account.add_user(user, 1)

        # Link the account appropriately in the database
        self._db.account_links.update_account_link_with_account(account.partner_account_id(), account.affiliate_id(), account.sector_id(), name, account.id())

        # Create reports needed for the account
        if account.sector_id() != sectors_by_name["Buyer"]:
            self._db.reports.make_reports_for_account(account.id())
        return account


    def update_account(self, account_id, name=NO_VALUE, company=NO_VALUE, sector_id=NO_VALUE, affiliate_id=NO_VALUE, address=NO_VALUE, city=NO_VALUE, state=NO_VALUE, zip=NO_VALUE, 
        phone = NO_VALUE, token=NO_VALUE, stripe_paid=NO_VALUE, manual_paid=NO_VALUE, stripe_customer_id=NO_VALUE):
        """Updates an account.

        Params:
            account_id: id of the account to update
            name: the account name
            company: the company name
            sector_id: the sector number
            address: Account address
            city: Account city
            state: Account state
            zip: Account zip
            phone: Phone number specified for the account
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
        if address is not NO_VALUE:
            set_frags = frag(
                            set_frags,
                            "address=:address,",
                            address=address
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

    def get_accounts(self, company=None, sector=None, is_partner=None, partner_account=None,
                            affiliate_id=None, address=None, city=None, state=None, zip=None, selectColumns=[]):
        """
        Get an account by the values specified.

        Returns:
            The account record if found else None
        """
        if len(selectColumns) > 0:
            selectColumns = ",".join(selectColumns)
        else:
            selectColumns = "*"

        #base query
        query = "SELECT " + selectColumns + " FROM accounts"
        
        query_condition_list = []
        query_values = {}

        if company is not None:
            query_condition_list.append(" company = %(company)s")
            query_values["company"] = company

        if sector is not None:
            query_condition_list.append(" sector = %(sector)s")
            query_values["sector"] = sector

        if is_partner is not None:
            query_condition_list.append(" is_partner = %(is_partner)s")
            query_values["is_partner"] = is_partner

        if partner_account is not None:
            query_condition_list.append(" partner_account = %(partner_account)s")
            query_values["partner_account"] = partner_account

        if affiliate_id is not None:
            query_condition_list.append(" affiliate_id = %(affiliate_id)s")
            query_values["affiliate_id"] = affiliate_id

        if address is not None:
            query_condition_list.append(" address = %(address)s")
            query_values["address"] = address

        if city is not None:
            query_condition_list.append(" city = %(city)s")
            query_values["city"] = city

        if state is not None:
            query_condition_list.append(" state = %(state)s")
            query_values["state"] = state

        if zip is not None:
            query_condition_list.append(" zip = %(zip)s")
            query_values["zip"] = zip

        if len(query_condition_list) >= 1:
            query_condition = " WHERE" + " AND ".join(query_condition_list)
        else:
            query_condition = ""
        
        query = query + query_condition

        account_rows = self._db.execute_d(query, query_values)
        if len(account_rows) > 0:
            return account_rows
        else:
            return []
