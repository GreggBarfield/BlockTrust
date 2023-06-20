from flask import (
    Response, Blueprint, g, request, url_for
)
from core.common_exceptions import ExportException
from core.config import FLATFILE_LICENSE
from core.database.tables.accounts import HEALTH_TRACK_PARTNER_COMPANY
from core.database.tables.api_inserts import ApiInserts
from core.database.tables.event_logs import EventLogs, EVENT_TYPE_NAMES_TO_IDS
from core.sectors import SECTORS_NAME_TO_ID
from core.utilities.constants import HTTP_OK
from ..renderers.partner import partner_render
from ..utilities import crut, csrf
from json import loads

bp = Blueprint('partner_bp', __name__, url_prefix="/partner")


@bp.route('/dashboard', methods=['GET'])
@crut.require_partner
def serve_dashboard():
    return partner_render("homepage.html", {
        "SECTORS_NAME_TO_ID": SECTORS_NAME_TO_ID,
        "animal_URL": url_for("partner_bp.serve_animal_eid"),
        "view_scores_URL": url_for("partner_bp.serve_view_account_sustainability_data")
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
    animal = g.db.matches.get_animal_by_eid(animal_eid)
    if show_animal := bool(len(animal.matches)):
        display_certificate = False
        owner_account_match = sorted(
            list(filter(lambda row: row["sector"] == SECTORS_NAME_TO_ID["Cow-Calf"], animal.matches)),
            key=lambda row: row["id"]
        )

        if owner_account_match:
            if owner_account_match[0]["partner_account"] != g.account.id():
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
    eligible_packers = g.db.accounts.get_accounts(company_like="National Beef")
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
