from flask import (
    request, Blueprint, g
)
from core.database.database import Database
from core.database.tables.accounts import AccountsException
from core.config import MYSQL_CONFIG
from core.common_exceptions import ExportException
from core.match_types import match_types_by_name

import datetime

bp = Blueprint('external_blueprint', __name__)


@bp.before_request
def before_request():
    """Per-request setup."""
    g.db = Database(MYSQL_CONFIG)


@bp.route("/fetch-animal-data", methods=["POST"])
def serve_fetch_animal_data():
    request_data = request.get_json()
    eid = request_data["eid"]
    token = request_data["token"]
    account_id = request_data["account"]
    assert isinstance(token, str)
    try:
        account = g.db.accounts.get_by_id(account_id)
        if account.token() != token:
            raise ExportException("Bad token")
    except AccountsException:
        raise ExportException("Bad account ID")
    match_birth_date_row = g.db.matches.get_match(eid=eid, type_int=match_types_by_name["Born"])
    match_visual_id_row = g.db.matches.get_match(eid=eid, visual_id_has_value=True)
    birth_date = None
    visual_id = None
    if match_birth_date_row is not None:
        birth_date = datetime.datetime.fromtimestamp(match_birth_date_row['time'])
    if match_visual_id_row is not None:
        visual_id = match_visual_id_row['visual_id']
    animal_data = {
        "animal_eid": eid,
        "animal_birth_date": birth_date,
        "animal_visual_id": visual_id
    }
    return animal_data
