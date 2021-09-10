from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)
from ..renderers.internal import internal_render
from ..renderers.outside import outside_render

from ..database.tables.users import UsersException
from ..database.tables.accounts import AccountsException

from ..common_exceptions import ExportException

from ..utilities import auth
from ..utilities import token
from ..utilities.email import send_email

from ..sectors import sectors_by_id
import bcrypt

bp = Blueprint('internal_bp', __name__)


@bp.route("/internal/dashboard", methods=["GET"])
def serve_internal_dashboard():
    return internal_render("/internal/accounts/homepage.html")


@bp.route("/internal/create-new-account", methods=["GET"])
def serve_internal_create_account():
    partners = g.db.accounts.get_partners()
    return internal_render("/internal/accounts/create-new-account.html", {"sectors_by_id": sectors_by_id, "partners": partners})


@bp.route("/internal/signup/action", methods=["POST"])
def serve_internal_signup():
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
                personal_phone=request.form['personal_phone']
            )
        except (auth.SignupFailedException, AccountsException, UsersException) as e:
            raise ExportException("Signup failed: " + str(e))
        return {"redirect": "/internal/dashboard"}
    except ExportException as e:
        return {"error": str(e)}


@bp.route("/internal/login", methods=["GET"])
def serve_internal_login():
    return outside_render("/outside/internal_login.html")


@bp.route("/internal/login/action", methods=["POST"])
def serve_internal_login_action():
    try:
        if 'identifier' not in request.form:
            raise ExportException("internal error, identifier missing from form")

        if 'password' not in request.form:
            raise ExportException("internal error, password missing from form")
        try:
            auth.internal_login(
                identifier=request.form['identifier'],
                password=request.form['password']
            )
            redirect_to = '/internal/dashboard'
            if (
                'requestRedirectTo' in request.form and
                request.form['requestRedirectTo'] is not None and
                request.form['requestRedirectTo'] != ''
            ):
                redirect_to = request.form['requestRedirectTo']
            return jsonify({"redirect": redirect_to})
        except auth.InternalLoginException as e:
            raise ExportException(str(e))
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route("/internal/addnewadmin", methods=["GET"])
def serve_add():
    password = "abcdefghijk"
    g.db.execute(
        """
        INSERT INTO staff(first_name,last_name,username,email,phone,`password`,is_admin)
        values("Nisheet","Thakur","testadminuser","testadminuser@gmil.com","2012087908",%(password)s, 1);
        """,
        {
            "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        }
    )
    return "Hello"
