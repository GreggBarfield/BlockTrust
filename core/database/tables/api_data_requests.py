from json import dumps

class APIDataRequests:

    def __init__(self, db):
        self._db = db

    def insert_api_data_request(self, api_route, request_data, account_id=None):
        """Inserts an api data request received.
        """
        self._db.execute(
            """INSERT INTO api_data_requests
                (account_id, api_route, request_data)
                VALUES
                    (%(account_id)s, %(api_route)s , %(request_data)s)
            """,
            {
                "account_id": account_id,
                "api_route": api_route,
                "request_data": dumps(request_data)
            }
        )