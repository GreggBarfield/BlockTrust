from flask import g, session


def get_product_data(id):
    """
    Gets the product data from the product table
    Params:
        id: The prod_no of the product requested

    Returns:
        Object containing product data
    """
    return g.db.products.get_by_id(id)


def get_product_price(id):
    """
    Gets the price of the product
    Params:
        id: The prod_no of the requested product

    Returns:
        Price of the requested product
    """
    return g.db.products.get_price_by_id(id)


def get_transaction_data(id):
    """
    Gets the transaction records for a particular user
    Params:
        id: The user_id of the user whose transactions are required

    Raise:
        TransactionException if user is not found

    Returns:
        Array containing transaction objects for the praticular user
    """
    return g.db.orders.getOrdersByAccountNumber(id)


def get_all_products():
    """
    Gets all the products stored in the database
    Returns:
        Array containing object data
    """
    return g.db.products.get_all_products()


def get_partner_products(partner):
    """
    Gets products by a particular partner
    Returns:
        Arrays containing object data
    """
    return g.db.products.get_partner_products(partner)


def get_partner_discount(coupon_code):
    """
    Gets the discount for a particular partner based on coupon code
    Params:
        coupon_code: Coupon code entered by the user

    Returns:
        discount: Discount percentage to be applied to the cart
    """
    return g.db.partners.get_discount_percentage(coupon_code)
