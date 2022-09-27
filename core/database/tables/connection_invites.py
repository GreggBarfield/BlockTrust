from core.database.tables.accounts import NO_VALUE
from .connections import Connections, connection_status, connection_type


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
            raise Exception("Email is blank.")
        if '@' not in company_email or '.' not in company_email or len(company_email) < 5:
            raise Exception("The email you entered is incomplete.")
        if ' ' in company_email:
            raise Exception("Spaces cannot be in the email.")
        if len(self.get_connection_invites(from_account=from_account, company_email=company_email)) > 0:
            raise Exception("Connection Invite already sent.")
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

    def convert_invites_to_connections(self, email, account):
        """
        Adds invites in the connection_invites table to connections table once a user signs up
        Removes row from the connection_invites table

        Params:
            email: Email of the user who has signed up

        Returns:
            None
        """
        invites = self.get_connection_invites(company_email=email)
        if len(invites) >= 1:
            for invite in invites:
                Connections(self._db).create_connection_or_fail(
                    from_account_id=invite["from_account"],
                    to_account_id=account.id(),
                    status=connection_status["Connected"],
                    connection_type=connection_type["Created"]
                )

    def get_connection_invites(self, from_account=NO_VALUE, to_account=NO_VALUE, company_sector=NO_VALUE,
                                company_name=NO_VALUE, company_contact=NO_VALUE, company_email=NO_VALUE):
        """
        Gets the connection invite by the values specified

        Params:
            from_account: Account ID of sending account
            company_sector: Sector of invited company connection
            company_name: Company name of invited company
            company_contact: Name of company contact
            company_email: Email of invited company connection

        Returns:
            A list of connection invite(s) record if found else []
        """
        # base query
        base_query = "SELECT * FROM connection_invites"

        query_conditions = []
        query_values = {}

        if from_account is not NO_VALUE:
            query_conditions.append(" from_account = %(from_account)s ")
            query_values["from_account"] = from_account

        if to_account is not NO_VALUE:
            query_conditions.append(" to_account = %(to_account)s ")
            query_values["to_account"] = to_account

        if company_sector is not NO_VALUE:
            query_conditions.append(" company_sector = %(company_sector)s ")
            query_values["company_sector"] = company_sector

        if company_name is not NO_VALUE:
            query_conditions.append(" company_name = %(company_name)s ")
            query_values["company_name"] = company_name

        if company_contact is not NO_VALUE:
            query_conditions.append(" company_contact = %(company_contact)s ")
            query_values["company_contact"] = company_contact

        if company_email is not NO_VALUE:
            query_conditions.append(" company_email = %(company_email)s ")
            query_values["company_email"] = company_email

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        connection_invite_rows = self._db.execute_d(query, query_values)
        if len(connection_invite_rows) > 0:
            return connection_invite_rows
        else:
            return []
