from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for, Response
)
from ..renderers.outside import outside_render
from ..renderers.dashboard import dashboard_render
from ..common_exceptions import ExportException
from ..config import ADMIN_EMAIL, STRIPE_PUBLISHABLE_KEY, EMAIL_SENDER
from ..database.tables.orders import Orders
from ..database.tables.order_products import OrderProducts
from ..database.tables.products import ProductTable, PRODUCT_TAG_STORE_LOCATION_NAMES_TO_IDS
from ..database.tables.product_categories import ProductCategories
from ..database.tables.product_discounts import ProductDiscountException, ProductDiscounts
from ..database.tables.product_vendors import ProductVendors
from ..database.tables.vendor_identifiers_for_account import VendorIdentifiersForAccounts
from ..utilities import crut
from ..utilities.constants import HTTP_BAD_REQUEST, HTTP_NO_CONTENT
from ..utilities.email import send_tag_store_email, send_multiple_tag_store_email
from ..utilities.shop.herdwhistle_api import HerdWhistleAPI
from ..renderers.email import render_email

import json

bp = Blueprint('shop_bp', __name__)

# Routes for shop homepage and cart iframes


@bp.route('/external/shop/<int:partner_id>', methods=['GET'])
def serve_partner_shop(partner_id):
    allProductData = ProductTable(g.db).get_products(partner=partner_id, include_images=True)
    productCategories = ProductCategories(g.db).get_product_categories()
    product_vendors = ProductVendors(g.db).get_product_vendors()
    product_vendor_ids_to_names = {}
    for product_vendor in product_vendors:
        product_vendor_ids_to_names[product_vendor["id"]] = product_vendor["vendor_name"]
    return outside_render('shop-iframe/shop-homepage.html', {
        "allProductData": allProductData,
        "partner_id": partner_id,
        "product_categories": productCategories,
        "product_vendor_ids_to_names": product_vendor_ids_to_names
        })


@bp.route('/external/shop', methods=['GET'])
def serve_external_shop():
    allProductData = ProductTable(g.db).get_products()
    return outside_render('shop-iframe/shop-homepage.html', {"allProductData": allProductData})


@bp.route('/external/cart/<partner_id>', methods=['GET'])
def serve_external_cart(partner_id):
    return outside_render('shop-iframe/shopping-cart.html', {"partner_id": partner_id})


@bp.route('/external/cart', methods=['POST'])
def serve_apply_coupon():
    try:
        # Getting the discounts applcable for the coupon code supplied
        discounts = ProductDiscounts(g.db).get_discounts(request.form['coupon_code'])
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


@bp.route('/shop/external/create-order', methods=['POST'])
def create_order():
    try:
        data = json.loads(request.data)

        order_details = eval(data["orderDetails"])
        # Adding order to orders table and getting current order id from orders table
        order_id = Orders(g.db).add_order(order_details, order_details["address_line"], order_details["city"], order_details["state"],
                                          order_details["zip_code"])
        # Getting the cart details
        cart = eval(order_details['shoppingCart'])
        # Adding product data and quantities to the OrderProducts table
        for key, value in cart.items():
            OrderProducts(g.db).add_order_product(order_id, key, value["quantity"])

        return {"orderId": order_id}
    except Exception as e:
        return {"error": str(e)}, 400


@bp.route('/shop/external/update-order', methods=['POST'])
def update_order():
    try:
        data = json.loads(request.data)
        # Updating the orders table if payment goes through
        Orders(g.db).update_order_as_stripe_paid(data["orderId"], data["paymentIntent"])

        order_details = eval(data["orderDetails"])
        shopping_cart = eval(order_details["shoppingCart"])
        # Once payment goes through sending email to confirm order to buyer
        premise_id = "N/A"
        if order_details["premise_id"] != "":
            premise_id = order_details["premise_id"]
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
                'shipping_address_line': order_details["address_line"],
                'shipping_city': order_details["city"],
                'shipping_state': order_details["state"],
                'shipping_zip_code': order_details["zip_code"],
                'cart': eval(order_details["shoppingCart"]),
                'premise_id': premise_id
            }),
            order_details["email"],
            "U.S. CattleTrace Purchase <info@uscattletrace.org>"
        )
        # Once payment goes through sending email to confirm order to seller
        # Creating a vendor oriented cart to facilitate sending separate emails to separate vendors
        vendor_oriented_cart = {}
        for product_id, product_details in shopping_cart.items():
            product_row = ProductTable(g.db).get_products(id=product_id)
            if len(product_row) > 0:
                product_vendor_id = product_row[0]["product_vendor_id"]
                if product_vendor_id in vendor_oriented_cart:
                    vendor_oriented_cart[product_vendor_id].append(product_details)
                else:
                    vendor_oriented_cart[product_vendor_id] = [product_details]

        for vendor_id, product_list in vendor_oriented_cart.items():
            vendor_row = ProductVendors(g.db).get_product_vendors(id=vendor_id)
            if len(vendor_row) > 0:
                vendor_email = vendor_row[0]["vendor_email"]
                send_tag_store_email(
                    "New order summary",
                    render_email("purchase_summary_vendor.html", {
                        'order_id': data["orderId"],
                        'first': order_details["first_name"],
                        'last': order_details["last_name"],
                        'shipping_address_line': order_details["address_line"],
                        'shipping_city': order_details["city"],
                        'shipping_state': order_details["state"],
                        'shipping_zip_code': order_details["zip_code"],
                        'cart': product_list,
                        'premise_id': premise_id
                        }),
                    vendor_email,
                    "U.S. CattleTrace Purchase <info@uscattletrace.org>"
                    )

        send_multiple_tag_store_email(
            "New order summary",
            render_email("purchase_summary_seller.html", {
                'order_id': data["orderId"],
                'first': order_details["first_name"],
                'last': order_details["last_name"],
                'total_price': order_details["total_price"],
                'total_tax': order_details["total_tax"],
                'discount': order_details["discount"],
                'shipping': order_details["shipping"],
                'grand_total': order_details["grand_total"],
                'shipping_address_line': order_details["address_line"],
                'shipping_city': order_details["city"],
                'shipping_state': order_details["state"],
                'shipping_zip_code': order_details["zip_code"],
                'cart': eval(order_details["shoppingCart"]),
                'premise_id': premise_id
            }),
            ["cgrund@uscattletrace.org", ADMIN_EMAIL],
            "U.S. CattleTrace Purchase <info@uscattletrace.org>"
        )

        return {"success": True}
    except Exception as e:
        return {"error": str(e)}, 400


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
        order_id = Orders(g.db).add_order(order_details, shipping_address_line, shipping_city, shipping_state, shipping_zip_code)
        # Getting the cart details
        cart = eval(order_details['shoppingCart'])
        # Adding product data and quantities to the OrderProducts table
        for key, value in cart.items():
            OrderProducts(g.db).add_order_product(order_id, key, value["quantity"])

        # Once payment goes through sending email to confirm order to buyer and seller
        return jsonify({"redirect": "/external/invoice/"+partner_id})
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/external/invoice/<partner_id>', methods=['GET'])
def serve_external_invoice(partner_id):
    return outside_render('shop-iframe/invoice.html', {'partner_id': partner_id})


@bp.route("/shop/tag-store", methods=["GET"])
@crut.require_account
def serve_tag_store():
    all_product_data = []
    product_vendors = ProductVendors(g.db).get_product_vendors()
    for product_vendor in product_vendors:
        product_vendor_id = product_vendor["id"]
        vendor_products_data = ProductTable(g.db).get_products(
            product_vendor_id=product_vendor_id,
            include_images=True,
            is_internal=PRODUCT_TAG_STORE_LOCATION_NAMES_TO_IDS["Internal"]
        )
        all_product_data.extend(vendor_products_data)
    
    product_categories = ProductCategories(g.db).get_product_categories()
    product_vendors = ProductVendors(g.db).get_product_vendors()
    product_vendor_ids_to_names = {}
    for product_vendor in product_vendors:
        product_vendor_ids_to_names[product_vendor["id"]] = product_vendor["vendor_name"]
    return dashboard_render("tag-store/homepage.html", {
        "all_product_data": all_product_data,
        "product_categories": product_categories,
        "product_vendor_ids_to_names": product_vendor_ids_to_names
    })


@bp.route("/shop/shopping-cart", methods=["GET"])
@crut.require_account
def serve_shopping_cart():
    return dashboard_render("tag-store/shopping-cart.html")


@bp.route("/shop/checkout", methods=["GET"])
@crut.require_account
def serve_checkout():
    return dashboard_render("tag-store/checkout.html")


@bp.route("/shop/invoice", methods=["GET"])
@crut.require_account
def serve_invoice():
    return dashboard_render("tag-store/invoice.html")


@bp.route("/shop/checkout-payment", methods=["GET"])
@crut.require_account
def serve_checkout_payment():
    return dashboard_render("tag-store/checkout-payment.html", {"stripe_key": STRIPE_PUBLISHABLE_KEY})


@bp.route("/shop/create-order", methods=["POST"])
@crut.require_account
def serve_create_order():
    try:
        data = json.loads(request.data)
        order_details = eval(data["orderDetails"])
        order_id = Orders(g.db).add_order(order_details, order_details["address_line"], order_details["city"],
                                          order_details["state"], order_details["zip_code"], account_id=g.account.id(),
                                          user_id=g.user.id())
        shopping_cart = json.loads(order_details['shopping_cart'])
        for product_id, product_details in shopping_cart.items():
            OrderProducts(g.db).add_order_product(order_id, product_id, product_details["quantity"])
        return {"orderId": order_id}
    except Exception as e:
        return {"error": str(e)}, HTTP_BAD_REQUEST


@bp.route("/shop/update-order", methods=["POST"])
@crut.require_account
def serve_update_order():
    try:
        data = json.loads(request.data)
        Orders(g.db).update_order_as_stripe_paid(data["orderId"], data["paymentIntent"])

        order_details = json.loads(data["orderDetails"])
        shopping_cart = json.loads(order_details["shopping_cart"])
        # Once payment goes through sending email to confirm order to buyer
        premise_id = "N/A"
        if order_details["premise_id"] != "":
            premise_id = order_details["premise_id"]
        send_tag_store_email(
            "Tag Store Purchase Summary",
            render_email("internal_tag_store/purchase_summary_customer.html", {
                'first': order_details["first_name"],
                'last': order_details["last_name"],
                'total_price': order_details["total_price"],
                'total_tax': order_details["total_tax"],
                'discount': order_details["discount"],
                'shipping': order_details["shipping"],
                'grand_total': order_details["grand_total"],
                'shipping_address_line': order_details["address_line"],
                'shipping_city': order_details["city"],
                'shipping_state': order_details["state"],
                'shipping_zip_code': order_details["zip_code"],
                'cart': shopping_cart,
                'premise_id': premise_id
            }),
            order_details["email"],
            EMAIL_SENDER
        )
        vendor_oriented_cart = {}
        for product_id, product_details in shopping_cart.items():
            product_row = ProductTable(g.db).get_products(id=product_id)
            product_vendor_id = product_row[0]["product_vendor_id"]
            if product_vendor_id in vendor_oriented_cart:
                vendor_oriented_cart[product_vendor_id].append(product_details)
            else:
                vendor_oriented_cart[product_vendor_id] = [product_details]

        for vendor_id, products_list in vendor_oriented_cart.items():
            vendor_row = ProductVendors(g.db).get_product_vendors(id=vendor_id)
            vendor_email = vendor_row[0]["vendor_email"]
            send_tag_store_email(
                "New order summary",
                render_email("internal_tag_store/purchase_summary_vendor.html", {
                    'order_id': data["orderId"],
                    'first': order_details["first_name"],
                    'last': order_details["last_name"],
                    'shipping_address_line': order_details["address_line"],
                    'shipping_city': order_details["city"],
                    'shipping_state': order_details["state"],
                    'shipping_zip_code': order_details["zip_code"],
                    'cart': products_list,
                    'premise_id': premise_id
                }),
                vendor_email,
            EMAIL_SENDER
            )

        send_multiple_tag_store_email(
            "New order summary",
            render_email("internal_tag_store/purchase_summary_seller.html", {
                'order_id': data["orderId"],
                'first': order_details["first_name"],
                'last': order_details["last_name"],
                'total_price': order_details["total_price"],
                'total_tax': order_details["total_tax"],
                'discount': order_details["discount"],
                'shipping': order_details["shipping"],
                'grand_total': order_details["grand_total"],
                'shipping_address_line': order_details["address_line"],
                'shipping_city': order_details["city"],
                'shipping_state': order_details["state"],
                'shipping_zip_code': order_details["zip_code"],
                'cart': shopping_cart,
                'premise_id': premise_id
            }),
            [ADMIN_EMAIL],
            EMAIL_SENDER
        )
        return Response(status=HTTP_NO_CONTENT)
    except Exception as e:
        return {"error": str(e)}, HTTP_BAD_REQUEST


@bp.route("/shop/send-order-to-herdwhistle-api", methods=["POST"])
@crut.require_account
def serve_send_order_to_herdwhistle_api():
    herd_whistle_data = ProductVendors(g.db).get_product_vendors(vendor_name='Herd Whistle')
    data = json.loads(request.data)
    order_details = json.loads(data["orderDetails"])
    shopping_cart = json.loads(order_details["shopping_cart"])
    customer_details = {
        'name': order_details["first_name"] + " " + order_details["last_name"],
        'street': order_details["address_line"],
        'street2': False,
        'city': order_details["city"],
        'state_id': order_details["state"],
        'zip': order_details["zip_code"],
        'country_id': 'United States',
        'phone': order_details["phone"],
        'email': order_details["email"],
        'company_type': 'company',
        'type': 'contact'
    }
    herdwhistle_identifiers_for_account = VendorIdentifiersForAccounts(g.db).get(
        product_vendor_id=herd_whistle_data[0]["id"],
        account_id=g.account.id()
    )
    if len(herdwhistle_identifiers_for_account) > 0:
        herdwhistle_customer_id = herdwhistle_identifiers_for_account[0]["vendor_customer_id"]
        herdwhistle_customer_shipping_id = herdwhistle_identifiers_for_account[0]["vendor_customer_shipping_id"]
    else:
        herdwhistle_customer_id, herdwhistle_customer_shipping_id = HerdWhistleAPI().create_new_herdwhistle_customer_credentials(
            customer_details=customer_details
        )
        VendorIdentifiersForAccounts(g.db).insert(
            account_id=g.account.id(),
            product_vendor_id=herd_whistle_data[0]["id"],
            vendor_customer_id=herdwhistle_customer_id,
            vendor_customer_shipping_id=herdwhistle_customer_shipping_id
        )
    if HerdWhistleAPI().verify_herdwhistle_customer_credentials(
        herdwhistle_customer_id=herdwhistle_customer_id,
        herdwhistle_customer_shipping_id=herdwhistle_customer_shipping_id):
        sale_order_id = HerdWhistleAPI().create_new_sale_order(
            herdwhistle_customer_id=herdwhistle_customer_id,
            herdwhistle_customer_shipping_id=herdwhistle_customer_shipping_id,
            shopping_cart=shopping_cart
        )
        Orders(g.db).update(id=data["orderId"], herdwhistle_sale_order_id=sale_order_id)
    return Response(status=HTTP_NO_CONTENT)


@bp.route("/shop/view-orders", methods=["GET"])
@crut.require_account
def serve_view_order_history():
    user_orders = Orders(g.db).get_orders(account_id=g.account.id(), user_id=g.user.id())
    return dashboard_render("tag-store/view-orders.html", {"user_orders": user_orders})


@bp.route("/shop/view-orders/<int:order_id>", methods=["GET"])
@crut.require_account
def serve_view_order(order_id):
    try:
        user_order = Orders(g.db).get_orders(id=order_id, account_id=g.account.id(), user_id=g.user.id())
        if len(user_order) > 0:
            user_order = user_order[0]
            order_products = OrderProducts(g.db).get_order_products(order_id)
            for product in order_products:
                product_details = ProductTable(g.db).get_products(id=product["product_id"])
                product["product_details"] = product_details[0]
            return dashboard_render("tag-store/view-order.html", {"order": user_order, "order_products": order_products})
        else:
            raise ExportException("Sorry, the requested order was not found. ")
    except ExportException as e:
        return dashboard_render("tag-store/view-order.html", {"error": str(e)})