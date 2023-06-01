from ..no_value import NoValue

NO_VALUE = NoValue()

TRANSACTION_TYPE_NAMES_TO_IDS = {
    "Subscription Credits": 1
}

TRANSACTION_TYPE_IDS_TO_NAMES = {value: key for key, value in TRANSACTION_TYPE_NAMES_TO_IDS.items()}


class Transactions:

    def __init__(self, db):
        self._db = db

    def insert_transaction(self, transaction_type_id, partner_id, subscription_credits):
        """
        Inserts a new transaction record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO transactions (transaction_type_id, partner_id, subscription_credits)
                VALUES (%(transaction_type_id)s, %(partner_id)s, %(subscription_credits)s)
            """,
            {
                "transaction_type_id": transaction_type_id,
                "partner_id": partner_id,
                "subscription_credits": subscription_credits
            }
        )
        return self._db.last_row_id()
