from json import dumps
from ..no_value import NoValue

NO_VALUE = NoValue()

PAYMENT_STATUS_NAMES_TO_IDS = {
    "unpaid": 0,
    "paid": 1
}

PAYMENT_STATUS_IDS_TO_NAMES = {value: key for key, value in PAYMENT_STATUS_NAMES_TO_IDS.items()}


class Payments:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id=None, employee_id=None, amount=None, status=None, reason=None, description=None,
               recurring_payment_id=None, paid_date=None, email=None, stripe_customer_id=None, details=None,
               stripe_invoice_id=None):
        """
        Inserts a new payment

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO payments (account_id, employee_id, amount, status, reason, description,
                    recurring_payment_id, paid_date, email, stripe_customer_id, details,
                    stripe_invoice_id)
                VALUES (%(account_id)s, %(employee_id)s, %(amount)s, %(status)s, %(reason)s, %(description)s,
                    %(recurring_payment_id)s, %(paid_date)s, %(email)s, %(stripe_customer_id)s, %(details)s,
                    %(stripe_invoice_id)s)
            """,
            {
                "account_id": account_id,
                "employee_id": employee_id,
                "amount": amount,
                "status": status,
                "reason": reason,
                "description": description,
                "recurring_payment_id": recurring_payment_id,
                "paid_date": paid_date,
                "email": email,
                "stripe_customer_id": stripe_customer_id,
                "details": dumps(details) if details else None,
                "stripe_invoice_id": stripe_invoice_id
            }
        )
        return self._db.last_row_id()

    def get(self, id=NO_VALUE, status=NO_VALUE, expand=False, employee_id=NO_VALUE, recurring_payment_id=NO_VALUE,
            stripe_invoice_id=NO_VALUE):
        """
        Gets the payments based on the provided parameters

        Returns:
            A list of payments or an empty array
        """
        if not expand:
            base_query = "SELECT * FROM payments p"
        else:
            base_query = """
                SELECT p.*, a.company as account_company FROM payments p
                LEFT JOIN accounts a ON a.id = p.account_id
            """

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append("p.id = %(id)s")
            query_values["id"] = id
        if status is not NO_VALUE:
            query_conditions.append("status = %(status)s")
            query_values["status"] = status
        if employee_id is not NO_VALUE:
            query_conditions.append("employee_id = %(employee_id)s")
            query_values["employee_id"] = employee_id
        if stripe_invoice_id is not NO_VALUE:
            query_conditions.append("stripe_invoice_id = %(stripe_invoice_id)s")
            query_values["stripe_invoice_id"] = stripe_invoice_id
        if recurring_payment_id is not NO_VALUE:
            query_conditions.append(
                "recurring_payment_id = %(recurring_payment_id)s" if recurring_payment_id
                else "recurring_payment_id IS %(recurring_payment_id)s"
            )
            query_values["recurring_payment_id"] = recurring_payment_id

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

    def update(self, id, status=NO_VALUE, details=NO_VALUE, paid_date=NO_VALUE,
               stripe_checkout_id=NO_VALUE, stripe_customer_id=NO_VALUE, email=NO_VALUE):
        """
        Updates a transaction.
        """
        base_query = "UPDATE payments"

        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if status is not NO_VALUE:
            query_conditions.append("status = %(status)s")
            query_values["status"] = status
        if details is not NO_VALUE:
            query_conditions.append("details = %(details)s")
            query_values["details"] = dumps(details) if details else None
        if paid_date is not NO_VALUE:
            query_conditions.append("paid_date = %(paid_date)s")
            query_values["paid_date"] = paid_date
        if stripe_checkout_id is not NO_VALUE:
            query_conditions.append("stripe_checkout_id = %(stripe_checkout_id)s")
            query_values["stripe_checkout_id"] = stripe_checkout_id
        if stripe_customer_id is not NO_VALUE:
            query_conditions.append("stripe_customer_id = %(stripe_customer_id)s")
            query_values["stripe_customer_id"] = stripe_customer_id
        if email is not NO_VALUE:
            query_conditions.append("email = %(email)s")
            query_values["email"] = email
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Values for fields to update payment record not given")
        return self._db.row_count()
