from .. import database
from ..objects.transaction import Transaction

transaction_type = {
    "Tag-Store": 0,
    "Subscription": 1
}
transaction_type_names = {
    0: "Tag-Store",
    1: "Subscription"
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

    def get_transactions(self, account=None, amount=None, type=None, selectColumns=[]):
        """
        Gets the transactions based on values specified

        Params:
            account: Account ID
            amount: Amount of transaction
            type: Type of transaction

        Returns:
            The transaction record if found, else an empty array
        """
        if len(selectColumns) > 0:
            selectColumns = ",".join(selectColumns)
        else:
            selectColumns = "*"

        # base query
        query = "SELECT " + selectColumns + " FROM transactions"
        query_condition_list = []
        query_values = {}

        if account is not None:
            query_condition_list.append("account = %(account)s")
            query_values["account"] = account

        if amount is not None:
            query_condition_list.append("amount = %(amount)s")
            query_values["amount"] = amount

        if type is not None:
            query_condition_list.append("type = %(type)s")
            query_values["type"] = type

        if len(query_condition_list) >= 1:
            query_condition = " WHERE" + " AND ".join(query_condition_list)
        else:
            query_condition = ""

        query = query + query_condition

        transaction_rows = self._db.execute_d(query, query_values)
        if len(transaction_rows) > 0:
            return transaction_rows
        else:
            return []
