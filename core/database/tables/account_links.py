from ..objects.account_link import AccountLink, AccountLinkException


class AccountLinksException(Exception):
    """AccountLinks generic exception."""

    def __init__(self, reason):
        """Constructor for AccountLinks.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

# account link is the link between the account in our accounts table and the account in our partner's database
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
        return AccountLink(self._db, account_link_rows[0])

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
        return [AccountLink(self._db, account_link_row) for account_link_row in account_link_rows]

    def get_by_company(self, company, insert_sector=None, insert=False, data_race_protection=True):
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
                WHERE company=%(company)s
            """,
            {
                "company": company
            }
        )
        if len(account_link_rows) == 0 and insert:
            try:
                self.insert(company=company, sector=insert_sector)
            except AccountLinksException as e:
                # *might* be a data race. Happens a lot in high thread environments.
                if data_race_protection:
                    return self.get_by_company(
                        company=company,
                        insert_sector=insert_sector,
                        insert=insert,
                        data_race_protection=False
                    )
                raise e
            return [self.get_by_id(self._db.last_row_id())]
        return [AccountLink(self._db, account_link_row) for account_link_row in account_link_rows]

    def get_by_uid(self, uid, uid_type, partner_account=None, insert=False, data_race_protection=True):
        """Gets all account links that match a uid.

        Params:
            uid: uid to search
            uid_type: the UID type to search ("MFA")
            insert: optional, if set to True it will insert when it doesn't exist and return a list with the single account link
        
        Returns:
            A list of AccountLink objects (could be empty)
        """
        account_link_rows = self._db.execute_d(
            """SELECT * FROM account_links
                WHERE uid=%(uid)s AND uid_type=%(uid_type)sx AND partner_account=%(partner_account)s
            """,
            {
                "uid": uid,
                "uid_type": uid_type,
                "partner_account": partner_account
            }
        )
        if len(account_link_rows) == 0 and insert:
            try:
                self.insert(partner_account=partner_account, uid=uid, uid_type=uid_type)
            except AccountLinksException as e:
                # *might* be a data race. Happens a lot in high thread environments.
                if data_race_protection:
                    return self.get_by_uid(
                        uid=uid,
                        uid_type=uid_type,
                        insert=insert,
                        data_race_protection=False
                    )
                raise e
            return [self.get_by_id(self._db.last_row_id())]
        return [AccountLink(self._db, account_link_row) for account_link_row in account_link_rows]

    def insert(self, account=None, uid_type=None, uid=None, company=None, sector=None, partner_account=None):
        """Inserts a new account link.

        Params:
            account: Account ID to bind to (optional)
            uid_type: UID

        Raises:
            AccountLinksException
        """

        # UID type not specified or specified and not uid
        if uid_type is not None and uid is None or uid_type is None and uid is not None:
            raise AccountLinksException("UID and UID type mismatch")

        where_clause_statements = []

        if uid is not None and company is not None:
            raise AccountLinksException("Account link empty")

        self._db.execute(
            """
                INSERT IGNORE INTO account_links
                    (account, uid_type, uid, company, sector, partner_account)
                    VALUES (%(account)s, %(uid_type)s, %(uid)s, %(company)s, %(sector)s, %(partner_account)s)
            """,
            {
                "account": account,
                "uid_type": uid_type,
                "uid": uid,
                "company": company,
                "sector": sector,
                "partner_account": partner_account
            }
        )

        if self._db.row_count() != 1:
            raise AccountLinksException("Conflict with another account link")

    def add_account_to_account_link(self, partner, uid, account):
        """Updates a account link with the account id

        Params:
            partner: Partner ID 
            uid: UID or partron id
            account: Account ID to bind
        """
        self._db.execute(
            """
                UPDATE account_links
                SET account=%(account)s
                WHERE account_links.partner_account=%(partner)s AND account_links.uid=%(uid)s
            """,
                {
                    "account": account,
                    "partner": partner,
                    "uid": uid
                }
        )