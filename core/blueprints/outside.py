from flask import (
    jsonify, request, Blueprint, g, redirect, url_for, send_from_directory, Response
)

from ..renderers.outside import outside_render
from ..database.combinations import send_email_to_admin_users
from ..database.tables.rejected_registrations import RejectedRegistrations
from ..database.tables.users import UsersException
from ..database.tables.accounts import AccountsException
from ..database.tables.files import Files
from ..database.tables.matches import Matches
from ..database.tables.sales_groups import SalesGroups
from ..database.tables.tips import Tips
from ..common_exceptions import ExportException
from ..utilities import auth
from ..utilities.email import send_email
from ..utilities import token
from ..utilities.constants import HTTP_BAD_REQUEST, HTTP_NO_CONTENT
from ..renderers.email import render_email
from core.config import (
    SUPPORT_GENERAL_EMAIL, ROOT as WEBSITE_ROOT, SUPPORT_TAG_STORE_EMAIL, RECAPTCHA_SITE_KEY,
    RECAPTCHA_SECRET_KEY, RECAPTCHA_MIN_SCORE, IPINFO_TOKEN, CHECK_IP, STRIPE_PUBLISHABLE_KEY
)
from ..sectors import SECTORS_NAME_TO_ID, SECTORS_ID_TO_NAME
from json import loads
from requests import post
from ..match_types import MATCH_TYPES_NAME_TO_ID


bp = Blueprint('outside_bp', __name__)


@bp.route('/', methods=['GET'])
def serve_landing():
    return outside_render('landing.html')


@bp.route('/logout', methods=['GET'])
def serve_logout():
    login_url = url_for('outside_bp.serve_employee_login') if "employee" in g else url_for('outside_bp.serve_login')
    auth.logout()
    return outside_render('logged-out.html', {"login_url": login_url})


@bp.route('/login', methods=['GET'])
def serve_login():
    redirect_to = ''

    # Might want to revisit this eventually to protect against users getting tricked
    if 'redirect' in request.args:
        redirect_to = request.args['redirect']

    return outside_render('login.html', {"redirect_to": redirect_to})


@bp.route('/login/action', methods=['POST'])
def serve_login_action():
    try:
        if 'identifier' not in request.form:
            raise ExportException("internal error, identifier missing from form")

        if 'password' not in request.form:
            raise ExportException("internal error, password missing from form")
        try:
            user_id = auth.login(
                identifier=request.form['identifier'],
                password=request.form['password']
            )
            auth.load_user(user_id)
            account_users = g.db.account_users.get_account_users(user=g.user.id())
            if len(account_users) == 1:
                auth.load_account(account_users[0]["account"])
            else:
                return {"redirect": url_for("dashboard_bp.serve_accounts")}

            if (
                'requestRedirectTo' in request.form and
                request.form['requestRedirectTo'] is not None and
                request.form['requestRedirectTo'] != ''
            ):
                redirect_to = request.form['requestRedirectTo']
            elif g.account.is_partner():
                redirect_to = url_for("partner_bp.serve_dashboard")
            else:
                redirect_to = url_for("dashboard_bp.serve_dashboard")
            return {"redirect": redirect_to}
        except auth.LoginException as e:
            raise ExportException(str(e))
        except auth.EmailNotVerifiedException as e:
            raise ExportException(str(e))
        except auth.SignupFailedException as e:
            raise ExportException("internal error in Users.login")
    except ExportException as e:
        return jsonify({"error": str(e)}), 400


@bp.route('/signup', methods=['GET'])
def serve_signup():
    available_sectors = {
        "Cow Calf Ranch": SECTORS_NAME_TO_ID["Cow-Calf"],
        "Stocker/Backgrounder": SECTORS_NAME_TO_ID["Stocker/Backgrounder"]
    }
    partners = g.db.accounts.get_accounts(
        sectors=[s for s in available_sectors.values()],
        is_partner=1,
        is_partner_used_for_signup=1
    )
    return outside_render('signup.html', {
        "available_sectors": available_sectors,
        "SECTORS_NAME_TO_ID": SECTORS_NAME_TO_ID,
        "partners": partners,
        "site_key": RECAPTCHA_SITE_KEY,
        "ipinfo_access_token": IPINFO_TOKEN,
        "check_ip": CHECK_IP
    })


@bp.route('/signup/action', methods=['POST'])
def serve_signup_action():
    try:
        required = {
            'company': None, 'sector': None, 'first_name': None, 'last_name': None,
            'address': None, 'city': None, 'state': None, 'zip_code': None,
            'username': None, 'email': None, 'password': None, 'confirm_password': None
        }
        for required_field in required:
            if required_field not in request.form:
                raise ExportException("internal error, {} missing from form".format(required_field))
            required[required_field] = request.form[required_field]
            if len(required[required_field].strip()) == 0:
                raise ExportException("'" + required_field.capitalize().replace("_", " ") + "' does not have a value")

        if request.form.get('token', None) is not None:
            data = {
                "secret" : RECAPTCHA_SECRET_KEY,
                "response": request.form['token']
            }
            verification_response = post("https://www.google.com/recaptcha/api/siteverify", data=data)
            verification_response_json = verification_response.json()
            if verification_response_json['success']  and verification_response_json['score'] >= RECAPTCHA_MIN_SCORE:
                # Sign up
                try:
                    auth.signup(
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
                        recaptcha_score=verification_response_json['score'],
                        ip_address=request.form['ip_address'],
                        ip_country=request.form['ip_country']
                    )
                except (auth.SignupFailedException, AccountsException, UsersException) as e:
                    raise ExportException("Signup failed: " + str(e))

                # Generating token identifier for user for email verification
                userToken = token.generateConfirmationToken(required['email'])
                # Creating URL for user to confirm email address
                confirm_url = WEBSITE_ROOT + url_for('outside_bp.serve_confirm', tok=userToken)
                # Sending an email to user including Blocktrust email template and verification link with validity of 24 hours
                send_email(
                    "BlockTrust Network Email Confirmation",
                    render_email("verification_email.html", {
                        'confirm_url': confirm_url
                    }), required['email']
                )
                return {"redirect": "/email_not_verified"}
            else:
                RejectedRegistrations(g.db).insert_rejected_registration(required, verification_response_json)
                return {"redirect": "/not-authorized-to-register"}
        else:
            raise ExportException("There was an error verifying your registration. Please try again or write to us at info@blocktrustnetwork.com")
    except ExportException as e:
        return {"error": str(e)}, 400

# About us


@bp.route('/about-us/<path:path>', methods=['GET'])
def serve_about_us(path):
    if '.' in path:
        return "Error accessing " + path + ": '.' should not be included"
    return outside_render('about-us/' + path + '.html')


@bp.route('/contact_us', methods=["GET"])
def serve_contact_us_old():
    return redirect("/about-us/contact-us")


# Our Partners


@bp.route('/our-partners/<path:path>', methods=['GET'])
def serve_our_partners(path):
    if '.' in path:
        return "Error accessing " + path + ": '.' should not be included"
    return outside_render('our-partners/' + path + '.html')

# Market Trust


@bp.route('/market-trust', methods=['GET'])
def serve_market_trust():
    return outside_render('market-trust/index.html')

# Developers


@bp.route('/developers', methods=['GET'])
def serve_developers():
    return outside_render('developers/index.html')

# Privacy


@bp.route('/privacy', methods=['GET'])
@bp.route('/privacypolicy', methods=['GET'])
@bp.route('/privacy-policy', methods=['GET'])
def serve_privacy():
    return outside_render('privacy.html')


@bp.route('/favicon.ico', methods=['GET'])
def serve_favicon():
    return redirect("/static/favicon.ico")


@bp.route('/outside/contact_response', methods=['POST'])
def serve_contact_form_response():
    send_email(
        "New Contact Us Response",
        render_email("contact_us_response.html", {
            'first': request.json['first'],
            'last': request.json['last'],
            'phone': request.json['phone'],
            'email': request.json['email'],
            'message': request.json['message'],
            'message_title': "New Contact Us Response"
        }),
        SUPPORT_TAG_STORE_EMAIL
    )
    return {}

# Request a password reset


@bp.route('/request-password-reset', methods=['GET'])
def serve_request_password_reset():
    redirect_to = ''
    if 'redirect' in request.args:
        redirect_to = request.args['redirect']

    return outside_render('request_password_reset.html', {"redirect_to": redirect_to})

# Request password reset action


@bp.route('/request-password-reset', methods=['POST'])
def serve_password_request_action():
    user = g.db.users.get_by_email(request.form['email'])
    if user is None:
        return {"error": "Sorry, we couldn't find this email address"}, 400
    elif user.is_email_verified() != 1:
        return {"error": "Sorry, this user does not have a verified email address"}, 400
    else:
        # Generating token identifier for changing password securely
        userToken = token.generateConfirmationToken(request.form['email'])
        # Creating URL for user to access change password functionality
        password_reset_url = WEBSITE_ROOT + url_for('outside_bp.serve_reset_password', tok=userToken)
        # Sending an email to user with the Blocktrust email template and including password change link
        send_email(
                "BlockTrust Network Password change",
                render_email("forgot_password.html", {
                    'password_reset_url': password_reset_url
                }), request.form['email']
        )
        return {"redirect": "/password-reset-message"}


# Password reset message page

@bp.route('/password-reset-message', methods=['GET'])
def serve_password_reset_message():
    return outside_render('password-reset-message.html')


# Reset Password


@bp.route('/reset-password/<tok>', methods=['GET'])
def serve_reset_password(tok):
    # Redirecting to password change page
    redirect_to = tok
    try:
        token.confirmToken(tok)
        return outside_render('reset_password.html', {"redirect_to": redirect_to})
    except ExportException as e:
        return outside_render('login.html')


@bp.route('/reset-password/<tok>', methods=['POST'])
def serve_reset_password_action(tok):
    redirect_to = tok
    try:
        # Getting the requested new password from the user
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Getting the user eamil using the encrypted token
        email = token.confirmToken(tok)
        # Changing user password using email as an identifier
        auth.reset_user_password(email, new_password, confirm_password)
        return jsonify({"redirect": "/login"})
    except Exception as e:
        return jsonify({"error": str(e)})


@bp.route('/confirm/<tok>', methods=['GET', 'POST'])
def serve_confirm(tok):
    try:
        # Try whether the token is valid by passing it to confirmToken
        email = token.confirmToken(tok)
        # Confirm the user account
        auth.confirm(email)
    except auth.SignupFailedException as e:
        raise ExportException("User email could not be verified")
    # Redirect to user login page
    return outside_render('email-verified.html')


@bp.route('/email_not_verified', methods=['GET'])
def serve_email_not_confirmed():
    return outside_render('email-not-verified.html')


@bp.route('/not-authorized-to-register', methods=['GET'])
def serve_not_auth_to_register():
    return outside_render('not-authorized-to-register.html')


@bp.route('/outside/contact-email', methods=['GET'])
def serve_contact_email():
    return jsonify(
        contactEmail=SUPPORT_GENERAL_EMAIL
    )

# Routes for shop, shopping cart, product and checkout pages
# TODO: These need to be fixed as part of BTN-254

# @bp.route('/shop', methods=['GET'])
# def serve_shop():
#     allProductData = g.db.products.get_all_products()
#     return outside_render('shop/shop_homepage.html', {"allProductData": allProductData})


# Routes for adding and deleting cart items


# @bp.route('/shop', methods=['POST'])
# def serve_add_to_cart():
#     try:
#         return outside_render("shop/shop_homepage.html")
#     except ExportException as e:
#         return jsonify({"error": e})


# Routes for shopping cart page


# @bp.route('/shopping-cart', methods=['GET'])
# def serve_shopping_cart():
#     return outside_render("shop/shopping_cart.html")

# # Checkout Login and Checkout Register pages 


# @bp.route('/checkout_payment', methods=['GET'])
# def serve_checkout_payment():
#     return outside_render('shop/checkout_payment.html')


# @bp.route('/checkout_payment', methods=['POST'])
# def serve_payment():
#     print(request.form)
#     return redirect('/invoice')


# @bp.route('/checkout_loggedIn', methods=['GET'])
# def serve_checkout_register():
#     if g.user is not None:
#         return outside_render('shop/checkout_loggedIn.html', {'redirect_to': '/checkout_payment'})


# @bp.route('/checkout_loggedIn', methods=['POST'])
# def serve_loggedIn_checkout():
#     try:
#         redirect_to = ''
#         if 'redirect' in request.args:
#             redirect_to = request.args['redirect']
#         # Need to modify this to update shipping address incase of change by logged in user
#         return redirect('/checkout_payment')
#         # return outside_render('shop/checkout_payment.html')
#     except ExportException as e:
#         return jsonify({"error": str(e)})


# @bp.route('/checkout_register/action', methods=['POST'])
# def serve_checkout_register_action():
#     try:
#         required = {
#             'company': None, 'sector': None, 'first_name': None, 'last_name': None,
#             'city': None, 'state': None, 'zip_code': None, 'address': None,
#             'username': None, 'email': None, 'password': None, 'confirm_password': None, 'affiliate_id': None,
#             'address': None, 'partner': None
#         }
#         for required_field in required:
#             if required_field not in request.form:
#                 raise ExportException("internal error, {} missing from form".format(required_field))
#             required[required_field] = request.form[required_field]
#             if len(required[required_field].strip()) == 0:
#                 raise ExportException("'" + required_field.capitalize().replace("_", " ") + "' does not have a value")

#         # Sign up
#         try:
#             auth.signup(
#                 username=required['username'],
#                 email=required['email'],
#                 phone=request.form['phone'],
#                 first_name=required['first_name'],
#                 last_name=required['last_name'],
#                 password=required['password'],
#                 confirm_password=required['confirm_password'],
#                 company=required['company'],
#                 affiliate_id=required['affiliate_id'],
#                 sector=required['sector'],
#                 address=required['address'],
#                 city=required['city'],
#                 state=required['state'],
#                 zip_code=required['zip_code'],
#                 partner=required['partner']
#             )
#         except (auth.SignupFailedException, AccountsException, UsersException) as e:
#             raise ExportException("Signup failed: " + str(e))
#     # We can send out an email for verification if needed. The verification method has been implemented above in signup
#         return jsonify({"redirect": "/checkout_payment"})
#     except ExportException as e:
#         return jsonify({"error": str(e)})


# # Checkout form to get user information and payment information
# @bp.route('/checkout', methods=['GET'])
# def serve_checkout():
#     if g.user is not None:
#         return redirect('/checkout_loggedIn')
#     else:
#         return outside_render('shop/checkout.html', {
#             "sectors_id_to_name": SECTORS_ID_TO_NAME,
#             "redirect_to": '/checkout'
#             })


# # Invoice routes
# @bp.route('/invoice', methods=['GET'])
# def serve_invoice():
#     return outside_render('shop/invoice.html')


@bp.route('/rfid-tags', methods=["GET"])
def serve_rfid_tags():
    return outside_render("/outside/rfid_tags.html")


@bp.route('/employee/login', methods=['GET'])
def serve_employee_login():
    return outside_render('employee-login.html', {"customer_login_URL": url_for("outside_bp.serve_login")})

@bp.route('/employee/login/action', methods=['POST'])
def serve_employee_login_action():
    try:
        if 'identifier' not in request.form:
            raise ExportException("internal error, identifier missing from form")

        if 'password' not in request.form:
            raise ExportException("internal error, password missing from form")
        try:
            auth.employee_login(
                identifier=request.form['identifier'],
                password=request.form['password']
            )
            redirect_to = '/employee/dashboard'
            if (
                'requestRedirectTo' in request.form and
                request.form['requestRedirectTo'] is not None and
                request.form['requestRedirectTo'] != ''
            ):
                redirect_to = request.form['requestRedirectTo']
            return jsonify({"redirect": redirect_to})
        except auth.LoginException as e:
            raise ExportException(str(e))
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/images/<path:path>')
def send_file(path):
    return send_from_directory('static/images', path)


@bp.route('/add-user/<string:invite_token>', methods=['GET'])
def serve_add_user(invite_token):
    try:
        invite_string = token.confirmToken(invite_token, expiration=0)
        invite_object = eval(invite_string)
        user_email = invite_object["user_email"]
        if g.db.users.get_users(email=user_email):
            raise Exception("An account with that email already exists")
        is_admin = invite_object["is_admin"]
        account_id = invite_object["account_id"]
        account_row = g.db.accounts.get_accounts(id=account_id)[0]
        if account_row:
            return outside_render("/outside/add-user-signup.html", {
                "user_email": user_email,
                "account_name": account_row["name"],
                "account_id": account_id,
                "is_admin": is_admin
            })
        else:
            raise Exception("Account not found")
    except Exception as e:
        return outside_render("/outside/error.html", {"error_reason": str(e)})


@bp.route('/add-user/action', methods=['POST'])
def serve_add_invited_user():
    try:
        auth.invited_signup(
            username=request.form['username'],
            email=request.form['user_email'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            password=request.form['password'],
            confirm_password=request.form['confirm_password'],
            account_id=int(request.form["account_id"]),
            is_admin=int(request.form["is_admin"])
        )
        return {"redirect": "/login"}
    except (auth.SignupFailedException, AccountsException, UsersException, ExportException) as e:
        return {"error": str(e)}, 400


@bp.route("/markettrust/<int:sales_group_id>", methods=["GET"])
def serve_external_sales_group_viewer(sales_group_id):
    sales_group_row = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)
    return outside_render("/outside/external-sales-group-viewer.html", {"sales_group": sales_group_row})


@bp.route("/retail/<int:eid>", methods=["GET"])
def serve_retail(eid):
    supply_chain_account_ids = []
    original_ranch_match_and_account_link = Matches(g.db).get_matches_with_account_links(
        matches_eid=eid,
        matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
        account_links_sector=SECTORS_NAME_TO_ID["Cow-Calf"],
        matches_order_by="created"
    )
    if len(original_ranch_match_and_account_link) > 0:
        supply_chain_account_ids.append(original_ranch_match_and_account_link[0]["account"])
    feedyard_match_and_account_link = Matches(g.db).get_matches_with_account_links(
        matches_eid=eid,
        matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
        account_links_sector=SECTORS_NAME_TO_ID["Feedlot"]
    )
    if len(feedyard_match_and_account_link) > 0:
        supply_chain_account_ids.append(feedyard_match_and_account_link[0]["account"])
    packer_match_and_account_link = Matches(g.db).get_matches_with_account_links(
        matches_eid=eid,
        matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
        account_links_sector=SECTORS_NAME_TO_ID["Packer"]
    )
    if len(packer_match_and_account_link) > 0:
        supply_chain_account_ids.append(packer_match_and_account_link[0]["account"])
    accounts_retail_data = []
    for account_id in supply_chain_account_ids:
        account = g.db.accounts.get_accounts(id=account_id)[0]
        retail_image_files = Files(g.db).get_files(retail_page_account_id=account["id"], get_url=True)
        accounts_retail_data.append({
            "retail_reference_number": account["id"],
            "retail_sector_name": SECTORS_ID_TO_NAME[account["sector"]] if account["sector"] != SECTORS_NAME_TO_ID["Cow-Calf"] else "Original Ranch",
            "retail_name": account["retail_name"],
            "retail_description": account["retail_description"],
            "retail_image_urls": [file["file_url"] for file in retail_image_files],
            "is_tipping_enabled": account["sector"] == SECTORS_NAME_TO_ID["Cow-Calf"]
        })
    return outside_render("/outside/retail.html", {
        "accounts_retail_data": accounts_retail_data,
        "eid": eid,
        "tip_URL": url_for('outside_bp.serve_tip', eid=eid, account_id=original_ranch_match_and_account_link[0]["account"])
    })


@bp.route("/contact-account", methods=["POST"])
def serve_contact_account():
    send_email_to_admin_users(
        g.db, request.form["retail_reference_number"],
        "New Retail Customer Message",
        render_email("retail_customer_message.html", {
            'name': request.form['name'],
            'phone': request.form['phone'],
            'email': request.form['email'],
            'message': request.form['message']
        })
    )
    retail_url = url_for('outside_bp.serve_retail', eid=request.form["eid"])
    return {"redirect": retail_url}


@bp.route("/tip/<int:eid>/<int:account_id>", methods=["GET"])
def serve_tip(eid, account_id):
    account_with_payouts_enabled = g.db.accounts.get_accounts(id=account_id, is_stripe_payouts_enabled=1)
    if len(account_with_payouts_enabled) > 0:
        original_ranch_match_and_account_link = Matches(g.db).get_matches_with_account_links(
            matches_eid=eid,
            matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
            account_links_sector=SECTORS_NAME_TO_ID["Cow-Calf"],
            matches_order_by="created"
        )
        if original_ranch_match_and_account_link and original_ranch_match_and_account_link[0]["account"] == account_id:
            return outside_render("/outside/tip.html", {
                "stripe_key": STRIPE_PUBLISHABLE_KEY, "account_id": account_id, "eid": eid,
                "retail_URL": url_for('outside_bp.serve_retail', eid=eid), "name": account_with_payouts_enabled[0]["retail_name"],
                "update_tip_URL": url_for('outside_bp.serve_modify_tip')
            })

    return outside_render("/outside/tip.html", {"has_error": True, "message": "Sorry, this operation cannot be completed at this time"})


@bp.route('/tip/', defaults={'tip_id': ''}, methods=['PUT'])
@bp.route("/tip/<int:tip_id>", methods=["PUT"])
def serve_modify_tip(tip_id):
    request_data = loads(request.get_data())
    # best practise to retreive the tip instead of updating it directly
    tip = Tips(g.db).get_tips(id=tip_id, stripe_payment_intent_id=request_data["stripe_payment_intent_id"])
    if tip:
        Tips(g.db).update_tip(id=tip[0]["id"], **request_data)
        return Response(status=HTTP_NO_CONTENT)
    else:
        return Response(status=HTTP_BAD_REQUEST)
