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
        first_account = Accounts(self._db).get_account_by_id(account_id=from_account_id)
        second_account = Accounts(self._db).get_account_by_id(account_id=to_account_id)
        from_account_name = first_account.name()
        to_account_name = second_account.name()
        if self.get_connection_between(from_account_id, to_account_id, connection_status["Connected"]) is not None:
            raise ConnectionException(to_account_name + " is already connected!")
        if self.get_connection_between(from_account_id, to_account_id, connection_status["Pending"]) is not None:
            raise ConnectionException("Connection Invite already sent to " + to_account_name)
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

    def get_connection_between(self, from_account_id, to_account_id, status):
        """
        Checks the connection status between two accounts

        Params:
        from_account_id: Account ID of user
        to_account_id: Account ID being sent the invite

        Returns:
        Connection object or None
        """

        connection = self._db.execute_d(
            """
            SELECT * FROM connections
            WHERE ((from_account_id= %(from_account_id)s AND to_account_id=%(to_account_id)s) OR
            (from_account_id= %(to_account_id)s AND to_account_id=%(from_account_id)s))
            AND status = %(status)s
            """,
            {
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "status": status
            }
        )
        if len(connection) == 1:
            return connection[0]
        return None

    def get_unconnected_accounts(self, account_id):
        """
        Get accounts not connected to the specified account

        Params:
            account_id: The account ID for which unconnected accounts are required

        Returns:
            A list of accounts which are not connected to the specified account or an empty list
        """
        unconnected_accounts = self._db.execute_d(
            """
            SELECT * FROM accounts WHERE id NOT IN(
            SELECT from_account_id as connected_account_id FROM connections WHERE to_account_id = %(account_id)s UNION
            SELECT to_account_id as connected_account_id FROM connections WHERE from_account_id = %(account_id)s
            ) AND id!=%(account_id)s AND is_partner=0
            """, {
                "account_id": account_id
            }
        )
        if len(unconnected_accounts) > 0:
            return unconnected_accounts
        return []
