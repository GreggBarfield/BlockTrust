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
from ..database.tables.transactions import Transactions
from ..database.tables.transactions import transaction_type, transaction_type_names
from ..database.tables.orders import Orders

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
        except (auth.SignupFailedException, AccountsException, UsersException) as e:
            raise ExportException("Signup failed: " + str(e))
        send_email(
            "New BlockTrust Network account",
            render_email("employee/new-account.html", {
                'username': required['email']
            }), required['email'], override=True
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


@bp.route("/employee/dashboard/edit-an-account", methods=["GET"])
@crut.require_employee
def serve_edit_account():
    accounts = g.db.accounts.get_accounts()
    return employee_render("/employee/accounts/select-account-to-edit.html", {"accounts": accounts})


@bp.route("/employee/dashboard/edit-an-account/action", methods=["POST"])
def serve_edit_account_action():
    redirect_to = "/employee/dashboard/edit-an-account/"+request.form['account']
    return {"redirect": redirect_to}


@bp.route("/employee/dashboard/edit-an-account/<tok>", methods=["GET"])
@crut.require_employee
def serve_edit_selected_account(tok):
    account_row = g.db.accounts.get_by_id(tok)
    return employee_render("/employee/accounts/edit-selected-account.html", {"account_row": account_row})


@bp.route("/employee/dashboard/edit-an-account/apply-changes", methods=["POST"])
def serve_apply_changes_to_account():
    g.db.accounts.update_account(
        account_id=request.form["id"],
        company=request.form["company"],
        address=request.form["address"],
        city=request.form["city"],
        state=request.form["state"],
        zip=request.form["zip_code"]
    )
    return {"redirect": "/employee/dashboard"}


@bp.route("/employee/dashboard/select-report-type", methods=["GET"])
@crut.require_employee
def serve_select_report_type():
    return employee_render("/employee/finance/select-report-type.html")


@bp.route("/employee/dashboard/select-report-type/all-reports", methods=["GET"])
@crut.require_employee
def serve_all_reports():
    tag_store_reports = Orders(g.db).get_orders(selectColumns=["account", "grand_total", "create_timestamp"])
    print(tag_store_reports)
    reports = Transactions(g.db).get_transactions()
    return employee_render("/employee/finance/all-reports.html", {"reports": reports, "transaction_type_names": transaction_type_names})


@bp.route("/employee/dashboard/select-report-type/subscription-reports", methods=["GET"])
@crut.require_employee
def serve_subscription_reports():
    reports = Transactions(g.db).get_transactions(type=transaction_type["Subscription"])
    return employee_render("/employee/finance/partial-reports.html", {"reports": reports, "transaction_type_names": transaction_type_names})


@bp.route("/employee/dashboard/select-report-type/tag-store-reports", methods=["GET"])
@crut.require_employee
def serve_tag_store_reports():
    reports = Transactions(g.db).get_transactions(type=transaction_type["Tag-Store"])
    return employee_render("/employee/finance/partial-reports.html", {"reports": reports, "transaction_type_names": transaction_type_names})
