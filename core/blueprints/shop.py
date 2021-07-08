from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)

from ..renderers.outside import outside_render
from ..database.tables.users import UsersException
from ..database.tables.accounts import AccountsException
from ..common_exceptions import ExportException
from ..utilities import auth
from ..utilities.email import send_email
from ..utilities import token
from ..renderers.email import render_email
from core.config import SUPPORT_GENERAL_EMAIL
from ..sectors import sectors_by_id, sectors_by_name


bp = Blueprint('shop_bp', __name__)
SESSION_CHECKOUT_INFO = "session_checkout_info"

# Routes for shop homepage and cart iframes


@bp.route('/external/shop/<tok>', methods=['GET'])
def serve_partner_shop(tok):
    allProductData = auth.get_partner_products(tok)
    return outside_render('shop_iframe/shop_homepage.html', {"allProductData": allProductData})


@bp.route('/external/shop', methods=['GET'])
def serve_external_shop():
    allProductData = auth.get_all_products()
    return outside_render('shop_iframe/shop_homepage.html', {"allProductData": allProductData})


@bp.route('/external/cart', methods=['GET'])
def serve_external_cart():
    return outside_render('shop_iframe/shopping_cart.html')


@bp.route('/external/checkout', methods=['GET'])
def serve_external_checkout():
    return outside_render('shop_iframe/checkout.html')


@bp.route('/external/checkout', methods=['POST'])
def serve_external_checkoutinfo():
    try:
        print(request.form)
        order = {
            'first_name': None, 'last_name': None, 'email': None, 'tel': None, 'company': None,
            'address_line': None, 'city': None, 'state': None, 'country': None, 'zip_code': None,
            'total_price': None, 'total_tax': None, 'shipping': None, 'grand_total': None, 'shoppingCart': None
        }
        for order_field in order:
            # if order_field not in request.form:
            #  raise ExportException("internal error, {} missing from form".format(order_field))
            order[order_field] = request.form[order_field]
            if len(order[order_field].strip()) == 0:
                raise ExportException("'" + order_field.capitalize().replace("_", " ") + "' does not have a value")
        session[SESSION_CHECKOUT_INFO] = order
        print(order)
        g.db.orders.addOrder(order)
        return jsonify({"redirect": "/external/checkout_payment"})
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/external/checkout_payment', methods=['GET'])
def serve_external_payment():
    return outside_render('shop_iframe/checkout_payment.html')


@bp.route('/external/checkout_payment', methods=['POST'])
def serve_external_paymentinfo():
    print(request.form)

    # We need to implement stripe payment function here
    # Cart and user information is stored in session[SESSION_CHECKOUT_INFO]
    # If billing address is same as shipping address then request.form["address_checkbox"]=="on"
    # Updating the orders table

    # Once payment goes through sending email to confirm order to buyer and seller

    return redirect('/external/invoice')


@bp.route('/external/invoice', methods=['GET'])
def serve_external_invoice():
    return outside_render('shop_iframe/invoice.html')
