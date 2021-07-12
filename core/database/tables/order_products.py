
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
        return 1
