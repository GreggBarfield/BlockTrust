from ..objects.order import Order
from .. import database


class Orders:

    def __init__(self, db: 'database.Database'):
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
            raise Exception("No order found with that ID.")
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

    def get_orders(self, account=None, shipping_address=None, shipping_city=None, shipping_state=None,
                   shipping_zipcode=None, first_name=None, last_name=None, email=None, phone=None,
                   discount=None, total_tax=None, total_shipping=None, total_cart=None, grand_total=None,
                   premise_id=None, selectColumns=[]):
        """
        Gets an order by the values specified

        Returns:
            The order records if found else and empty array
        """
        if len(selectColumns) > 0:
            selectColumns = ",".join(selectColumns)
        else:
            selectColumns = "*"

        # base query
        query = "SELECT " + selectColumns + " FROM orders "
        query_condition_list = []
        query_values = {}

        if account is not None:
            query_condition_list.append(" account = %(account)s ")
            query_values["account"] = account

        if shipping_address is not None:
            query_condition_list.append(" shipping_address = %(shipping_address)s ")
            query_values["shipping_address"] = shipping_address

        if shipping_city is not None:
            query_condition_list.append(" shipping_city = %(shipping_city)s ")
            query_values["shipping_city"] = shipping_city

        if shipping_state is not None:
            query_condition_list.append(" shipping_state = %(shipping_state)s ")
            query_values["shipping_state"] = shipping_state

        if shipping_zipcode is not None:
            query_condition_list.append(" shipping_zipcode = %(shipping_zipcode)s ")
            query_values["shipping_zipcode"] = shipping_zipcode

        if first_name is not None:
            query_condition_list.append(" first_name = %(first_name)s ")
            query_values["first_name"] = first_name

        if last_name is not None:
            query_condition_list.append(" last_name = %(last_name)s ")
            query_values["last_name"] = last_name

        if email is not None:
            query_condition_list.append(" email = %(email)s ")
            query_values["email"] = email

        if phone is not None:
            query_condition_list.append(" phone = %(phone)s ")
            query_values["phone"] = phone

        if discount is not None:
            query_condition_list.append(" discount = %(discount)s ")
            query_values["discount"] = discount

        if total_tax is not None:
            query_condition_list.append(" total_tax = %(total_tax)s ")
            query_values["total_tax"] = total_tax

        if total_shipping is not None:
            query_condition_list.append(" total_shipping = %(total_shipping)s ")
            query_values["total_shipping"] = total_shipping

        if total_cart is not None:
            query_condition_list.append(" total_cart = %(total_cart)s ")
            query_values["total_cart"] = total_cart

        if grand_total is not None:
            query_condition_list.append(" grand_total = %(grand_total)s ")
            query_values["grand_total"] = grand_total

        if premise_id is not None:
            query_condition_list.append(" premise_id = %(premise_id)s ")
            query_values["premise_id"] = premise_id

        if len(query_condition_list) >= 1:
            query_condition = " WHERE " + " AND ".join(query_condition_list)
        else:
            query_condition = ""

        query = query + query_condition

        order_rows = self._db.execute_d(query, query_values)
        if len(order_rows) > 0:
            return order_rows
        else:
            return []
