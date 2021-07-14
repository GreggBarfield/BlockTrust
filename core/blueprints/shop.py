from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)

from ..renderers.outside import outside_render
from ..common_exceptions import ExportException
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


@bp.route('/external/checkout', methods=['GET'])
def serve_external_checkout():
    return outside_render('shop-iframe/checkout.html')

@bp.route('/external/checkout_payment', methods=['GET'])
def serve_external_payment():
    return outside_render('shop-iframe/checkout-payment.html')


@bp.route('/external/checkout_payment', methods=['POST'])
def serve_external_paymentinfo():
    try:
        # print(request.form)
        # We need to implement stripe payment function here
        # Cart and user information is stored in session[SESSION_CHECKOUT_INFO]
        # If billing address is same as shipping address then request.form["address_checkbox"]=="on"

        # Updating the orders table if payment goes through
        order_details = eval(request.form["order_details"])
        print(order_details)
        # Adding order to orders table and getting current order id from orders table
        order_id = g.db.orders.add_order(order_details)
        # Getting the cart details
        cart = eval(order_details['shoppingCart'])
        # Adding product data and quantities to the OrderProducts table
        for key, value in cart.items():
            g.db.order_products.add_order_product(order_id, key, value["quantity"])

        # Once payment goes through sending email to confirm order to buyer and seller
        """
        send_email(
            "Tag Store Purchase Summary",
            render_email("purchase_summary.html", {
                'first': order['first_name'],
                'last': order['last_name'],
                'grand_total': order['grand_total'],
                'cart': cart
            }),
            "nisheet.thakur@blocktrustnetwork.com"
        )
        """
        return jsonify({"redirect": "/external/invoice"})
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/external/invoice', methods=['GET'])
def serve_external_invoice():
    return outside_render('shop-iframe/invoice.html')
