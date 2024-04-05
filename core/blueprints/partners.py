from flask import (
    Response, Blueprint, g, redirect, request, url_for
)
from core.common_exceptions import ExportException
from core.config import FLATFILE_LICENSE
from core.database.combinations import perform_new_account_actions
from core.database.tables.account_links import AccountLinks
from core.database.tables.accounts import Accounts, HEALTH_TRACK_PARTNER_COMPANY, AccountsException
from core.database.tables.api_inserts import ApiInserts
from core.database.tables.connections import CONNECTION_STATUS_NAME_TO_ID, CONNECTION_TYPE_ID_TO_NAME, CONNECTION_TYPE_NAME_TO_ID, Connections
from core.database.tables.event_logs import EventLogs, EVENT_TYPE_NAMES_TO_IDS
from core.database.tables.impersonations import Impersonations
from core.database.tables.matches import Matches
from core.database.tables.reports import Reports
from core.database.tables.sustainability_responses import SustainabilityResponses, QUESTIONNAIRE_STATUS_NAMES_TO_IDS
from core.database.tables.users import UsersException
from core.reports.query_types import count_distribution
from core.sectors import SECTORS_NAME_TO_ID, SECTORS_ID_TO_NAME
from core.utilities import auth
from core.utilities.constants import HTTP_OK
from ..renderers.partner import partner_render
from ..utilities import crut, csrf
from json import loads
import json

bp = Blueprint('partner_bp', __name__, url_prefix="/partner")


@bp.route('/dashboard', methods=['GET'])
@crut.require_partner
def serve_dashboard():
    pending_connection_requests_count = len(Connections(g.db).get_connections(
        to_account_id=g.account.id(), status=CONNECTION_STATUS_NAME_TO_ID["Pending"])
    )

    return partner_render("homepage.html", {
        "SECTORS_NAME_TO_ID": SECTORS_NAME_TO_ID,
        "animal_URL": url_for("partner_bp.serve_animal_eid"),
        "view_scores_URL": url_for("partner_bp.serve_view_account_sustainability_data"),
        "pending_connection_requests_count": pending_connection_requests_count
    })


@bp.route('/edit-user', methods=['GET'])
@crut.require_partner
@csrf.csrf_protect
def serve_edit_user():
    user = g.db.users.get_by_username(g.user.username())
    return partner_render("/partner/edit-user.html", {
        "user": user, "is_website_admin": False
    })


@bp.route('/animals/', defaults={'animal_eid': ''}, methods=['GET'])
@bp.route("/animals/<int:animal_eid>", methods=["GET"])
@crut.require_partner
def serve_animal_eid(animal_eid):
    animal = Matches(g.db).get_animal_by_eid(animal_eid)
    if show_animal := bool(len(animal.matches)):
        display_certificate = False
        owner_account_match = sorted(
            list(filter(lambda row: row["sector"] == SECTORS_NAME_TO_ID["Cow-Calf"], animal.matches)),
            key=lambda row: row["id"]
        )

        if owner_account_match:
            if owner_account_match[0]["partner_account"] != g.account.id():
                connection = Connections(g.db).get_connection_between(
                    from_account_id=g.account.id(), to_account_id=owner_account_match[0]["account"]
                )
                if not connection:
                    connected_account_ids = Connections(g.db).get_connected_account_ids(
                        account_id=owner_account_match[0]["account"]
                    )
                    for account_id in connected_account_ids:
                        account = g.db.accounts.get_accounts(id=account_id)[0]
                        if account["partner_account"] == g.account.id():
                            break
                    else:
                        show_animal = False

            health_track_partner = g.db.accounts.get_partners(company=HEALTH_TRACK_PARTNER_COMPANY)[0]
            if owner_account_match[0]["partner_account"] == health_track_partner["id"]:
                display_certificate = True
        else:
            show_animal = False

        if show_animal:
            return partner_render("animals/animal.html", {"animal": animal, "display_certificate": display_certificate})            

    return partner_render("animals/animal_not_found.html", {"eid": animal_eid})


@bp.route('/view-account-sustainability-scores/', defaults={'account_id': ''}, methods=['GET'])
@bp.route("/view-account-sustainability-scores/<int:account_id>", methods=["GET"])
@crut.require_partner
def serve_view_account_sustainability_data(account_id):
    account_data = g.db.accounts.get_accounts(id=account_id)
    account_name = account_data[0]["name"] if len(account_data) > 0 else "N/A"
    return partner_render("sustainability/view_account_sustainability_scores.html", {
        "account_id": account_id, "account_name": account_name
    })


@bp.route('/upload-tags', methods=['GET', 'POST'])
@crut.require_partner
def serve_upload_tags():
    if request.method == 'POST':
        data = loads(request.data)
        try:
            for row in data["eids"]:
                ApiInserts(g.db).insert(g.account.id(), "PARTNER", "TagUpload", row)
            EventLogs(g.db).insert(
                account_id=g.account.id(), user_id=g.user.id(), event_type_id=EVENT_TYPE_NAMES_TO_IDS["Tag Upload"]
            )
            return "", 200
        except Exception as e:
            raise ExportException(e)
    elif request.method == 'GET':
        return partner_render("upload-tags.html",  {
            "account": g.account, "user": g.user, "license": FLATFILE_LICENSE
        })


@bp.route('/upload-packer-data', methods=['GET', 'POST'])
@crut.require_partner
def serve_upload_packer_data():
    # hard coded for now should be changed later
    eligible_packers = g.db.accounts.get_accounts(company_like="National Beef", is_partner=int(False))
    if request.method == 'POST':
        data = loads(request.data)
        try:
            packer_account_numbers = {packer["id"] for packer in eligible_packers}
            for row in data["eids"]:
                if int(row["packer_account_number"]) not in packer_account_numbers:
                    raise Exception("Packer account number is incorrect")
                ApiInserts(g.db).insert(g.account.id(), "PARTNER", "PackerDataUpload", row)

            return Response(status=HTTP_OK)
        except Exception as e:
            raise ExportException(e)

    return partner_render("upload-packer-data.html",  {
        "account": g.account, "user": g.user, "license": FLATFILE_LICENSE, "eligible_packers": eligible_packers
    })


@bp.route('/connections', methods=['GET'])
@crut.require_partner
def serve_connections():
    connections_data_access = Connections(g.db)
    account_connections = connections_data_access.get_connections(
        from_account_id_OR_to_account_id=g.account.id(),
        status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
        get_related_data=True
    )

    requests = connections_data_access.get_connections(
        to_account_id=g.account.id(), status=CONNECTION_STATUS_NAME_TO_ID["Pending"], get_related_data=True
    )

    blocked_connections = connections_data_access.get_connections(
        from_account_id_OR_to_account_id=g.account.id(),
        status=CONNECTION_STATUS_NAME_TO_ID["Blocked"],
        get_related_data=True
    )

    return partner_render("connections/connections.html", {
        "account_connections": account_connections,
        "requests": requests,
        "blocked_connections": blocked_connections,
        "CONNECTION_TYPE_ID_TO_NAME": CONNECTION_TYPE_ID_TO_NAME
    })


@bp.route('/profile/<int:account_id>', methods=['GET'])
@crut.require_partner
def serve_view_profile(account_id):
    if Connections(g.db).get_connection_between(g.account.id(), account_id, CONNECTION_STATUS_NAME_TO_ID["Connected"]) is not None:
        account_details = g.db.accounts.get_account_by_id(account_id)
        return partner_render("connections/profile.html", {"account_details": account_details})
    else:
        return redirect(url_for("partner_bp.serve_connections"))


@bp.route('/view-partner-accounts-sustainability-data', methods=['GET'])
@crut.require_partner
def serve_view_partner_accounts_sustainability_data():
    sector_based_account_data_for_connections = {}
    eid_based_account_data_for_connections = {}
    account_id_and_connected_account_ids = Connections(g.db).get_connected_account_ids(g.account.id())
    account_id_and_connected_account_ids.append(g.account.id())
    for connected_account_id in account_id_and_connected_account_ids:
        connected_account_data = Accounts(g.db).get_accounts(id=connected_account_id)
        connected_account_name = connected_account_data[0]["name"]
        partner_accounts_data = Accounts(g.db).get_accounts(partner_account=connected_account_id)
        sector_based_accounts = {
            SECTORS_NAME_TO_ID["Cow-Calf"]: {},
            SECTORS_NAME_TO_ID["Feedlot"]: {},
            SECTORS_NAME_TO_ID["Packer"]: {},
        }
        for partner_account_data in partner_accounts_data:
            account_id = partner_account_data["id"]
            account_links = AccountLinks(g.db).get_account_links(account_id=account_id)
            if len(account_links) > 0:
                for account_link in account_links:
                    matched_accounts = Matches(g.db).get_sighted_match_accounts_for_account_link(account_link["id"])
                    for matched_account in matched_accounts:
                        matched_account_id = matched_account["account_id"]
                        accounts_object_for_sector = sector_based_accounts[matched_account["account_sector_id"]]
                        if matched_account_id not in accounts_object_for_sector:
                            # Sustainability data for matched account
                            account_sustainability_responses_data = SustainabilityResponses(g.db).get_sustainability_responses(
                                account_id=matched_account_id,
                                questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Completed"]
                            )
                            if len(account_sustainability_responses_data) > 0:
                                account_sustainability_response_data = account_sustainability_responses_data[0]
                                matched_account["account_sustainability_data"] = account_sustainability_response_data
                            else:
                                matched_account["account_sustainability_data"] = None

                            # USDA Quality and Yield grade
                            usda_quality_grade_data = Reports(g.db).get_ready_by_query(count_distribution.create(matched_account_id, "USDA Quality Grade", 0))
                            matched_account["usda_quality_grade_data"] = usda_quality_grade_data["result"] if usda_quality_grade_data else None

                            usda_yield_grade_data = Reports(g.db).get_ready_by_query(count_distribution.create(matched_account_id, "USDA Yield Grade", 0))
                            matched_account["usda_yield_grade_data"] = usda_yield_grade_data["result"] if usda_yield_grade_data else None

                            accounts_object_for_sector[matched_account_id] = matched_account
                            sector_based_accounts[matched_account["account_sector_id"]] = accounts_object_for_sector
                            sector_based_account_data_for_connections[connected_account_name] = sector_based_accounts
                        else:
                            matched_account_data = accounts_object_for_sector[matched_account_id]
                            matched_account_data["count"] += matched_account["count"]

        ranch_matches_for_partner_account = Matches(g.db).get_matches_for_partner_accounts(
            partner_account_id=connected_account_id
        )
        ranches_data = {}
        for ranch_match in ranch_matches_for_partner_account:
            account_id = ranch_match["account_id"]
            if account_id not in ranches_data:
                ranches_data[account_id] = {}

        for account_id, account_data in ranches_data.items():
            # Sustainability data for matched account
            account_sustainability_responses_data = SustainabilityResponses(g.db).get_sustainability_responses(
                account_id=account_id,
                questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Completed"]
            )
            if len(account_sustainability_responses_data) > 0:
                account_sustainability_response_data = account_sustainability_responses_data[0]
                account_data["account_sustainability_data"] = account_sustainability_response_data
            else:
                account_data["account_sustainability_data"] = None

        for ranch_match in ranch_matches_for_partner_account:
            account_id = ranch_match["account_id"]
            ranch_match["account_sustainability_data"] = ranches_data[account_id]["account_sustainability_data"]
            if ranch_match["usda_quality_grade"] is not None:
                ranch_match["usda_quality_grade"] = ranch_match["usda_quality_grade"].replace('"', '')
        eid_based_account_data_for_connections[connected_account_name] = ranch_matches_for_partner_account

    return partner_render("sustainability/view-partner-accounts-sustainability.html", {
        "sector_based_account_data_for_connections": sector_based_account_data_for_connections,
        "eid_based_account_data_for_connections": eid_based_account_data_for_connections,
        "sectors_id_to_name": SECTORS_ID_TO_NAME
    })


@bp.route('/add-connection', methods=["GET", "POST"])
@crut.require_partner
def serve_add_connection():
    if request.method == "GET":
        invitable_partner_accounts = Connections(g.db).get_unconnected_accounts(g.account.id(), get_partners_only=True)
        return partner_render("connections/add-connections.html", {
            "invitable_partner_accounts": invitable_partner_accounts
        })
    if request.method == "POST":
        Connections(g.db).create_or_fail_connection(
            g.account.id(),
            request.json["invited_account_id"],
            CONNECTION_STATUS_NAME_TO_ID["Pending"],
            connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Created"]
        )
        return Response(status=HTTP_OK)


@bp.route('/create-patron', methods=["GET"])
@crut.require_partner
def serve_create_patron():
    return partner_render("create-patron.html")


@bp.route('/patrons', methods=["GET", "POST"])
@crut.require_partner
def serve_patrons():
    if request.method == "POST":
        try:
            fields = {key: value for key, value in request.form.items()}
            sector, phone, affiliate_id = Accounts(g.db).validate_new_account(
                g.account.sector_id(), g.account.id(), fields["affiliate_id"], fields["phone"]
            )
            account_obj = Accounts(g.db).create_account(
                    phone=phone,
                    company=fields['company'],
                    partner=g.account.id(),
                    affiliate_id=affiliate_id,
                    sector=sector,
                    address=fields['address'],
                    city=fields['city'],
                    state=fields['state'],
                    zip=fields['zip'],
                    created_by_user_id=g.user.id()
            )

            user_id = g.db.users.create_pseudo_user(account_obj.id(), False)
            g.db.account_users.insert_account_user(user_id, account_obj.id(), int(True))

            perform_new_account_actions(
                db=g.db, account_id=account_obj.id(), user_id=user_id,
                event_type_id=EVENT_TYPE_NAMES_TO_IDS["Account Created By Partner"],
                sector_id=account_obj.sector_id()
            )

            return {"redirect": url_for("partner_bp.serve_patrons")}
        except (ExportException, AccountsException, UsersException, ValueError) as e:
            raise ExportException(str(e))
    patrons = g.db.accounts.get_accounts(partner_account=g.account.id())
    for patron in patrons:
        if len(user := g.db.users.get_users(is_system_generated=int(True), account_users__account=patron["id"])) > 0:
            patron["user_id"] = user[0]["id"]
        elif len(
            user := g.db.users.get_users(account_users__is_admin=int(True), account_users__account=patron["id"])
        ) > 0:
            patron["user_id"] = user[0]["id"]
    return partner_render("patrons.html", {
        "patrons": patrons
    })


@bp.route('/patrons/<int:patron_id>/<int:user_id>', methods=["POST"])
@crut.require_partner
def serve_patron(patron_id, user_id):
    patron = g.db.accounts.get_accounts(id=patron_id)[0]
    if patron["can_partner_login"] and len(user := g.db.users.get_users(id=user_id, account_users__account=patron_id)) > 0:
        auth.login_as_user(
            account_id=patron["id"], user_id=user[0]["id"], is_admin=True, impersonated_by_user_id=g.user.id()
        )
        g.db.users.update_user(
            g.impersonated_by_user_id, impersonating_as_user_id=user[0]["id"]
        )
        Impersonations(g.db).insert(user_id=user[0]["id"], impersonated_by_user_id=g.impersonated_by_user_id)
        return redirect(url_for("dashboard_bp.serve_dashboard"))
    else:
        raise ExportException("Login not allowed or not available")


@bp.route('/log-back-in', methods=["GET"])
@crut.require_user
def log_back_in():
    if g.impersonated_by_user_id:
        user = g.db.users.get_users(id=g.impersonated_by_user_id)[0]
        if user["impersonating_as_user_id"] == g.user.id():
            g.db.users.update_user(id=user["id"], impersonating_as_user_id=None)
            account_user = g.db.account_users.get_account_users(user=user["id"])[0]
            auth.login_as_user(account_id=account_user["account"], user_id=user["id"], is_admin=int(False))
            return redirect(url_for("partner_bp.serve_patrons"))
        else:
            auth.logout()
            return redirect(url_for("outside_bp.serve_login"))
    else:
        auth.logout()
        return redirect(url_for("outside_bp.serve_login"))
