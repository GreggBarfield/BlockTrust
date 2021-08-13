from core.renderers.outside import outside_render
from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)

from ..renderers.dashboard import dashboard_render

from ..sectors import sectors_by_id

from ..common_exceptions import ExportException

from ..database.tables.account_users import NoAccountUserFound
from ..database.tables.accounts import AccountsException
from ..database.objects.account import AccountException
from ..database.tables.users import UsersException

from ..renderers.email import render_email

from ..utilities import crut, auth
from ..utilities import token
from ..utilities.email import send_email

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
        auth.session_start_account(account_users[0].account_id())
        return redirect('/dashboard/accounts/' + str(account_users[0].account_id()))
    else:
        return redirect('/dashboard/accounts')

# Accounts

# 6/3/21 Deprecated
@bp.route('/dashboard/accounts/new-account', methods=['GET'])
@crut.require_user
def serve_accounts_new_account():
    return dashboard_render("accounts/new_account.html", {
        "sectors_by_id": sectors_by_id
    })

# 6/3/21 Deprecated
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
            auth.session_start_account(account.id())
            return {"redirect": "/dashboard/accounts/" + str(account.id())}
        except AccountsException as e:
            raise ExportException("Account creation failed: " + str(e))
    except ExportException as e:
        return {"error": str(e)}

# 6/3/21 Deprecated
@bp.route('/dashboard/accounts/join-account', methods=['GET'])
@crut.require_user
def serve_accounts_join_account():
    return dashboard_render("accounts/join_account.html")


@bp.route('/dashboard/accounts/select/<int:account_id>', methods=['GET'])
@crut.require_user
def serve_select_account_id(account_id):
    auth.session_start_account(account_id)

    return redirect("/dashboard/accounts/" + str(g.account.id()))


@bp.route('/dashboard/accounts/<int:account_id>', methods=['GET'])
@crut.require_user
def serve_account_id(account_id):
    try:
        account_user = g.db.account_users.get_by_user_and_account_id(g.user, account_id)
    except NoAccountUserFound as e:
        return dashboard_render(
            "accounts/account_not_found.html",
            {"account_id": account_id}
        )

    account = account_user.account()
    account_links = account.account_links()

    sector_params = {"account": account, "account_links": account_links}

    if account.sector_name() == "Auction House":
        return dashboard_render("sectors/auction.html", sector_params)
    elif account.sector_name() == "Feedlot":
        return dashboard_render("sectors/feedlot.html", sector_params)
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
        return dashboard_render(
            "sales-groups/sales-group/view.html",
            {"sales_group": sales_group_row}
        )
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


@bp.route('/dashboard/data', methods=['GET'])
@crut.require_account
def serve_data():
    return dashboard_render("data/index.html")


@bp.route('/dashboard/plans', methods=['GET'])
@crut.require_account
def serve_plans():
    return dashboard_render("stripe/plans.html")


@bp.route('/dashboard/subscribe', methods=['GET'])
@crut.require_account
def serve_subscribe():
    return dashboard_render("stripe/subscribe.html")

@bp.route('/dashboard/sustainability', methods=['GET'])
@crut.require_account
def serve_sustainability():
    return dashboard_render("sustainability/sustainability_questionaire.html")

@bp.route('/dashboard/sustainability/summary', methods=['GET'])
@crut.require_account
def serve_sustainability_summary():
    return dashboard_render("sustainability/sustainability_summary.html")

@bp.route('/dashboard/retained-ownership', methods=['GET'])
@crut.require_account
def serve_retained_ownership():
    return dashboard_render("retained-ownership.html")


@bp.route('/dashboard/data/upload-tags', methods=['GET'])
@crut.require_account
def serve_upload_tags():
    return dashboard_render("data/upload-tags.html")


# edit user profile
@bp.route('/dashboard/edit/edituser', methods=['GET', 'POST'])
@crut.require_user
def serve_edit_edituser():
    if request.method == 'POST':
        try:
            g.db.users.update_user(
                        username=g.user.username(),
                        first=request.form["first"],
                        last=request.form["last"],
                        phone=request.form["phone"],
                        password=request.form["password"],
                        confirm_password=request.form["confirm_password"]
                        )
            return {"redirect": "/dashboard/edit/edituser"}
        except UsersException as e:
            return {"error": str(e)}
    elif request.method == 'GET':
        user = g.db.users.get_by_username(g.user.username())
        return dashboard_render("/dashboard/edit/edituser.html", {"user": user})


@bp.route('/dashboard/inviteuser', methods=['GET', 'POST'])
@crut.require_user
def serve_invite_user():
    if request.method == 'POST':
        try:
            user_email = request.form["email"]
            current_account = request.form["current_account"]
            current_account_id = request.form["current_account_id"]
            invite_object = {"user_email": user_email, "current_account": current_account, "current_account_id": current_account_id}
            invite_string = str(invite_object)
            # Generating token identifier with account and user email informatiom
            userToken = token.generateConfirmationToken(invite_string)
            # Creating URL for user to join an account
            confirm_url = url_for('dashboard_bp.serve_add_user', tok=userToken, _external=True)
            # Sending an email to user including Blocktrust email template and verification link with validity of 24 hours
            send_email(
                "BlockTrust Network Email Confirmation",
                render_email("invite_user.html", {
                    'confirm_url': confirm_url,
                    'current_account': current_account
                }), user_email, override=True
            )
            return {"redirect": "/dashboard"}
        except ExportException as e:
            return {"error": str(e)}
    elif request.method == 'GET':
        return dashboard_render("/dashboard/accounts/invite_user.html")


@bp.route('/dashboard/adduser/<tok>', methods=['GET', 'POST'])
def serve_add_user(tok):
    if request.method == 'GET':
        try:
            invite_string = token.confirmToken(tok)
            invite_object = eval(invite_string)
            user_email = invite_object["user_email"]
            account_name = invite_object["current_account"]
            account_id = invite_object["current_account_id"]
            return outside_render("/outside/invited-user-signup.html", {"user_email": user_email, "account_name": account_name, "account_id": account_id})
        except ExportException as e:
            return outside_render("/outside/error.html")


@bp.route('/dashboard/adduser', methods=['POST'])
def serve_add_invited_user():
    try:
        account_details = g.db.accounts.get_by_id(request.form["account_id"])
        auth.invited_signup(
            username=request.form['username'],
            email=request.form['user_email'],
            phone=str(account_details.phone()),
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            password=request.form['password'],
            confirm_password=request.form['confirm_password'],
            account_name=request.form['account_name'],
            account_id=request.form['account_id']
        )
        return {"redirect": "/login"}
    except (auth.SignupFailedException, AccountsException, UsersException, ExportException) as e:
        return {"error": str(e)}
