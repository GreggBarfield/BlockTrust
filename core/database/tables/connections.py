from datetime import datetime
from .accounts import Accounts
from ..no_value import NoValue

NO_VALUE = NoValue()

connection_status_name_to_id = {
    "Pending": 0,
    "Connected": 1,
    "Blocked": 2
}

connection_type_name_to_id = {
    "Created": 1,
    "Acquired": 2
}

connection_type_id_to_name = {
    value: key for key, value in connection_type_name_to_id.items()
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

    def __init__(self, db):
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
            WHERE (from_account_id= %(account_id)s OR to_account_id=%(account_id)s) AND connection_status_id= %(status)s
            """,
            {
                "account_id": account_id,
                "status": status
            }
        )
        return connections

    def update_connection_between(self, from_account_id, to_account_id, status):
        """
        Updates the connection between two accounts
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
            SET connection_status_id=%(status)s
            WHERE ((from_account_id=%(from_account_id)s AND to_account_id=%(to_account_id)s) OR
                (from_account_id= %(to_account_id)s AND to_account_id=%(from_account_id)s))
            """,
            {
                "status": status,
                "from_account_id": from_account_id,
                "to_account_id": to_account_id
            }
        )
    
    def create_or_fail_connection(self, from_account_id, to_account_id, status, connection_type_id):
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
        existing_connection = self.get_connection_between(from_account_id, to_account_id)
        if existing_connection is not None:
            if existing_connection["connection_status_id"] == connection_status_name_to_id["Connected"]:
                raise ConnectionException(to_account_name + " is already connected!")
            if existing_connection["connection_status_id"] == connection_status_name_to_id["Pending"]:
                raise ConnectionException("Connection Invite already sent to " + to_account_name)
            if existing_connection["connection_status_id"] == connection_status_name_to_id["Blocked"]:
                raise ConnectionException("Cannot send Connection Invite")
        self.insert_connection(from_account_id, to_account_id, status, from_account_name, to_account_name, connection_type_id)

    def insert_connection(self, from_account_id, to_account_id, status, from_account_name, to_account_name, connection_type_id):
        """
        Returns:
            None
        """

        self._db.execute(
            """
                INSERT INTO  connections
                    (from_account_id, from_account_name, to_account_id, to_account_name, connection_status_id, connection_type_id)
                    VALUES
                        (%(from_account_id)s, %(from_account_name)s, %(to_account_id)s, %(to_account_name)s, %(status)s, %(connection_type_id)s)
            """,
            {
                "from_account_id": from_account_id,
                "from_account_name": from_account_name,
                "to_account_id": to_account_id,
                "to_account_name": to_account_name,
                "status": status,
                "connection_type_id": connection_type_id
            }
        )

    def get_connection_between(self, from_account_id, to_account_id, status=NO_VALUE):
        """
        Checks the connection status between two accounts

        Params:
        from_account_id: Account ID of user
        to_account_id: Account ID being sent the invite

        Returns:
        Connection object or None
        """
        query = """
            SELECT * FROM connections
            WHERE ((from_account_id= %(from_account_id)s AND to_account_id=%(to_account_id)s) OR
            (from_account_id= %(to_account_id)s AND to_account_id=%(from_account_id)s))
            """
        query_values = {
            "from_account_id": from_account_id,
            "to_account_id": to_account_id
        }
        if status is not NO_VALUE:
            query += " AND connection_status_id = %(status)s"
            query_values["status"] = status
        connection = self._db.execute_d(query, query_values)
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
                        to_account_name=NO_VALUE, status=NO_VALUE, connection_type_id=NO_VALUE, blocked_by_account_id=NO_VALUE,
                        blocked_date_time=NO_VALUE):
        """
        Gets the connections based on the provided parameters

        Params:
            id: Connection table ID
            from_account_id: Account ID of first account
            to_account_id: Account ID of second account
            from_account_name: Account name of first account
            to_account_name: Account name of second account
            status: Connection status between accounts
            connection_type_id: Type of connection established
            blocked_by_account_id: Account ID which blocked the other account. (Only for "Blocked" status)
            blocked_date_time: UTC time of blocking

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
            query_conditions.append(" connection_status_id = %(status)s")
            query_values["status"] = status
        if connection_type_id is not NO_VALUE:
            query_conditions.append(" connection_type_id = %(connection_type_id)s")
            query_values["connection_type_id"] = connection_type_id
        if blocked_by_account_id is not NO_VALUE:
            query_conditions.append(" blocked_by_account_id = %(blocked_by_account_id)s")
            query_values["blocked_by_account_id"] = blocked_by_account_id
        if blocked_date_time is not NO_VALUE:
            query_conditions.append(" blocked_date_time = %(blocked_date_time)s")
            query_values["blocked_date_time"] = blocked_date_time

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

    def update_connection(self, id, connection_status_id=NO_VALUE, connection_type_id=NO_VALUE,
                          blocked_by_account_id=NO_VALUE):
        """
        Updates the connection based on the id specified

        Params:
            id: The ID of the connection to be updated
            connection_status_id: The status id of the connection
            connection_type_id: Type of connection established
            blocked_by_account_id: Account ID which blocked the other account. (Only for "Blocked" status)

        Returns:
            Number of rows affected.
        """
        base_query = "UPDATE connections "

        query_updated_columns = []
        query_updated_values = {}
        query_updated_values["id"] = id
        if connection_status_id is not NO_VALUE:
            query_updated_columns.append("connection_status_id = %(connection_status_id)s")
            query_updated_values["connection_status_id"] = connection_status_id
        if connection_type_id is not NO_VALUE:
            query_updated_columns.append("connection_type_id = %(connection_type_id)s")
            query_updated_values["connection_type_id"] = connection_type_id
        if blocked_by_account_id is not NO_VALUE:
            if blocked_by_account_id is not None:
                query_updated_columns.append("blocked_by_account_id = %(blocked_by_account_id)s")
                query_updated_values["blocked_by_account_id"] = blocked_by_account_id
                query_updated_columns.append("blocked_date_time = %(blocked_date_time)s")
                query_updated_values["blocked_date_time"] = datetime.utcnow()
            else:
                query_updated_columns.append("blocked_by_account_id = %(blocked_by_account_id)s")
                query_updated_values["blocked_by_account_id"] = None
                query_updated_columns.append("blocked_date_time = %(blocked_date_time)s")
                query_updated_values["blocked_date_time"] = None
        if len(query_updated_columns) >= 1:
            combined_query_updated_values = " SET " + ", ".join(query_updated_columns) + " WHERE id=%(id)s"
            query = base_query + combined_query_updated_values
            self._db.execute(query, query_updated_values)
        return self._db.row_count()
