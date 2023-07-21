from ..no_value import NoValue

NO_VALUE = NoValue()


class Tips:

    def __init__(self, db):
        self._db = db

    def insert_tip(self, to_account_id, amount, charged_amount=None, from_name=None, from_email=None, from_phone=None, stripe_payment_intent_id=None):
        """
        Inserts a new tip record

        Returns:
            id of row inserted
        """

        self._db.execute(
            """
                INSERT INTO tips (to_account_id, amount, charged_amount, from_name, from_email, from_phone, stripe_payment_intent_id)
                VALUES (%(to_account_id)s, %(amount)s, %(charged_amount)s, %(from_name)s, %(from_email)s, %(from_phone)s, %(stripe_payment_intent_id)s)
            """,
            {
                "to_account_id": to_account_id,
                "amount": amount,
                "charged_amount": charged_amount,
                "from_name": from_name,
                "from_email": from_email,
                "from_phone": from_phone,
                "stripe_payment_intent_id": stripe_payment_intent_id
            }
        )
        return self._db.last_row_id()

    def get_tips(self, id=NO_VALUE, stripe_payment_intent_id=NO_VALUE):
        """
        Get a tip by the values specified.

        Returns:
            A list of tip row(s) if found else []
        """
        base_query = "SELECT * FROM tips"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id

        if stripe_payment_intent_id is not NO_VALUE:
            query_conditions.append("stripe_payment_intent_id = %(stripe_payment_intent_id)s")
            query_values["stripe_payment_intent_id"] = stripe_payment_intent_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        tip_rows = self._db.execute_d(query, query_values)
        if len(tip_rows) > 0:
            return tip_rows
        else:
            return []

    def update_tip(self, id, stripe_payment_intent_id=NO_VALUE, is_stripe_payment_success=NO_VALUE, stripe_error=NO_VALUE):
        """
        Updates an account.

        Params:
            id: ID of the tip to update
            stripe_payment_intent_id: id internal to stripe
            is_stripe_payment_success: 1 if payment is successful else 0
            stripe_error: log any error message sent by stripe

        Returns:
            number of rows affected
        """

        base_query = "UPDATE tips "

        query_conditions = []
        query_values = {}
        query_values["id"] = id
        if stripe_payment_intent_id is not NO_VALUE:
            query_conditions.append("stripe_payment_intent_id = %(stripe_payment_intent_id)s")
            query_values["stripe_payment_intent_id"] = stripe_payment_intent_id
        if is_stripe_payment_success is not NO_VALUE:
            query_conditions.append("is_stripe_payment_success = %(is_stripe_payment_success)s")
            query_values["is_stripe_payment_success"] = is_stripe_payment_success
        if stripe_error is not NO_VALUE:
            query_conditions.append("stripe_error = %(stripe_error)s")
            query_values["stripe_error"] = stripe_error

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("No values given for update")

        return self._db.row_count()
