from .. import database
from ..objects.transaction import Transaction

transaction_type = {
    "Tag-Store": 0,
    "Subscription": 1
}


class Transactions:

    def __init__(self, db: 'database.Database'):
        self._db = db

    def get_by_id(self, id):
        """
        Gets a transaction by an ID.

        Params:
            id: the transaction id

        Returns:
            A Transaction object

        Raises:
            Exception on ID not found
        """
        order_rows = self._db.execute_d(
            """
            SELECT * FROM transactions
            WHERE id=%(id)s
            """,
            {
                "id": id
            }
        )
        if len(order_rows) != 1:
            raise Exception("No transaction found with that ID.")
        return Transaction(self._db, order_rows[0])

    def create_transaction(self, account, amount, type):
        """
        Adds a new transaction to the table

        Params:
            account: Account performing the transaction
            amount: Transaction amount
            type: Type of transaction

        Returns:
            None
        """
        self._db.execute(
            """
            INSERT INTO transactions
            (account, amount, type)
            VALUES
            (%(account)s, %(amount)s, %(type)s)
            """,
            {
                "account": account,
                "amount": amount,
                "type": type
            }
        )

    def get_transactions(self):
        """
        Gets all transactions from the database

        Returns:
            A list of all transactions
        """
        transaction_rows = self._db.execute_d(
            """
            SELECT * FROM transactions
            """
        )
        return transaction_rows
