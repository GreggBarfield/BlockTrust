from json import dumps
from ..no_value import NoValue

NO_VALUE = NoValue()

RECURRING_STATUS_NAMES_TO_IDS = {
    "unpaid": 0,
    "active": 1,
    "incomplete": 2,
    "incomplete_expired": 3,
    "trialing": 4,
    "past_due": 5,
    "canceled": 6
}

RECURRING_STATUS_IDS_TO_NAMES = {
    value: ' '.join(key.split('_')).capitalize() for key, value in RECURRING_STATUS_NAMES_TO_IDS.items()
}


class RecurringPayments:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id, employee_id=None, recurring_interval=None, amount=None, status=None, reason=None, description=None):
        """
        Inserts a new recurring payment

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO recurring_payments (account_id, employee_id, recurring_interval, amount, status, reason, description)
                VALUES (%(account_id)s, %(employee_id)s, %(recurring_interval)s, %(amount)s, %(status)s, %(reason)s, %(description)s)
            """,
            {
                "account_id": account_id,
                "employee_id": employee_id,
                "recurring_interval": recurring_interval,
                "amount": amount,
                "status": status,
                "reason": reason,
                "description": description
            }
        )
        return self._db.last_row_id()

    def get(self, id=NO_VALUE, status=NO_VALUE, expand=False, employee_id=NO_VALUE, stripe_customer_id=NO_VALUE,
            stripe_subscription_id=NO_VALUE):
        """
        Gets the recurring payments based on the provided parameters

        Returns:
            A list of recurring payments or an empty array
        """
        if not expand:
            base_query = "SELECT * FROM recurring_payments rp"
        else:
            base_query = """
                SELECT rp.*, a.company as account_company FROM recurring_payments rp
                LEFT JOIN accounts a ON a.id = rp.account_id
            """

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("rp.id = %(id)s")
            query_values["id"] = id
        if status is not NO_VALUE:
            query_conditions.append("status = %(status)s")
            query_values["status"] = status
        if employee_id is not NO_VALUE:
            query_conditions.append("employee_id = %(employee_id)s")
            query_values["employee_id"] = employee_id
        if stripe_customer_id is not NO_VALUE:
            query_conditions.append("stripe_customer_id = %(stripe_customer_id)s")
            query_values["stripe_customer_id"] = stripe_customer_id
        if stripe_subscription_id is not NO_VALUE:
            query_conditions.append("stripe_subscription_id = %(stripe_subscription_id)s")
            query_values["stripe_subscription_id"] = stripe_subscription_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""
        query = base_query + combined_query_condition + " ORDER BY ID DESC"
        rows = self._db.execute_d(query, query_values)

        if len(rows) > 0:
            return rows
        else:
            return []

    def update(self, id, status=NO_VALUE, details=NO_VALUE, start_date=NO_VALUE, end_date=NO_VALUE,
               stripe_checkout_id=NO_VALUE, stripe_customer_id=NO_VALUE, stripe_subscription_id=NO_VALUE,
               email=NO_VALUE):
        """
        Updates a recurring payment.
        """
        base_query = "UPDATE recurring_payments"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if status is not NO_VALUE:
            query_conditions.append("status = %(status)s")
            query_values["status"] = status
        if details is not NO_VALUE:
            query_conditions.append("details = %(details)s")
            query_values["details"] = dumps(details) if details else None
        if start_date is not NO_VALUE:
            query_conditions.append("start_date = %(start_date)s")
            query_values["start_date"] = start_date
        if end_date is not NO_VALUE:
            query_conditions.append("end_date = %(end_date)s")
            query_values["end_date"] = end_date
        if stripe_checkout_id is not NO_VALUE:
            query_conditions.append("stripe_checkout_id = %(stripe_checkout_id)s")
            query_values["stripe_checkout_id"] = stripe_checkout_id
        if stripe_customer_id is not NO_VALUE:
            query_conditions.append("stripe_customer_id = %(stripe_customer_id)s")
            query_values["stripe_customer_id"] = stripe_customer_id
        if stripe_subscription_id is not NO_VALUE:
            query_conditions.append("stripe_subscription_id = %(stripe_subscription_id)s")
            query_values["stripe_subscription_id"] = stripe_subscription_id
        if email is not NO_VALUE:
            query_conditions.append("email = %(email)s")
            query_values["email"] = email
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Values for fields to update recurring payment record not given")
        return self._db.row_count()
