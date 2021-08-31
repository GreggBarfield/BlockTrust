class Connections:

    def __init__(self, db):
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
            WHERE user_account_id= %(account_id)s
            """,
            {
                "account_id": account_id
            }
        )
        return connections
