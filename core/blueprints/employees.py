from flask import (
    request, Blueprint, g, redirect, Response
)
from ..renderers.employee import employee_render
from ..renderers.outside import outside_render

from ..database.tables.accounts import Accounts
from ..database.tables.users import Users, UsersException
from ..database.tables.accounts import AccountsException
from ..database.tables.employees import EmployeesException
from ..database.tables.user_logins_by_employee import UserLoginsByEmployee
from ..database.tables.orders import Orders

from ..common_exceptions import ExportException

from ..utilities.email import send_email
from ..renderers.email import render_email

from ..sectors import sectors_by_id, sectors_by_name
import bcrypt
import json
import flask_excel as excel
from ..utilities import crut, auth

bp = Blueprint('employees_bp', __name__)

excel.init_excel(bp)


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
    subscription_reports = Accounts(g.db).get_accounts(generated_paid=1, selectColumns=["id", "company", "last_updated_timestamp"])
    reports = []
    for tag_store_report in tag_store_reports:
        report = {
            "account": tag_store_report["account"],
            "account_name": "Test account name",  # Need to change after orders table fix
            "amount": tag_store_report["grand_total"],
            "type": "Tag Store",
            "create_timestamp": tag_store_report["create_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
            }
        reports.append(report)
    for subscription_report in subscription_reports:
        report = {
            "account": subscription_report["id"],
            "account_name": subscription_report["company"],
            "amount": 5.99,
            "type": "Subscription",
            "create_timestamp": subscription_report["last_updated_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
        }
        reports.append(report)
    return employee_render("/employee/finance/all-reports.html", {"reports": reports})


@bp.route("/employee/dashboard/select-report-type/subscription-reports", methods=["GET"])
@crut.require_employee
def serve_subscription_reports():
    subscription_reports = Accounts(g.db).get_accounts(generated_paid=1, selectColumns=["id", "company", "last_updated_timestamp"])
    reports = []
    for subscription_report in subscription_reports:
        report = {
            "account": subscription_report["id"],
            "account_name": subscription_report["company"],
            "amount": 5.99,
            "type": "Subscription",
            "create_timestamp": subscription_report["last_updated_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
        }
        reports.append(report)
    return employee_render("/employee/finance/subscription-reports.html", {"reports": reports})


@bp.route("/employee/dashboard/select-report-type/tag-store-reports", methods=["GET"])
@crut.require_employee
def serve_tag_store_reports():
    tag_store_reports = Orders(g.db).get_orders(selectColumns=["account", "grand_total", "create_timestamp"])
    reports = []
    for tag_store_report in tag_store_reports:
        report = {
            "account": tag_store_report["account"],
            "account_name": "Test account name",  # Need to change after orders table fix
            "amount": tag_store_report["grand_total"],
            "type": "Tag Store",
            "create_timestamp": tag_store_report["create_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
            }
        reports.append(report)
    return employee_render("/employee/finance/tag-store-reports.html", {"reports": reports})


@bp.route("/employee/dashboard/select-report-type/all-reports/download", methods=['GET'])
@crut.require_employee
def serve_all_reports_download():
    subscription_reports = Accounts(g.db).get_accounts(generated_paid=1, selectColumns=["id", "company", "last_updated_timestamp"])
    tag_store_reports = Orders(g.db).get_orders(selectColumns=["account", "grand_total", "create_timestamp"])
    reports = []
    reports.append(["Account ID", "Account Name", "Amount", "Transaction type", "Timestamp"])
    for subscription_report in subscription_reports:
        report = [
            subscription_report["id"],
            subscription_report["company"],
            5.99,
            "Subscription",
            subscription_report["last_updated_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
        ]
        reports.append(report)
    for tag_store_report in tag_store_reports:
        report = [
            tag_store_report["account"],
            "Test account name",  # Need to change after orders table fix
            tag_store_report["grand_total"],
            "Tag Store",
            tag_store_report["create_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
        ]
        reports.append(report)
    return excel.make_response_from_array(reports, "xlsx", file_name="all-reports")


@bp.route("/employee/dashboard/select-report-type/subscription-reports/download", methods=["GET"])
@crut.require_employee
def serve_subscription_reports_download():
    subscription_reports = Accounts(g.db).get_accounts(generated_paid=1, selectColumns=["id", "company", "last_updated_timestamp"])
    reports = []
    reports.append(["Account ID", "Account Name", "Amount", "Transaction type", "Timestamp"])
    for subscription_report in subscription_reports:
        report = [
            subscription_report["id"],
            subscription_report["company"],
            5.99,
            "Subscription",
            subscription_report["last_updated_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
        ]
        reports.append(report)
    return excel.make_response_from_array(reports, "xlsx", file_name="subscription-reports")


@bp.route("/employee/dashboard/select-report-type/tag-store-reports/download", methods=["GET"])
@crut.require_employee
def serve_tag_store_reports_download():
    tag_store_reports = Orders(g.db).get_orders(selectColumns=["account", "grand_total", "create_timestamp"])
    reports = []
    reports.append(["Account ID", "Account Name", "Amount", "Transaction type", "Timestamp"])
    for tag_store_report in tag_store_reports:
        report = [
            tag_store_report["account"],
            "Test account name",  # Need to change after orders table fix
            tag_store_report["grand_total"],
            "Tag Store",
            tag_store_report["create_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
        ]
        reports.append(report)
    return excel.make_response_from_array(reports, "xlsx", file_name="tag-store-reports")
