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


from ..sectors import sectors_by_id, sectors_by_name
import bcrypt
from ..utilities import crut, auth
from random import randint
from ..utilities.general_utilities import format_field


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
            'company': None, 'sector': None, 'address': None, 'city': None,
            'state': None, 'zip_code': None, 'phone': None, 'company': None
        }
        for required_field in required:
            if required_field not in request.form:
                raise ExportException("internal error, {} missing from form".format(required_field))
            required[required_field] = request.form[required_field]
            if len(required[required_field].strip()) == 0:
                raise ExportException("'" + required_field.capitalize().replace("_", " ") + "' does not have a value")

        # Creating an account without an admin
        account = g.db.accounts.create_account(
                phone=format_field(request.form['phone']),
                company=format_field(required['company']),
                partner=format_field(request.form['partner']),
                affiliate_id=format_field(request.form['affiliate_id']),
                sector=format_field(required['sector']),
                address=format_field(required['address']),
                city=format_field(required['city']),
                state=format_field(required['state']),
                zip=format_field(required['zip_code'])
        )

        # Creating a default pseudo admin user for created account
        username = "DefaultAdminAccount#" + str(account.id())
        first_name = "Default"
        last_name = "Admin"
        # password is a random 8 digit number
        password = str(randint(10000000, 99999999))
        user = g.db.users.create_pseudo_user(username, password, first_name, last_name)
        # Assigning user as admin
        account.add_user(user, 1)

        return {"redirect": "/employee/dashboard"}
    except (ExportException, AccountsException, UsersException, ValueError) as e:
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
    accounts_and_account_admins = Accounts(g.db).get_accounts()
    for account in accounts_and_account_admins:
        account['company'] = account['company'].upper()
        account_admin_user_id = 0
        account_admin_username = ""
        admin_user = g.db.account_users.get_account_users(account=account["id"], is_admin=1)
        if(len(admin_user) >= 1):
            user = g.db.users.get_user_by_id(admin_user[0]['user'])
            if user is not None:
                account_admin_user_id = user.id()
                account_admin_username = user.email()
                account["account_admin_user_id"] = account_admin_user_id
                account["account_admin_username"] = account_admin_username
            else:
                account["account_admin_user_id"] = account_admin_user_id
                account["account_admin_username"] = account_admin_username
        else:
            account["account_admin_user_id"] = account_admin_user_id
            account["account_admin_username"] = account_admin_username
    accounts_and_account_admins = sorted(accounts_and_account_admins, key=lambda i: i['company'])
    return employee_render("/employee/accounts/view-accounts.html", {"accounts_and_account_admins": accounts_and_account_admins, "sectors_by_id": sectors_by_id})


@bp.route("/employee/dashboard/login-as-user/<int:user_id>", methods=["GET"])
@crut.require_employee
def serve_login_as_user(user_id):
    employee_id = g.employee.id()
    auth.logout()
    auth.employee_login_as_user(user_id, employee_id)
    UserLoginsByEmployee(g.db).insert_user_logins_by_employee(user_id, employee_id)
    return redirect("/dashboard")
