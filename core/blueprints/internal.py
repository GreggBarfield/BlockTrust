from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)
from ..renderers.internal import internal_render

from ..database.tables.users import UsersException
from ..database.tables.accounts import AccountsException
from ..common_exceptions import ExportException
from ..utilities import auth
from ..utilities.email import send_email
from ..utilities import token

from ..sectors import sectors_by_id

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
