from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)
from ..renderers.employee import employee_render
from ..renderers.outside import outside_render

from ..database.tables.users import UsersException
from ..database.tables.accounts import AccountsException
from ..database.tables.employees import EmployeesException

from ..common_exceptions import ExportException

from ..utilities import auth
from ..utilities.email import send_email
from ..utilities import token
from ..renderers.email import render_email

from ..sectors import sectors_by_id
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
        send_email(
            "New BlockTrust Network account",
            render_email("employee/new_account.html", {
                'username': required['email']
            }), required['email'], override=True
        )
        return {"redirect": "/employee/dashboard"}
    except ExportException as e:
        return {"error": str(e)}


@bp.route("/employee/addnewemployee", methods=["GET"])
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
    return "Added Employee"


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
    accounts = g.db.accounts.get_accounts()
    return employee_render("/employee/accounts/view-accounts.html", {"accounts": accounts})


@bp.route("/employee/dashboard/view-accounts/action", methods=["POST"])
def serve_view_account_action():
    redirect_to = "/employee/dashboard/view-accounts/"+request.form["account"]
    return {"redirect": redirect_to}


@bp.route("/employee/dashboard/view-accounts/<tok>", methods=["GET"])
@crut.require_employee
def serve_view_account_users(tok):
    account_users = g.db.users.get_rows_by_account(tok)
    return employee_render("/employee/accounts/view-account-users.html", {"account_users": account_users})


@bp.route("/employee/dashboard/login-as-user/action", methods=["POST"])
def serve_login_as_user_action():
    redirect_to = "/employee/dashboard/login-as-user/"+request.form['user']
    return {"redirect": redirect_to}


@bp.route("/employee/dashboard/login-as-user/<tok>", methods=["GET"])
@crut.require_employee
def serve_login_as_user(tok):
    auth.logout()
    auth.employee_login_as_user(tok)
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
