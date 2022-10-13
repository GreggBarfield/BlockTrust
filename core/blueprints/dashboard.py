from core.database.tables.notification_recipients import NotificationRecipients
from flask import (
    request, Blueprint, g, redirect, url_for, send_from_directory
)

from core.config import FLATFILE_LICENSE, STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY
from core.database.tables.view_logs import DATA_TYPE_ID_TO_NAME, DATA_TYPE_NAME_TO_ID, DATA_TYPE_NAME_TO_ID, ViewLogs
from ..renderers.dashboard import dashboard_render

from ..sectors import sectors_by_id, sectors_by_name

from ..common_exceptions import ExportException

from ..database.tables.connections import Connections
from ..database.tables.connections import CONNECTION_STATUS_NAME_TO_ID, CONNECTION_TYPE_ID_TO_NAME
from ..database.tables.event_logs import EventLogs, event_type_by_name
from ..database.tables.invited_users import InvitedUsers
from ..database.tables.notifications import Notifications
from ..database.tables.account_users import NoAccountUserFound
from ..database.tables.users import UsersException

from ..renderers.email import render_email

from ..utilities import crut, auth, csrf
from ..utilities import token
from ..utilities.email import send_email

from core.config import SUPPORT_GENERAL_EMAIL, ROOT as WEBSITE_ROOT

import json
import stripe

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
    # Indicator for unread notifications
    unread_notifications_count = 0
    # Checking if user has unread notifications
    unread_notifications_list = Notifications(g.db).get_notification_and_notification_recipients(
        user_id=g.user.id(),
        is_archived=0,
        is_notification_seen=0
    )
    unread_notifications_count = len(unread_notifications_list)

    pending_connection_requests_count = 0
    pending_connection_requests_count = len(Connections(g.db).get_connections(to_account_id=g.account.id(), status=CONNECTION_STATUS_NAME_TO_ID["Pending"]))

    account_params = {
        "account": account,
        "account_links": account_links,
        "unread_notifications_count": unread_notifications_count,
        "pending_connection_requests_count": pending_connection_requests_count
    }

    if account.sector_name() == "Auction House":
        return dashboard_render("sectors/auction.html", account_params)
    elif account.sector_name() == "Feedlot" or account.sector_name() == "Packer":
        return dashboard_render("sectors/feedlot-packer.html", account_params)
    elif account.sector_name() == "Buyer":
        return dashboard_render("sectors/buyer.html", account_params)
    else:
        return dashboard_render("sectors/generic.html", account_params)


@bp.route('/dashboard/animals/', defaults={'animal_eid': ''}, methods=['GET'])
@bp.route('/dashboard/animals/<int:animal_eid>', methods=['GET'])
@crut.require_user
def serve_animal_eid(animal_eid):
    animal = g.db.matches.get_animal_by_eid(animal_eid)

    if len(animal.matches) > 0 and any((row["account_links.account"] == g.account.id() for row in animal.matches)):

        # first ranch is owner
        owner_account_id = sorted(
            list(filter(lambda row: row["account_links.sector"] == sectors_by_name["Cow-Calf"], animal.matches)),
            key=lambda row: row["id"]
        )[0]["account_links.account"]
        if owner_account_id != g.account.id():
            ViewLogs(g.db).insert_view_logs(owner_account_id=owner_account_id, viewer_account_id=g.account.id(),
                                            viewer_user_id=g.user.id(),
                                            data_type_id=DATA_TYPE_NAME_TO_ID["EID"], eid=animal_eid)

        return dashboard_render("animals/animal.html", {"animal": animal, "account_name": g.account.name()})
    else:
        return dashboard_render("animals/animal_not_found.html", {"eid": animal_eid})

@bp.route('/dashboard/animals/<int:animal_eid>/certificates', methods=['GET'])
@crut.require_user
def serve_animal_cert(animal_eid):
    animal = g.db.matches.get_animal_by_eid(animal_eid)
    return dashboard_render("animals/animal-certificate.html", {"animal": animal})

@bp.route('/dashboard/accounts', methods=['GET'])
@crut.require_user
def serve_accounts():
    accounts = g.db.accounts.get_by_user(g.user)
    return dashboard_render("accounts/account_select.html", {"accounts": accounts})


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


@bp.route('/dashboard/sales-groups', methods=['GET'])
@crut.require_paid_account
def serve_sales_groups():
    return dashboard_render("sales-groups/list.html")


@bp.route('/dashboard/sales-groups/new', methods=['GET'])
@crut.require_paid_account
def serve_new_sales_group():
    form_post_route = url_for('widgets_bp.serve_create_sales_group')
    return dashboard_render("sales-groups/sales-group/create.html", {"form_post_route": form_post_route})


@bp.route('/dashboard/sales-groups/edit/<int:sales_group_id>', methods=['GET'])
@crut.require_paid_account
def serve_edit_sales_group(sales_group_id):
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(sales_group_id)

    if sales_group_row['account'] != g.account.id():
        return dashboard_render("sales-groups/sales-group/no.html")

    external_shareable_link = WEBSITE_ROOT + url_for('outside_bp.serve_external_sales_group_viewer',
        sales_group_id=sales_group_row['id'])
    form_post_route = url_for('widgets_bp.serve_update_sales_group')
    return dashboard_render(
        "sales-groups/sales-group/edit.html", {
            "sales_group": sales_group_row,
            "external_shareable_link": external_shareable_link,
            "form_post_route": form_post_route}
    )


@bp.route('/dashboard/sales-groups/archive', methods=['GET'])
@crut.require_account
def serve_sales_group_archive():
    return dashboard_render("sales-groups/sales-group/archive.html", {"account_id": g.account.id()})


@bp.route('/dashboard/sales-groups/view/<int:sales_group_id>', methods=['GET'])
@crut.require_paid_account
def serve_view_sales_group(sales_group_id):
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(sales_group_id)

    if sales_group_row['account'] == g.account.id() or sales_group_row['published'] > 0:
        external_shareable_link = WEBSITE_ROOT + url_for(
            'outside_bp.serve_external_sales_group_viewer',
            sales_group_id=sales_group_row['id']
            )
        return dashboard_render(
            "sales-groups/sales-group/view.html", {
                "sales_group": sales_group_row,
                "external_shareable_link": external_shareable_link
                }
        )
    return dashboard_render("sales-groups/sales-group/not-published.html")


@bp.route('/dashboard/sales-groups/manage-eids/<int:sales_group_id>', methods=["GET"])
@crut.require_account
def serve_manage_eids_sales_group(sales_group_id):
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(sales_group_id)
    if sales_group_row['account'] == g.account.id() or sales_group_row['published'] > 0:
        return dashboard_render(
            "sales-groups/sales-group/manage-eids.html",
            {"sales_group": sales_group_row}
        )
    return dashboard_render("sales-groups/sales-group/no.html")


@bp.route('/dashboard/sales-groups/manage', methods=['GET'])
@crut.require_paid_account
def serve_manage_sales_groups():
    return dashboard_render("sales-groups/manage.html", {"account": g.account})


@bp.route('/dashboard/auction-sales', methods=['GET'])
@bp.route('/dashboard/auction-sales/manage', methods=['GET'])
@crut.require_paid_account
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
@crut.require_paid_account
def serve_auction_sales_new():
    return serve_auction_sales_manage(True)


@bp.route('/dashboard/plans', methods=['GET'])
@crut.require_account
def serve_plans():
    return dashboard_render("stripe/plans.html")


@bp.route('/dashboard/subscribe', methods=['GET'])
@crut.require_account
def serve_subscribe():
    return dashboard_render("stripe/subscribe.html")


@bp.route('/dashboard/upload-tags', methods=['GET', 'POST'])
@crut.require_paid_account
def serve_upload_tags():
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            for row in data["eids"]:
                g.db.api_inserts.insert(g.account.id(), "SELF", "TagUpload", row)
            EventLogs(g.db).insert_event_log(account_id=g.account.id(), user_id=g.user.id(), event_type_id=event_type_by_name["Tag Upload"])
            return "", 200
        except Exception as e:
            return {'error':{'message': str(e)}}, 400
    elif request.method == 'GET':
        return dashboard_render("data/upload-tags.html",  {"account": g.account, "user": g.user, "license": FLATFILE_LICENSE})


@bp.route('/dashboard/sustainability', methods=['GET'])
@crut.require_paid_account
def serve_sustainability():
    sustainability_enabled_for_sector = True
    if sectors_by_id[g.account.sector_id()] == "Buyer" or sectors_by_id[g.account.sector_id()] == "Financial":
        sustainability_enabled_for_sector = False
    return dashboard_render("sustainability/summary.html", {
        "sector_id": g.account.sector_id(),
        "sector": sectors_by_id[g.account.sector_id()],
        "accountName": g.account.name(),
        "sustainability_enabled_for_sector": sustainability_enabled_for_sector
    })


@bp.route('/dashboard/data/market', methods=['GET'])
@crut.require_paid_account
def serve_market_state_data():
    return dashboard_render("data/market-data-filter.html")


@bp.route('/dashboard/data/market/<string:state>/<int:slug_id>', methods=['GET'])
@crut.require_paid_account
def serve_market_data(state, slug_id):
    stateLabel = {'market_location_state': state}
    market_states = g.db.usda_reports.get_all_states()
    report = g.db.usda_reports.get_by_slug_id(slug_id)[0]
    city = report["market_location_city"]
    # get rid of any "- <city name>" and/or ", <state>" that some locations have
    market_name = report["market_location_name"].replace("- " + city, "").replace(", " + state, "")

    if stateLabel in market_states:
        return dashboard_render("data/market-data.html",
            {
                "slug_id": slug_id,
                "state": state,
                "city": city,
                "market_name": market_name
            })
    raise Exception("Invalid state")

# edit account profile


@bp.route('/dashboard/edit/edit-account', methods=['GET', 'POST'])
@crut.require_user
@csrf.csrf_protect
def serve_edit_account():
    # Get account information
    if request.method == 'POST':
        try:
            g.db.accounts.update_account(
                    account_id=g.account.id(),
                    company=request.form["company"],
                    address=request.form["address"],
                    city=request.form["city"],
                    state=request.form["state"],
                    zip=request.form["zip"],
                    phone=request.form["phone"]
            )
            EventLogs(g.db).insert_event_log(account_id=g.account.id(), user_id=g.user.id(), event_type_id=event_type_by_name["Account Info Edit"])
            return {"redirect": "/dashboard/edit/edit-account"}
        except UsersException as e:
            return {"error": str(e)}, 400
    elif request.method == 'GET':
        stripe.api_key = STRIPE_SECRET_KEY
        is_stripe_charges_enabled = False
        if bool(request.args.get("stripe_onboarding")) and g.account.stripe_account_id() is not None and not bool(g.account.is_stripe_charges_enabled()):
            # Check if this has changed
            stripe_account = stripe.Account.retrieve(g.account.stripe_account_id())
            if stripe_account["charges_enabled"]:
                g.db.accounts.update_account(account_id=g.account.id(), is_stripe_charges_enabled=1)
                is_stripe_charges_enabled = True
        else:
            is_stripe_charges_enabled = bool(g.account.is_stripe_charges_enabled())
        return dashboard_render("/dashboard/accounts/edit_account.html", {"sectors": sectors_by_name, "is_stripe_charges_enabled": is_stripe_charges_enabled })


# edit user profile
@bp.route('/dashboard/edit/edituser', methods=['GET', 'POST'])
@crut.require_user
@csrf.csrf_protect
def serve_edit_edituser():
    if request.method == 'POST':
        try:
            g.db.users.update_user(
                username=g.user.username(),
                first_name=request.form["first"],
                last_name=request.form["last"],
                phone=request.form["phone"],
                password=request.form["password"] if request.form["password"] != "" else None,
                confirm_password=request.form["confirm_password"] if request.form["confirm_password"] != "" else None
            )
            EventLogs(g.db).insert_event_log(account_id=g.account.id(), user_id=g.user.id(), event_type_id=event_type_by_name["User Info Edit"])
            return {"redirect": "/dashboard/edit/edituser"}
        except UsersException as e:
            return {"error": str(e)}, 400
    elif request.method == 'GET':
        user = g.db.users.get_by_username(g.user.username())
        return dashboard_render("/dashboard/edit/edituser.html", {"user": user})


@bp.route('/dashboard/inviteuser', methods=['GET', 'POST'])
@crut.require_account
def serve_invite_user():
    if request.method == 'POST':
        try:
            user_email = request.form["email"]
            if g.db.users.get_by_email(user_email) is not None:
                raise ExportException("A user with that email already exists!")
            current_account = g.account.name()
            current_account_id = g.account.id()
            invite_object = {"user_email": user_email, "current_account": current_account, "current_account_id": current_account_id}
            invite_string = str(invite_object)
            # Generating token identifier with account and user email informatiom
            userToken = token.generateConfirmationToken(invite_string)
            # Creating URL for user to join an account
            confirm_url = WEBSITE_ROOT + url_for('outside_bp.serve_add_user', invite_token=userToken)
            # Sending an email to user including Blocktrust email template and verification link with validity of 24 hours
            send_email(
                "BlockTrust Network Account Invite",
                render_email("invite_user.html", {
                    'confirm_url': confirm_url,
                    'account_company': g.account.company(),
                    'user_name': g.user.first_name() + " " + g.user.last_name()
                }), user_email
            )
            InvitedUsers(g.db).insert_invited_user(user_email, g.user.id(), 0, 0)
            return {"redirect": "/dashboard"}
        except ExportException as e:
            return {"error": str(e)}, 400
    elif request.method == 'GET':
        return dashboard_render("/dashboard/accounts/invite_user.html")


@bp.route('/dashboard/connections', methods=['GET'])
@crut.require_account
def serve_connections():
    account_connections = Connections(g.db).get_account_connections(g.account.id(), CONNECTION_STATUS_NAME_TO_ID["Connected"])
    requests = Connections(g.db).get_connections(to_account_id=g.account.id(), status=CONNECTION_STATUS_NAME_TO_ID["Pending"])
    blocked_connections = Connections(g.db).get_connections(blocked_by_account_id=g.account.id())
    return dashboard_render("/dashboard/connections/connections.html", {
        "account_connections": account_connections,
        "requests": requests,
        "blocked_connections": blocked_connections,
        "CONNECTION_TYPE_ID_TO_NAME": CONNECTION_TYPE_ID_TO_NAME
    })


@bp.route('/dashboard/add-connection', methods=['GET'])
@crut.require_account
def serve_add_connection():
    return dashboard_render("/dashboard/connections/add-connection.html")


@bp.route('/dashboard/accept-invite', methods=['POST'])
@crut.require_account
def serve_accept_invite():
    Connections(g.db).update_connection_between(
        from_account_id=request.json["account_id"],
        to_account_id=g.account.id(),
        status=CONNECTION_STATUS_NAME_TO_ID["Connected"]
    )
    return {}

# Deprecated 10/04/2022
# @bp.route('/dashboard/decline-invite', methods=['POST'])
# @crut.require_account
# def serve_decline_invite():
#     Connections(g.db).update_connection_between(
#         from_account_id=request.json["account_id"],
#         to_account_id=g.account.id(),
#         status=connection_status_name_to_id["Blocked"]
#     )
#     return {}


@bp.route('/dashboard/block-connection', methods=['POST'])
@crut.require_account
def serve_block_connection():
    Connections(g.db).update_connection(
        id=request.json["connection_id"],
        connection_status_id=CONNECTION_STATUS_NAME_TO_ID["Blocked"],
        blocked_by_account_id=g.account.id()
    )
    return {}


@bp.route('/dashboard/unblock-connection', methods=['POST'])
@crut.require_account
def serve_unblock_connection():
    Connections(g.db).update_connection(
        id=request.json["connection_id"],
        connection_status_id=CONNECTION_STATUS_NAME_TO_ID["Connected"],
        blocked_by_account_id=None
    )
    return {}


@bp.route('/dashboard/view-profile/<int:account_id>', methods=['GET'])
@crut.require_account
def serve_view_profile(account_id):
    account_details = g.db.accounts.get_account_by_id(account_id)
    if Connections(g.db).get_connection_between(g.account.id(), account_details.id(), CONNECTION_STATUS_NAME_TO_ID["Connected"]) is not None:
        return dashboard_render("/dashboard/connections/view-profile.html", {"account_details": account_details})
    else:
        return redirect("/dashboard/connections")


@bp.route('/dashboard/support', methods=['GET'])
@crut.require_account
def serve_support():
    return dashboard_render("/dashboard/support/support.html")


@bp.route('/dashboard/support/action', methods=["POST"])
@crut.require_account
def serve_support_response():
    send_email(
        "New Dashboard Support Response",
        render_email("contact_us_response.html", {
            'first': request.form['first'],
            'last': request.form['last'],
            'phone': request.form['phone'],
            'email': request.form['email'],
            'message': request.form['message'],
            'message_title': "New Dashboard Support Response"
        }),
        SUPPORT_GENERAL_EMAIL
        )
    return {"redirect": "/dashboard"}


@bp.route('/dashboard/notifications', methods=["GET"])
@crut.require_account
def serve_notifications():
    notifications_and_data_for_user = Notifications(g.db).get_notification_and_notification_recipients(
        user_id=g.user.id(),
        is_archived=0,
        notifications_order_by="id",
        notifications_sort_by="DESC"
    )
    return dashboard_render("/dashboard/notifications/notifications.html", {
        "notifications_and_data_for_user": notifications_and_data_for_user
        })


@bp.route('/dashboard/notifications/view-notification/<int:notification_id>', methods=["GET"])
@crut.require_account
def serve_view_notification(notification_id):
    # Verifying if the notification is not archived and if user is an actual recipient
    notification = Notifications(g.db).get_notification_and_notification_recipients(
        user_id=g.user.id(),
        notification_id=notification_id,
        is_archived=0
    )
    if len(notification) > 0:
        notification_row = notification[0]
        # Marking notification as read if it is unread
        if notification_row["is_notification_seen"] == 0:
            NotificationRecipients(g.db).update_notification_recipients(
                id=notification_row["notification_recipients_id"],
                is_notification_seen=1
            )
        return dashboard_render("/dashboard/notifications/view-notification.html", {"notification": notification_row})
    # If notification is invalid return to main notifications page
    return redirect('/dashboard/notifications')


@bp.route('/dashboard/sales-groups/purchase/<int:sales_group_id>', methods=["GET", "POST"])
@crut.require_account
def serve_sales_group_transaction(sales_group_id):
    if request.method == "GET":
        sales_group_row = g.db.sales_groups.get_sales_group_by_id(sales_group_id)
        if sales_group_row["is_sold"] == 0:
            return dashboard_render("/dashboard/sales-groups/sales-group/purchase.html", {
                "sales_group_row": sales_group_row, "stripe_key": STRIPE_PUBLISHABLE_KEY, "name": g.user.first_name() + ' ' + g.user.last_name()
            })
        else:
            return {"error": "Sales group has been sold"}, 400
    else:
        try:
            request_data = json.loads(request.data)

            g.db.sales_groups.update_sales_group(id=sales_group_id, is_sold=1, buyer_account_id=g.account.id())
            EventLogs(g.db).insert_event_log(
                account_id=g.account.id(),
                user_id=g.user.id(),
                event_type_id=event_type_by_name["Sales Group Purchase"],
                details={
                    'sales_group_id': sales_group_id,
                    'transaction_amount': request_data['amount'],
                    'buyer_account_id': g.account.id(),
                    'seller_account_id': request_data['to_account_id'],
                    'payment_intent': request_data['paymentIntent']
                }
            )
            return {}
        except Exception as e:
            return {"error": str(e)}, 400


@bp.route('/dashboard/sales-groups/<int:sales_group_id>/select-eids-by-grouping-id', methods=["GET"])
@crut.require_account
def serve_select_eids_by_application_id(sales_group_id):
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(sales_group_id)
    if sales_group_row['account'] == g.account.id() or sales_group_row['published'] > 0:
        return dashboard_render(
            "sales-groups/sales-group/select-eids-by-grouping-id.html",
            {"sales_group_id": sales_group_id}
        )
    return dashboard_render("sales-groups/sales-group/no.html")


@bp.route('/dashboard/files/<path:path>')
@crut.require_account
def send_document(path):
    return send_from_directory('static/files/dashboard/', path)


@bp.route("/dashboard/sustainability/questionnaire", methods=["GET"])
@crut.require_paid_account
def serve_sustainability_questionnaire():
    return dashboard_render("sustainability/questionnaire_v2.html", {"sector": sectors_by_id[g.account.sector_id()]})

@bp.route("/dashboard/data-views", methods=["GET"])
@crut.require_account
def serve_views():
    view_logs = ViewLogs(g.db).get_view_logs(owner_account_id=g.account.id(), get_related_details=True)

    return dashboard_render("privacy/view-logs.html",
                            {"view_logs": view_logs, "view_logs_count": len(view_logs), "data_type_id_to_name": DATA_TYPE_ID_TO_NAME,
                             "animal_url": url_for("dashboard_bp.serve_animal_eid", animal_eid='')})
