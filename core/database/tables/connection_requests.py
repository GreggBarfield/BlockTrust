class ConnectionRequests:

    def __init__(self, db):
        self._db = db

    def set_connection_request(self, request_from, request_to):
        """
        Params:
            user_account_id: Account ID of user
            friend_account_id: Account ID of connection request

        Returns:
            None
        """
        self._db.execute(
            """
                INSERT INTO  connection_requests
                    (request_from, request_to)
                    VALUES
                        (%(request_from)s, %(request_to)s)
            """,
            {
                "request_from": request_from,
                "request_to": request_to
            }
        )

    def get_connection_requests(self, request_to):
        """
        Params:
            request_to: The account ID whose requests are to be fetched

        Returns:
            requests: Connection requests received by the account
        """
        requests = self._db.execute_d(
            """
            SELECT * FROM connection_requests
            WHERE request_to= %(request_to)s
            """,
            {
                "request_to": request_to
            }
        )
        return requests
