from core.renderers.outside import outside_render
from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, url_for
)

from core.config import FLATFILE_LICENSE
from ..renderers.dashboard import dashboard_render

from ..sectors import sectors_by_id

from ..common_exceptions import ExportException

from ..data_requests.router import unauth_route

from ..database.tables.connections import Connections, connection_status
from ..database.tables.connection_invites import ConnectionInvites
from ..database.tables.connections import connection_status
from ..database.tables.invited_users import InvitedUsers
from ..database.tables.account_users import NoAccountUserFound
from ..database.tables.accounts import AccountsException
from ..database.tables.users import UsersException

from ..renderers.email import render_email

from ..utilities import crut, auth
from ..utilities import token
from ..utilities.email import send_email

from core.config import SUPPORT_GENERAL_EMAIL, ROOT as WEBSITE_ROOT

import json
import flask_excel as excel

bp = Blueprint('dashboard_bp', __name__)

excel.init_excel(bp)


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

# @bp.route('/dashboard/accounts/new-account', methods=['GET'])
# @crut.require_user
# def serve_accounts_new_account():
#     return dashboard_render("accounts/new_account.html", {
#         "sectors_by_id": sectors_by_id
#     })

# # 6/3/21 Deprecated
# @bp.route('/dashboard/accounts/new-account/action', methods=['POST'])
# @crut.require_user
# def serve_accounts_new_account_action():
#     try:
#         required = {
#             'name': None, 'company': None, 'sector': None
#         }
#         for required_field in required:
#             if required_field not in request.form:
#                 raise ExportException("internal error, {} missing from form".format(required_field))
#             required[required_field] = request.form[required_field]

#         # Create Account
#         try:
#             sector_id = -1
#             try:
#                 sector_id = int(required['sector'])
#             except:
#                 raise ExportException("Sector ID not a number.")
#             if sector_id not in sectors_by_id:
#                 raise ExportException("Sector ID not recognized.")
#             account = g.db.accounts.create_account(
#                 user=g.user,
#                 company=required['company'],
#                 sector=required['sector'],
#             )
#             auth.session_start_account(account.id())
#             return {"redirect": "/dashboard/accounts/" + str(account.id())}
#         except AccountsException as e:
#             raise ExportException("Account creation failed: " + str(e))
#     except ExportException as e:
#         return {"error": str(e)}, 400

# # 6/3/21 Deprecated
# @bp.route('/dashboard/accounts/join-account', methods=['GET'])
# @crut.require_user
# def serve_accounts_join_account():
#     return dashboard_render("accounts/join_account.html")


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
    elif account.sector_name() == "Buyer":
        return dashboard_render("sectors/buyer.html", sector_params)
    else:
        return dashboard_render("sectors/generic.html", sector_params)


@bp.route('/dashboard/animals/<int:animal_eid>', methods=['GET'])
@crut.require_user
def serve_animal_eid(animal_eid):
    animal = g.db.animals.get_by_eid(animal_eid)

    if len(animal.matches()) == 0:
        return dashboard_render("animals/animal_not_found.html", {"eid": animal_eid})

    return dashboard_render("animals/animal.html", {"animal": animal, "company": g.account.company()})

@bp.route('/dashboard/animals/<int:animal_eid>/certificates', methods=['GET'])
@crut.require_user
def serve_animal_cert(animal_eid):
    animal = g.db.animals.get_by_eid(animal_eid)
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
    new_id = g.db.sales_groups.insert(g.account.id(), {})['id']

    return redirect('/dashboard/sales-groups/edit/' + str(new_id) + '')


@bp.route('/dashboard/sales-groups/edit/<int:sales_group_id>', methods=['GET'])
@crut.require_paid_account
def serve_edit_sales_group(sales_group_id):
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(sales_group_id)

    if sales_group_row['account'] != g.account.id():
        return dashboard_render("sales-groups/sales-group/no.html")

    return dashboard_render("sales-groups/sales-group/edit.html", {"sales_group": sales_group_row})


@bp.route('/dashboard/sales-groups/archive', methods=['GET'])
@crut.require_account
def serve_sales_group_archive():
    return dashboard_render("sales-groups/sales-group/archive.html", {"account_id": g.account.id()})


@bp.route('/dashboard/sales-groups/view/<int:sales_group_id>', methods=['GET'])
@crut.require_paid_account
def serve_view_sales_group(sales_group_id):
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(sales_group_id)

    if sales_group_row['account'] == g.account.id() or sales_group_row['published'] > 0:
        return dashboard_render(
            "sales-groups/sales-group/view.html",
            {"sales_group": sales_group_row}
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
            return "", 200
        except Exception as e:
            return {'error':{'message': str(e)}}, 400
    elif request.method == 'GET':
        return dashboard_render("data/upload-tags.html",  {"account": g.account, "user": g.user, "license": FLATFILE_LICENSE})


@bp.route('/dashboard/sustainability', methods=['GET'])
@crut.require_paid_account
def serve_sustainability():
    return dashboard_render("sustainability/summary.html", 
    { 
        "sector": sectors_by_id[g.account.sector_id()],
        "sectorID": g.account.sector_id()
    })


@bp.route('/dashboard/sustainability/survey', methods=['GET'])
@crut.require_paid_account
def serve_sustainability_survey():
    return dashboard_render("sustainability/questionaire.html", 
    { 
        "sector": sectors_by_id[g.account.sector_id()]
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

    if stateLabel in market_states:
        return dashboard_render("data/market-data.html",
            {
                "slug_id": slug_id,
                "state": state
            })
    raise Exception("Invalid state")

# edit account profile


@bp.route('/dashboard/edit/edit-account', methods=['GET', 'POST'])
@crut.require_user
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
            return {"redirect": "/dashboard/edit/edit-account"}
        except UsersException as e:
            return {"error": str(e)}, 400
    elif request.method == 'GET':
        return dashboard_render("/dashboard/accounts/edit_account.html", {"account": g.account})


# edit user profile
@bp.route('/dashboard/edit/edituser', methods=['GET', 'POST'])
@crut.require_user
def serve_edit_edituser():
    if request.method == 'POST':
        try:
            g.db.users.update_user(
                        username=g.user.username(),
                        first_name=request.form["first"],
                        last_name=request.form["last"],
                        phone=request.form["phone"],
                        password=request.form["password"],
                        confirm_password=request.form["confirm_password"]
                        )
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
            confirm_url = WEBSITE_ROOT + url_for('outside_bp.serve_add_user', tok=userToken)
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
    account_connections = Connections(g.db).get_account_connections(g.account.id(), connection_status["Connected"])
    return dashboard_render("/dashboard/connections/connections.html", {"account_connections": account_connections})


@bp.route('/dashboard/add-connection', methods=['GET'])
@crut.require_account
def serve_add_connection():
    account_rows = g.db.accounts.get_accounts(is_partner=0)
    for account_row in account_rows:
        if account_row["id"] == g.account.id():
            account_rows.remove(account_row)
    return dashboard_render("/dashboard/connections/add-connection.html", {"account_rows": account_rows})


@bp.route('/dashboard/add-connection', methods=['POST'])
@crut.require_account
def serve_add_connection_request():
    try:
        if request.form["company_id"] != "0":
            Connections(g.db).create_connection(g.account.id(), request.form["company_id"], connection_status["Pending"])
        else:
            ConnectionInvites(g.db).add_connection_invite(
                from_account=g.account.id(),
                company_sector=request.form["sector"],
                company_name=request.form["new_company_name"],
                company_contact=request.form["new_company_contact"],
                company_email=request.form["new_company_email"]
            )
            send_email(
                "BlockTrust Network Connection Invite",
                render_email("send_connection_invite.html", {
                    'new_company_contact': request.form["new_company_name"],
                    'account_company': g.account.name()
                }), request.form["new_company_email"]
            )
        return {"redirect": "/dashboard/connections"}
    except Exception as e:
        return {"error": str(e)}, 400


@bp.route('/dashboard/view-invites', methods=['GET'])
@crut.require_account
def serve_view_invites():
    requests = Connections(g.db).get_account_connections(g.account.id(), connection_status["Pending"])
    return dashboard_render("/dashboard/connections/view-invites.html", {"requests": requests})


@bp.route('/dashboard/calf-crop-summary/download', methods=['GET'])
@crut.require_account
def serve_summary_download():
    count_eid_distinct = unauth_route({"type": 'count_eid_distinct', "params": {}})
    global_usda_yield_grade_distribution = unauth_route({"type": 'count_distribution_global', "params": {'match_type': 'USDA Yield Grade'}})
    global_usda_quality_grade_distribution = unauth_route({"type": 'count_distribution_global', "params": {'match_type': 'USDA Quality Grade'}})

    account_total_distinct = unauth_route({"type": 'count_eid_distinct_by_account', "params": {}})
    account_usda_yield_grade_distribution = unauth_route({"type": 'count_distribution', "params": {'match_type': 'USDA Yield Grade', 'account': None}})
    account_usda_quality_grade_distribution = unauth_route({"type": 'count_distribution', "params": {'match_type': 'USDA Quality Grade', 'account': None}})

    if count_eid_distinct["result"] is not None:
        global_calves = count_eid_distinct["result"]["count_eid_distinct"]
    else:
        global_calves = None

    if global_usda_yield_grade_distribution["result"] is not None:
        global_yield = global_usda_yield_grade_distribution["result"]["count_distribution"]
    else:
        global_yield = None

    if global_usda_quality_grade_distribution["result"] is not None:
        global_quality = global_usda_quality_grade_distribution["result"]["count_distribution"]
    else:
        global_quality = None
    if account_total_distinct["result"] is not None:
        account_calves = account_total_distinct["result"]
    else:
        account_calves = None
    if account_usda_yield_grade_distribution["result"] is not None:
        account_yield = account_usda_yield_grade_distribution["result"]
    else:
        account_yield = None
    account_quality = account_usda_quality_grade_distribution["result"]

    # Global Yield grade calculatiuon
    yg_global = [0, 0, 0, 0, 0]
    global_total_available = 0
    if global_yield is not None:
        for gy in global_yield:
            global_total_available += gy["count"]
            if gy["data"] >= 1 or gy["data"] <= 5:
                yg_global[5-gy["data"]] += gy["count"]
            else:
                yg_global[5] += gy["count"]
        for i in range(len(yg_global)):
            if(global_total_available > 0):
                yg_global[i] = round(100 * yg_global[i] / global_total_available)
            else:
                yg_global[i] = "N/A"

    # Global Quality grade calculation
    qg_global = [0, 0, 0, 0]
    global_total_available = 0
    if global_quality is not None:
        for gq in global_quality:
            global_total_available += gq["count"]
            if gq["data"] == "Prime":
                qg_global[0] += gq["count"]
            if gq["data"] == "Choice":
                qg_global[1] += gq["count"]
            if gq["data"] == "Select or Lower":
                qg_global[2] += gq["count"]
            else:
                qg_global[3] += gq["count"]
        for i in range(len(qg_global)):
            if(global_total_available > 0):
                qg_global[i] = round(100 * qg_global[i] / global_total_available)
            else:
                qg_global[i] = "N/A"

    # Account Yield Grade claculation
    yg_account = [0, 0, 0, 0, 0]
    account_total_available = 0
    if account_yield is not None:
        for ay in account_yield:
            account_total_available += ay["count"]
            if ay["data"] >= 1 or ay["data"] <= 5:
                yg_account[5-ay["data"]] += ay["count"]
            else:
                yg_account[5] += ay["count"]
        for i in range(len(yg_account)):
            if(account_total_available > 0):
                yg_account[i] = round(100 * yg_account[i] / account_total_available)
            else:
                yg_account[i] = "N/A"

    # Account Quality Grade calculation
    qg_account = [0, 0, 0, 0]
    account_total_available = 0
    if account_quality is not None:
        for aq in account_quality:
            account_total_available += aq["count"]
            if aq["data"] == "Prime":
                qg_account[0] += aq["count"]
            if aq["data"] == "Choice":
                qg_account[1] += aq["count"]
            if aq["data"] == "Select or Lower":
                qg_account[2] += aq["count"]
            else:
                qg_account[3] += aq["count"]
        for i in range(len(qg_account)):
            if(account_total_available > 0):
                qg_account[i] = round(100 * qg_account[i] / account_total_available)
            else:
                qg_account[i] = "N/A"

    global_percentage_available = 0
    account_percentage_available = 0
    if global_calves is not None and global_total_available != 0:
        global_percentage_available = round(100 * global_total_available / global_calves)
    if account_calves is not None and account_total_available != 0:
        account_percentage_available = round(100 * account_total_available / account_calves)
    if global_calves is None:
        global_calves = "N/A"
    if account_calves is None:
        account_calves = "N/A"

    # Generating the excel report
    summary = []
    summary.append(["", g.account.company() + "(%)", "Global Benchmark (%)"])
    summary.append(["Sightings Summary", "", ""])
    summary.append(["Total Calves", account_calves, global_calves])
    summary.append(["Total Available", account_total_available, global_total_available])
    summary.append(["% Available", account_percentage_available, global_percentage_available])
    summary.append(["Carcass Quality(Percentage of Available)", "", ""])
    summary.append(["Prime", qg_account[0], qg_global[0]])
    summary.append(["Choice", qg_account[1], qg_global[1]])
    summary.append(["Select or Lower", qg_account[2], qg_global[2]])
    summary.append(["Other", qg_account[3], qg_global[3]])
    summary.append(["Carcass Yield Grade(Percentage of Available)", "", ""])
    summary.append(["YG 5", yg_account[0], yg_global[0]])
    summary.append(["YG 4", yg_account[1], yg_global[1]])
    summary.append(["YG 3", yg_account[2], yg_global[2]])
    summary.append(["YG 2", yg_account[3], yg_global[3]])
    summary.append(["YG 1", yg_account[4], yg_global[4]])
    summary.append(["Other", 0, 0])

    return excel.make_response_from_array(summary, "xlsx", file_name="Calf-Crop-Summary")


@bp.route('/dashboard/animal-data/<string:eid>/download', methods=['GET'])
@crut.require_account
def serve_animal_data_download(eid):
    match_rows = unauth_route({"type": 'matches_by_eids', "params": {"eids": eid, "ljoin_account_links": True}})
    results = match_rows["result"]["matches"]
    # for result in results:
    #    print(result)
    # print(len(results))

    health_data_match_rows = unauth_route({"type": 'matches_by_eids', "params": {"eids": eid, "ljoin_account_links": True, "types": ["Medical"]}})
    health_data_results = health_data_match_rows["result"]["matches"]
    animal_data = []
    animal_data.append(["Date", "Symptom", "Diagnosis", "Product", "Location"])
    for health_data_result in health_data_results:
        symptom = ""
        product = ""
        diagnosis = ""
        location = ""
        if "symptom" in health_data_result["data"]:
            symptom = health_data_result["data"]["symptom"]
        if "product" in health_data_result["data"]:
            product = health_data_result["data"]["product"]
        if "diagnosis" in health_data_result["data"]:
            diagnosis = health_data_result["data"]["diagnosis"]
        if "location" in health_data_result["data"]:
            location = health_data_result["data"]["location"]
        animal_data.append([
            health_data_result["created_timestamp"].strftime("%m/%d/%Y" + " at " + "%H:%M"),
            symptom,
            product,
            diagnosis,
            location
            ])
    print(animal_data)
    return {}


@bp.route('/dashboard/accept-invite', methods=['POST'])
@crut.require_account
def serve_accept_invite():
    Connections(g.db).update_connection(
        from_account_id=request.json["account_id"],
        to_account_id=g.account.id(),
        status=connection_status["Connected"]
    )
    return {}


@bp.route('/dashboard/decline-invite', methods=['POST'])
@crut.require_account
def serve_decline_invite():
    Connections(g.db).update_connection(
        from_account_id=request.json["account_id"],
        to_account_id=g.account.id(),
        status=connection_status["Declined"]
    )
    return {}


@bp.route('/dashboard/view-profile/<int:account_id>', methods=['GET'])
@crut.require_account
def serve_view_profile(account_id):
    account_details = g.db.accounts.get_by_id(account_id)
    if Connections(g.db).get_connection_between(g.account.id(), account_details.id()) == connection_status["Connected"]:
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
