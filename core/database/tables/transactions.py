class TransactionException(Exception):
    """Generic Transaction exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for TransactionException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Transactions:

    def __init__(self, db):
        self._db = db

    def getTransactionByID(self, user_id):
        """Gets the transactions by a user.

        Params:
            user_id: User's ID

        Returns:
            A Transaction object array on success, or None on no match.
        """
        matching_transactions = self._db.execute_d(
            """
                SELECT * FROM transactions
                WHERE
                    acct_no=%(acct_no)s
            """,
            {
                "acct_no": user_id
            }
        )

        if len(matching_transactions) < 1:
            raise TransactionException()

        return matching_transactions
