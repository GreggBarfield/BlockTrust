from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)

from ..renderers.dashboard import dashboard_render

from ..sectors import sectors_by_id

from ..common_exceptions import ExportException

from ..database.tables.account_users import NoAccountUserFound
from ..database.tables.accounts import AccountsException
from ..database.objects.account import AccountException

from ..renderers.email import render_email

from ..utilities import crut

bp = Blueprint('dashboard_bp', __name__)

@bp.route('/dashboard', methods=['GET'])
@crut.require_user
def serve_dashboard():
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
@crut.require_user
def serve_accounts_new_account():
    return dashboard_render("accounts/new_account.html", {
        "sectors_by_id": sectors_by_id
    })


@bp.route('/dashboard/accounts/new-account/action', methods=['POST'])
@crut.require_user
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
            g.db.accounts.session_start(account.id())
            return {"redirect": "/dashboard/accounts/" + str(account.id())}
        except AccountsException as e:
            raise ExportException("Account creation failed: " + str(e))
    except ExportException as e:
        return {"error": str(e)}


@bp.route('/dashboard/accounts/join-account', methods=['GET'])
@crut.require_user
def serve_accounts_join_account():
    return dashboard_render("accounts/join_account.html")


@bp.route('/dashboard/accounts/select/<int:account_id>', methods=['GET'])
@crut.require_user
def serve_select_account_id(account_id):
    g.db.accounts.session_start(account_id)

    return redirect("/dashboard/accounts/" + str(g.account.id()))


@bp.route('/dashboard/accounts/<int:account_id>', methods=['GET'])
@crut.require_user
def serve_account_id(account_id):
    try:
        account_user = g.db.account_users.get_by_user_and_account_id(g.user, account_id)
    except NoAccountUserFound as e:
        return dashboard_render("accounts/account_not_found.html", {"account_id":account_id})

    account = account_user.account()
    account_links = account.account_links()

    sector_params = {"account": account, "account_links": account_links}

    if account.sector_name() == "Auction House":
        return dashboard_render("sectors/auction.html", sector_params)
    else:
        return dashboard_render("sectors/generic.html", sector_params)


@bp.route('/dashboard/animals/<int:animal_eid>', methods=['GET'])
@crut.require_user
def serve_animal_eid(animal_eid):
    animal = g.db.animals.get_by_eid(animal_eid)

    if len(animal.matches()) == 0:
        return dashboard_render("animals/animal_not_found.html", {"eid": animal_eid})

    return dashboard_render("animals/animal.html", {"animal": animal})

@bp.route('/dashboard/accounts', methods=['GET'])
@crut.require_user
def serve_accounts():
    accounts = g.db.accounts.get_by_user(g.user)
    return dashboard_render("accounts/account_select.html", {"accounts": accounts})

@bp.route('/dashboard/sales-groups', methods=['GET'])
@crut.require_account
def serve_sales_groups():
    return dashboard_render("sales-groups/list.html")

@bp.route('/dashboard/messages', methods=['GET'])
@crut.require_account
def serve_messages(open_message_id=None):

    messages_attributes = ""

    if open_message_id is not None:
        messages_attributes += (
            " data-widget-messages-open='" + str(int(open_message_id)) + "' "
        )

    return dashboard_render(
        "messages/messages.html",
        {
            'messages_attributes': messages_attributes
        }
    )

@bp.route('/dashboard/messages/<int:open_message_id>', methods=['GET'])
def serve_messages_specific(open_message_id):
    return serve_messages(open_message_id)

@bp.route('/dashboard/sales-groups/new', methods=['GET'])
@crut.require_account
def serve_new_sales_group():
    new_id = g.db.sales_groups.insert(g.account.id(), {})['id']

    return redirect('/dashboard/sales-groups/edit/' + str(new_id) + '')

@bp.route('/dashboard/sales-groups/edit/<int:sales_group_id>', methods=['GET'])
@crut.require_account
def serve_edit_sales_group(sales_group_id):
    sales_group_row = g.db.sales_groups.row_by_id(sales_group_id)

    if sales_group_row['account'] != g.account.id():
        return dashboard_render("sales-groups/sales-group/no.html")
    
    return dashboard_render("sales-groups/sales-group/edit.html", {"sales_group": sales_group_row})

@bp.route('/dashboard/sales-groups/view/<int:sales_group_id>', methods=['GET'])
@crut.require_account
def serve_view_sales_group(sales_group_id):
    sales_group_row = g.db.sales_groups.row_by_id(sales_group_id)

    if sales_group_row['account'] == g.account.id() or sales_group_row['published'] > 0:
        return dashboard_render("sales-groups/sales-group/view.html", {"sales_group": sales_group_row})
    return dashboard_render("sales-groups/sales-group/not-published.html")

@bp.route('/dashboard/sales-groups/manage', methods=['GET'])
@crut.require_user
def serve_manage_sales_groups():
    return dashboard_render("sales-groups/manage.html", {"account": g.account})


@bp.route('/dashboard/auction-sales', methods=['GET'])
@bp.route('/dashboard/auction-sales/manage', methods=['GET'])
@crut.require_account
def serve_auction_sales_manage(new_auction_sale=False):
    manage_auction_sales_attr = ""

    if new_auction_sale:
        manage_auction_sales_attr = " data-widget-manage-auction-sales-new "

    return dashboard_render(
        "auction-sales/manage.html",
        {
            "manage_auction_sales_attr": manage_auction_sales_attr
        }
    )

@bp.route('/dashboard/auction-sales/new', methods=['GET'])
def serve_auction_sales_new():
    return serve_auction_sales_manage(True)
