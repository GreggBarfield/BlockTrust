from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)
from core.database.database import Database
from core.database.tables.accounts import Accounts
from core.config import MYSQL_CONFIG
from core.common_exceptions import ExportException

import json
import gzip

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
    # account_row = Accounts(g.db).get_accounts(token=token)
    # if len(account_row) == 0:
    #     raise ExportException("Bad Account token")
    match_birth_date_row = g.db.matches.get_by_eids(eids=eid, restrict_types=4)
    match_visual_id_row = g.db.matches.get_by_eids(eids=eid, restrict_types=10)
    print(match_birth_date_row[0]['data'])
    print(match_visual_id_row[0]['data'])
    return {}
