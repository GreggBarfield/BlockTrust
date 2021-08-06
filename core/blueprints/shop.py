from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)
from ..utilities.aws.aws import get_ses_client
from ..renderers.outside import outside_render
from ..common_exceptions import ExportException
from ..database.tables.product_discounts import ProductDiscountException
from ..utilities import shop
from ..utilities.email import send_email
from ..utilities.email_tag_store import send_tag_store_email
from ..renderers.email import render_email
from core.config import SUPPORT_GENERAL_EMAIL
from ..sectors import sectors_by_id, sectors_by_name


bp = Blueprint('shop_bp', __name__)

# Routes for shop homepage and cart iframes


@bp.route('/external/shop/<tok>', methods=['GET'])
def serve_partner_shop(tok):
    allProductData = shop.get_partner_products(tok)
    return outside_render('shop-iframe/shop-homepage.html', {"allProductData": allProductData, "partner_id": tok})


@bp.route('/external/shop', methods=['GET'])
def serve_external_shop():
    allProductData = shop.get_all_products()
    return outside_render('shop-iframe/shop-homepage.html', {"allProductData": allProductData})


@bp.route('/external/cart/<partner_id>', methods=['GET'])
def serve_external_cart(partner_id):
    return outside_render('shop-iframe/shopping-cart.html', {"partner_id": partner_id})


@bp.route('/external/cart', methods=['POST'])
def serve_apply_coupon():
    try:
        # Getting the discounts applcable for the coupon code supplied
        discounts = g.db.product_discounts.get_discounts(request.form['coupon_code'])
        # Creating a new object to store discount values
        discount_percentages = {}
        # Creating a browser friendly object to calculate discounts
        for product_discount in discounts:
            product_id = product_discount["product"]
            discount_percentage = product_discount["discount_percentage"]
            discount_percentages[product_id] = discount_percentage
        return jsonify({"discount_percentages": discount_percentages})
    except ProductDiscountException as e:
        return jsonify({"error": str(e)})


@bp.route('/external/checkout/<partner_id>', methods=['GET'])
def serve_external_checkout(partner_id):
    return outside_render('shop-iframe/checkout.html', {'partner_id': partner_id})


@bp.route('/external/checkout_payment/<partner_id>', methods=['GET'])
def serve_external_payment(partner_id):
    return outside_render('shop-iframe/checkout-payment.html', {'partner_id': partner_id})


@bp.route('/external/checkout_payment/<partner_id>', methods=['POST'])
def serve_external_paymentinfo(partner_id):
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
        """
        html = render_email("purchase_summary_customer.html", {
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
            })
        get_ses_client().send_email(
            Destination={
                'ToAddresses': [
                    order_details["email"],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': html,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': "Please use an email client that supports HTML email to view this email.",
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': "Tag Store Purchase Summary",
                },
            },
            Source="U.S. CattleTrace Purchase <info@uscattletrace.org>"
        )
        """
        send_tag_store_email(
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
            order_details["email"]
        )
        # Sending email to seller including order ID
        """
        send_tag_store_email(
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
            "cattletrace@fort-supply.com"
        )
        send_tag_store_email(
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
            "klangvardt@uscattletrace.org"
        )
        send_tag_store_email(
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
            "gregg.barfield@ledgerspace.net"
        )
        """
        return jsonify({"redirect": "/external/invoice/"+partner_id})
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/external/invoice/<partner_id>', methods=['GET'])
def serve_external_invoice(partner_id):
    return outside_render('shop-iframe/invoice.html', {'partner_id': partner_id})
