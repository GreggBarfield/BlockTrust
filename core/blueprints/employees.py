from flask import (
    request, Blueprint, g, redirect, url_for, Response
)
from ..renderers.employee import employee_render
from ..renderers.email import render_email

from ..database.tables.accounts import Accounts
from ..database.tables.api_inserts import ApiInserts
from ..database.tables.debug_logs import DebugLogs
from ..database.tables.invited_users import InvitedUsers
from ..database.tables.users import Users, UsersException
from ..database.tables.accounts import AccountsException
from ..database.tables.employees import EmployeesException
from ..database.tables.notifications import Notifications
from ..database.tables.notification_recipients import NotificationRecipients
from ..database.tables.orders import Orders
from ..database.tables.user_logins_by_employee import UserLoginsByEmployee
from ..database.tables.notifications import notification_type_name_to_id, notification_type_id_to_name
from ..database import scripts
from ..database.combinations import perform_new_account_actions
from ..database.tables.event_logs import event_type_by_name
from ..common_exceptions import ExportException

from ..sectors import sectors_by_id, sectors_by_name
from ..utilities import crut, auth, token
from ..utilities.email import send_email
from random import randint
from ..utilities.general_utilities import format_field, validate_email
import flask_excel as excel
from core.config import ROOT as WEBSITE_ROOT, FLATFILE_LICENSE
import json

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
    return employee_render("/employee/accounts/create-new-account.html", {
        "sectors_by_name": sectors_by_name,
        "partners": partners
        })


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
        account_obj = g.db.accounts.create_account(
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
        username = "DefaultAdminAccount#" + str(account_obj.id())
        first_name = "Default"
        last_name = "Admin"
        # password is a random 8 digit number
        password = str(randint(10000000, 99999999))
        user = g.db.users.create_pseudo_user(username, password, first_name, last_name)
        # Assigning user as admin
        account_obj.add_user(user, 1)

        perform_new_account_actions(g.db, account_obj.id(), user.id(), event_type_by_name["Account Created"], g.employee.id())

        return {"redirect": "/employee/dashboard"}
    except (ExportException, AccountsException, UsersException, ValueError) as e:
        return {"error": str(e)}, 400


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
        return {"error": str(e)}, 400


@bp.route("/employee/dashboard/view-accounts", methods=["GET"])
@crut.require_employee
def serve_view_account():
    accounts_and_account_admins = []
    accounts = Accounts(g.db).get_accounts()
    for account in accounts:
        account['company'] = account['company'].upper()
        admin_user = g.db.account_users.get_account_users(account=account["id"], is_admin=1)
        account["account_partner_name"] = g.db.accounts.get_accounts(id=account["partner_account"])[0]["company"] if account["partner_account"] is not None else ""
        if(len(admin_user) > 0):
            user = g.db.users.get_user_by_id(admin_user[0]['user'])
            if user is not None and (user.is_email_verified() == 1 or user.is_system_generated() == 1):
                account["account_admin_name"] = user.first_name() + " " + user.last_name()
                account["account_admin_user_id"] = user.id()
                account["account_admin_email"] = user.email()
                accounts_and_account_admins.append(account)
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


@bp.route("/employee/dashboard/accounts-with-option-to-invite-admin", methods=["GET"])
@crut.require_employee
def serve_accounts_with_option_to_invite_admin():
    accounts = Accounts(g.db).get_accounts()
    return employee_render("/employee/accounts/accounts-with-option-to-invite-admin.html", {"accounts": accounts})


@bp.route("/employee/dashboard/invite-admin/<int:account_id>", methods=["GET"])
@crut.require_employee
def serve_invite_admin(account_id):
    return employee_render("/employee/accounts/invite-admin.html", {"account_id": account_id})


@bp.route("/employee/dashboard/invite-admin/<int:account_id>/action", methods=["POST"])
@crut.require_employee
def serve_invite_admin_action(account_id):
    try:
        email = request.form["email"]
        email_validation = validate_email(email)
        if email_validation["success"]:
            user = g.db.users.get_by_email(email)
            if user is not None:
                return {"error": "Email is already being used."}, 400
            account_row = g.db.accounts.get_account_by_id(account_id)
            invite_object = {"admin_email": email, "account_id": account_id}
            invite_string = str(invite_object)
            adminToken = token.generateConfirmationToken(invite_string)
            invite_url = WEBSITE_ROOT + url_for('outside_bp.serve_add_admin_user', invite_token=adminToken)
            send_email(
                "BlockTrust Network Account Invite",
                render_email("invite-admin-email.html", {
                    'invite_url': invite_url,
                    'account_name': account_row.name()
                }), email
            )
            InvitedUsers(g.db).insert_invited_user(email, g.employee.id(), 1, 1)
            return {"redirect": "/employee/dashboard/accounts-with-option-to-invite-admin"}
        else:
            raise Exception(email_validation["message"])
    except (Exception, AccountsException) as e:
        return {"error": str(e)}, 400


@bp.route("/employee/dashboard/edit-accounts", methods=["GET"])
@crut.require_employee
def serve_edit_account():
    accounts = g.db.accounts.get_accounts()
    return employee_render("/employee/accounts/select-account-to-edit.html", {"accounts": accounts})


@bp.route("/employee/dashboard/edit-account/<int:account_id>", methods=["GET", "POST"])
@crut.require_employee
def serve_edit_selected_account(account_id):
    if request.method == "GET":
        account_row = g.db.accounts.get_account_by_id(account_id)
        partners = g.db.accounts.get_accounts(
            sector=sectors_by_name["Cow-Calf"],
            is_partner=1,
            is_partner_used_for_signup=1
        )
        return employee_render("/employee/accounts/edit-selected-account.html", {"account_row": account_row, "partners": partners})
    if request.method == "POST":
        g.db.accounts.update_account(
            account_id=account_id,
            partner_account=format_field(request.form["partner"]),
            affiliate_id=format_field(request.form["affiliate_id"]),
            company=format_field(request.form["company"]),
            phone=format_field(request.form["phone"]),
            address=format_field(request.form["address"]),
            city=format_field(request.form["city"]),
            state=format_field(request.form["state"]),
            zip=format_field(request.form["zip_code"])
        )
        return {"redirect": "/employee/dashboard"}


@bp.route("/employee/dashboard/edit-partner/<int:partner_id>", methods=["GET", "POST"])
@crut.require_employee
def serve_edit_selected_partner(partner_id):
    if request.method == "GET":
        partner_rows = g.db.accounts.get_accounts(id=partner_id)
        partner_row = partner_rows[0] if len(partner_rows) > 0 else {}
        return employee_render("/employee/accounts/edit-selected-partner.html", {"partner_row": partner_row})
    if request.method == "POST":
        is_partner_used_for_signup = 0
        if(format_field(request.form["is_partner_used_for_signup"]) == 'true'):
            is_partner_used_for_signup = 1
        g.db.accounts.update_partner(
            account_id=partner_id,
            company=format_field(request.form["company"]),
            phone=format_field(request.form["phone"]),
            address=format_field(request.form["address"]),
            city=format_field(request.form["city"]),
            state=format_field(request.form["state"]),
            zip=format_field(request.form["zip_code"]),
            is_partner_used_for_signup=is_partner_used_for_signup
        )
        return {"redirect": "/employee/dashboard"}


@bp.route("/employee/dashboard/view-partners", methods=["GET"])
def serve_view_partners():
    partner_rows = g.db.accounts.get_accounts(is_partner=1)
    return employee_render("/employee/accounts/partners.html", {"partner_rows": partner_rows, "sectors_by_id": sectors_by_id})


@bp.route("/employee/dashboard/create-new-partner", methods=["GET"])
def serve_create_new_partner():
    return employee_render("/employee/accounts/create-new-partner.html", {
        "sectors_by_name": sectors_by_name
        })


@bp.route("/employee/dashboard/create-new-partner/action", methods=["POST"])
def serve_create_new_partner_action():
    try:
        required = {
            'company': None, 'sector': None, 'address': None, 'city': None,
            'state': None, 'zip_code': None, 'phone': None, 'contact_name': None,
            'contact_email': None
        }
        for required_field in required:
            if required_field not in request.form:
                raise ExportException("internal error, {} missing from form".format(required_field))
            required[required_field] = request.form[required_field]
            if len(required[required_field].strip()) == 0:
                raise ExportException("'" + required_field.capitalize().replace("_", " ") + "' does not have a value")
        # Creating an account without an admin
        is_partner_used_for_signup = 0
        if request.form["used_for_signup"] == "true":
            is_partner_used_for_signup = 1
        account = g.db.accounts.create_partner(
                phone=format_field(request.form['phone']),
                company=format_field(required['company']),
                sector=format_field(required['sector']),
                partner_contact_name=format_field(required['contact_name']),
                partner_contact_email=format_field(required['contact_email']),
                address=format_field(required['address']),
                city=format_field(required['city']),
                state=format_field(required['state']),
                zip=format_field(required['zip_code']),
                is_partner_used_for_signup=is_partner_used_for_signup
        )
        return {"redirect": "/employee/dashboard/view-partners"}
    except (ExportException, AccountsException, UsersException, ValueError) as e:
        return {"error": str(e)}


@bp.route("/employee/upload-packer-data", methods=["GET", "POST"])
def serve_upload_packer_data():
    if request.method == 'POST':
        data = json.loads(request.data)
        #partner account is assumed to be ILS
        partner_account = g.db.accounts.get_accounts(company_like="ILS", sector=sectors_by_name["Feedlot"], is_partner=1)
        try:
            for row in data["eids"]:
                ApiInserts(g.db).insert(partner_account[0]["id"], "EMP", "PackerDataUpload", row)
            return "", 200
        except Exception as e:
            return {'error':{'message': str(e)}}, 400
    elif request.method == 'GET':
        return employee_render("data/upload-packer-data.html",  {"employee": g.employee, "license": FLATFILE_LICENSE})


@bp.route("/employee/dashboard/notifications", methods=["GET"])
def serve_notifications():
    notifications = Notifications(g.db).get_notifications()
    return employee_render("/employee/accounts/notifications/notifications.html", {
        "notifications": notifications,
        "notification_type_id_to_name": notification_type_id_to_name
        })


@bp.route("/employee/dashboard/create-new-notification", methods=["GET"])
def serve_create_new_notifcation():
    return employee_render("/employee/accounts/notifications/create-new-notification.html")


@bp.route("/employee/dashboard/create-new-notification/global", methods=["GET"])
def serve_create_global_notification():
    return employee_render("/employee/accounts/notifications/create-global-notification.html")


@bp.route("/employee/dashboard/create-new-notification/global/action", methods=["POST"])
def serve_create_global_notification_action():
    notification_id = Notifications(g.db).insert_notification(
        subject=request.form["subject"],
        message=request.form["message"],
        notification_type=notification_type_name_to_id["Global"]
    )
    NotificationRecipients(g.db).insert_global_notification_recipients(notification_id=notification_id)
    return {"redirect": "/employee/dashboard/notifications"}


@bp.route("/employee/dashboard/create-new-notification/partner", methods=["GET"])
def serve_create_partner_notification():
    partners = g.db.accounts.get_accounts(is_partner=1)
    return employee_render("/employee/accounts/notifications/create-partner-notification.html", {"partners": partners})


@bp.route("/employee/dashboard/create-new-notification/partner/action", methods=["POST"])
def serve_create_partner_notification_action():
    notification_id = Notifications(g.db).insert_notification(
        subject=request.form["subject"],
        message=request.form["message"],
        notification_type=notification_type_name_to_id["Partner"]
    )
    NotificationRecipients(g.db).insert_partner_notification_recipients(
        notification_id=notification_id,
        partner_id=request.form["partner"]
    )
    return {"redirect": "/employee/dashboard/notifications"}


@bp.route("/employee/dashboard/create-new-notification/sector", methods=["GET"])
def serve_create_sector_notification():
    return employee_render("/employee/accounts/notifications/create-sector-notification.html", {"sectors": sectors_by_id})


@bp.route("/employee/dashboard/create-new-notification/sector/action", methods=["POST"])
def serve_create_sector_notification_action():
    notification_id = Notifications(g.db).insert_notification(
        subject=request.form["subject"],
        message=request.form["message"],
        notification_type=notification_type_name_to_id["Sector"]
    )
    NotificationRecipients(g.db).insert_sector_notification_recipients(
        notification_id=notification_id,
        sector=request.form["sector"]
    )
    return {"redirect": "/employee/dashboard/notifications"}


@bp.route("/employee/dashboard/archive-notification", methods=["POST"])
def serve_archive_notification():
    Notifications(g.db).update_notification(id=int(request.json["notification_id"]), is_archived=1)
    return {}


@bp.route("/employee/update-account-paid-status", methods=["POST"])
@crut.require_employee
def serve_update_account_paid_status():
    request_data = json.loads(request.data)
    account_id = int(request_data["account_id"])
    paid_status = bool(request_data["paid_status"])
    if paid_status:
        g.db.accounts.update_account(account_id, manual_paid=1)
    else:
        account = g.db.accounts.get_account_by_id(account_id)
        if account.stripe_paid() == 1:
            raise ExportException(f"This account ({account_id}) has paid through stripe and cannot be marked unpaid")
        g.db.accounts.update_account(account_id, manual_paid=0)
    return {}, 200


@bp.route('/employee/dashboard/animals/', defaults={'animal_eid': ''}, methods=['GET'])
@bp.route("/employee/dashboard/animals/<int:animal_eid>", methods=["GET"])
def serve_animal_eid(animal_eid):
    animal = g.db.matches.get_animal_by_eid(animal_eid)
    if len(animal.matches) == 0:
        return employee_render("animals/animal_not_found.html", {"eid": animal_eid})
    else:
        return employee_render("animals/animal.html", {"animal": animal})


@bp.route("/employee/run/<string:script>", methods=["POST"])
@crut.require_employee
def serve_run_script(script):
    if script in scripts.get_available_scripts():
        script_function = getattr(scripts, script)
        kwargs = {}
        kwargs["db"] = g.db
        kwargs["dry_run"] = bool(request.args.get("dry_run")) if request.args.get("dry_run") else False
        if not (log := script_function(**kwargs)):
            log = {}
        log["runner"] = "Employee"
        log["runner_id"] = g.employee.id()
        DebugLogs(g.db).insert_debug_log("Scripts", f"{script} invoked successfully by employee id: {g.employee.id()}", None, log)
        return ("", 204)
    else:
        return script + " not found", 404


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
    total = 0
    for tag_store_report in tag_store_reports:
        report = {
            "account": tag_store_report["account"],
            "account_name": "Test account name",  # Need to change after orders table fix
            "amount": tag_store_report["grand_total"],
            "type": "Tag Store",
            "create_timestamp": tag_store_report["create_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
            }
        reports.append(report)
        total = total + tag_store_report["grand_total"]
    for subscription_report in subscription_reports:
        report = {
            "account": subscription_report["id"],
            "account_name": subscription_report["company"],
            "amount": 5.99,
            "type": "Subscription",
            "create_timestamp": subscription_report["last_updated_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
        }
        reports.append(report)
        total = total + 5.99
    return employee_render("/employee/finance/all-reports.html", {"reports": reports, "total": round(total, 2)})


@bp.route("/employee/dashboard/select-report-type/subscription-reports", methods=["GET"])
@crut.require_employee
def serve_subscription_reports():
    subscription_reports = Accounts(g.db).get_accounts(generated_paid=1, selectColumns=["id", "company", "last_updated_timestamp"])
    reports = []
    total = 0
    for subscription_report in subscription_reports:
        report = {
            "account": subscription_report["id"],
            "account_name": subscription_report["company"],
            "amount": 5.99,
            "type": "Subscription",
            "create_timestamp": subscription_report["last_updated_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
        }
        reports.append(report)
        total = total + 5.99
    return employee_render("/employee/finance/subscription-reports.html", {"reports": reports, "total": round(total, 2)})


@bp.route("/employee/dashboard/select-report-type/tag-store-reports", methods=["GET"])
@crut.require_employee
def serve_tag_store_reports():
    tag_store_reports = Orders(g.db).get_orders(selectColumns=["account", "grand_total", "create_timestamp"])
    reports = []
    total = 0
    for tag_store_report in tag_store_reports:
        report = {
            "account": tag_store_report["account"],
            "account_name": "Test account name",  # Need to change after orders table fix
            "amount": tag_store_report["grand_total"],
            "type": "Tag Store",
            "create_timestamp": tag_store_report["create_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M")
            }
        reports.append(report)
        total = total + tag_store_report["grand_total"]
    return employee_render("/employee/finance/tag-store-reports.html", {"reports": reports, "total": round(total, 2)})


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

