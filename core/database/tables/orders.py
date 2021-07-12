class TransactionException(Exception):
    """Generic Transaction exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for TransactionException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class Orders:

    def __init__(self, db):
        self._db = db

    def get_order_ID(self, transaction_id):
        """
        Gets the id of a transaction.

        Params:
            transaction_id: Unique transaction id

        Returns:
            Order ID corresponding to transaction id
        """
        match = self._db.execute_d(
            """
                SELECT id FROM orders
                WHERE
                    transaction_id=%(transaction_id)s
            """,
            {
                "transaction_id": transaction_id
            }
        )
        return match[0]["id"]

    def add_order(self, order):
        """
        Adds a new order to the orders table

        Params:
            order : An object which has all order details
        """
        transaction_id = order['transaction_id']
        total_tax = order["total_tax"]
        total_shipping = order["shipping"]
        total_cart = order["total_price"]
        grand_total = order["grand_total"]
        shipping_address = order["address_line"]
        shipping_city = order["city"]
        shipping_state = order["state"]
        shipping_country = order["country"]
        shipping_zipcode = order["zip_code"]
        first_name = order["first_name"]
        last_name = order["last_name"]
        self._db.execute(
            """
                INSERT INTO orders
                    (transaction_id, total_tax, total_shipping, total_cart, grand_total, shipping_address, shipping_city, shipping_state, shipping_country, shipping_zipcode, first_name, last_name)
                    VALUES
                        (%(transaction_id)s, %(total_tax)s, %(total_shipping)s, %(total_cart)s, %(grand_total)s, %(shipping_address)s, %(shipping_city)s, %(shipping_state)s, %(shipping_country)s, %(shipping_zipcode)s, %(first_name)s, %(last_name)s)
            """,
            {
                "transaction_id": transaction_id,
                "total_tax": total_tax,
                "total_shipping": total_shipping,
                "total_cart": total_cart,
                "grand_total": grand_total,
                "shipping_address": shipping_address,
                "shipping_city": shipping_city,
                "shipping_state": shipping_state,
                "shipping_country": shipping_country,
                "shipping_zipcode": shipping_zipcode,
                "first_name": first_name,
                "last_name": last_name,
            }
        )
