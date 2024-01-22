from ..no_value import NoValue

NO_VALUE = NoValue()

TRANSACTION_TYPE_NAMES_TO_IDS = {
    "Subscription Credits": 1
}

TRANSACTION_TYPE_IDS_TO_NAMES = {value: key for key, value in TRANSACTION_TYPE_NAMES_TO_IDS.items()}


class Transactions:

    def __init__(self, db):
        self._db = db

    def insert(self, transaction_type_id, partner_id, account_id=None,
                           subscription_credits=None, employee_id=None):
        """
        Inserts a new transaction record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO transactions (transaction_type_id, partner_id, account_id,  subscription_credits, 
                employee_id)
                VALUES (%(transaction_type_id)s, %(partner_id)s, %(account_id)s, %(subscription_credits)s, 
                %(employee_id)s)
            """,
            {
                "transaction_type_id": transaction_type_id,
                "partner_id": partner_id,
                "account_id": account_id,
                "subscription_credits": subscription_credits,
                "employee_id": employee_id
            }
        )
        return self._db.last_row_id()
