from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)
from ..renderers.employee import employee_render
from ..renderers.outside import outside_render

from ..database.tables.users import UsersException
from ..database.tables.accounts import AccountsException

from ..common_exceptions import ExportException

from ..utilities import auth
from ..utilities import token
from ..utilities.email import send_email

from ..sectors import sectors_by_id
import bcrypt
from ..utilities import crut, auth


bp = Blueprint('employees_bp', __name__)


@bp.route('/employee/dashboard', methods=['GET'])
@crut.require_employee
def serve_employee_dashboard():
    return employee_render("/employee/homepage.html")


@bp.route("/employee/dashboard/create-new-account", methods=["GET"])
@crut.require_employee
def serve_employee_create_account():
    partners = g.db.accounts.get_partners()
    return employee_render("/employee/accounts/create-new-account.html", {"sectors_by_id": sectors_by_id, "partners": partners})


@bp.route("/employee/dashboard/signup/action", methods=["POST"])
def serve_employee_signup():
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
        return {"redirect": "/employee/dashboard"}
    except ExportException as e:
        return {"error": str(e)}


@bp.route("/employee/addnewadmin", methods=["GET"])
def serve_add():
    password = "abcdefghijk"
    g.db.execute(
        """
        INSERT INTO employees(first_name,last_name,username,email,phone,`password`)
        values("Nisheet","Thakur","testadminuser","testadminuser@gmil.com","2012087908",%(password)s);
        """,
        {
            "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        }
    )
    return "Hello"


@bp.route("/employee/dashboard/add-new-employee", methods=["GET"])
@crut.require_employee
def serve_add_new_employee():
    return employee_render("/employee/add_new_employee/add-new-employee.html")
