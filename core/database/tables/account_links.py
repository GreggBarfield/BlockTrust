from ..objects.account_link import AccountLink, AccountLinkException


class AccountLinksException(Exception):
    """AccountLinks generic exception."""

    def __init__(self, reason):
        """Constructor for AccountLinks.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

# account link is the link between the account in our accounts table and the account in our partner's database. 
class AccountLinks:

    def __init__(self, db):
        self._db = db

    def get_by_id(self, account_link_id):
        """Gets an account link by ID.

        Params:
            id: row ID

        Returns:
            An AccountLink object

        Raises:
            AccountLinksException
        """
        account_link_rows = self._db.execute_d(
            """SELECT * FROM account_links
                WHERE id=%(id)s
            """,
            {
                "id": account_link_id
            }
        )
        if len(account_link_rows) != 1:
            raise AccountLinkException("No account link with that ID")
        return AccountLink(account_link_rows[0])

    def get_by_account_id(self, account_id):
        """Gets account links attached to the provided account.

        Params:
            account_id: The account to get account links on

        Returns:
            A list of AccountLink objects (could be empty)
        """
        account_link_rows = self._db.execute_d(
            """SELECT * FROM account_links
                WHERE account=%(account)s
            """,
            {
                "account": account_id
            }
        )
        return [AccountLink(account_link_row) for account_link_row in account_link_rows]

    def get_by_company(self, company, partner_account=None, api_insert=None, insert_sector=None, insert=False, data_race_protection=True):
        """Gets all account links that match company.

        Params:
            company: company to search
            insert: optional, if set to True it will insert when it doesn't exist and return a list with the single account link
            insert_sector: optional, if set to an integer it will be inserted if the row is inserted
        
        Returns:
            A list of AccountLink objects (could be empty)
        """
        account_link_rows = self._db.execute_d(
            """SELECT * FROM account_links
                WHERE company=%(company)s AND partner_account=%(partner_account)s
            """,
            {
                "company": company,
                "partner_account": partner_account
            }
        )
        if len(account_link_rows) == 0 and insert:
            try:
                self.insert(partner_account=partner_account, company=company, sector=insert_sector, api_insert=api_insert)
            except AccountLinksException as e:
                # *might* be a data race. Happens a lot in high thread environments.
                if data_race_protection:
                    return self.get_by_company(
                        partner_account=partner_account,
                        company=company,
                        api_insert=api_insert,
                        insert_sector=insert_sector,
                        insert=insert,
                        data_race_protection=False
                    )
                raise e
            return [self.get_by_id(self._db.last_row_id())]
        return [AccountLink(account_link_row) for account_link_row in account_link_rows]

    def get_by_affiliate_id(self, affiliate_id, partner_account=None, api_insert=None, sector=None, insert=False, data_race_protection=True):
        """Gets all account links that match a affiliate_id.

        Params:
            affiliate_id: affiliate_id to search
            insert: optional, if set to True it will insert when it doesn't exist and return a list with the single account link
        
        Returns:
            A list of AccountLink objects (could be empty)
        """
        account_link_rows = self._db.execute_d(
            """SELECT * FROM account_links
                WHERE affiliate_id=%(affiliate_id)s AND partner_account=%(partner_account)s
            """,
            {
                "affiliate_id": affiliate_id,
                "partner_account": partner_account
            }
        )
        if len(account_link_rows) == 0 and insert:
            try:
                self.insert(partner_account=partner_account, affiliate_id=affiliate_id, api_insert=api_insert, sector=sector)
            except AccountLinksException as e:
                # *might* be a data race. Happens a lot in high thread environments.
                if data_race_protection:
                    return self.get_by_affiliate_id(
                        affiliate_id=affiliate_id,
                        partner_account=partner_account,
                        api_insert=api_insert,
                        insert=insert,
                        data_race_protection=False
                    )
                raise e
            return [self.get_by_id(self._db.last_row_id())]
        return [AccountLink(account_link_row) for account_link_row in account_link_rows]

    def insert(self, account=None, affiliate_id=None, company=None, sector=None, partner_account=None, api_insert=None):
        """Inserts a new account link.

        Params:
            account: Account ID to bind to (optional)

        Raises:
            AccountLinksException
        """

        where_clause_statements = []

        # if affiliate_id is not None and company is not None:
        #     raise AccountLinksException("Account link empty")

        self._db.execute(
            """
                INSERT INTO account_links
                    (account, affiliate_id, company, sector, partner_account, api_insert)
                    VALUES (%(account)s, %(affiliate_id)s, %(company)s, %(sector)s, %(partner_account)s, %(api_insert)s)
            """,
            {
                "account": account,
                "affiliate_id": affiliate_id,
                "company": company,
                "sector": sector,
                "partner_account": partner_account,
                "api_insert": api_insert
            }
        )

    def update_account_link_with_account(self, partner_id, affiliate_id, sector, company,  account_id):
        """Updates a account link with the account id

        Params:
            partner: Partner ID 
            affiliate_id: affiliate_id or partron id
            account: Account ID to bind
        """
        self._db.execute(
            """
                UPDATE account_links
                SET account=%(account)s, sector=%(sector)s, company=%(company)s
                WHERE account_links.partner_account=%(partner)s AND account_links.affiliate_id=%(affiliate_id)s
            """,
            {
                "account": account_id,
                "sector": sector,
                "company": company,
                "partner": partner_id,
                "affiliate_id": affiliate_id
            }
        )
        if self._db.row_count() == 0:
            # insert the account_link
            self.insert(account=account_id, affiliate_id=affiliate_id, company=company, sector=sector, partner_account=partner_id)