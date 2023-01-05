from ...sectors import SECTORS_ID_TO_NAME, SECTORS_NAME_TO_ID
from ..objects.account import Account
from ..no_value import NoValue

NO_VALUE = NoValue()
HEALTH_TRACK_PARTNER_COMPANY = "MFA Health Track"
RED_ANGUS_PARTNER_COMPANY = "Red Angus Assoc"

account_cols = ("id", "name", "company", "sector", "is_partner", "partner_contact_name", "partner_contact_email",
                "partner_account", "affiliate_id", "address", "city", "state", "zip", "phone", "token", "stripe_paid",
                "manual_paid", "generated_paid", "stripe_customer_id", "stripe_account_id", "is_stripe_payouts_enabled",
                "partner_stripe_publishable_key", "partner_stripe_secret_key", "created_timestamp", "last_updated_timestamp",
                "partner_private_logo", "is_partner_used_for_signup", "retail_name", "retail_description")


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

    def get_account_by_id(self, account_id):
        """Gets an account by an ID.

        Params:
            id: the account id

        Returns:
            An Account() object or None if Account ID is not found
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
            return None
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
        return self.get_account_by_id(account_user.account_id())
    

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


    def validate_new_account(self, sector, partner, affiliate_id, phone):
        """validates input to create account

        Params:
            sector: the sector number
            partner: partner id
            affiliate_id: account number in our partners system

        Returns:
            Processed sector and phone in that order

        Raises:
            AccountsException
        """
        if partner is not None:
            if affiliate_id is None:
                raise AccountsException("You have not entered a partner id for the selected partner")
            accounts = self.get_accounts(affiliate_id=affiliate_id, partner_account=partner)
            if len(accounts) > 0:
                raise AccountsException(f"This partner id: {affiliate_id} for the selected partner has already been taken by another account.")

        try:
            sector = int(sector)
        except Exception as e:
            raise AccountsException("Sector number (" + str(sector) + ") is invalid.")

        if sector not in SECTORS_ID_TO_NAME:
            raise AccountsException("Sector number is not listed internally.")

        # Process phone
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

        return sector, phone

    def create_account(self, company, sector, partner, affiliate_id, address, city, state, zip, phone):
        """Creates a new account without a user.

        Params:
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
        if affiliate_id and affiliate_id.isdigit():
            affiliate_id = int(affiliate_id)
        sector, phone = self.validate_new_account(sector, partner, affiliate_id, phone)

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
        account = self.get_account_by_id(self._db.last_row_id())

        # update account name
        name = company
        if sector == SECTORS_NAME_TO_ID["Cow-Calf"]:
            name = "Ranch " + str(account.id())
        self.update_account(account.id(), name=name)

        # Link the account appropriately in the database
        self._db.account_links.update_account_link_with_account(account.partner_account_id(), account.affiliate_id(), account.sector_id(), company, name, account.id())

        return account

    def create_account_with_admin(self, user, company, sector, partner, affiliate_id, address, city, state, zip, phone):
        """Creates a new account with the user automatically added as the admin.

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

        account = self.create_account(company, sector, partner, affiliate_id, address, city, state, zip, phone)

        # make the first user the account admin
        account.add_user(user, 1)

        return account

    def create_partner(self, company, sector, partner_contact_name, partner_contact_email, address, city, state, zip, phone, is_partner_used_for_signup):
        """Creates a new partner without a user.

        Params:
            company: the company name
            sector: the sector number
            partner_contact_name: Partner contact name
            partner_contact_email: Partner contact email
            address: company's address
            city: company's city
            state: company's state
            zip: company's zip
            phone: company's phone
            is_partner_used_for_signup: Show the partner name on signup page

        Returns:
            An Account object

        Raises:
            AccountsException
        """
        # Process phone
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
                (company, name, sector, is_partner, partner_contact_name, partner_contact_email, address, city, state, zip, phone, is_partner_used_for_signup)
                VALUES
                    (%(company)s, %(name)s, %(sector)s, %(is_partner)s, %(partner_contact_name)s, %(partner_contact_email)s, %(address)s, %(city)s, %(state)s, %(zip)s, %(phone)s, %(is_partner_used_for_signup)s)
            """,
            {
                "company": company,
                "name": company,
                "sector": sector,
                "is_partner": 1,
                "partner_contact_name": partner_contact_name,
                "partner_contact_email": partner_contact_email,
                "address": address,
                "city": city,
                "state": state,
                "zip": zip,
                "phone": phone,
                "is_partner_used_for_signup": is_partner_used_for_signup
            }
        )
        partner = self.get_account_by_id(self._db.last_row_id())
        return partner

    def get_accounts(self, id=NO_VALUE, company=NO_VALUE, company_like=NO_VALUE, sector=NO_VALUE, is_partner=NO_VALUE,
                     partner_account=NO_VALUE, affiliate_id=NO_VALUE, address=NO_VALUE, city=NO_VALUE, state=NO_VALUE,
                     zip=NO_VALUE, is_partner_used_for_signup=NO_VALUE, token=NO_VALUE, stripe_customer_id=NO_VALUE,
                     stripe_account_id=NO_VALUE, accounts_order_by=NO_VALUE, accounts_sort_by=NO_VALUE,
                     generated_paid=NO_VALUE, is_stripe_payouts_enabled=NO_VALUE):
        """
        Get an account by the values specified.

        Returns:
            A list of account row(s) if found else []
        """
        # base query
        base_query = "SELECT * FROM accounts"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id

        if company is not NO_VALUE:
            query_conditions.append("company = %(company)s")
            query_values["company"] = company

        if company_like is not NO_VALUE:
            query_conditions.append("company LIKE %(company_like)s")
            query_values["company_like"] = "%" + company_like + "%"

        if sector is not NO_VALUE:
            query_conditions.append("sector = %(sector)s")
            query_values["sector"] = sector

        if is_partner is not NO_VALUE:
            query_conditions.append("is_partner = %(is_partner)s")
            query_values["is_partner"] = is_partner

        if partner_account is not NO_VALUE:
            query_conditions.append("partner_account = %(partner_account)s")
            query_values["partner_account"] = partner_account

        if affiliate_id is not NO_VALUE:
            query_conditions.append("affiliate_id = %(affiliate_id)s")
            query_values["affiliate_id"] = affiliate_id

        if address is not NO_VALUE:
            query_conditions.append("address = %(address)s")
            query_values["address"] = address

        if city is not NO_VALUE:
            query_conditions.append("city = %(city)s")
            query_values["city"] = city

        if state is not NO_VALUE:
            query_conditions.append("state = %(state)s")
            query_values["state"] = state

        if zip is not NO_VALUE:
            query_conditions.append("zip = %(zip)s")
            query_values["zip"] = zip

        if is_partner_used_for_signup is not NO_VALUE:
            query_conditions.append("is_partner_used_for_signup = %(is_partner_used_for_signup)s")
            query_values["is_partner_used_for_signup"] = is_partner_used_for_signup

        if token is not NO_VALUE:
            query_conditions.append("token = %(token)s")
            query_values["token"] = token
        
        if stripe_customer_id is not NO_VALUE:
            query_conditions.append("stripe_customer_id = %(stripe_customer_id)s")
            query_values["stripe_customer_id"] = stripe_customer_id

        if stripe_account_id is not NO_VALUE:
            query_conditions.append("stripe_account_id = %(stripe_account_id)s")
            query_values["stripe_account_id"] = stripe_account_id

        if generated_paid is not NO_VALUE:
            query_conditions.append("generated_paid = %(generated_paid)s ")
            query_values["generated_paid"] = generated_paid

        if is_stripe_payouts_enabled is not NO_VALUE:
            query_conditions.append(" is_stripe_payouts_enabled = %(is_stripe_payouts_enabled)s ")
            query_values["is_stripe_payouts_enabled"] = is_stripe_payouts_enabled

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        if accounts_order_by is not NO_VALUE:
            if accounts_order_by not in account_cols:
                raise Exception("accounts_order_by column doesn't exist")
            order_by_clause = " ORDER BY " + accounts_order_by
            if accounts_sort_by is not NO_VALUE:
                if accounts_sort_by not in ("ASC", "DESC"):
                    raise Exception("Incorrect value for auction_markets_sort_by")
                order_by_clause += " " + accounts_sort_by
            query = query + order_by_clause

        account_rows = self._db.execute_d(query, query_values)
        if len(account_rows) > 0:
            return account_rows
        else:
            return []

    def update_partner(self, account_id, name=NO_VALUE, company=NO_VALUE, sector_id=NO_VALUE, affiliate_id=NO_VALUE,
                       address=NO_VALUE, city=NO_VALUE, state=NO_VALUE, zip=NO_VALUE, phone=NO_VALUE, token=NO_VALUE,
                       stripe_paid=NO_VALUE, manual_paid=NO_VALUE, stripe_customer_id=NO_VALUE,
                       partner_account=NO_VALUE, is_partner_used_for_signup=NO_VALUE):
        """
        Updates an account.

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
        # base query
        base_query = "UPDATE accounts "

        query_conditions = []
        query_values = {}
        query_values["id"] = account_id
        if name is not NO_VALUE:
            query_conditions.append(" name = %(name)s")
            query_values["name"] = name
        if company is not NO_VALUE:
            query_conditions.append(" company = %(company)s")
            query_values["company"] = company
        if sector_id is not NO_VALUE:
            query_conditions.append(" sector = %(sector_id)s")
            query_values["sector_id"] = sector_id
        if affiliate_id is not NO_VALUE:
            query_conditions.append(" affiliate_id = %(affiliate_id)s")
            query_values["affiliate_id"] = affiliate_id
        if address is not NO_VALUE:
            query_conditions.append(" address = %(address)s")
            query_values["address"] = address
        if city is not NO_VALUE:
            query_conditions.append(" city = %(city)s")
            query_values["city"] = city
        if state is not NO_VALUE:
            query_conditions.append(" state = %(state)s")
            query_values["state"] = state
        if zip is not NO_VALUE:
            query_conditions.append(" zip = %(zip)s")
            query_values["zip"] = zip
        if phone is not NO_VALUE:
            query_conditions.append(" phone = %(phone)s")
            query_values["phone"] = phone
        if token is not NO_VALUE:
            query_conditions.append(" token = %(token)s")
            query_values["token"] = token
        if stripe_paid is not NO_VALUE:
            query_conditions.append(" stripe_paid = %(stripe_paid)s")
            query_values["stripe_paid"] = stripe_paid
        if manual_paid is not NO_VALUE:
            query_conditions.append(" manual_paid = %(manual_paid)s")
            query_values["manual_paid"] = manual_paid
        if stripe_customer_id is not NO_VALUE:
            query_conditions.append(" stripe_customer_id = %(stripe_customer_id)s")
            query_values["stripe_customer_id"] = stripe_customer_id
        if partner_account is not NO_VALUE:
            query_conditions.append(" partner_account = %(partner_account)s")
            query_values["partner_account"] = partner_account
        if is_partner_used_for_signup is not NO_VALUE:
            query_conditions.append(" is_partner_used_for_signup = %(is_partner_used_for_signup)s")
            query_values["is_partner_used_for_signup"] = is_partner_used_for_signup
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Account")

    def update_account(self, account_id, name=NO_VALUE, company=NO_VALUE, sector_id=NO_VALUE, affiliate_id=NO_VALUE,
                       address=NO_VALUE, city=NO_VALUE, state=NO_VALUE, zip=NO_VALUE, phone=NO_VALUE, token=NO_VALUE,
                       stripe_paid=NO_VALUE, manual_paid=NO_VALUE, stripe_customer_id=NO_VALUE,
                       partner_account=NO_VALUE, stripe_account_id=NO_VALUE, is_stripe_payouts_enabled=NO_VALUE,
                       retail_name=NO_VALUE, retail_description=NO_VALUE):
        """
        Updates an account.

        Params:
            account_id: ID of the account to update
            name: the account name
            company: the company name
            sector_id: the sector number
            address: Account address
            city: Account city
            state: Account state
            zip: Account zip
            phone: Phone number specified for the account
            token: token that we give the customer to use our APIs
            stripe_paid: indicates if this account has an active subscription in stripe
            manual_paid: indicates if it is a manually marked paid account
            stripe_customer_id: the id for the corresponding customer object in stripe
            retail_name: Retail name visible externally
            retail_description: Retail Information visible externally
        """
        base_query = "UPDATE accounts "

        query_conditions = []
        query_values = {}
        query_values["id"] = account_id
        if name is not NO_VALUE:
            query_conditions.append("name = %(name)s")
            query_values["name"] = name
        if company is not NO_VALUE:
            query_conditions.append("company = %(company)s")
            query_values["company"] = company
        if sector_id is not NO_VALUE:
            query_conditions.append("sector = %(sector_id)s")
            query_values["sector_id"] = sector_id
        if affiliate_id is not NO_VALUE:
            query_conditions.append("affiliate_id = %(affiliate_id)s")
            query_values["affiliate_id"] = affiliate_id
        if address is not NO_VALUE:
            query_conditions.append("address = %(address)s")
            query_values["address"] = address
        if city is not NO_VALUE:
            query_conditions.append("city = %(city)s")
            query_values["city"] = city
        if state is not NO_VALUE:
            query_conditions.append("state = %(state)s")
            query_values["state"] = state
        if zip is not NO_VALUE:
            query_conditions.append("zip = %(zip)s")
            query_values["zip"] = zip
        if phone is not NO_VALUE:
            query_conditions.append("phone = %(phone)s")
            query_values["phone"] = phone
        if token is not NO_VALUE:
            query_conditions.append("token = %(token)s")
            query_values["token"] = token
        if stripe_paid is not NO_VALUE:
            query_conditions.append("stripe_paid = %(stripe_paid)s")
            query_values["stripe_paid"] = stripe_paid
        if manual_paid is not NO_VALUE:
            query_conditions.append("manual_paid = %(manual_paid)s")
            query_values["manual_paid"] = manual_paid
        if stripe_customer_id is not NO_VALUE:
            query_conditions.append("stripe_customer_id = %(stripe_customer_id)s")
            query_values["stripe_customer_id"] = stripe_customer_id
        if partner_account is not NO_VALUE:
            query_conditions.append("partner_account = %(partner_account)s")
            query_values["partner_account"] = partner_account
        if stripe_account_id is not NO_VALUE:
            query_conditions.append("stripe_account_id = %(stripe_account_id)s")
            query_values["stripe_account_id"] = stripe_account_id
        if is_stripe_payouts_enabled is not NO_VALUE:
            query_conditions.append("is_stripe_payouts_enabled = %(is_stripe_payouts_enabled)s")
            query_values["is_stripe_payouts_enabled"] = is_stripe_payouts_enabled
        if retail_name is not NO_VALUE:
            query_conditions.append("retail_name = %(retail_name)s")
            query_values["retail_name"] = retail_name
        if retail_description is not NO_VALUE:
            query_conditions.append("retail_description = %(retail_description)s")
            query_values["retail_description"] = retail_description
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Account")
