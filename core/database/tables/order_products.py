
class OrderProducts:

    def __init__(self, db):
        self._db = db

    def add_order_product(self, order_no, product_name, product_quantity):
        """
        Adds product entry to database

        Params:
            order_no: Order ID
            product_name: Name of the product
            product_quantity: Quantity of specified product

        Returns:
            None
        """
        self._db.execute(
            """
            INSERT INTO orderproducts
                (order_no, product_name, product_quantity)
            VALUES
                (%(order_no)s,%(product_name)s,%(product_quantity)s)
            """,
            {
                "order_no": order_no,
                "product_name": product_name,
                "product_quantity": product_quantity
            }
        )

    def get_order(self, order_no):
        """
        Gets the producst associated with a particular order number

        Params:
            order_no: Order number

        Returns:
            matching_orders: Array with order produc details
        """
        matching_orders = self._db.execute_d(
            """
                SELECT * FROM orderproducts
                WHERE
                    order_no=%(order_no)s
            """,
            {
                "order_no": order_no
            }
        )

        if len(matching_orders) != 1:
            return {}
        return matching_orders
