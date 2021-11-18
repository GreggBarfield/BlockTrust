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
import json
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
            # verify user email
            users_table = Users(g.db)
            username = users_table._format_field(required['username'])
            users_table.update_user(username, is_email_verified=1)
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
    auth.employee_login_as_user(user_id)
    UserLoginsByEmployee(g.db).insert_user_logins_by_employee(user_id, employee_id)
    return redirect("/dashboard")


@bp.route("/employee/dashboard/edit-accounts", methods=["GET"])
@crut.require_employee
def serve_edit_account():
    accounts = g.db.accounts.get_accounts()
    return employee_render("/employee/accounts/select-account-to-edit.html", {"accounts": accounts})


@bp.route("/employee/dashboard/edit-account/<int:account_id>", methods=["GET"])
@crut.require_employee
def serve_edit_selected_account(account_id):
    account_row = g.db.accounts.get_by_id(account_id)
    return employee_render("/employee/accounts/edit-selected-account.html", {"account_row": account_row})


@bp.route("/employee/dashboard/edit-account/<int:account_id>/action", methods=["POST"])
@crut.require_employee
def serve_apply_changes_to_account(account_id):
    print(type(request.form["zip_code"]))
    g.db.accounts.update_account(
        account_id=account_id,
        company=request.form["company"],
        address=request.form["address"],
        city=request.form["city"],
        state=request.form["state"],
        zip=request.form["zip_code"]
    )
    return {"redirect": "/employee/dashboard"}
