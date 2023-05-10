from ..no_value import NoValue

NO_VALUE = NoValue()

# TABLE_COLUMNS = ("id", "owner_account_id", "viewer_account_id", "viewer_user_id", "data_type_id",
#                  "created_timestamp", "last_updated_timestamp")

TRANSACTION_TYPE_NAMES_TO_IDS = {
    "Subscription": 1
}

TRANSACTION_TYPE_IDS_TO_NAMES = {value: key for key, value in TRANSACTION_TYPE_NAMES_TO_IDS.items()}


class Transactions:

    def __init__(self, db):
        self._db = db

    def insert_transaction(self, transaction_type_id, purchasing_account_id, account_credits_purchased):
        """
        Inserts a new transaction record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO transactions (transaction_type_id, purchasing_account_id, account_credits_purchased)
                VALUES (%(transaction_type_id)s, %(purchasing_account_id)s, %(account_credits_purchased)s)
            """,
            {
                "transaction_type_id": transaction_type_id,
                "purchasing_account_id": purchasing_account_id,
                "account_credits_purchased": account_credits_purchased
            }
        )
        return self._db.last_row_id()
