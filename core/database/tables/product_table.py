from ..objects.product_table import ProductTable


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

    def get_by_id(self, prod_no):
        """Gets a product by their ID.

        Params:
            prod_no: Product's ID number

        Returns:
            A Product object on success, or None on no match.
        """
        matching_products = self._db.execute_d(
            """
                SELECT * FROM product_table
                WHERE
                    prod_no=%(prod_no)s
            """,
            {
                "prod_no": prod_no
            }
        )

        if len(matching_products) != 1:
            raise ProductTableException()
        return matching_products[0]

    def get_price_by_id(self, prod_no):
        """Gets a product price by their ID.

        Params:
            prod_no: Product's ID number

        Returns:
            Product price on success, or None on no match.
        """
        matching_products = self._db.execute_d(
            """
                SELECT * FROM product_table
                WHERE
                    prod_no=%(prod_no)s
            """,
            {
                "prod_no": prod_no
            }
        )

        if len(matching_products) != 1:
            raise ProductTableException()
        return matching_products[0]['price']
