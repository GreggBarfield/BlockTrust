class TransactionException(Exception):
    """Generic Transaction exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for TransactionException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Orders:

    def __init__(self, db):
        self._db = db

    def getOrdersByAccountNumber(self, account_no):
        """Gets the transactions by a user.

        Params:
            account_no: User account number

        Returns:
            A Transaction object array on success, or None on no match.
        """
        matching_orders = self._db.execute_d(
            """
                SELECT * FROM orders
                WHERE
                    account_no=%(account_no)s
            """,
            {
                "account_no": account_no
            }
        )

        if len(matching_orders) < 1:
            raise TransactionException()

        return matching_orders
