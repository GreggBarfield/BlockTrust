from flask import (
    request, Blueprint, g
)
from core.database.database import Database
from core.database.tables.accounts import AccountsException
from core.config import MYSQL_CONFIG
from core.common_exceptions import ExportException
from core.match_types import match_types_by_name


bp = Blueprint('fetch_blueprint', __name__)


@bp.before_request
def before_request():
    """Per-request setup."""
    g.db = Database(MYSQL_CONFIG)


@bp.route("/fetch_animal_data", methods=["GET"])
def serve_fetch_animal_data():
    request_data = request.get_json()
    eid = request_data["eid"]
    token = request_data["token"]
    account = request_data["account"]
    assert isinstance(token, str)
    try:
        account_row = g.db.accounts.get_by_id(account)
        if account_row.token() != token:
            raise ExportException("Bad token")
    except AccountsException:
        raise ExportException("Bad account ID")
    match_birth_date_row = g.db.matches.get_by_eids(eids=eid, restrict_types=match_types_by_name["Born"])
    match_visual_id_row = g.db.matches.get_by_eids(eids=eid, restrict_types=match_types_by_name["Visual ID"])
    match_birth_date = ""
    match_visual_id = ""
    if len(match_birth_date_row) > 0:
        match_birth_date = match_birth_date_row[0]['data']
    if len(match_visual_id_row) > 0:
        match_visual_id = match_visual_id_row[0]['data']
    animal_data = {
        "animal_eid": eid,
        "animal_birth_date": match_birth_date,
        "animal_visual_id": match_visual_id
    }
    return animal_data
