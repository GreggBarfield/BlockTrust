from json import dumps
from ..no_value import NoValue

NO_VALUE = NoValue()

PAYMENT_STATUS_NAMES_TO_IDS = {
    "Unpaid": 1,
    "Paid": 2
}

PAYMENT_STATUS_IDS_TO_NAMES = {value: key for key, value in PAYMENT_STATUS_NAMES_TO_IDS.items()}


class Payments:

    def __init__(self, db):
        self._db = db

    def insert(self, account_id=None, employee_id=None, amount=None, status=None, reason=None, description=None):
        """
        Inserts a new payment

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO payments (account_id, employee_id, amount, status, reason, description)
                VALUES (%(account_id)s, %(employee_id)s, %(amount)s, %(status)s, %(reason)s, %(description)s)
            """,
            {
                "account_id": account_id,
                "employee_id": employee_id,
                "amount": amount,
                "status": status,
                "reason": reason,
                "description": description
            }
        )
        return self._db.last_row_id()

    def get(self, id=NO_VALUE, status=NO_VALUE, expand=False, employee_id=NO_VALUE):
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

    def update(self, id, status=NO_VALUE, details=NO_VALUE, paid_date=NO_VALUE):
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
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Values for fields to update payment record not given")
        return self._db.row_count()
