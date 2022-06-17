from ..no_value import NoValue

NO_VALUE = NoValue()

offer_status_by_name = {
    "Pending": 0,
    "Accepted": 1,
    "Declined": 2
}
offer_status_by_id = {
    value: key
    for key, value in offer_status_by_name.items()
}


class SalesGroupOffers:

    def __init__(self, db):
        self._db = db

    def get_sales_group_offers(self, id=NO_VALUE, sales_group_id=NO_VALUE, offering_account_id=NO_VALUE,
                               offer_amount=NO_VALUE, offer_status=NO_VALUE):
        """
        Gets the Sales group offers based on provided attributes

        Params:
            id: ID of the sales group offer
            sales_group_id: Sales group ID for an offer
            offering_account_id: Account ID of account making the offer
            offer_amount: Amount being offered for the sales group
            offer_status: Offer status(Pending, Accepted, Declined)

        Returns:
            A list of sales group offers or an empty list
        """
        base_query = "SELECT * FROM sales_group_offers"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if sales_group_id is not NO_VALUE:
            query_conditions.append(" sales_group_id = %(sales_group_id)s")
            query_values["sales_group_id"] = sales_group_id
        if offering_account_id is not NO_VALUE:
            query_conditions.append(" offering_account_id = %(offering_account_id)s")
            query_values["offering_account_id"] = offering_account_id
        if offer_amount is not NO_VALUE:
            query_conditions.append(" offer_amount = %(offer_amount)s")
            query_values["offer_amount"] = offer_amount
        if offer_status is not NO_VALUE:
            query_conditions.append(" offer_status = %(offer_status)s")
            query_values["offer_status"] = offer_status

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        sales_group_offers_rows = self._db.execute_d(query, query_values)
        if len(sales_group_offers_rows) > 0:
            return sales_group_offers_rows
        else:
            return []

    def insert_sales_group_offer(self, sales_group_id=NO_VALUE, offering_account_id=NO_VALUE, offer_amount=NO_VALUE,
                                 offer_status=NO_VALUE):
        """
        Inserts a Sales group offer

        Params:
            sales_group_id: Sales group ID for an offer
            offering_account_id: Account ID of account making the offer
            offer_amount: Amount being offered for the sales group
            offer_status: Offer status(Pending, Accepted, Declined)
        """
        self._db.execute(
            """
            INSERT INTO sales_group_offers (sales_group_id, offering_account_id, offer_amount, offer_status)
            VALUES (%(sales_group_id)s, %(offering_account_id)s, %(offer_amount)s, %(offer_status)s)
            """,
            {
                "sales_group_id": sales_group_id,
                "offering_account_id": offering_account_id,
                "offer_amount": offer_amount,
                "offer_status": offer_status
            }
        )

    def update_sales_group_offer(self, sales_group_offer_id, sales_group_id=NO_VALUE, offering_account_id=NO_VALUE,
                                 offer_amount=NO_VALUE, offer_status=NO_VALUE):
        """
        Gets the Sales group offers based on provided attributes

        Params:
            id: ID of the sales group offer
            sales_group_id: Sales group ID for an offer
            offering_account_id: Account ID of account making the offer
            offer_amount: Amount being offered for the sales group
            offer_status: Offer status(Pending, Accepted, Declined)

        Returns:
            A list of sales group offers or an empty list
        """
        base_query = "UPDATE sales_group_offers"

        query_conditions = []
        query_values = {}
        query_values["id"] = sales_group_offer_id
        if sales_group_id is not NO_VALUE:
            query_conditions.append(" sales_group_id = %(sales_group_id)s")
            query_values["sales_group_id"] = sales_group_id
        if offering_account_id is not NO_VALUE:
            query_conditions.append(" offering_account_id = %(offering_account_id)s")
            query_values["offering_account_id"] = offering_account_id
        if offer_amount is not NO_VALUE:
            query_conditions.append(" offer_amount = %(offer_amount)s")
            query_values["offer_amount"] = offer_amount
        if offer_status is not NO_VALUE:
            query_conditions.append(" offer_status = %(offer_status)s")
            query_values["offer_status"] = offer_status
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Sales group offers")

    def accept_sales_group_offer(self, sales_group_id, accepted_sales_group_offer_id):
        """
        Accept a sales group offer and decline existing offers automatically

        Params:
            sales_group_id: ID of sales group offer
            offering_account_id: Account ID of accepted sales group offer
        """
        self._db.execute(
            """
            UPDATE sales_group_offers
            SET offer_status = %(offer_status)s
            WHERE sales_group_id = %(sales_group_id)s AND id != %(id)s
            """, {
                "offer_status": offer_status_by_name["Declined"],
                "sales_group_id": sales_group_id,
                "id": accepted_sales_group_offer_id
            }
        )
        self._db.execute(
            """
            UPDATE sales_group_offers
            SET offer_status = %(offer_status)s
            WHERE id = %(id)s
            """, {
                "offer_status": offer_status_by_name["Accepted"],
                "id": accepted_sales_group_offer_id
            }
        )