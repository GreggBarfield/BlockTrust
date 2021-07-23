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

    def add_order(self, order, shipping_address_line, shipping_city, shipping_state, shipping_zip_code):
        """
        Adds a new order to the orders table

        Params:
            order : An object which has all order details

        Returns:
            Order number assigned to current order
        """
        total_tax = order["total_tax"]
        discount = order["discount"]
        total_shipping = order["shipping"]
        total_cart = order["total_price"]
        grand_total = order["grand_total"]
        shipping_address = shipping_address_line
        shipping_city = shipping_city
        shipping_state = shipping_state
        shipping_zipcode = shipping_zip_code
        first_name = order["first_name"]
        last_name = order["last_name"]
        email = order["email"]
        phone = order["phone"]
        self._db.execute(
            """
                INSERT INTO orders
                    (total_tax, discount, total_shipping, total_cart, grand_total, shipping_address, shipping_city, shipping_state, shipping_zipcode, first_name, last_name, email, phone)
                    VALUES
                        ( %(total_tax)s, %(discount)s, %(total_shipping)s, %(total_cart)s, %(grand_total)s, %(shipping_address)s, %(shipping_city)s, %(shipping_state)s, %(shipping_zipcode)s, %(first_name)s, %(last_name)s, %(email)s, %(phone)s)
            """,
            {
                "total_tax": total_tax,
                "discount": discount,
                "total_shipping": total_shipping,
                "total_cart": total_cart,
                "grand_total": grand_total,
                "shipping_address": shipping_address,
                "shipping_city": shipping_city,
                "shipping_state": shipping_state,
                "shipping_zipcode": shipping_zipcode,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone
            }
        )
        return self._db.last_row_id()
