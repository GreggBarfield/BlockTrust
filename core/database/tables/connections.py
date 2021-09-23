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

    def get_account_connections(self, account_id):
        """
        Params:
            account_id: Account ID whose connections are requested

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
                "status": connection_status["Connected"]
            }
        )
        return connections

    def create_account_connection(self, from_account_id, to_account_id):
        """
        Params:
            user_account_id: Account ID of user
            friend_account_id:
        Returns:
            None
        """
        first_account = Accounts.get_by_id(self, account_id=from_account_id)
        second_account = Accounts.get_by_id(self, account_id=to_account_id)
        from_account_name = first_account.company()
        to_account_name = second_account.company()
        # First account is the sender of the request, Second is the reciever
        # For the first account we already have a an entry in the table with status 0(pending)
        # We update the pending entry and add a new entry for the connection between second and first user
        # This helps save time during lookup and simplifies generating the account connection list
        self._db.execute(
            """
            UPDATE TABLE connections
            SET status=%(status)s
            WHERE from_account_id=%(from_account_id)s, to_account_id=%(to_account_id)s
            """,
            {
                "status": connection_status["Connected"],
                "from_account_id": from_account_id,
                "to_account_id": to_account_id
            }
        )

    def create_connection_request(self, from_account_id, to_account_id):
        """
        Params:
            from_account_id: Account ID of user
            to_account_id: Account ID of connection request

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
                        (%(from_account_id)s, %(from_account_name)s, %(to_account_id)s, %(to_account_name)s, 0)
            """,
            {
                "from_account_id": from_account_id,
                "from_account_name": from_account_name,
                "to_account_id": to_account_id,
                "to_account_name": to_account_name,
            }
        )

    def get_connection_requests(self, account_id):
        """
        Params:
            account_id: The account ID whose requests are to be fetched

        Returns:
            requests: Connection requests received by the account
        """
        requests = self._db.execute_d(
            """
            SELECT * FROM connections
            WHERE to_account_id= %(account_id)s AND status=%(status)s
            """,
            {
                "status": connection_status["Pending"],
                "account_id": account_id
            }
        )
        return requests

    def decline_conection_request(self, from_account_id, to_account_id):
        """
        Marks the connnection request as declined in the database

        Params:
            from_account_id: Sender account id
            to_account_id: Account which received the invite

        Returns:
            None
        """
        self._db.execute(
            """
                UPDATE  connections
                SET status=%(status)s
                WHERE from_account_id=%(from_account_id)s AND to_account_id=%(to_account_id)s
            """,
            {
                "status": connection_status["Declined"],
                "from_account_id": from_account_id,
                "to_account_id": to_account_id
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
