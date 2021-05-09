from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)

from ..renderers.outside import outside_render
from ..database.tables.users import UsersException
from ..database.tables.accounts import AccountsException
from ..common_exceptions import ExportException
from ..utilities import auth
from ..utilities.email import send_email
from ..renderers.email import render_email
from core.config import SUPPORT_GENERAL_EMAIL
from ..sectors import sectors_by_id

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
        except auth.SignupFailedException as e:
            raise ExportException("internal error in Users.login")
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/sign-up', methods=['GET'])
@bp.route('/register', methods=['GET'])
@bp.route('/signup', methods=['GET'])
def serve_signup():
    return outside_render('signup.html', {
        "sectors_by_id": sectors_by_id
    })


@bp.route('/signup/action', methods=['POST'])
def serve_signup_action():
    try:
        required = {
            'company':None, 'sector':None, 'first_name':None, 'last_name':None,
            'city':None, 'state':None, 'zip_code':None,
            'username':None, 'email':None, 'password':None, 'confirm_password':None
        }
        for required_field in required:
            if required_field not in request.form:
                raise ExportException("internal error, {} missing from form".format(required_field))
            required[required_field] = request.form[required_field]
            if len(required[required_field].strip()) == 0:
                raise ExportException("'" + required_field.capitalize().replace("_"," ") + "' does not have a value")

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
                company = required['company'],
                affiliate_id = request.form['affiliate_id'],
                sector = required['sector'],
                city=required['city'],
                state=required['state'],
                zip_code=required['zip_code']
            )
        except (auth.SignupFailedException, AccountsException, UsersException) as e:
            raise ExportException("Signup failed: " + str(e))

        #TODO: redirect to thank you page (which will ask them to also verify their email). Below line is for testing and should be removed later
        raise ExportException("Success!")
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


@bp.route('/outside/contact-email', methods=['GET'])
def serve_contact_email():
    return jsonify(
        contactEmail=SUPPORT_GENERAL_EMAIL
    )