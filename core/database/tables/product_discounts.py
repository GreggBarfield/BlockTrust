class ProductDiscountException(Exception):
    """ProductDiscount generic exception."""

    def __init__(self, reason):
        """Constructor for ProductDiscountException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


class ProductDiscounts:

    def __init__(self, db):
        self._db = db

    def get_discounts(self, coupon_code):
        """
        Gets the product discounts for a specific coupon code

        Params:
            coupon_code: The coupon code provided

        Returns:
            discounts: Discounts for each product for the coupon code

        Raises:
            ProductDiscountException if coupon code not found

        """
        discounts = self._db.execute_d(
            """
                SELECT product_id, discount_percentage FROM product_discounts
                WHERE coupon_code=%(coupon_code)s
            """,
            {
                "coupon_code": coupon_code
            }
        )
        if len(discounts) < 1:
            raise ProductDiscountException("Coupon code invalid")
        return discounts
