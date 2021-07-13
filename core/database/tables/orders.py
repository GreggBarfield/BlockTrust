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

    def add_order(self, order):
        """
        Adds a new order to the orders table

        Params:
            order : An object which has all order details

        Returns:
            Order number assigned to current order
        """
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
                    (total_tax, total_shipping, total_cart, grand_total, shipping_address, shipping_city, shipping_state, shipping_country, shipping_zipcode, first_name, last_name)
                    VALUES
                        ( %(total_tax)s, %(total_shipping)s, %(total_cart)s, %(grand_total)s, %(shipping_address)s, %(shipping_city)s, %(shipping_state)s, %(shipping_country)s, %(shipping_zipcode)s, %(first_name)s, %(last_name)s)
            """,
            {
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
        return self._db.last_row_id()
