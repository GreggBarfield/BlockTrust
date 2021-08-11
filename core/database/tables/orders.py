from ..objects.order import Order

class Orders:

    def __init__(self, db):
        self._db = db

    def get_by_id(self, id):
        """Gets an order by an ID.

        Params:
            id: the order id
        
        Returns:
            An Order() object

        Raises:
            OrderException on ID not found
        """
        order_rows = self._db.execute_d(
            """SELECT * FROM orders
                WHERE id=%(id)s
            """,
            {
                "id": id
            }
        )
        if len(order_rows) != 1:
            raise Exception("No account found with that ID.")
        return Order(self._db, order_rows[0])

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
                    (total_tax, discount, total_shipping, total_cart, grand_total, shipping_address, shipping_city, shipping_state, shipping_zip, first_name, last_name, email, phone)
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

    def update_order_as_stripe_paid(self, id, payment_intent):
        """Updates an order with the payment intent from stripe.

        Params:
            id: The ID of the order 
            payment_intent: id of the payment intent object from stripe
        """
        self._db.execute("""
            UPDATE orders
                SET stripe_payment_intent=%(payment_intent)s,
                stripe_paid = 1
                WHERE id=%(id)s
            """,
            {
                "payment_intent": payment_intent,
                "id": id
            }
        )