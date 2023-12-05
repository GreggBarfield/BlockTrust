from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for, Response
)

from ..common_exceptions import ExportException
from core.config import (
    ROOT as WEBSITE_ROOT, RECAPTCHA_SITE_KEY, IPINFO_TOKEN, CHECK_IP, STRIPE_PUBLISHABLE_KEY, ADMIN_EMAIL
)
from ..database.combinations import convert_auction_market_to_account
from ..database.tables.accounts import AccountsException
from ..database.tables.auction_markets import AuctionMarkets
from ..database.tables.error_logs import ErrorLogs
from ..database.tables.orders import Orders
from ..database.tables.order_products import OrderProducts
from ..database.tables.products import ProductTable
from ..database.tables.product_categories import ProductCategories
from ..database.tables.product_discounts import ProductDiscounts, ProductDiscountException
from ..database.tables.product_vendors import ProductVendors, HERD_WHISTLE_VENDOR_NAME
from ..database.tables.sales_groups import SalesGroups, TARGET_DATE_KEYS_TO_DESC
from ..database.tables.sales_group_fields_values import SalesGroupFieldsValues, SALES_GROUP_FORM_TYPES_NAMES_TO_IDS
from ..database.tables.sales_group_searches import SalesGroupSearches
from ..database.tables.users import UsersException
from ..renderers.email import render_email
from ..renderers.outside import outside_render
from ..sectors import SECTORS_NAME_TO_ID
from ..utilities import auth, crut
from ..utilities.email import send_tag_store_email, send_multiple_tag_store_email

from json import loads
from traceback import format_exc

import json

bp = Blueprint('iframe_bp', __name__)


@bp.route('/iframe/sales-group/create', methods=['GET', 'POST'])
@crut.require_user_iframe
def serve_create_sales_group():
    if request.method == 'GET':
        auction_markets = AuctionMarkets(g.db).get_auction_markets()
        form_post_route = url_for('iframe_bp.serve_create_sales_group')
        sales_group_fields_values = SalesGroupFieldsValues(g.db).get(
            sales_group_form_type=SALES_GROUP_FORM_TYPES_NAMES_TO_IDS["Internal"]
        )
        return outside_render("/outside/iframes/sales-groups/create-sales-group.html", {
            "auction_markets": auction_markets,
            "form_post_route": form_post_route,
            "pre_select_auction_market": False,
            "pre_selected_auction_market_id": None,
            "sales_group_fields_values": sales_group_fields_values
        })
    if request.method == 'POST':
        images = []
        if 'images' in request.json["reported"]:
            images = request.json["reported"]["images"]
        try:
            SalesGroups(g.db).validate_or_fail_sales_group(
                account_id=g.account.id(),
                group_name=request.json["group_name"],
                zip=request.json["zip"],
                delivery_location_type=request.json["delivery_location_type"],
                count=request.json["reported"]["count"],
                weight=request.json["reported"]["weight"],
                category=request.json["category"],
                breeds=request.json["reported"]["breeds"],
                sale_date=request.json["sale_date"],
                delivery_location=request.json["delivery_location"],
                auction_market_location=request.json["auction_market_location"],
                images=images,
                price=request.json["price"],
                slide=request.json["reported"]["marketing_slide"],
                weighing_conditions=request.json["reported"]["marketing_weighing_conditions"]
            )
        except ExportException as e:
            return {"error": str(e)}
        delivery_location = ""
        auction_market_id = None
        if request.json["delivery_location_type"] == "Direct/Off Ranch":
            delivery_location = request.json["delivery_location"]
        else:
            delivery_location = request.json["auction_market_location"]
            if request.json["delivery_location_type"] == "Auction":
                auction_market_id = request.json["auction_market_id"]
                convert_auction_market_to_account(g.db, auction_market_id, request.json["group_name"])
        sales_group_id = SalesGroups(g.db).insert_sales_group(
            account=g.account.id(),
            reported=request.json["reported"],
            published=request.json["published"],
            zip_code=request.json["zip"],
            delivery_location=delivery_location,
            sale_date=request.json["sale_date"],
            auction_market_id=auction_market_id,
            group_name=request.json["group_name"],
            is_archived=0,
            delivery_location_type=request.json["delivery_location_type"],
            price=request.json["price"],
            category=request.json["category"],
            breed_comments=request.json["breed_comments"],
            weighing_conditions=request.json["weighing_conditions"],
            are_annual_cattle_herd_vaccinations_given=request.json["are_annual_cattle_herd_vaccinations_given"],
            show_account_carcass_data=request.json["show_account_carcass_data"],
            is_api_insert=0
        )
        return {"redirect": "/iframe/sales-group/sales-group-created"}


@bp.route('/iframe/sales-group/create/<int:auction_market_id>', methods=["GET"])
@crut.require_user_iframe
def serve_create_sales_group_with_preselected_auction_market(auction_market_id):
    auction_markets = AuctionMarkets(g.db).get_auction_markets(id=auction_market_id)
    if len(auction_markets) == 0:
        auction_markets = AuctionMarkets(g.db).get_auction_markets()
    form_post_route = url_for('iframe_bp.serve_create_sales_group')
    sales_group_fields_values = SalesGroupFieldsValues(g.db).get(
        sales_group_form_type=SALES_GROUP_FORM_TYPES_NAMES_TO_IDS["Internal"]
    )
    return outside_render("/outside/iframes/sales-groups/create-sales-group.html", {
        "auction_markets": auction_markets,
        "form_post_route": form_post_route,
        "pre_select_auction_market": True,
        "pre_selected_auction_market_id": auction_market_id,
        "sales_group_fields_values": sales_group_fields_values
    })

@bp.route('/iframe/sales-group/sales-group-created')
@crut.require_user_iframe
def serve_sales_group_created():
    return outside_render("/outside/iframes/sales-groups/sales-group-created.html")


@bp.route('/iframe/login', methods=['GET'])
def serve_iframe_login():
    redirect_to = ''
    if 'redirect' in request.args:
        redirect_to = request.args['redirect']
    if 'user' in g and g.user is not None:
        return redirect(redirect_to)
    return outside_render("/outside/iframes/login.html", {"redirect_to": redirect_to})


@bp.route('/iframe/sales-group/manage-sales-groups', methods=['GET'])
@crut.require_user_iframe
def serve_manage_sales_groups():
    sales_groups = SalesGroups(g.db).get_sales_groups(account_id=g.account.id(), is_archived=0)
    return outside_render("/outside/iframes/sales-groups/manage-sales-groups.html", {"sales_groups": sales_groups})


@bp.route('/iframe/sales-group/edit/<int:sales_group_id>', methods=['GET', 'POST'])
@crut.require_user_iframe
def serve_edit_sales_group(sales_group_id):
    if request.method == 'GET':
        sales_group = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)
        auction_markets = AuctionMarkets(g.db).get_auction_markets()
        form_post_route = url_for('iframe_bp.serve_edit_sales_group', sales_group_id=sales_group_id)
        if(sales_group["account"] != g.account.id()):
            return outside_render("/outside/iframes/sales-groups/unauthorized.html")
        external_shareable_link = WEBSITE_ROOT + url_for('outside_bp.serve_external_sales_group_viewer',
            sales_group_id=sales_group['id'])
        sales_group_fields_values = SalesGroupFieldsValues(g.db).get(
            sales_group_form_type=SALES_GROUP_FORM_TYPES_NAMES_TO_IDS["Internal"]
        )
        return outside_render("/outside/iframes/sales-groups/edit-sales-group.html", {
            "sales_group": sales_group,
            "auction_markets": auction_markets,
            "form_post_route": form_post_route,
            "external_shareable_link": external_shareable_link,
            "sales_group_fields_values": sales_group_fields_values
        })
    if request.method == 'POST':
        # Check that the account selected is the owner of the sales group
        original_row = SalesGroups(g.db).get_sales_group_by_id(request.json["id"])
        if original_row["account"] != g.account.id():
            raise ExportException("Insufficient permissions to edit this sales group.")
        # Validate sales group fields
        images = []
        SalesGroups(g.db).validate_or_fail_sales_group(
            account_id=g.account.id(),
            group_name=request.json["group_name"],
            zip=request.json["zip"],
            delivery_location_type=request.json["delivery_location_type"],
            count=request.json["reported"]["count"],
            weight=request.json["reported"]["weight"],
            category=request.json["category"],
            breeds=request.json["reported"]["breeds"],
            sale_date=request.json["sale_date"],
            delivery_location=request.json["delivery_location"],
            auction_market_location=request.json["auction_market_location"],
            images=images,
            price=request.json["price"],
            slide=request.json["reported"]["marketing_slide"],
            weighing_conditions=request.json["reported"]["marketing_weighing_conditions"]
        )
        delivery_location = ""
        auction_market_id = None
        if request.json["delivery_location_type"] == "Direct/Off Ranch":
            delivery_location = request.json["delivery_location"]
        else:
            delivery_location = request.json["auction_market_location"]
            if request.json["delivery_location_type"] == "Auction":
                auction_market_id = request.json["auction_market_id"]
                convert_auction_market_to_account(g.db, auction_market_id, request.json["group_name"])
        SalesGroups(g.db).update_sales_group(
            id=request.json["id"],
            reported=request.json["reported"],
            published=request.json["published"],
            zip_code=request.json["zip"],
            delivery_location=delivery_location,
            sale_date=request.json["sale_date"],
            auction_market_id=auction_market_id,
            group_name=request.json["group_name"],
            is_archived=0,
            delivery_location_type=request.json["delivery_location_type"],
            price=request.json["price"],
            category=request.json["category"],
            breed_comments=request.json["breed_comments"],
            weighing_conditions=request.json["weighing_conditions"],
            are_annual_cattle_herd_vaccinations_given=request.json["are_annual_cattle_herd_vaccinations_given"],
            show_account_carcass_data=request.json["show_account_carcass_data"]
        )
        return {"redirect": "/iframe/sales-group/manage-sales-groups"}


@bp.route('/iframe/sales-group/view/<int:sales_group_id>', methods=['GET', 'POST'])
@crut.require_user_iframe
def serve_view_sales_group(sales_group_id):
    sales_group = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)
    if(sales_group["account"] != g.account.id()):
        return outside_render("/outside/iframes/sales-groups/unauthorized.html")
    external_shareable_link = WEBSITE_ROOT + url_for('outside_bp.serve_external_sales_group_viewer',
        sales_group_id=sales_group['id'])
    return outside_render("/outside/iframes/sales-groups/view-sales-group.html", {
        "sales_group": sales_group,
        "external_shareable_link": external_shareable_link
    })


@bp.route('/iframe/signup', methods=['GET', 'POST'])
def serve_iframe_signup():
    if request.method == 'GET':
        available_sectors = {
            "Cow Calf Ranch": SECTORS_NAME_TO_ID["Cow-Calf"],
            "Stocker/Backgrounder": SECTORS_NAME_TO_ID["Stocker/Backgrounder"]
        }
        partners = g.db.accounts.get_accounts(
            sectors=[s for s in available_sectors.values()],
            is_partner=1,
            is_partner_used_for_signup=1
        )
        auction_markets = AuctionMarkets(g.db).get_auction_markets(
            is_archived=0,
            auction_markets_order_by="name",
            auction_markets_sort_by="ASC"
        )
        return outside_render("/outside/iframes/signup.html", {
            "available_sectors": available_sectors,
            "SECTORS_NAME_TO_ID": SECTORS_NAME_TO_ID,
            "partners": partners,
            "site_key": RECAPTCHA_SITE_KEY,
            "ipinfo_access_token": IPINFO_TOKEN,
            "check_ip": CHECK_IP,
            "auction_markets": auction_markets
        })
    if request.method == 'POST':
        try:
            required = {
                'company': None, 'sector': None, 'first_name': None, 'last_name': None,
                'address': None, 'city': None, 'state': None, 'zip_code': None,
                'username': None, 'email': None, 'password': None, 'confirm_password': None
            }
            for required_field in required:
                if required_field not in request.form:
                    raise ExportException("Missing Required Field: " + required_field)
                required[required_field] = request.form[required_field]
                if len(required[required_field].strip()) == 0:
                    raise ExportException("'" + required_field.capitalize().replace("_", " ") + "' does not have a value")
        
            try:
                auth.verified_signup(
                    username=required['username'],
                    email=required['email'],
                    phone=request.form['phone'],
                    first_name=required['first_name'],
                    last_name=required['last_name'],
                    password=required['password'],
                    confirm_password=required['confirm_password'],
                    company=required['company'],
                    partner=request.form['partner'],
                    affiliate_id=request.form['affiliate_id'],
                    sector=required['sector'],
                    address=required['address'],
                    city=required['city'],
                    state=required['state'],
                    zip_code=required['zip_code'],
                    personal_phone=request.form['personal_phone'],
                    auction_markets_used=loads(request.form["auction_markets"]),
                    preconditioning_programs=loads(request.form["preconditioning_programs"]),
                    pvp_programs=loads(request.form["pvp_programs"])
                )
            except (auth.SignupFailedException, AccountsException, UsersException) as e:
                raise ExportException("Signup failed for " + required['company'] +" : " + str(e))

            redirect_to = ""
            if (
                    'requestRedirectTo' in request.form and
                    request.form['requestRedirectTo'] is not None and
                    request.form['requestRedirectTo'] != ''
                ):
                redirect_to = request.form['requestRedirectTo']
            return {"redirect": redirect_to}
        except ExportException as e:
            raise e
        except Exception as e:
            ErrorLogs(g.db).insert_error_log("Create Account using Iframe", e.__class__.__name__ + ": " + str(e), format_exc())
            return {"error": "Internal Server Error"}, 500


@bp.route('/iframe/logout', methods=['GET'])
def serve_iframe_logout():
    auth.logout()
    return outside_render('/outside/iframes/logged-out.html')


@bp.route('/iframe/request-password-reset', methods=['GET'])
def serve_iframe_request_password_reset():
    redirect_to = "/iframe/password-reset-message"
    return outside_render('/outside/iframes/request-password-reset.html', {"redirect_to": redirect_to})


@bp.route('/iframe/password-reset-message')
def serve_iframe_password_reset_message():
    return outside_render('/outside/iframes/password-reset-message.html')


@bp.route('/iframe/sales-group/search/', defaults={'id': ''}, methods=['GET'])
@bp.route('/iframe/sales-group/search/<int:id>', methods=['GET'])
@crut.require_user_iframe
def serve_iframe_search_sales_groups(id):
    search = {}
    if id:
        if len(search := SalesGroupSearches(g.db).get(id=id, user_id=g.user.id())) > 0:
            search = search[0]
        else:
            raise ExportException("Bad Request")
    return outside_render("/outside/iframes/sales-groups/search-sales-groups.html", {
        "search": search, "search_link": url_for(request.endpoint),
        "dates": [v for v in TARGET_DATE_KEYS_TO_DESC.values()]
    })


@bp.route('/iframe/shop/tag-store', methods=["GET"])
@crut.require_user_iframe
def serve_iframe_tag_store():
    all_product_data = []
    product_vendors = ProductVendors(g.db).get_product_vendors()
    for product_vendor in product_vendors:
        vendor_products_data = ProductTable(g.db).get_products(
            product_vendor_id=product_vendor["id"],
            include_images=True,
            is_internal=int(True)
        )
        all_product_data.extend(vendor_products_data)
    
    product_categories = ProductCategories(g.db).get_product_categories()
    product_vendors = ProductVendors(g.db).get_product_vendors()
    product_vendor_ids_to_names = {}

    shopping_cart_link = WEBSITE_ROOT + url_for('iframe_bp.serve_iframe_shopping_cart')
    for product_vendor in product_vendors:
        product_vendor_ids_to_names[product_vendor["id"]] = product_vendor["vendor_name"]
    return outside_render("/outside/iframes/tag-store/homepage.html", {
        "all_product_data": all_product_data,
        "product_categories": product_categories,
        "product_vendor_ids_to_names": product_vendor_ids_to_names,
        "shopping_cart_link": shopping_cart_link
    })


@bp.route('/iframe/shop/shopping-cart', methods=["GET"])
@crut.require_user_iframe
def serve_iframe_shopping_cart():
    shop_homepage_link = WEBSITE_ROOT + url_for('iframe_bp.serve_iframe_tag_store')
    checkout_link = WEBSITE_ROOT + url_for('iframe_bp.serve_iframe_checkout')
    return outside_render("/outside/iframes/tag-store/shopping-cart.html", {
        "shop_homepage_link": shop_homepage_link,
        "checkout_link": checkout_link
    })


@bp.route('/iframe/shop/checkout', methods=["GET"])
@crut.require_user_iframe
def serve_iframe_checkout():
    user_first_name = g.user.first_name()
    user_last_name = g.user.last_name()
    user_account = g.account
    shop_homepage_link = WEBSITE_ROOT + url_for('iframe_bp.serve_iframe_tag_store')
    shopping_cart_link = WEBSITE_ROOT + url_for('iframe_bp.serve_iframe_shopping_cart')
    checkout_payment_link = WEBSITE_ROOT + url_for('iframe_bp.serve_iframe_checkout_payment')
    return outside_render("/outside/iframes/tag-store/checkout.html", {
        "user_first_name": user_first_name,
        "user_last_name": user_last_name,
        "user_account": user_account,
        "shop_homepage_link": shop_homepage_link,
        "shopping_cart_link": shopping_cart_link,
        "checkout_payment_link": checkout_payment_link
    })


@bp.route('/iframe/shop/checkout-payment', methods=["GET"])
@crut.require_user_iframe
def serve_iframe_checkout_payment():
    herd_whistle_vendor_data = ProductVendors(g.db).get_product_vendors(vendor_name=HERD_WHISTLE_VENDOR_NAME)
    herd_whistle_vendor_id = herd_whistle_vendor_data[0]["id"]
    invoice_link = WEBSITE_ROOT + url_for('iframe_bp.serve_iframe_invoice')
    return outside_render("/outside/iframes/tag-store/checkout-payment.html", {
        "stripe_key": STRIPE_PUBLISHABLE_KEY,
        "herd_whistle_vendor_id": herd_whistle_vendor_id,
        "invoice_link": invoice_link
    })


@bp.route('/iframe/shop/invoice', methods=["GET"])
@crut.require_user_iframe
def serve_iframe_invoice():
    shop_homepage_link = WEBSITE_ROOT + url_for('iframe_bp.serve_iframe_tag_store')
    return outside_render("/outside/iframes/tag-store/invoice.html", {
        "shop_homepage_link": shop_homepage_link
    })


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

