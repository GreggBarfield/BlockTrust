from .accounts import Accounts
from .. import database

connection_status = {
    "Pending": 0,
    "Connected": 1,
    "Declined": 2
}


class ConnectionException(Exception):
    """Generic connection exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for UsersException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Connections:

    def __init__(self, db: 'database.Database'):
        self._db = db

    def get_account_connections(self, account_id, status):
        """
        Params:
            account_id: Account ID whose connections are requested
            status: Status of the connections requested
        Returns:
            connections: List of connected accounts

        """
        connections = self._db.execute_d(
            """
            SELECT * FROM connections
            WHERE (from_account_id= %(account_id)s OR to_account_id=%(account_id)s) AND status= %(status)s
            """,
            {
                "account_id": account_id,
                "status": status
            }
        )
        return connections

    def update_connection(self, from_account_id, to_account_id, status):
        """
        Params:
            from_account_id: Account ID of user
            to_account_id:  Second account ID
            status: Status of the connection which needs to be updated
        Returns:
            None
        """
        from_account = Accounts.get_by_id(self, account_id=from_account_id)
        to_account = Accounts.get_by_id(self, account_id=to_account_id)
        from_account_name = from_account.company()
        to_account_name = to_account.company()
        # From account is the sender of the request, To is the reciever
        # For the from account we already have a an entry in the table with status 0(pending)
        self._db.execute(
            """
            UPDATE connections
            SET status=%(status)s
            WHERE ((from_account_id=%(from_account_id)s AND to_account_id=%(to_account_id)s) OR
                (from_account_id= %(to_account_id)s AND to_account_id=%(from_account_id)s))
            """,
            {
                "status": status,
                "from_account_id": from_account_id,
                "to_account_id": to_account_id
            }
        )

    def create_connection(self, from_account_id, to_account_id, status):
        """
        Params:
            from_account_id: Account ID of user
            to_account_id: Account ID of connection request
            status: Status of the connection created
        Returns:
            None

        Raises:
            ConnectionException on connection being present or connection request being present
        """
        if self.get_connection_between(from_account_id, to_account_id) == 1:
            raise ConnectionException("Account is already connected!")
        if self.get_connection_between(from_account_id, to_account_id) == 0:
            raise ConnectionException("Request already sent!")
        first_account = Accounts.get_by_id(self, account_id=from_account_id)
        second_account = Accounts.get_by_id(self, account_id=to_account_id)
        from_account_name = first_account.company()
        to_account_name = second_account.company()
        self._db.execute(
            """
                INSERT INTO  connections
                    (from_account_id, from_account_name, to_account_id, to_account_name, status)
                    VALUES
                        (%(from_account_id)s, %(from_account_name)s, %(to_account_id)s, %(to_account_name)s, %(status)s)
            """,
            {
                "from_account_id": from_account_id,
                "from_account_name": from_account_name,
                "to_account_id": to_account_id,
                "to_account_name": to_account_name,
                "status": status
            }
        )

    def get_connection_between(self, from_account_id, to_account_id):
        """
        Checks the connection status between two accounts

        Params:
        from_account_id: Account ID of user
        to_account_id: Account ID being sent the invite

        Returns:
        Status of connection. 0-Pending. 1-Connected, 2-Declined
        """

        status = self._db.execute_d(
            """
            SELECT status FROM connections
            WHERE ((from_account_id= %(from_account_id)s AND to_account_id=%(to_account_id)s) OR
            (from_account_id= %(to_account_id)s AND to_account_id=%(from_account_id)s))
            """,
            {
                "from_account_id": from_account_id,
                "to_account_id": to_account_id
            }
        )
        if len(status) >= 1:
            return status[0]["status"]
        return None
