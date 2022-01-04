from flask import (
    jsonify, request, Blueprint, g, redirect, url_for, send_from_directory
)

from ..renderers.outside import outside_render
from ..database.tables.rejected_registrations import RejectedRegistrations
from ..database.tables.users import UsersException
from ..database.tables.accounts import AccountsException
from ..common_exceptions import ExportException
from ..utilities import auth
from ..utilities.email import send_email
from ..utilities import token
from ..renderers.email import render_email
from core.config import SUPPORT_GENERAL_EMAIL, ROOT as WEBSITE_ROOT, SUPPORT_TAG_STORE_EMAIL, RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY, RECAPTCHA_MIN_SCORE, IPINFO_TOKEN, CHECK_IP
from ..sectors import sectors_by_name
from requests import post


bp = Blueprint('outside_bp', __name__)


@bp.route('/', methods=['GET'])
def serve_landing():
    return outside_render('landing.html')


@bp.route('/logout', methods=['GET'])
def serve_logout():
    auth.logout()
    return redirect('/')


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
            auth.login(
                identifier=request.form['identifier'],
                password=request.form['password']
            )
            redirect_to = '/dashboard'
            if (
                'requestRedirectTo' in request.form and
                request.form['requestRedirectTo'] is not None and
                request.form['requestRedirectTo'] != ''
            ):
                redirect_to = request.form['requestRedirectTo']
            return jsonify({"redirect": redirect_to})
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
    # Only add cowcalf partners
    cow_calf_sector_id = sectors_by_name['Cow-Calf']
    partners = g.db.accounts.get_accounts(
        sector=cow_calf_sector_id,
        is_partner=1,
        show_on_signup=1
    )
    return outside_render('signup.html', {
        "default_sector_id": cow_calf_sector_id,  # setting default sector_id to cowcalf
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
    return outside_render('password_reset_message.html')


# Reset Password


@bp.route('/reset-password/<tok>', methods=['GET'])
def serve_reset_password(tok):
    # Redirecting to password change page
    redirect_to = tok
    try:
        email = token.confirmToken(tok)
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
        auth.change_user_password(email, new_password, confirm_password)
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
    return outside_render('email_verified.html')


@bp.route('/email_not_verified', methods=['GET'])
def serve_email_not_confirmed():
    return outside_render('email_not_verified.html')


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
#             "sectors_by_id": sectors_by_id,
#             "redirect_to": '/checkout'
#             })


# # Invoice routes
# @bp.route('/invoice', methods=['GET'])
# def serve_invoice():
#     return outside_render('shop/invoice.html')


@bp.route('/add-user/<string:invite_token>', methods=['GET'])
def serve_add_user(invite_token):
    try:
        invite_string = token.confirmToken(invite_token)
        invite_object = eval(invite_string)
        user_email = invite_object["user_email"]
        account_name = invite_object["current_account"]
        account_id = invite_object["current_account_id"]
        return outside_render("/outside/add-user-signup.html", {
            "user_email": user_email,
            "account_name": account_name,
            "account_id": account_id,
            "is_admin": 0
            })
    except Exception as e:
        return outside_render("/outside/error.html", {"error_reason": "The Invite link is Invalid or Expired"})


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


@bp.route('/rfid-tags', methods=["GET"])
def serve_rfid_tags():
    return outside_render("/outside/rfid_tags.html")


@bp.route('/employee/login', methods=['GET'])
def serve_employee_login():
    return outside_render('employee-login.html')


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


@bp.route('/add-admin/<string:invite_token>', methods=["GET"])
def serve_add_admin_user(invite_token):
    try:
        invite_string = token.confirmToken(invite_token)
        invite_object = eval(invite_string)
        account_id = invite_object["account_id"]
        admin_email = invite_object["admin_email"]
        account_row = g.db.accounts.get_by_id(account_id)
        return outside_render("/outside/add-user-signup.html", {
            "user_email": admin_email,
            "account_name": account_row.name(),
            "account_id": account_id,
            "is_admin": 1
            })
    except Exception as e:
        return outside_render("/outside/error.html", {"error_reason": "The Invite link is Invalid or Expired"})