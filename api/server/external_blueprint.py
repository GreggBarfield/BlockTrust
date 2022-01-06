from flask import (
    request, Blueprint, g
)
from core.database.database import Database
from core.database.tables.accounts import AccountsException
from core.database.tables.api_data_requests import APIDataRequests
from core.database.tables.error_logs import ErrorLogs
from core.config import MYSQL_CONFIG
from core.common_exceptions import ExportException
from core.match_types import match_types_by_name
from json import loads
from datetime import datetime
from traceback import format_exc

bp = Blueprint('external_blueprint', __name__)


@bp.before_request
def before_request():
    """Per-request setup."""
    g.db = Database(MYSQL_CONFIG)


@bp.route("/fetch-animal-data", methods=["POST"])
def serve_get_animal_data():
    try:
        request_data = loads(request.data)
        eid = request_data["eid"]
        token = request_data["token"]
        account_id = request_data["account"]
        APIDataRequests(g.db).insert_api_data_request(account_id=account_id, api_route=request.path, request_data=request_data)

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
            birth_date = datetime.utcfromtimestamp(match_birth_date_row['time']).strftime('%Y-%m-%d %H:%M:%S')
        if match_visual_id_row is not None:
            visual_id = match_visual_id_row['visual_id']
        animal_data = {
            "eid": eid,
            "birthDate": birth_date,
            "visualID": visual_id
        }
        return animal_data
    except ExportException as e:
        raise e
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("External API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500
