from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)

from ..renderers.outside import outside_render
from ..database.tables.users import UsersException
from ..common_exceptions import ExportException
from ..utilities import auth
from ..utilities.email import send_email
from ..utilities import token
from ..renderers.email import render_email
from core.config import SUPPORT_GENERAL_EMAIL

bp = Blueprint('outside_bp', __name__)


@bp.route('/', methods=['GET'])
def serve_landing():
    return outside_render('landing.html')


@bp.route('/logout', methods=['GET'])
@bp.route('/log-out', methods=['GET'])
@bp.route('/signout', methods=['GET'])
@bp.route('/sign-out', methods=['GET'])
def serve_logout():
    auth.logout()
    return redirect('/')


@bp.route('/login', methods=['GET'])
@bp.route('/log-in', methods=['GET'])
@bp.route('/signin', methods=['GET'])
@bp.route('/sign-in', methods=['GET'])
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
    except auth.SignupFailedException as e:
        raise ExportException("internal error in Users.login")
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/sign-up', methods=['GET'])
@bp.route('/register', methods=['GET'])
@bp.route('/signup', methods=['GET'])
def serve_signup():
    return outside_render('signup.html')


@bp.route('/signup/action', methods=['POST'])
def serve_signup_action():
    try:
        required = {
            'username': None, 'password': None, 'confirm_password': None,
            'email': None, 'first': None, 'last': None, 'phone': None
        }
        for required_field in required:
            if required_field not in request.form:
                raise ExportException("internal error, {} missing from form".format(required_field))
            required[required_field] = request.form[required_field]

        # Sign up
        try:
            auth.signup(
                username=required['username'],
                email=required['email'],
                phone=required['phone'],
                first=required['first'],
                last=required['last'],
                password=required['password'],
                confirm_password=required['confirm_password']
            )
        except auth.SignupFailedException as e:
            raise ExportException("Signup failed: " + str(e))

        # Sign up worked, now log in and redirect
        try:
            auth.login(
                identifier=required['username'],
                password=required['password']
            )
            return jsonify({"redirect": "/dashboard"})
        except auth.LoginException as e:
            raise ExportException("Sorry, we created your account but had difficulties logging you in. Contact us for help.")
        except auth.UsersException as e:
            raise ExportException("internal error in Users.login")
    except ExportException as e:
        return jsonify({"error": str(e)})

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
        }),
        SUPPORT_GENERAL_EMAIL
    )
    return {}

# Request a password reset


@bp.route('/request_password_reset', methods=['GET'])
def serve_request_password_reset():
    redirect_to = ''
    print("Return request")
    if 'redirect' in request.args:
        redirect_to = request.args['redirect']

    return outside_render('request_password_reset.html', {"redirect_to": redirect_to})

# Request password reset action


@bp.route('/request_password_reset', methods=['POST'])
def serve_password_request_action():
    # Generating token identifier for changing password securely
    userToken = token.generateConfirmationToken(request.form['email'])
    # Creating URL for user to access change password functionality
    password_reset_url = url_for('outside_bp.serve_reset_password', tok=userToken, _external=True)
    # Sending an email to user with the Blocktrust email template and including password change link
    send_email(
            "BlockTrust Network Password change",
            render_email("forgot_password.html", {
                'password_reset_url': password_reset_url
            }), request.form['email']
    )
    return outside_render('passsord_reset_message.html')

# Passowrd reset message page


@bp.route('/password_reset_message', methods=['GET'])
def serve_password_reset_message():
    return outside_render('password_reset_message.html')


# Reset Password


@bp.route('/reset_password/<tok>', methods=['GET'])
def serve_reset_password(tok):
    # Redirecting to password change page
    redirect_to = ''
    try:
        email = token.confirmToken(tok)
        return outside_render('reset_password.html', {"redirect_to": redirect_to})
    except ExportException as e:
        return outside_render('login.html')


@bp.route('/reset_password/<tok>', methods=['POST'])
def serve_reset_password_action(tok):
    try:
        try:
            # Getting the requested new password from the user
            new_password = request.form['password']
            confirm_password = request.form['confirm_password']
            # Getting the user eamil using the encrypted token
            email = token.confirmToken(tok)
            # Changing user password using email as an identifier
            auth.change_password(email, new_password, confirm_password)
            return outside_render('login.html')
        except auth.PasswordChangeFailedException as e:
            raise ExportException(str(e))
    except ExportException as e:
        return outside_render('reset_password.html', {"redirect_to": str(e)})
