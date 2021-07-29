from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)

from ..renderers.outside import outside_render
from ..common_exceptions import ExportException
from ..database.tables.product_discounts import ProductDiscountException
from ..utilities import shop
from ..utilities.email import send_email
from ..renderers.email import render_email
from core.config import SUPPORT_GENERAL_EMAIL
from ..sectors import sectors_by_id, sectors_by_name


bp = Blueprint('shop_bp', __name__)

# Routes for shop homepage and cart iframes


@bp.route('/external/shop/<tok>', methods=['GET'])
def serve_partner_shop(tok):
    allProductData = shop.get_partner_products(tok)
    return outside_render('shop-iframe/shop-homepage.html', {"allProductData": allProductData})


@bp.route('/external/shop', methods=['GET'])
def serve_external_shop():
    allProductData = shop.get_all_products()
    return outside_render('shop-iframe/shop-homepage.html', {"allProductData": allProductData})


@bp.route('/external/cart', methods=['GET'])
def serve_external_cart():
    return outside_render('shop-iframe/shopping-cart.html')


@bp.route('/external/cart', methods=['POST'])
def serve_apply_coupon():
    try:
        # Getting the discounts applcable for the coupon code supplied
        discounts = g.db.product_discounts.get_discounts(request.form['coupon_code'])
        # Creating a new object to store discount values
        discount_percentages = {}
        # Creating a browser friendly object to calculate discounts
        for product_discount in discounts:
            product_id = product_discount["product_id"]
            discount_percentage = product_discount["discount_percentage"]
            discount_percentages[product_id] = discount_percentage
        return jsonify({"discount_percentages": discount_percentages})
    except ProductDiscountException as e:
        return jsonify({"error": str(e)})


@bp.route('/external/checkout', methods=['GET'])
def serve_external_checkout():
    return outside_render('shop-iframe/checkout.html')


@bp.route('/external/checkout_payment', methods=['GET'])
def serve_external_payment():
    return outside_render('shop-iframe/checkout-payment.html')


@bp.route('/external/checkout_payment', methods=['POST'])
def serve_external_paymentinfo():
    try:
        # We need to implement stripe payment function here
        # Cart and user information is stored in request.form
        # If billing address is same as shipping address then request.form["address_checkbox"]=="on"

        # Updating the orders table if payment goes through
        # Getting order details and shipping address from form
        order_details = eval(request.form["order_details"])
        shipping_address_line = request.form['shipping_address_line']
        shipping_city = request.form['shipping_city']
        shipping_state = request.form['shipping_state']
        shipping_zip_code = request.form['shipping_zip_code']
        # Adding order to orders table and getting current order id from orders table
        order_id = g.db.orders.add_order(order_details, shipping_address_line, shipping_city, shipping_state, shipping_zip_code)
        # Getting the cart details
        cart = eval(order_details['shoppingCart'])
        # Adding product data and quantities to the OrderProducts table
        for key, value in cart.items():
            g.db.order_products.add_order_product(order_id, key, value["quantity"])

        # Once payment goes through sending email to confirm order to buyer and seller

        send_email(
            "Tag Store Purchase Summary",
            render_email("purchase_summary_customer.html", {
                'first': order_details["first_name"],
                'last': order_details["last_name"],
                'total_price': order_details["total_price"],
                'total_tax': order_details["total_tax"],
                'discount': order_details["discount"],
                'shipping': order_details["shipping"],
                'grand_total': order_details["grand_total"],
                'shipping_address_line': shipping_address_line,
                'shipping_city': shipping_city,
                'shipping_state': shipping_state,
                'shipping_zip_code': shipping_zip_code,
                'cart': cart
            }),
            # tags@blocktrustnetwork.com
            "nisheet.thakur@blocktrustnetwork.com",
            override=True
        )
        # Sending email to seller including order ID
        """
        send_email(
            "New order summary",
            render_email("purchase_summary_seller.html", {
                'order_id': order_id,
                'first': order_details["first_name"],
                'last': order_details["last_name"],
                'total_price': order_details["total_price"],
                'total_tax': order_details["total_tax"],
                'discount': order_details["discount"],
                'shipping': order_details["shipping"],
                'grand_total': order_details["grand_total"],
                'shipping_address_line': shipping_address_line,
                'shipping_city': shipping_city,
                'shipping_state': shipping_state,
                'shipping_zip_code': shipping_zip_code,
                'cart': cart
            }),
            # cattletrace@fort-supply.com
            "nisheet.thakur@blocktrustnetwork.com"
        )
        """
        return jsonify({"redirect": "/external/invoice"})
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/external/invoice', methods=['GET'])
def serve_external_invoice():
    return outside_render('shop-iframe/invoice.html')


@bp.route('/external/testshop', methods=['GET'])
def serve_email():
    testdata = {
        'order_id': 1,
        'first': "Nisheet",
        'last': "Thakur",
        'total_price': 10,
        'total_tax': 10,
        'discount': 3,
        'shipping': 15,
        'grand_total': 10,
        'shipping_address_line': "XYZ",
        'shipping_city': "ABC",
        'shipping_state': "NJ",
        'shipping_zip_code': "07306",
        'cart': {"1": {"prod_no": "7", "price": 44, "product_name": "Strip Tag", "quantity": 5}, "2": {"prod_no": "8", "price": 44, "product_name": "Large Panel Tag", "quantity": 5}}
    }
    return outside_render('testemail/purchase_summary_customer.html', testdata)
