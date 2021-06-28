from ..objects.product import Product


class ProductTableException(Exception):
    """Generic Product exception."""

    def __init__(self, reason="unspecified"):
        """Constructor for ProductException.

        Params:
            reason: The reason it failed.
        """
        super().__init__(reason)


class NoProductFoundException(ProductTableException):
    """Product was not found."""
    pass


class ProductTable:

    def __init__(self, db):
        self._db = db

    def get_all_products(self):
        """
        Gets all products

        Returns:
            A product array on success
        """
        all_products = self._db.execute_d(
            """
            SELECT * FROM products
            """
        )
        return all_products

    def get_by_id(self, product_no):
        """Gets a product by their ID.

        Params:
            product_no: Product's ID number

        Returns:
            A Product object on success, or None on no match.
        """
        matching_products = self._db.execute_d(
            """
                SELECT * FROM products
                WHERE
                    product_no=%(product_no)s
            """,
            {
                "product_no": product_no
            }
        )

        if len(matching_products) != 1:
            return {}
        return matching_products[0]

    def get_price_by_id(self, product_no):
        """Gets a product price by their ID.

        Params:
            product_no: Product's ID number

        Returns:
            Product price on success, or None on no match.
        """
        matching_products = self._db.execute_d(
            """
                SELECT * FROM products
                WHERE
                    product_no=%(product_no)s
            """,
            {
                "product_no": product_no
            }
        )

        if len(matching_products) != 1:
            raise ProductTableException()
        return matching_products[0]['price']
