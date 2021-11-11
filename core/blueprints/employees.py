from flask import (
    request, Blueprint, g, redirect
)
from ..renderers.employee import employee_render
from ..renderers.outside import outside_render

from ..database.tables.accounts import Accounts
from ..database.tables.users import Users, UsersException
from ..database.tables.accounts import AccountsException
from ..database.tables.employees import EmployeesException
from ..database.tables.user_logins_by_employee import UserLoginsByEmployee

from ..common_exceptions import ExportException

from ..utilities.email import send_email
from ..renderers.email import render_email

from ..sectors import sectors_by_id, sectors_by_name
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
    partners = Accounts(g.db).get_accounts(is_partner=1)
    return employee_render("/employee/accounts/create-new-account.html", {"sectors_by_name": sectors_by_name, "partners": partners})


@bp.route("/employee/dashboard/create-new-account/action", methods=["POST"])
def serve_employee_create_account_action():
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
            auth.confirm(required["email"])
        except (auth.SignupFailedException, AccountsException, UsersException) as e:
            raise ExportException("Signup failed: " + str(e))
        send_email(
            "New BlockTrust Network account",
            render_email("employee/new-account.html", {
                'username': required['email']
            }), required['email']
        )
        return {"redirect": "/employee/dashboard"}
    except ExportException as e:
        return {"error": str(e)}


@bp.route("/employee/dashboard/add-new-employee", methods=["GET"])
@crut.require_employee
def serve_add_new_employee():
    return employee_render("/employee/add_new_employee/add-new-employee.html")


@bp.route("/employee/dashboard/add-new-employee/action", methods=["POST"])
def serve_add_new_employee_action():
    try:
        required = {
            'first_name': None, 'last_name': None, 'phone': None, 'username': None,
            'email': None, 'password': None, 'confirm_password': None
        }
        for required_field in required:
            if required_field not in request.form:
                raise ExportException("internal error, {} missing from form".format(required_field))
            required[required_field] = request.form[required_field]
            if len(required[required_field].strip()) == 0:
                raise ExportException("'" + required_field.capitalize().replace("_", " ") + "' does not have a value")
        auth.employee_signup(
                first_name=required['first_name'],
                last_name=required['last_name'],
                username=required['username'],
                email=required['email'],
                phone=required['phone'],
                password=required['password'],
                confirm_password=required['confirm_password']
            )
        return {"redirect": "/employee/dashboard"}
    except (auth.SignupFailedException, EmployeesException) as e:
        return {"error": str(e)}


@bp.route("/employee/dashboard/view-accounts", methods=["GET"])
@crut.require_employee
def serve_view_account():
    accounts = Accounts(g.db).get_accounts(is_partner=0)
    return employee_render("/employee/accounts/view-accounts.html", {"accounts": accounts})


@bp.route("/employee/dashboard/view-accounts/<int:account_id>", methods=["GET"])
@crut.require_employee
def serve_view_account_users(account_id):
    account_users = Users(g.db).get_rows_by_account(account_id)
    return employee_render("/employee/accounts/view-account-users.html", {"account_users": account_users})


@bp.route("/employee/dashboard/login-as-user/<int:user_id>", methods=["GET"])
@crut.require_employee
def serve_login_as_user(user_id):
    employee_id = g.employee.id()
    auth.logout()
    auth.employee_login_as_user(user_id)
    UserLoginsByEmployee(g.db).insert_user_logins_by_employee(user_id, employee_id)
    return redirect("/dashboard")
