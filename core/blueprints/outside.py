from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)

from renderers.outside import outside_render
from database.tables.users import UsersException, LoginException, SignupFailedException
from common_exceptions import ExportException

bp = Blueprint('outside_bp', __name__)

@bp.route('/', methods=['GET'])
def serve_landing():
    return outside_render('landing.html')

@bp.route('/logout', methods=['GET'])
@bp.route('/log-out', methods=['GET'])
@bp.route('/signout', methods=['GET'])
@bp.route('/sign-out', methods=['GET'])
def serve_logout():
    g.db.users.logout()
    return redirect('/')

@bp.route('/login', methods=['GET'])
@bp.route('/log-in', methods=['GET'])
@bp.route('/signin', methods=['GET'])
@bp.route('/sign-in', methods=['GET'])
def serve_login():
    return outside_render('login.html')


@bp.route('/login/action', methods=['POST'])
def serve_login_action():
    try:
        if 'identifier' not in request.form:
            raise ExportException("internal error, identifier missing from form")

        if 'password' not in request.form:
            raise ExportException("internal error, password missing from form")
        try:
            g.db.users.login(
                identifier=request.form['identifier'],
                password=request.form['password']
            )
            return jsonify({"redirect": "/dashboard"})
        except LoginException as e:
            raise ExportException(str(e))
        except UsersException as e:
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
            'username':None, 'password':None, 'confirm_password':None,
            'email':None, 'first':None, 'last':None, 'phone':None
        }
        for required_field in required:
            if required_field not in request.form:
                raise ExportException("internal error, {} missing from form".format(required_field))
            required[required_field] = request.form[required_field]
    
        # Sign up
        try:
            g.db.users.signup(
                username=required['username'],
                email=required['email'],
                phone=required['phone'],
                first=required['first'],
                last=required['last'],
                password=required['password'],
                confirm_password=required['confirm_password']
            )
        except SignupFailedException as e:
            raise ExportException("Signup failed: " + str(e))
    
        # Sign up worked, now log in and redirect
        try:
            g.db.users.login(
                identifier=required['username'],
                password=required['password']
            )
            return jsonify({"redirect": "/dashboard"})
        except LoginException as e:
            raise ExportException("Sorry, we created your account but had difficulties logging you in. Contact us for help.")
        except UsersException as e:
            raise ExportException("internal error in Users.login")
    except ExportException as e:
        return jsonify({"error": str(e)})

# About us

@bp.route('/about-us/<path:path>', methods=['GET'])
def serve_about_us(path):
    if '.' in path:
        return "Error accessing " + path + ": '.' should not be included"
    return outside_render('about-us/' + path + '.html')

# Our Partners

@bp.route('/our-partners/<path:path>', methods=['GET'])
def serve_our_partners(path):
    if '.' in path:
        return "Error accessing " + path + ": '.' should not be included"
    return outside_render('our-partners/' + path + '.html')

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
