from .accounts import Accounts
from .. import database
from ..no_value import NoValue

NO_VALUE = NoValue()

connection_status = {
    "Pending": 0,
    "Connected": 1,
    "Blocked": 2
}

connection_type = {
    "Created": 1,
    "Acquired": 2
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
    
    def create_connection_or_fail(self, from_account_id, to_account_id, status, connection_type):
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
        self.insert_connection(from_account_id, to_account_id, status, from_account_name, to_account_name, connection_type)

    def insert_connection(self, from_account_id, to_account_id, status, from_account_name, to_account_name, connection_type):
        """
        Returns:
            None
        """

        self._db.execute(
            """
                INSERT INTO  connections
                    (from_account_id, from_account_name, to_account_id, to_account_name, status, connection_type)
                    VALUES
                        (%(from_account_id)s, %(from_account_name)s, %(to_account_id)s, %(to_account_name)s, %(status)s, %(connection_type)s)
            """,
            {
                "from_account_id": from_account_id,
                "from_account_name": from_account_name,
                "to_account_id": to_account_id,
                "to_account_name": to_account_name,
                "status": status,
                "connection_type": connection_type
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

    def get_connections(self, id=NO_VALUE, from_account_id=NO_VALUE, to_account_id=NO_VALUE, from_account_name=NO_VALUE,
                        to_account_name=NO_VALUE, status=NO_VALUE, connection_type=NO_VALUE):
        """
        Gets the connections based on the provided parameters

        Params:
            id: Connection table ID
            from_account_id: Account ID of first account
            to_account_id: Account ID of second account
            from_account_name: Account name of first account
            to_account_name: Account name of second account
            status: Connection status between accounts

        Returns:
            A list of connections or and empty list
        """
        base_query = "SELECT * FROM connections"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if from_account_id is not NO_VALUE:
            query_conditions.append(" from_account_id = %(from_account_id)s")
            query_values["from_account_id"] = from_account_id
        if to_account_id is not NO_VALUE:
            query_conditions.append(" to_account_id = %(to_account_id)s")
            query_values["to_account_id"] = to_account_id
        if from_account_name is not NO_VALUE:
            query_conditions.append(" from_account_name = %(from_account_name)s")
            query_values["from_account_name"] = from_account_name
        if to_account_name is not NO_VALUE:
            query_conditions.append(" to_account_name = %(to_account_name)s")
            query_values["to_account_name"] = to_account_name
        if status is not NO_VALUE:
            query_conditions.append(" status = %(status)s")
            query_values["status"] = status
        if connection_type is not NO_VALUE:
            query_conditions.append(" connection_type = %(connection_type)s")
            query_values["connection_type"] = connection_type

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        connection_rows = self._db.execute_d(query, query_values)
        if len(connection_rows) > 0:
            return connection_rows
        else:
            return []
