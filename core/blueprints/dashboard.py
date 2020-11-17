from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)

from renderers.dashboard import dashboard_render

from sectors import sectors_by_id

from common_exceptions import ExportException

from database.tables.account_users import NoAccountUserFound
from database.tables.accounts import AccountsException
from database.objects.account import AccountException

bp = Blueprint('dashboard_bp', __name__)

@bp.route('/dashboard', methods=['GET'])
def serve_dashboard():
    if g.user is None:
        return redirect('/')
    
    account_users = g.db.account_users.get_by_user(g.user)

    if len(account_users) == 0:
        # No accounts
        return dashboard_render("accounts/welcome.html")
    elif g.account is not None:
        return redirect('/dashboard/accounts/' + str(g.account.id()))
    elif len(account_users) == 1:
        g.db.accounts.session_start(account_users[0].account_id())
        return redirect('/dashboard/accounts/' + str(account_users[0].account_id()))
    else:
        return redirect('/dashboard/accounts')

# Accounts

@bp.route('/dashboard/accounts/new-account', methods=['GET'])
def serve_accounts_new_account():
    if g.user is None:
        return redirect('/')

    return dashboard_render("accounts/new_account.html", {
        "sectors_by_id": sectors_by_id
    })


@bp.route('/dashboard/accounts/new-account/action', methods=['POST'])
def serve_accounts_new_account_action():
    try:
        required = {
            'name': None, 'company': None, 'sector': None
        }
        for required_field in required:
            if required_field not in request.form:
                raise ExportException("internal error, {} missing from form".format(required_field))
            required[required_field] = request.form[required_field]
    
        # Create Account
        try:
            sector_id = -1
            try:
                sector_id = int(required['sector'])
            except:
                raise ExportException("Sector ID not a number.")
            if sector_id not in sectors_by_id:
                raise ExportException("Sector ID not recognized.")
            account = g.db.accounts.create_account(
                user=g.user,
                name=required['name'],
                company=required['company'],
                sector=required['sector'],
            )
            return jsonify({"redirect": "/dashboard/accounts/" + str(account.id())})
        except AccountsException as e:
            raise ExportException("Account creation failed: " + str(e))
    except ExportException as e:
        return jsonify({"error": str(e)})


@bp.route('/dashboard/accounts/join-account', methods=['GET'])
def serve_accounts_join_account():
    if g.user is None:
        return redirect('/')

    return dashboard_render("accounts/join_account.html")


@bp.route('/dashboard/accounts/select/<int:account_id>', methods=['GET'])
def serve_select_account_id(account_id):
    if g.user is None:
        return redirect('/')

    g.db.accounts.session_start(account_id)

    return redirect("/dashboard/accounts/" + str(g.account.id()))


@bp.route('/dashboard/accounts/<int:account_id>', methods=['GET'])
def serve_account_id(account_id):
    if g.user is None:
        return redirect('/')

    try:
        account_user = g.db.account_users.get_by_user_and_account_id(g.user, account_id)
    except NoAccountUserFound as e:
        return dashboard_render("accounts/account_not_found.html", {"account_id":account_id})

    account = account_user.account()
    account_links = account.account_links()

    return dashboard_render("accounts/account/account_dashboard.html", {"account": account, "account_links": account_links})

@bp.route('/dashboard/animals/<int:animal_eid>', methods=['GET'])
def serve_animal_eid(animal_eid):
    if g.user is None:
        return redirect('/')

    animal = g.db.animals.get_by_eid(animal_eid)

    if len(animal.matches()) == 0:
        return dashboard_render("animals/animal_not_found.html", {"eid": animal_eid})

    return dashboard_render("animals/animal.html", {"animal": animal})

@bp.route('/dashboard/accounts', methods=['GET'])
def serve_accounts():
    if g.user is None:
        return redirect('/')
    
    accounts = g.db.accounts.get_by_user(g.user)
    return dashboard_render("accounts/account_select.html", {"accounts": accounts})

@bp.route('/dashboard/sales-groups', methods=['GET'])
def serve_sales_groups():
    if g.user is None:
        return redirect('/')
    if g.account is None:
        return dashboard_render("sales-groups/no-account.html")
    
    return dashboard_render("sales-groups/list.html")

@bp.route('/dashboard/sales-groups/new', methods=['GET'])
def serve_new_sales_group():
    if g.user is None:
        return redirect('/')
    if g.account is None:
        return dashboard_render("sales-groups/no-account.html")
    

    new_id = g.db.sales_groups.insert(g.account.id(), {})['id']

    return redirect('/dashboard/sales-groups/edit/' + str(new_id) + '')

@bp.route('/dashboard/sales-groups/edit/<int:sales_group_id>', methods=['GET'])
def serve_edit_sales_group(sales_group_id):
    if g.user is None:
        return redirect('/')
    if g.account is None:
        return dashboard_render("sales-groups/no-account.html")

    sales_group_row = g.db.sales_groups.row_by_id(sales_group_id)

    if sales_group_row['account'] != g.account.id():
        return dashboard_render("sales-groups/sales-group/no.html")
    
    return dashboard_render("sales-groups/sales-group/edit.html", {"sales_group": sales_group_row})
