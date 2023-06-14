from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)
from ..renderers.outside import outside_render
from ..renderers.dashboard import dashboard_render
from ..common_exceptions import ExportException
from ..config import STRIPE_PUBLISHABLE_KEY
from ..database.tables.orders import Orders
from ..database.tables.order_products import OrderProducts
from ..database.tables.products import ProductTable
from ..database.tables.product_categories import ProductCategories
from ..database.tables.product_discounts import ProductDiscountException, ProductDiscounts
from ..database.tables.product_vendors import ProductVendors
from ..utilities import crut
from ..utilities.email import send_tag_store_email, send_multiple_tag_store_email
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
            order_details["email"]
        ) 
        # Once payment goes through sending email to confirm order to seller
        # Creating a vendor oriented cart to facilitate sending separate emails to separate vendors
        vendor_oriented_cart = {}
        # TODO: Name iterating variables explicitly. So here I think key should really be product_id. I am not sure what value stands for.
        for key, value in shopping_cart.items():
            product_row = ProductTable(g.db).get_products(id=key)
            if len(product_row) > 0:
                product_vendor_id = product_row[0]["product_vendor_id"]
                if product_vendor_id in vendor_oriented_cart:
                    vendor_oriented_cart[product_vendor_id].append(value)
                else:
                    vendor_oriented_cart[product_vendor_id] = [value]
        # TODO: Same comment as on line 109
        for key, value in vendor_oriented_cart.items():
            vendor_row = ProductVendors(g.db).get_product_vendors(id=key)
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
                        'cart': value,
                        'premise_id': premise_id
                        }),
                    vendor_email
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
            ["cgrund@uscattletrace.org", "gregg.barfield@ledgerspace.net"]
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
    all_product_data = ProductTable(g.db).get_products(product_vendor_id=4, include_images=True)
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
