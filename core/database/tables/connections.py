from datetime import datetime
from .accounts import Accounts
from ..no_value import NoValue
from json import dumps

NO_VALUE = NoValue()

CONNECTION_STATUS_NAME_TO_ID = {
    "Pending": 0,
    "Connected": 1,
    "Blocked": 2
}

CONNECTION_TYPE_NAME_TO_ID = {
    "Created": 1,
    "Acquired": 2
}

CONNECTION_TYPE_ID_TO_NAME = {
    value: key for key, value in CONNECTION_TYPE_NAME_TO_ID.items()
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

    def create_or_fail_connection(self, from_account_id, to_account_id, status, connection_type_id, details=None):
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
        from_account = Accounts(self._db).get_accounts(id=from_account_id)[0]
        to_account = Accounts(self._db).get_accounts(id=to_account_id)[0]
        existing_connection = self.get_connection_between(from_account_id, to_account_id)
        if existing_connection is not None:
            if existing_connection["connection_status_id"] == CONNECTION_STATUS_NAME_TO_ID["Connected"]:
                raise ConnectionException(from_account["name"] + " is already connected!")
            if existing_connection["connection_status_id"] == CONNECTION_STATUS_NAME_TO_ID["Pending"]:
                raise ConnectionException("Connection Invite already sent to " + to_account["name"])
            if existing_connection["connection_status_id"] == CONNECTION_STATUS_NAME_TO_ID["Blocked"]:
                raise ConnectionException("Cannot send Connection Invite")
        self.insert_connection(
            from_account_id, to_account_id, status, connection_type_id, details
        )

    def insert_connection(self, from_account_id, to_account_id, status, connection_type_id, details):
        """
        Returns:
            None
        """
        accepted_date = datetime.utcnow() if status == CONNECTION_STATUS_NAME_TO_ID["Connected"] else None

        self._db.execute(
            """
                INSERT INTO  connections
                    (from_account_id, to_account_id, connection_status_id, connection_type_id, accepted_date, details)
                    VALUES
                        (%(from_account_id)s, %(to_account_id)s, %(status)s, %(connection_type_id)s, %(accepted_date)s,
                         %(details)s)
            """,
            {
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "status": status,
                "connection_type_id": connection_type_id,
                "accepted_date": accepted_date,
                "details": dumps(details) if details else details
            }
        )

        return self._db.last_row_id()

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

    def get_unconnected_accounts(self, account_id, get_partners_only=False):
        """
        Get accounts not connected to the specified account

        Params:
            account_id: The account ID for which unconnected accounts are required

        Returns:
            A list of accounts which are not connected to the specified account or an empty list
        """
        query = """SELECT * FROM accounts WHERE id NOT IN(
                SELECT from_account_id as connected_account_id FROM connections WHERE to_account_id = %(account_id)s UNION
                SELECT to_account_id as connected_account_id FROM connections WHERE from_account_id = %(account_id)s
                ) AND id!=%(account_id)s
                """
        
        if get_partners_only is not False:
            query = query + " AND is_partner = 1"
        unconnected_accounts = self._db.execute_d(query, {"account_id": account_id})

        if len(unconnected_accounts) > 0:
            return unconnected_accounts
        return []

    def get_connections(self, id=NO_VALUE, from_account_id=NO_VALUE, to_account_id=NO_VALUE, status=NO_VALUE,
                        connection_type_id=NO_VALUE, blocked_by_account_id=NO_VALUE, get_related_data=False,
                        from_account_id_OR_to_account_id=NO_VALUE):
        """
        Gets the connections based on the provided parameters

        Params:
            id: Connection table ID
            from_account_id: Account ID of first account
            to_account_id: Account ID of second account
            status: Connection status between accounts
            connection_type_id: Type of connection established
            blocked_by_account_id: Account ID which blocked the other account. (Only for "Blocked" status)

        Returns:
            A list of connections or and empty list
        """

        if get_related_data:
            base_query = """
                SELECT c.*, fa.name as from_account_name, fa.sector as from_account_sector_id,
                ta.name as to_account_name, ta.sector as to_account_sector_id FROM connections c
                INNER JOIN accounts fa ON c.from_account_id = fa.id
                INNER JOIN accounts ta on c.to_account_id=ta.id
            """
        else:
            base_query = "SELECT * FROM connections c"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("c.id = %(id)s")
            query_values["id"] = id
        if from_account_id is not NO_VALUE:
            query_conditions.append("from_account_id = %(from_account_id)s")
            query_values["from_account_id"] = from_account_id
        if to_account_id is not NO_VALUE:
            query_conditions.append("to_account_id = %(to_account_id)s")
            query_values["to_account_id"] = to_account_id
        if from_account_id_OR_to_account_id is not NO_VALUE:
            query_conditions.append("(from_account_id = %(account_id)s OR to_account_id = %(account_id)s)")
            query_values["account_id"] = from_account_id_OR_to_account_id
        if status is not NO_VALUE:
            query_conditions.append("connection_status_id = %(status)s")
            query_values["status"] = status
        if connection_type_id is not NO_VALUE:
            query_conditions.append("connection_type_id = %(connection_type_id)s")
            query_values["connection_type_id"] = connection_type_id
        if blocked_by_account_id is not NO_VALUE:
            query_conditions.append("blocked_by_account_id = %(blocked_by_account_id)s")
            query_values["blocked_by_account_id"] = blocked_by_account_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        connection_rows = self._db.execute_d(query, query_values)
        if len(connection_rows) > 0:
            return connection_rows
        else:
            return []

    def update_connection(self, id, connection_status_id=NO_VALUE, blocked_by_account_id=NO_VALUE, details=NO_VALUE):
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
            existing_row = self.get_connections(id=id)[0]
            # setting columns which depend on connection status
            # status changed to Blocked
            if connection_status_id == CONNECTION_STATUS_NAME_TO_ID["Blocked"] \
                    and existing_row["connection_status_id"] != CONNECTION_STATUS_NAME_TO_ID["Blocked"]:
                if blocked_by_account_id is not NO_VALUE:
                    if blocked_by_account_id is not None:
                        query_updated_columns.append("blocked_by_account_id = %(blocked_by_account_id)s")
                        query_updated_values["blocked_by_account_id"] = blocked_by_account_id
                        query_updated_columns.append("blocked_date = %(blocked_date)s")
                        query_updated_values["blocked_date"] = datetime.utcnow()
                else:
                    raise ConnectionException("Blocked by account not provided")
            # status changed to Connected
            elif connection_status_id == CONNECTION_STATUS_NAME_TO_ID["Connected"] \
                    and existing_row["connection_status_id"] != CONNECTION_STATUS_NAME_TO_ID["Connected"]:
                query_updated_columns.append("accepted_date = %(accepted_date)s")
                query_updated_values["accepted_date"] = datetime.utcnow()
        if details is not NO_VALUE:
            query_updated_columns.append("details = %(details)s")
            query_updated_values["details"] = dumps(details) if details is not None else None
        if len(query_updated_columns) >= 1:
            combined_query_updated_values = " SET " + ", ".join(query_updated_columns) + " WHERE id=%(id)s"
            query = base_query + combined_query_updated_values
            self._db.execute(query, query_updated_values)
        return self._db.row_count()

    def get_connected_account_ids(self, account_id, sector_id=None):
        connections = Connections(self._db).get_connections(
            from_account_id_OR_to_account_id=account_id, status=CONNECTION_STATUS_NAME_TO_ID["Connected"], get_related_data=True
        )

        connected_account_ids = []
        for c in connections:
            if c["from_account_id"] == account_id:
                if sector_id:
                    if c["to_account_sector_id"] == sector_id:
                        connected_account_ids.append(c["to_account_id"])
                else:
                    connected_account_ids.append(c["to_account_id"])

            elif c["to_account_id"] == account_id:
                if sector_id:
                    if c["from_account_sector_id"] == sector_id:
                        connected_account_ids.append(c["from_account_id"])
                else:
                    connected_account_ids.append(c["from_account_id"])

        return connected_account_ids
