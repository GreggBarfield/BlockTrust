from flask import (
    Response, request, Blueprint, g, redirect, url_for, send_from_directory
)

from core.config import ADMIN_EMAIL, FLATFILE_LICENSE, STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, EMAIL_SENDER
from core.database.tables.matches import Matches
from core.database.tables.sales_group_searches import SalesGroupSearches
from ..renderers.dashboard import dashboard_render

from ..sectors import SECTORS_ID_TO_NAME, SECTORS_NAME_TO_ID
from ..match_types import MATCH_TYPES_NAME_TO_ID

from ..common_exceptions import ExportException
from core.database.tables.accounts import HEALTH_TRACK_PARTNER_COMPANY
from ..database.tables.api_inserts import ApiInserts
from ..database.tables.auction_markets import AuctionMarkets
from ..database.tables.connections import Connections
from ..database.tables.connections import CONNECTION_STATUS_NAME_TO_ID, CONNECTION_TYPE_ID_TO_NAME
from ..database.tables.event_logs import EventLogs, EVENT_TYPE_NAMES_TO_IDS
from ..database.tables.files import Files
from ..database.tables.genetics import Genetics
from ..database.tables.invited_users import InvitedUsers
from ..database.tables.notifications import Notifications
from ..database.tables.notification_recipients import NotificationRecipients
from ..database.tables.account_users import NoAccountUserFound
from ..database.tables.orders import Orders
from ..database.tables.order_products import OrderProducts
from ..database.tables.products import ProductTable
from ..database.tables.product_categories import ProductCategories
from ..database.tables.product_vendors import ProductVendors, HERD_WHISTLE_VENDOR_NAME
from ..database.tables.sales_group_animals import SalesGroupAnimals
from ..database.tables.sales_groups import TARGET_DATE_KEYS_TO_DESC, SalesGroups
from ..database.tables.sales_group_fields_values import SalesGroupFieldsValues, SALES_GROUP_FIELD_IDS_TO_NAMES, SALES_GROUP_FIELD_NAMES_TO_IDS
from ..database.tables.seedstock_producers import SeedstockProducers
from ..database.tables.sustainability_responses import SustainabilityResponses, QUESTIONNAIRE_STATUS_NAMES_TO_IDS
from ..database.tables.usda_reports import USDAReports
from ..database.tables.users import UsersException
from ..database.tables.vendor_identifiers_for_account import VendorIdentifiersForAccounts
from core.database.tables.view_logs import DATA_TYPE_ID_TO_NAME, DATA_TYPE_NAME_TO_ID, DATA_TYPE_NAME_TO_ID, ViewLogs

from ..renderers.email import render_email

from ..utilities import crut, auth, csrf
from ..utilities import token
from ..utilities.constants import DEFAULT_PASSWORD, HTTP_BAD_REQUEST, HTTP_NO_CONTENT, HTTP_NOT_FOUND, HTTP_OK
from ..utilities.email import send_email, send_tag_store_email, send_multiple_tag_store_email
from ..utilities.shop.herdwhistle_api import HerdWhistleAPI
from ..utilities.general_utilities import str_to_bool

from core.config import SUPPORT_GENERAL_EMAIL, ROOT as WEBSITE_ROOT
import json
import stripe

bp = Blueprint('dashboard_bp', __name__)


@bp.route('/dashboard/accounts/select/<int:account_id>', methods=['GET'])
@crut.require_user
def serve_select_account_id(account_id):
    auth.load_account(account_id)
    if g.account.is_partner():
        return redirect(url_for("partner_bp.serve_dashboard"))
    else:
        return redirect(url_for("dashboard_bp.serve_dashboard"))


@bp.route('/dashboard', methods=['GET'])
@crut.require_account
def serve_dashboard():
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
        "account": g.account,
        "unread_notifications_count": unread_notifications_count,
        "pending_connection_requests_count": pending_connection_requests_count,
        "animal_URL": url_for('dashboard_bp.serve_animal_eid')
    }

    if g.account.sector_id() in (SECTORS_NAME_TO_ID["Auction"], SECTORS_NAME_TO_ID["Feedlot"], SECTORS_NAME_TO_ID["Packer"]):
        account_params["sales_groups"] = None
        if g.account.sector_id() == SECTORS_NAME_TO_ID["Auction"] and g.account.auction_market_id():
            account_params["sales_groups"] = SalesGroups(g.db).get_sales_groups(
                auction_market_id=g.account.auction_market_id(), is_archived=int(False)
            )
        return dashboard_render("sectors/auction-feedlot-packer.html", account_params)
    elif g.account.sector_id() == SECTORS_NAME_TO_ID["Buyer"]:
        return dashboard_render("sectors/buyer.html", account_params)
    else:
        return dashboard_render("sectors/generic.html", account_params)


@bp.route('/dashboard/animals/', defaults={'animal_eid': ''}, methods=['GET'])
@bp.route('/dashboard/animals/<int:animal_eid>', methods=['GET'])
@crut.require_paid_account
def serve_animal_eid(animal_eid):
    animal = Matches(g.db).get_animal_by_eid(animal_eid)
    available_account_ids = [g.account.id()] if g.account.sector_id() == SECTORS_NAME_TO_ID["Cow-Calf"] else []
    available_account_ids += Connections(g.db).get_connected_account_ids(
        account_id=g.account.id(), sector_id=SECTORS_NAME_TO_ID["Cow-Calf"]
    )
    if len(animal.matches) > 0:
        owner_account_match = sorted(
            list(filter(lambda row: row["sector"] == SECTORS_NAME_TO_ID["Cow-Calf"], animal.matches)),
            key=lambda row: row["id"]
        )[0]
        owner_account_id = owner_account_match["account"]
        owner_account_name = owner_account_match["name"]
        healthtrack_partner = g.db.accounts.get_partners(company=HEALTH_TRACK_PARTNER_COMPANY)[0]
        display_certificate = True if owner_account_match["partner_account"] == healthtrack_partner["id"] else False

        if owner_account_id in available_account_ids:
            if owner_account_id != g.account.id():
                ViewLogs(g.db).insert_view_logs(
                    owner_account_id=owner_account_id, viewer_account_id=g.account.id(),
                    viewer_user_id=g.user.id(),
                    data_type_id=DATA_TYPE_NAME_TO_ID["EID"], eid=animal_eid
                )

            return dashboard_render("animals/animal.html", {
                "animal": animal, "account_name": owner_account_name, "display_certificate": display_certificate
            })
        else:
            return dashboard_render("animals/animal_not_found.html", {"eid": animal_eid})
    else:
        return dashboard_render("animals/animal_not_found.html", {"eid": animal_eid})


@bp.route('/dashboard/animals/<int:animal_eid>/certificates', methods=['GET'])
@crut.require_user
def serve_animal_cert(animal_eid):
    animal = Matches(g.db).get_animal_by_eid(animal_eid)
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


@bp.route('/dashboard/sales-groups/', defaults={'id': ''}, methods=['GET'])
@bp.route('/dashboard/sales-groups/<int:id>', methods=['GET'])
@crut.require_paid_account
def serve_sales_groups(id):
    search = {}
    if id:
        if len(search := SalesGroupSearches(g.db).get(id=id, user_id=g.user.id())) > 0:
            search = search[0]
        else:
            raise ExportException("Bad Request")
    return dashboard_render("sales-groups/list.html", {
        "search": search, "search_link": url_for(request.endpoint),
        "dates": [v for v in TARGET_DATE_KEYS_TO_DESC.values()],
        "view_link": url_for("dashboard_bp.serve_view_sales_group")
    })


@bp.route('/dashboard/sales-groups/new', methods=['GET'])
@crut.require_paid_account
def serve_new_sales_group():
    auction_markets = AuctionMarkets(g.db).get_auction_markets()
    sales_group_fields_values = SalesGroupFieldsValues(g.db).get(is_archived=0)
    form_post_route = url_for('widgets_bp.serve_create_sales_group')
    payment_URL = url_for("stripe_bp.serve_sales_group_payment")
    if g.account.partner_account_id():
        if g.account.partner_pays():
            payment_URL = ""
        partner = g.db.accounts.get_partners(id=g.account.partner_account_id())[0]
        per_head_fee = partner["per_head_fee"]
    else:
        per_head_fee = g.account.per_head_fee()
    return dashboard_render("sales-groups/sales-group/create.html", {
        "form_post_route": form_post_route,
        "auction_markets": auction_markets,
        "pre_select_auction_market": False,
        "pre_selected_auction_market_id": None,
        "sales_group_fields_values": sales_group_fields_values,
        "field_ids_to_names": SALES_GROUP_FIELD_IDS_TO_NAMES,
        "payment_URL": payment_URL,
        "view_sales_group_URL": url_for("dashboard_bp.serve_view_sales_group"),
        "per_head_fee": per_head_fee
    })


@bp.route('/dashboard/sales-groups/edit/<int:sales_group_id>', methods=['GET'])
@crut.require_paid_account
def serve_edit_sales_group(sales_group_id):
    sales_group_row = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)

    if sales_group_row['account'] != g.account.id():
        return dashboard_render("sales-groups/sales-group/no.html")

    external_shareable_link = WEBSITE_ROOT + url_for('outside_bp.serve_external_sales_group_viewer',
                                                     sales_group_id=sales_group_row['id'])
    form_post_route = url_for('widgets_bp.serve_update_sales_group')
    sales_group_fields_values = SalesGroupFieldsValues(g.db).get(is_archived=0)
    payment_URL = url_for("stripe_bp.serve_sales_group_payment")
    if g.account.partner_account_id():
        if g.account.partner_pays():
            payment_URL = ""
        partner = g.db.accounts.get_partners(id=g.account.partner_account_id())[0]
        per_head_fee = partner["per_head_fee"]
    else:
        per_head_fee = g.account.per_head_fee()
    return dashboard_render(
        "sales-groups/sales-group/edit.html", {
            "sales_group": sales_group_row,
            "external_shareable_link": external_shareable_link,
            "form_post_route": form_post_route,
            "sales_group_fields_values": sales_group_fields_values,
            "field_ids_to_names": SALES_GROUP_FIELD_IDS_TO_NAMES,
            "payment_URL": payment_URL,
            "view_sales_group_URL": url_for("dashboard_bp.serve_view_sales_group"),
            "per_head_fee": per_head_fee
        }
    )


@bp.route('/dashboard/sales-groups/archive', methods=['GET'])
@crut.require_account
def serve_sales_group_archive():
    return dashboard_render("sales-groups/sales-group/archive.html", {"account_id": g.account.id()})


@bp.route('/dashboard/sales-groups/view/', defaults={'sales_group_id': ''}, methods=['GET'])
@bp.route('/dashboard/sales-groups/view/<int:sales_group_id>', methods=['GET'])
@crut.require_paid_account
def serve_view_sales_group(sales_group_id):
    sales_group_row = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)

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
    sales_group_row = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)
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


@bp.route('/dashboard/plans', methods=['GET'])
@crut.require_account
def serve_plans():
    return dashboard_render("stripe/plans.html")


@bp.route('/dashboard/subscribe', methods=['GET'])
@crut.require_account
def serve_subscribe():
    return dashboard_render("stripe/subscribe.html")


@bp.route('/dashboard/payment', defaults={'id':''}, methods=['GET'])
@bp.route('/dashboard/payment/<int:id>', methods=['GET'])
@crut.require_account
def serve_payment(id):
    if id:
        sales_group = SalesGroups(g.db).get_sales_groups(id=id)[0]
        if not sales_group["is_paid"]:
            return dashboard_render("stripe/payment.html", {
                "STRIPE_KEY": STRIPE_PUBLISHABLE_KEY,
                "sales_group_id": sales_group["id"],
                "sales_group_name": sales_group["group_name"],
                "amount": sales_group["reported"]["count"]
            })
        else:
            return redirect(url_for("dashboard_bp.serve_payment", id=''))
    return dashboard_render("stripe/payment.html", {
        "STRIPE_KEY": STRIPE_PUBLISHABLE_KEY
    })


@bp.route('/dashboard/upload-tags', methods=['GET', 'POST'])
@crut.require_paid_account
def serve_upload_tags():
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            for row in data["eids"]:
                ApiInserts(g.db).insert(g.account.id(), "SELF", "TagUpload", row)
            EventLogs(g.db).insert(account_id=g.account.id(), user_id=g.user.id(), event_type_id=EVENT_TYPE_NAMES_TO_IDS["Tag Upload"])
            return "", 200
        except Exception as e:
            return {'error': {'message': str(e)}}, 400
    elif request.method == 'GET':
        return dashboard_render("data/upload-tags.html",  {"account": g.account, "user": g.user, "license": FLATFILE_LICENSE})


@bp.route('/dashboard/sustainability', methods=['GET'])
@crut.require_paid_account
def serve_sustainability():
    sustainability_enabled_for_sector = True
    if SECTORS_ID_TO_NAME[g.account.sector_id()] == "Buyer" or SECTORS_ID_TO_NAME[g.account.sector_id()] == "Financial":
        sustainability_enabled_for_sector = False
    pending_questionnaires = SustainabilityResponses(g.db).get_sustainability_responses(
        account_id=g.account.id(),
        user_id=g.user.id(),
        questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Pending"]
    )
    pending_questionnaires_for_user = False
    if len(pending_questionnaires) > 0:
        pending_questionnaires_for_user = True
    return dashboard_render("sustainability/summary.html", {
        "sector_id": g.account.sector_id(),
        "sector": SECTORS_ID_TO_NAME[g.account.sector_id()],
        "accountName": g.account.name(),
        "sustainability_enabled_for_sector": sustainability_enabled_for_sector,
        "pending_questionnaires_for_user": pending_questionnaires_for_user
    })


@bp.route('/dashboard/data/market', methods=['GET'])
@crut.require_paid_account
def serve_market_state_data():
    return dashboard_render("data/market-data-filter.html")


@bp.route('/dashboard/data/market/<string:state>/<int:slug_id>', methods=['GET'])
@crut.require_paid_account
def serve_market_data(state, slug_id):
    stateLabel = {'market_location_state': state}
    market_states = USDAReports(g.db).get_all_states()
    report = USDAReports(g.db).get_by_slug_id(slug_id)[0]
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
@crut.require_account
@csrf.csrf_protect
def serve_edit_account():
    # Get account information
    if request.method == 'POST':
        try:
            g.db.accounts.modify_account(
                account_id=g.account.id(),
                company=request.form["company"],
                address=request.form["address"],
                city=request.form["city"],
                state=request.form["state"],
                zip=request.form["zip"],
                phone=request.form["phone"],
                show_real_name=int(str_to_bool(request.form["show_real_name"])),
                can_partner_login=int(str_to_bool(request.form["can_partner_login"]))
            )
            EventLogs(g.db).insert(account_id=g.account.id(), user_id=g.user.id(), event_type_id=EVENT_TYPE_NAMES_TO_IDS["Account Info Edit"])
            return {"redirect": "/dashboard/edit/edit-account"}
        except UsersException as e:
            return {"error": str(e)}, HTTP_BAD_REQUEST
    elif request.method == 'GET':
        stripe.api_key = STRIPE_SECRET_KEY
        is_stripe_payouts_enabled = False
        if bool(request.args.get("stripe_onboarding")) and g.account.stripe_account_id() is not None and not bool(g.account.is_stripe_payouts_enabled()):
            # Check if this has changed
            stripe_account = stripe.Account.retrieve(g.account.stripe_account_id())
            if stripe_account["charges_enabled"]:
                g.db.accounts.update_account(account_id=g.account.id(), is_stripe_payouts_enabled=1)
                is_stripe_payouts_enabled = True
        else:
            is_stripe_payouts_enabled = bool(g.account.is_stripe_payouts_enabled())

        users = g.db.users.get_users(account_users__account=g.account.id(), is_email_verified=int(True))
        users = list(filter(lambda user: user['id'] != g.user.id(), users))
        return dashboard_render(
            "/dashboard/accounts/edit_account.html", {
                "sectors": SECTORS_NAME_TO_ID,
                "is_stripe_payouts_enabled": is_stripe_payouts_enabled,
                "users": users
            }
        )


# edit user profile
@bp.route('/dashboard/edit/edituser', methods=['GET', 'POST'])
@crut.require_account
@csrf.csrf_protect
def serve_edit_edituser():
    if request.method == 'POST':
        try:
            email = request.form["email"] if g.user.email() == ADMIN_EMAIL else g.user.email()
            if request.form["password"]:
                password = request.form["password"]
                confirm_password = request.form["confirm_password"]
                g.db.users.validate_user(email, password, confirm_password)
                g.db.users.modify_user(
                    id=g.user.id(), email=email, first_name=request.form["first"],
                    last_name=request.form["last"], phone=request.form["phone"], password=password
                )
            else:
                g.db.users.validate_user(email)
                g.db.users.modify_user(
                    id=g.user.id(), email=email, first_name=request.form["first"],
                    last_name=request.form["last"], phone=request.form["phone"]
                )
            EventLogs(g.db).insert(account_id=g.account.id(), user_id=g.user.id(), event_type_id=EVENT_TYPE_NAMES_TO_IDS["User Info Edit"])
            return {"redirect": "/dashboard/edit/edituser"}
        except UsersException as e:
            return {"error": str(e)}, 400
    elif request.method == 'GET':
        user = g.db.users.get_by_username(g.user.username())
        return dashboard_render("/dashboard/edit/edituser.html", {
            "user": user, "is_website_admin": True if g.user.username() == ADMIN_EMAIL else False
        })


@bp.route('/dashboard/inviteuser', methods=['GET', 'POST'])
@crut.require_account
def serve_invite_user():
    if request.method == 'POST':
        try:
            user_email = request.form["email"]
            if g.db.users.get_by_email(user_email) is not None:
                raise ExportException("A user with that email already exists!")

            confirm_url = token.create_user_invitation_link(user_email, g.account.id(), int(False))
            # Sending an email to user including Blocktrust email template and verification link with validity of 24 hours
            send_email(
                "BlockTrust Network Account Invite",
                render_email("invite_user.html", {
                    'confirm_url': confirm_url,
                    'account_name': g.account.name()
                }), user_email
            )
            employee_id = g.employee_id if "employee_id" in g else None
            InvitedUsers(g.db).insert_invited_user(
                email=user_email, invited_by_user_id=g.user.id(), invited_by_employee_id=employee_id
            )
            EventLogs(g.db).insert(
                event_type_id=EVENT_TYPE_NAMES_TO_IDS["User Invited By Account"],
                account_id=g.account.id(),
                user_id=g.user.id(),
                details={"invited_user_email": user_email}
            )
            return {"redirect": url_for("dashboard_bp.serve_dashboard")}
        except ExportException as e:
            return {"error": str(e)}, 400
    elif request.method == 'GET':
        return dashboard_render("/dashboard/accounts/invite_user.html")


@bp.route('/dashboard/connections', methods=['GET'])
@crut.require_account
def serve_connections():
    connections_data_access = Connections(g.db)

    account_connections = connections_data_access.get_connections(
        from_account_id_OR_to_account_id=g.account.id(),
        status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
        get_related_data=True
    )
    requests = connections_data_access.get_connections(to_account_id=g.account.id(), status=CONNECTION_STATUS_NAME_TO_ID["Pending"], get_related_data=True)

    blocked_connections = connections_data_access.get_connections(
        from_account_id_OR_to_account_id=g.account.id(),
        status=CONNECTION_STATUS_NAME_TO_ID["Blocked"],
        get_related_data=True
    )

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
@crut.require_user
def serve_accept_invite():
    Connections(g.db).update_connection_between(
        from_account_id=request.json["account_id"],
        to_account_id=g.account.id(),
        status=CONNECTION_STATUS_NAME_TO_ID["Connected"]
    )
    return Response(status=HTTP_NO_CONTENT)

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
@crut.require_user
def serve_block_connection():
    Connections(g.db).update_connection(
        id=request.json["connection_id"],
        connection_status_id=CONNECTION_STATUS_NAME_TO_ID["Blocked"],
        blocked_by_account_id=g.account.id()
    )
    return Response(status=HTTP_NO_CONTENT)


@bp.route('/dashboard/unblock-connection', methods=['POST'])
@crut.require_user
def serve_unblock_connection():
    Connections(g.db).update_connection(
        id=request.json["connection_id"],
        connection_status_id=CONNECTION_STATUS_NAME_TO_ID["Connected"]
    )
    return Response(status=HTTP_NO_CONTENT)


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
    return {"redirect": url_for("dashboard_bp.serve_dashboard")}


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
        sales_group_row = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)
        if sales_group_row["is_sold"] == 0:
            return dashboard_render("/dashboard/sales-groups/sales-group/purchase.html", {
                "sales_group_row": sales_group_row, "stripe_key": STRIPE_PUBLISHABLE_KEY, "name": g.user.first_name() + ' ' + g.user.last_name()
            })
        else:
            return {"error": "Sales group has been sold"}, 400
    else:
        try:
            request_data = json.loads(request.data)

            SalesGroups(g.db).update_sales_group(id=sales_group_id, is_sold=1, buyer_account_id=g.account.id())
            EventLogs(g.db).insert(
                account_id=g.account.id(),
                user_id=g.user.id(),
                event_type_id=EVENT_TYPE_NAMES_TO_IDS["Sales Group Purchase"],
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
    sales_group_row = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)
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
    return dashboard_render("sustainability/questionnaire_v2.html", {"sector": SECTORS_ID_TO_NAME[g.account.sector_id()]})


@bp.route("/dashboard/data-views", methods=["GET"])
@crut.require_account
def serve_views():
    view_logs = ViewLogs(g.db).get_view_logs(owner_account_id=g.account.id(), get_related_details=True)

    return dashboard_render("privacy/view-logs.html",
                            {"view_logs": view_logs, "view_logs_count": len(view_logs), "data_type_id_to_name": DATA_TYPE_ID_TO_NAME,
                             "animal_url": url_for("dashboard_bp.serve_animal_eid", animal_eid='')})


@bp.route("/dashboard/edit/edit-account-retail-data", methods=["GET"])
@crut.require_account
def serve_edit_account_retail_data():
    uploaded_retail_image_files = Files(g.db).get_files(
        retail_page_account_id=g.account.id(),
        select_columns=["id", "name"]
    )
    # json.dumps() helps to convert uploaded_retail_image_files into a JSON string which can be converted back in the widget without any errors.
    return dashboard_render("accounts/edit_account_retail_data.html", {"uploaded_retail_image_files": json.dumps(uploaded_retail_image_files)})


@bp.route("/dashboard/view-account-sustainability-scores/<int:account_id>", methods=["GET"])
@crut.require_account
def serve_view_account_sustainability_data(account_id):
    account_data = g.db.accounts.get_accounts(id=account_id)
    account_name = account_data[0]["name"] if len(account_data) > 0 else "N/A"
    return dashboard_render("sustainability/view_account_sustainability_scores.html", {"account_id": account_id, "account_name": account_name})


@bp.route("/dashboard/marketplace", methods=["GET"])
@crut.require_account
def serve_marketplace():
    return dashboard_render("marketplace/marketplace.html")


@bp.route("/dashboard/user/<int:user_id>", methods=["PUT"])
@crut.require_account
def update_user(user_id):
    request_data = json.loads(request.data)
    allowed_keys = {'reset_password'}
    if all(key in allowed_keys for key in request_data):
        if g.db.users.update_user(id=user_id, password=DEFAULT_PASSWORD):
            EventLogs(g.db).insert(
                event_type_id=EVENT_TYPE_NAMES_TO_IDS["Password Reset By Admin"],
                account_id=g.account.id(),
                user_id=g.user.id(),
                details={"password_reset_for_user_id": user_id}
            )
            return Response(status=HTTP_NO_CONTENT)
        else:
            return Response(status=HTTP_NOT_FOUND)
    else:
        return Response(status=HTTP_BAD_REQUEST)


@bp.route("/shop/tag-store", methods=["GET"])
@crut.require_account
def serve_tag_store():
    all_product_data = []
    product_vendors = ProductVendors(g.db).get_product_vendors()
    for product_vendor in product_vendors:
        vendor_products_data = ProductTable(g.db).get_products(
            product_vendor_id=product_vendor["id"],
            include_images=True,
            is_internal=int(True)
        )
        all_product_data.extend(vendor_products_data)
    
    product_categories = ProductCategories(g.db).get_product_categories()
    product_vendors = ProductVendors(g.db).get_product_vendors()
    product_vendor_ids_to_names = {}

    shopping_cart_link = WEBSITE_ROOT + url_for('dashboard_bp.serve_shopping_cart')
    for product_vendor in product_vendors:
        product_vendor_ids_to_names[product_vendor["id"]] = product_vendor["vendor_name"]
    return dashboard_render("tag-store/homepage.html", {
        "all_product_data": all_product_data,
        "product_categories": product_categories,
        "product_vendor_ids_to_names": product_vendor_ids_to_names,
        "shopping_cart_link": shopping_cart_link
    })


@bp.route("/shop/shopping-cart", methods=["GET"])
@crut.require_account
def serve_shopping_cart():
    shop_homepage_link = WEBSITE_ROOT + url_for('dashboard_bp.serve_tag_store')
    checkout_link = WEBSITE_ROOT + url_for('dashboard_bp.serve_checkout')
    return dashboard_render("tag-store/shopping-cart.html", {
        "shop_homepage_link": shop_homepage_link, 
        "checkout_link": checkout_link
    })


@bp.route("/shop/checkout", methods=["GET"])
@crut.require_account
def serve_checkout():
    shop_homepage_link = WEBSITE_ROOT + url_for('dashboard_bp.serve_tag_store')
    shopping_cart_link = WEBSITE_ROOT + url_for('dashboard_bp.serve_shopping_cart')
    checkout_payment_link = WEBSITE_ROOT + url_for('dashboard_bp.serve_checkout_payment')
    return dashboard_render("tag-store/checkout.html", {
        "shop_homepage_link": shop_homepage_link,
        "shopping_cart_link": shopping_cart_link,
        "checkout_payment_link": checkout_payment_link
    })


@bp.route("/shop/invoice", methods=["GET"])
@crut.require_account
def serve_invoice():
    shop_homepage_link = WEBSITE_ROOT + url_for("dashboard_bp.serve_tag_store")
    return dashboard_render("tag-store/invoice.html", {"shop_homepage_link": shop_homepage_link})


@bp.route("/shop/checkout-payment", methods=["GET"])
@crut.require_account
def serve_checkout_payment():
    herd_whistle_vendor_data = ProductVendors(g.db).get_product_vendors(vendor_name=HERD_WHISTLE_VENDOR_NAME)
    herd_whistle_vendor_id = herd_whistle_vendor_data[0]["id"]
    invoice_link = WEBSITE_ROOT + url_for('dashboard_bp.serve_invoice')
    return dashboard_render("tag-store/checkout-payment.html", {
        "stripe_key": STRIPE_PUBLISHABLE_KEY,
        "herd_whistle_vendor_id": herd_whistle_vendor_id,
        "invoice_link": invoice_link
    })


@bp.route("/shop/create-order", methods=["POST"])
@crut.require_account
def serve_create_order():
    try:
        data = json.loads(request.data)
        order_details = eval(data["orderDetails"])
        order_id = Orders(g.db).add_order(order_details, order_details["address_line"], order_details["city"],
                                          order_details["state"], order_details["zip_code"], account_id=g.account.id(),
                                          user_id=g.user.id())
        shopping_cart = json.loads(order_details['shopping_cart'])
        for product_id, product_details in shopping_cart.items():
            OrderProducts(g.db).add_order_product(order_id, product_id, product_details["quantity"])
        return {"orderId": order_id}
    except Exception as e:
        return {"error": str(e)}, HTTP_BAD_REQUEST


@bp.route("/shop/update-order", methods=["POST"])
@crut.require_account
def serve_update_order():
    try:
        data = json.loads(request.data)
        Orders(g.db).update_order_as_stripe_paid(data["orderId"], data["paymentIntent"])

        order_details = json.loads(data["orderDetails"])
        shopping_cart = json.loads(order_details["shopping_cart"])
        # Once payment goes through sending email to confirm order to buyer
        premise_id = "N/A"
        if order_details["premise_id"] != "":
            premise_id = order_details["premise_id"]
        send_tag_store_email(
            "Tag Store Purchase Summary",
            render_email("internal_tag_store/purchase_summary_customer.html", {
                'first': order_details["first_name"],
                'last': order_details["last_name"],
                'total_price': order_details["total_price"],
                'total_tax': order_details["total_tax"],
                'discount': order_details["discount"],
                'shipping': order_details["shipping"],
                'grand_total': order_details["grand_total"],
                'shipping_address_line': order_details["address_line"],
                'shipping_city': order_details["city"],
                'shipping_state': order_details["state"],
                'shipping_zip_code': order_details["zip_code"],
                'cart': shopping_cart,
                'premise_id': premise_id
            }),
            order_details["email"],
            EMAIL_SENDER
        )
        vendor_oriented_cart = {}
        for product_id, product_details in shopping_cart.items():
            product_row = ProductTable(g.db).get_products(id=product_id)
            product_vendor_id = product_row[0]["product_vendor_id"]
            if product_vendor_id in vendor_oriented_cart:
                vendor_oriented_cart[product_vendor_id].append(product_details)
            else:
                vendor_oriented_cart[product_vendor_id] = [product_details]

        for vendor_id, products_list in vendor_oriented_cart.items():
            vendor_row = ProductVendors(g.db).get_product_vendors(id=vendor_id)
            vendor_email = vendor_row[0]["vendor_email"]
            send_tag_store_email(
                "New order summary",
                render_email("internal_tag_store/purchase_summary_vendor.html", {
                    'order_id': data["orderId"],
                    'first': order_details["first_name"],
                    'last': order_details["last_name"],
                    'shipping_address_line': order_details["address_line"],
                    'shipping_city': order_details["city"],
                    'shipping_state': order_details["state"],
                    'shipping_zip_code': order_details["zip_code"],
                    'cart': products_list,
                    'premise_id': premise_id
                }),
                vendor_email,
                EMAIL_SENDER
            )

        send_multiple_tag_store_email(
            "New order summary",
            render_email("internal_tag_store/purchase_summary_seller.html", {
                'order_id': data["orderId"],
                'first': order_details["first_name"],
                'last': order_details["last_name"],
                'total_price': order_details["total_price"],
                'total_tax': order_details["total_tax"],
                'discount': order_details["discount"],
                'shipping': order_details["shipping"],
                'grand_total': order_details["grand_total"],
                'shipping_address_line': order_details["address_line"],
                'shipping_city': order_details["city"],
                'shipping_state': order_details["state"],
                'shipping_zip_code': order_details["zip_code"],
                'cart': shopping_cart,
                'premise_id': premise_id
            }),
            [ADMIN_EMAIL],
            EMAIL_SENDER
        )
        return Response(status=HTTP_NO_CONTENT)
    except Exception as e:
        return {"error": str(e)}, HTTP_BAD_REQUEST


@bp.route("/shop/send-order-to-herdwhistle-api", methods=["POST"])
@crut.require_account
def serve_send_order_to_herdwhistle_api():
    herd_whistle_data = ProductVendors(g.db).get_product_vendors(vendor_name=HERD_WHISTLE_VENDOR_NAME)
    data = json.loads(request.data)
    order_details = json.loads(data["orderDetails"])
    shopping_cart = json.loads(order_details["shopping_cart"])
    customer_details = {
        'name': order_details["first_name"] + " " + order_details["last_name"],
        'street': order_details["address_line"],
        'street2': False,
        'city': order_details["city"],
        'state_id': order_details["state"],
        'zip': order_details["zip_code"],
        'country_id': 'United States',
        'phone': order_details["phone"],
        'email': order_details["email"],
        'company_type': 'company',
        'type': 'contact'
    }
    herdwhistle_identifiers_for_account = VendorIdentifiersForAccounts(g.db).get(
        product_vendor_id=herd_whistle_data[0]["id"],
        account_id=g.account.id()
    )
    if len(herdwhistle_identifiers_for_account) > 0:
        herdwhistle_customer_id = herdwhistle_identifiers_for_account[0]["vendor_customer_id"]
        herdwhistle_customer_shipping_id = herdwhistle_identifiers_for_account[0]["vendor_customer_shipping_id"]
    else:
        herdwhistle_customer_id, herdwhistle_customer_shipping_id = HerdWhistleAPI().create_new_herdwhistle_customer_credentials(
            customer_details=customer_details
        )
        VendorIdentifiersForAccounts(g.db).insert(
            account_id=g.account.id(),
            product_vendor_id=herd_whistle_data[0]["id"],
            vendor_customer_id=herdwhistle_customer_id,
            vendor_customer_shipping_id=herdwhistle_customer_shipping_id
        )
    if HerdWhistleAPI().verify_herdwhistle_customer_credentials(
        herdwhistle_customer_id=herdwhistle_customer_id,
        herdwhistle_customer_shipping_id=herdwhistle_customer_shipping_id
    ):
        herdwhistle_products_shopping_cart = []
        for product_details in shopping_cart.values():
            if product_details["product_vendor_id"] == herd_whistle_data[0]["id"]:
                herdwhistle_products_shopping_cart.append(product_details)
        sale_order_id = HerdWhistleAPI().create_new_sale_order(
            herdwhistle_customer_id=herdwhistle_customer_id,
            herdwhistle_customer_shipping_id=herdwhistle_customer_shipping_id,
            herdwhistle_products_shopping_cart=herdwhistle_products_shopping_cart
        )
        Orders(g.db).update(id=data["orderId"], herdwhistle_sale_order_id=sale_order_id)
    return Response(status=HTTP_NO_CONTENT)


@bp.route("/shop/view-orders", methods=["GET"])
@crut.require_account
def serve_view_order_history():
    user_orders = Orders(g.db).get_orders(account_id=g.account.id(), user_id=g.user.id())
    return dashboard_render("tag-store/view-orders.html", {"user_orders": user_orders})


@bp.route("/shop/view-orders/<int:order_id>", methods=["GET"])
@crut.require_account
def serve_view_order(order_id):
    try:
        user_order = Orders(g.db).get_orders(id=order_id, account_id=g.account.id(), user_id=g.user.id())
        if len(user_order) > 0:
            user_order = user_order[0]
            order_products = OrderProducts(g.db).get_order_products(order_id)
            for product in order_products:
                product_details = ProductTable(g.db).get_products(id=product["product_id"])
                product["product_details"] = product_details[0]
            return dashboard_render("tag-store/view-order.html", {"order": user_order, "order_products": order_products})
        else:
            raise ExportException("Sorry, the requested order was not found. ")
    except ExportException as e:
        return dashboard_render("tag-store/view-order.html", {"error": str(e)})


@bp.route("/dashboard/seedstock-producers", methods=["GET"])
@crut.require_account
def serve_seedstock_producers():
    seedstock_producers = SeedstockProducers(g.db).get(is_archived=0, include_logo_url=True)
    return dashboard_render("marketplace/seedstock-producers.html", {"seedstock_producers": seedstock_producers})

@bp.route("/dashboard/genetics", methods=["GET", "POST"])
@crut.require_account
def serve_genetics():
    if request.method == "GET":
        if g.account.sector_id() == SECTORS_NAME_TO_ID["Cow-Calf"]:
            breeds = SalesGroupFieldsValues(g.db).get(field_id=SALES_GROUP_FIELD_NAMES_TO_IDS["breed"])
            return dashboard_render("genetics/genetics-cow-calf.html", {"breeds": breeds})
        if g.account.sector_id() == SECTORS_NAME_TO_ID["Seedstock Producer"]:
            return dashboard_render("genetics/genetics.html", {"license": FLATFILE_LICENSE, "user": g.user})
    elif request.method == "POST":
        if g.account.sector_id() == SECTORS_NAME_TO_ID["Cow-Calf"]:
            insemination_data = {
                "genetics_uid": request.form["genetics_uid"],
                "genetics_kit_breed": request.form["genetics_kit_breed"],
                "animal_breed" : request.form["animal_breed"]
            }
            account_link_id = None
            account_links = g.account.account_links()
            if len(account_links) > 0:
                account_link_data = account_links[0]
                account_link_id = account_link_data.id()
            Matches(g.db).insert(
                eid=request.form["eid"],
                type_int=MATCH_TYPES_NAME_TO_ID["Insemination"],
                data=insemination_data,
                partner_account=g.account.partner_account_id(),
                account_link=account_link_id
            )
            return {"redirect": "/dashboard"}
        if g.account.sector_id == SECTORS_NAME_TO_ID["Seedstock Producer"]:
            for genetics_data in request.json["genetics_data"]:
                Genetics(g.db).insert(
                    owner_account_id=g.account.id(),
                    uid=genetics_data["uid"],
                    breed=genetics_data["breed"],
                    ranch_name=genetics_data["ranch_name"],
                    address=genetics_data["address"],
                    city=genetics_data["city"],
                    state=genetics_data["state"],
                    zip_code=genetics_data["zip_code"]
                )
            return Response(status=HTTP_OK)


@bp.route('/dashboard/sales-groups/upload-eids-using-excel/<int:sales_group_id>', methods=["GET", "POST"])
@crut.require_account
def serve_upload_eids_using_excel(sales_group_id):
    if request.method == "GET":
        try:
            sales_group = SalesGroups(g.db).get_sales_group_by_id(sales_group_id)
            sales_group_animals = SalesGroupAnimals(g.db).get(sales_group_id=sales_group_id)
            if sales_group["account"] != g.account.id():
                return dashboard_render("errors/no-access.html")
            return dashboard_render("sales-groups/sales-group/upload-eids.html", {
                "sales_group": sales_group,
                "sales_group_animals": sales_group_animals,
                "license": FLATFILE_LICENSE,
                "user": g.user
            })
        except Exception as e:
            return dashboard_render("errors/no-access.html")
    elif request.method == "POST":
        eids_list = [eid_and_visual_id["eid"] for eid_and_visual_id in request.json["uploaded_eids_and_visual_ids"]]
        sales_group_animals = SalesGroupAnimals(g.db).check_if_eids_are_present(eids=eids_list)
        if len(sales_group_animals) == 0:
            uploaded_eids_and_visual_ids = []
            for uploaded_eid_and_visual_id in request.json["uploaded_eids_and_visual_ids"]:
                visual_id = None
                if "visual_id" in uploaded_eid_and_visual_id and len(uploaded_eid_and_visual_id["visual_id"]) > 0:
                    visual_id = int(uploaded_eid_and_visual_id["visual_id"])
                uploaded_eids_and_visual_ids.append({
                    "eid": uploaded_eid_and_visual_id["eid"],
                    "visual_id": visual_id
                })
            SalesGroupAnimals(g.db).insert(
                sales_group_id=sales_group_id,
                eids_and_visual_ids=uploaded_eids_and_visual_ids
            )
            return {"upload_completed": True}
        return {"upload_completed": False, "sales_group_animals": sales_group_animals}