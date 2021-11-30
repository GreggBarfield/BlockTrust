from flask import (
    request, Blueprint, g, redirect, url_for
)
from ..renderers.employee import employee_render
from ..renderers.email import render_email

from ..database.tables.accounts import Accounts
from ..database.tables.users import Users, UsersException
from ..database.tables.accounts import AccountsException
from ..database.tables.employees import EmployeesException
from ..database.tables.user_logins_by_employee import UserLoginsByEmployee

from ..common_exceptions import ExportException


from ..sectors import sectors_by_id, sectors_by_name
from ..utilities import crut, auth, token
from ..utilities.email import send_email
from random import randint
from ..utilities.general import format_field

from core.config import ROOT as WEBSITE_ROOT


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


@bp.route("/employee/dashboard/invite-account-admin", methods=["GET"])
@crut.require_employee
def serve_invite_account_admin():
    accounts = Accounts(g.db).get_accounts()
    return employee_render("/employee/accounts/invite-account-admin.html", {"accounts": accounts})


@bp.route("/employee/dashboard/invite-account-admin/<int:account_id>", methods=["GET"])
@crut.require_employee
def serve_send_admin_invite(account_id):
    return employee_render("/employee/accounts/send-admin-invite.html", {"account_id": account_id})


@bp.route("/dashboard/invite-account-admin/action", methods=["POST"])
@crut.require_employee
def serve_invite_account_admin_action():
    try:
        email = request.form["email"]
        if len(email) == 0:
            return {"error": "Email is blank."}
        if '@' not in email or '.' not in email or len(email) < 5:
            return {"error": "The email you entered is incomplete."}
        if ' ' in email:
            return {"error": "Spaces cannot be in the email."}
        account_id = request.form["account_id"]
        account_row = g.db.accounts.get_by_id(account_id)
        invite_object = {"admin_email": email, "account_id": account_id}
        invite_string = str(invite_object)
        adminToken = token.generateConfirmationToken(invite_string)
        invite_url = WEBSITE_ROOT + url_for('outside_bp.serve_add_admin_user', invite_token=adminToken)
        send_email(
            "BlockTrust Network Account Invite",
            render_email("invite-admin.html", {
                'invite_url': invite_url,
                'account_name': account_row.name()
            }), email
        )
        return {"redirect": "/employee/dashboard/invite-account-admin"}
    except (Exception, AccountsException) as e:
        return {"error": str(e)}


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
    g.db.accounts.update_account(
        account_id=account_id,
        company=request.form["company"],
        address=request.form["address"],
        city=request.form["city"],
        state=request.form["state"],
        zip=request.form["zip_code"]
    )
    return {"redirect": "/employee/dashboard"}
