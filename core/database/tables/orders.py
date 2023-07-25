from ..objects.order import Order
from ..no_value import NoValue

NO_VALUE = NoValue()

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
            raise Exception("No order found with that ID.")
        return Order(self._db, order_rows[0])

    def add_order(self, order, shipping_address_line, shipping_city, shipping_state, shipping_zip_code, account_id=None,
                  user_id=None):
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
        premise_id = order["premise_id"]
        self._db.execute(
            """
                INSERT INTO orders
                    (total_tax, discount, total_shipping, total_cart, grand_total, shipping_address, shipping_city,
                    shipping_state, shipping_zip, first_name, last_name, email, phone, premise_id, account_id, user_id)
                    VALUES
                    ( %(total_tax)s, %(discount)s, %(total_shipping)s, %(total_cart)s, %(grand_total)s,
                    %(shipping_address)s, %(shipping_city)s, %(shipping_state)s, %(shipping_zipcode)s,
                    %(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(premise_id)s, %(account_id)s, %(user_id)s
                    )
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
                "phone": phone,
                "premise_id": premise_id,
                "account_id": account_id,
                "user_id": user_id
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

    def get_orders(self, id=NO_VALUE, account_id=NO_VALUE, shipping_address=NO_VALUE, shipping_city=NO_VALUE,
                   shipping_state=NO_VALUE, shipping_zipcode=NO_VALUE, first_name=NO_VALUE, last_name=NO_VALUE,
                   email=NO_VALUE, phone=NO_VALUE, discount=NO_VALUE, total_tax=NO_VALUE, total_shipping=NO_VALUE,
                   total_cart=NO_VALUE, grand_total=NO_VALUE, premise_id=NO_VALUE, stripe_paid=NO_VALUE, user_id=NO_VALUE):
        """
        Gets an order by the values specified

        Returns:
            The order records if found else and empty array
        """

        # base query
        query = "SELECT * FROM orders "
        query_condition_list = []
        query_values = {}

        if id is not NO_VALUE:
            query_condition_list.append("id = %(id)s ")
            query_values["id"] = id

        if account_id is not NO_VALUE:
            query_condition_list.append("account_id = %(account_id)s ")
            query_values["account_id"] = account_id


        if user_id is not NO_VALUE:
            query_condition_list.append("user_id = %(user_id)s ")
            query_values["user_id"] = user_id

        if shipping_address is not NO_VALUE:
            query_condition_list.append("shipping_address = %(shipping_address)s ")
            query_values["shipping_address"] = shipping_address

        if shipping_city is not NO_VALUE:
            query_condition_list.append("shipping_city = %(shipping_city)s ")
            query_values["shipping_city"] = shipping_city

        if shipping_state is not NO_VALUE:
            query_condition_list.append("shipping_state = %(shipping_state)s ")
            query_values["shipping_state"] = shipping_state

        if shipping_zipcode is not NO_VALUE:
            query_condition_list.append("shipping_zipcode = %(shipping_zipcode)s ")
            query_values["shipping_zipcode"] = shipping_zipcode

        if first_name is not NO_VALUE:
            query_condition_list.append("first_name = %(first_name)s ")
            query_values["first_name"] = first_name

        if last_name is not NO_VALUE:
            query_condition_list.append("last_name = %(last_name)s ")
            query_values["last_name"] = last_name

        if email is not NO_VALUE:
            query_condition_list.append("email = %(email)s ")
            query_values["email"] = email

        if phone is not NO_VALUE:
            query_condition_list.append("phone = %(phone)s ")
            query_values["phone"] = phone

        if discount is not NO_VALUE:
            query_condition_list.append("discount = %(discount)s ")
            query_values["discount"] = discount

        if total_tax is not NO_VALUE:
            query_condition_list.append("total_tax = %(total_tax)s ")
            query_values["total_tax"] = total_tax

        if total_shipping is not NO_VALUE:
            query_condition_list.append("total_shipping = %(total_shipping)s ")
            query_values["total_shipping"] = total_shipping

        if total_cart is not NO_VALUE:
            query_condition_list.append("total_cart = %(total_cart)s ")
            query_values["total_cart"] = total_cart

        if grand_total is not NO_VALUE:
            query_condition_list.append("grand_total = %(grand_total)s ")
            query_values["grand_total"] = grand_total

        if premise_id is not NO_VALUE:
            query_condition_list.append("premise_id = %(premise_id)s ")
            query_values["premise_id"] = premise_id

        if stripe_paid is not NO_VALUE:
            query_condition_list.append("stripe_paid = %(stripe_paid)s ")
            query_values["stripe_paid"] = stripe_paid

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

    def update(self, id, account_id=NO_VALUE, shipping_address=NO_VALUE, shipping_city=NO_VALUE, shipping_state=NO_VALUE,
                   shipping_zipcode=NO_VALUE, first_name=NO_VALUE, last_name=NO_VALUE, email=NO_VALUE, phone=NO_VALUE,
                   discount=NO_VALUE, total_tax=NO_VALUE, total_shipping=NO_VALUE, total_cart=NO_VALUE, grand_total=NO_VALUE,
                   premise_id=NO_VALUE, stripe_paid=NO_VALUE, herdwhistle_sale_order_id=NO_VALUE, user_id=NO_VALUE):
        """
        Update orders based on attributes provided
        """
        base_query = "UPDATE orders"
        query_conditions = []
        query_values = {}
        query_values["id"] = id

        if account_id is not NO_VALUE:
            query_conditions.append("account_id = %(account_id)s ")
            query_values["account_id"] = account_id
        if user_id is not NO_VALUE:
            query_conditions.append("user_id = %(user_id)s ")
            query_values["user_id"] = user_id
        if shipping_address is not NO_VALUE:
            query_conditions.append("shipping_address = %(shipping_address)s ")
            query_values["shipping_address"] = shipping_address
        if shipping_city is not NO_VALUE:
            query_conditions.append("shipping_city = %(shipping_city)s ")
            query_values["shipping_city"] = shipping_city
        if shipping_state is not NO_VALUE:
            query_conditions.append("shipping_state = %(shipping_state)s ")
            query_values["shipping_state"] = shipping_state
        if shipping_zipcode is not NO_VALUE:
            query_conditions.append("shipping_zipcode = %(shipping_zipcode)s ")
            query_values["shipping_zipcode"] = shipping_zipcode
        if first_name is not NO_VALUE:
            query_conditions.append("first_name = %(first_name)s ")
            query_values["first_name"] = first_name
        if last_name is not NO_VALUE:
            query_conditions.append("last_name = %(last_name)s ")
            query_values["last_name"] = last_name
        if email is not NO_VALUE:
            query_conditions.append("email = %(email)s ")
            query_values["email"] = email
        if phone is not NO_VALUE:
            query_conditions.append("phone = %(phone)s ")
            query_values["phone"] = phone
        if discount is not NO_VALUE:
            query_conditions.append("discount = %(discount)s ")
            query_values["discount"] = discount
        if total_tax is not NO_VALUE:
            query_conditions.append("total_tax = %(total_tax)s ")
            query_values["total_tax"] = total_tax
        if total_shipping is not NO_VALUE:
            query_conditions.append("total_shipping = %(total_shipping)s ")
            query_values["total_shipping"] = total_shipping
        if total_cart is not NO_VALUE:
            query_conditions.append("total_cart = %(total_cart)s ")
            query_values["total_cart"] = total_cart
        if grand_total is not NO_VALUE:
            query_conditions.append("grand_total = %(grand_total)s ")
            query_values["grand_total"] = grand_total
        if premise_id is not NO_VALUE:
            query_conditions.append("premise_id = %(premise_id)s ")
            query_values["premise_id"] = premise_id
        if stripe_paid is not NO_VALUE:
            query_conditions.append("stripe_paid = %(stripe_paid)s ")
            query_values["stripe_paid"] = stripe_paid
        if herdwhistle_sale_order_id is not NO_VALUE:
            query_conditions.append("herdwhistle_sale_order_id = %(herdwhistle_sale_order_id)s ")
            query_values["herdwhistle_sale_order_id"] = herdwhistle_sale_order_id

        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Products")