
class OrderProducts:

    def __init__(self, db):
        self._db = db

    def add_order_product(self, order_id, product_id, product_quantity):
        """
        Adds product entry to database

        Params:
            order_id: Order ID
            product_id: ID of the product
            product_quantity: Quantity of specified product

        Returns:
            None
        """
        self._db.execute(
            """
            INSERT INTO order_products
                (`order_id`, product_id, product_quantity)
            VALUES
                (%(order_id)s,%(product_id)s,%(product_quantity)s)
            """,
            {
                "order_id": order_id,
                "product_id": product_id,
                "product_quantity": product_quantity
            }
        )

    def get_order_products(self, order_id):
        """
        Gets the producst associated with a particular order

        Params:
            order_id: Order id

        Returns:
            matching_orders: Array with order product details
        """
        matching_orders = self._db.execute_d(
            """
                SELECT * FROM order_products
                WHERE order_id=%(order_id)s
            """,
            {
                "order_id": order_id
            }
        )

        return matching_orders
