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
