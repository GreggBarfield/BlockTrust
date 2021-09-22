from .accounts import Accounts
from .. import database


class ConnectionException(Exception):
    """Generic user exception."""

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
            WHERE first_account_id= %(account_id)s AND status=1
            """,
            {
                "account_id": account_id
            }
        )
        return connections

    def create_account_connection(self, first_account_id, second_account_id):
        """
        Params:
            user_account_id: Account ID of user
            friend_account_id:
        Returns:
            None
        """
        first_account = Accounts.get_by_id(self, account_id=first_account_id)
        second_account = Accounts.get_by_id(self, account_id=second_account_id)
        first_account_name = first_account.company()
        second_account_name = second_account.company()
        # First account is the sender of the request, Second is the reciever
        # For the first account we already have a an entry in the table with status 0(pending)
        # We update the pending entry and add a new entry for the connection between second and first user
        # This helps save time during lookup and simplifies generating the account connection list
        self._db.execute(
            """
            UPDATE TABLE connections
            SET status=1
            WHERE first_account_id=%(first_account_id)s, second_account_id=%(second_account_id)s
            """,
            {
                "first_account_id": first_account_id,
                "second_account_id": second_account_id
            }
        )

        self._db.execute(
            """
                INSERT INTO connections
                    (first_account_id, first_account_name, second_account_id, second_account_name, status)
                    VALUES
                        (%(second_account_id)s, %(second_account_name)s, %(first_account_id)s, %(frist_account_name)s, 1)
            """,
            {
                "second_account_id": second_account_id,
                "second_account_name": second_account_name,
                "first_account_id": first_account_id,
                "first_account_name": first_account_name
            }
        )

    def set_connection_request(self, first_account_id, second_account_id):
        """
        Params:
            first_account_id: Account ID of user
            second_account_id: Account ID of connection request

        Returns:
            None

        Raises:
            ConnectionException on connection being present or connection request being present
        """
        if self.connection_exists(first_account_id, second_account_id):
            raise ConnectionException("Account is already connected!")
        if self.connection_request_exists(first_account_id, second_account_id):
            raise ConnectionException("Request already sent!")
        first_account = Accounts.get_by_id(self, account_id=first_account_id)
        second_account = Accounts.get_by_id(self, account_id=second_account_id)
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
                "first_account_id": first_account_id,
                "first_account_name": first_account_name,
                "second_account_id": second_account_id,
                "second_account_name": second_account_name,
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
            WHERE second_account_id= %(account_id)s AND status=0
            """,
            {
                "account_id": account_id
            }
        )
        return requests

    def decline_conection_request(self, first_account_id, second_account_id):
        """
        Marks the connnection request as declined in the database

        Params:
            first_account_id: Sender account id
            second_account_id: Account which received the invite

        Returns:
            None
        """
        self._db.execute(
            """
                UPDATE  connections
                SET status=2
                WHERE first_account_id=%(first_account_id)s AND second_account_id=%(second_account_id)s
            """,
            {
                "first_account_id": first_account_id,
                "second_account_id": second_account_id
            }
        )

    def connection_exists(self, first_account_id, second_account_id):
        """
        Checks if a connection exists between two accounts

        Params:
        first_account_id: Account ID of user
        second_account_id: Account ID being sent the invite

        Returns:
        True if a connection exists. False if not connection found
        """

        connections = self._db.execute_d(
            """
            SELECT * FROM connections
            WHERE ((first_account_id= %(first_account_id)s AND second_account_id=%(second_account_id)s) OR
            (first_account_id= %(second_account_id)s AND second_account_id=%(first_account_id)s))
            AND status=1
            """,
            {
                "first_account_id": first_account_id,
                "second_account_id": second_account_id
            }
        )
        if len(connections) >= 1:
            return True
        return False

    def connection_request_exists(self, first_account_id, second_account_id):
        """
        Checks if a connection request exists between two accounts

        Params:
        first_account_id: Account ID of user
        second_account_id: Account ID being sent the invite

        Returns:
        True if a connection request exists. False if not connection request found
        """

        connection_requests = self._db.execute_d(
            """
            SELECT * FROM connections
            WHERE ((first_account_id= %(first_account_id)s AND second_account_id=%(second_account_id)s) OR
            (first_account_id= %(second_account_id)s AND second_account_id=%(first_account_id)s))
            AND status=0
            """,
            {
                "first_account_id": first_account_id,
                "second_account_id": second_account_id
            }
        )
        if len(connection_requests) >= 1:
            return True
        return False
