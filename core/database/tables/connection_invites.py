from .accounts import Accounts


class ConnectionInviteException(Exception):
    """Generic user exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for UsersException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class ConnectionInvites:

    def __init__(self, db):
        self._db = db

    def add_connection_invite(self, from_account, company_sector, company_name, company_contact, company_email):
        """
        Params:
            from_Account: Account sending the invite
            comapny_name: Name of new company invited
            company_contact: Contact name for new company
            company_email: Company email of the new company

        Returns:
            None
        """
        if len(company_email) == 0:
            raise ConnectionInviteException("Email is blank.")
        if '@' not in company_email or '.' not in company_email or len(company_email) < 5:
            raise ConnectionInviteException("The email you entered is incomplete.")
        if ' ' in company_email:
            raise ConnectionInviteException("Spaces cannot be in the email.")
        if self.connection_invite_exists(from_account, company_email):
            raise ConnectionInviteException("Connection Invite already sent.")
        self._db.execute(
            """
                INSERT INTO  connection_invites
                    (from_account, company_sector, company_name, company_contact, company_email)
                    VALUES
                        (%(from_account)s, %(company_sector)s, %(company_name)s, %(company_contact)s, %(company_email)s)
            """,
            {
                "from_account": from_account,
                "company_sector": company_sector,
                "company_name": company_name,
                "company_contact": company_contact,
                "company_email": company_email
            }
        )

    def add_pending_invites(self, email, account):
        """
        Adds invites in the connection_invites table to connections table once a user signs up
        Removes row from the connection_invites table

        Params:
            email: Email of the user who has signed up

        Returns:
            None
        """
        invites = self._db.execute_d(
            """
            SELECT * from connection_invites
            WHERE company_email=%(email)s
            """,
            {
                "email": email
            }
        )
        if len(invites) >= 1:
            for invite in invites:
                first_account = Accounts.get_by_id(self, account_id=invite["from_account"])
                second_account = Accounts.get_by_id(self, account_id=account.id())
                first_account_name = first_account.company()
                second_account_name = second_account.company()
                self._db.execute(
                    """
                        INSERT INTO  connections
                            (first_account_id, first_account_name, second_account_id, second_account_name, status)
                            VALUES
                                (%(first_account_id)s, %(first_account_name)s, %(second_account_id)s, %(second_account_name)s, 0)
                    """,
                    {
                        "first_account_id": invite["from_account"],
                        "first_account_name": first_account_name,
                        "second_account_id": account.id(),
                        "second_account_name": second_account_name,
                    }
                )
            self._db.execute(
                """
                DELETE from connection_invites
                WHERE company_email=%(email)s
                """,
                {
                    "email": email
                }
            )

    def connection_invite_exists(self, from_account, company_email):
        """
        Checks if a connection invite already exists in the database

        Params:
            from__account: Account sending the invite
            company_email: Email the invite is being sent out to

        Returns:
            True if connection invite exists. False if no invite exists
        """
        invite = self._db.execute_d(
            """
            SELECT * from connection_invites
            WHERE from_account=%(from_account)s AND company_email=%(company_email)s
            """,
            {
                "from_account": from_account,
                "company_email": company_email
            }
        )
        if len(invite) >= 1:
            return True
        return False
