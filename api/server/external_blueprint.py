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

import json

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
        account = g.db.accounts.get_account_by_id(account_id)
        # Authenticating request
        if account is None:
            raise ExportException("Bad account ID")
        if account.token() != token:
            raise ExportException("Bad token")
        # Fetching required rows from matches table
        match_birth_date_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Born"])
        match_visual_id_row = g.db.matches.get_matches(eid=eid, visual_id_has_value=True)
        match_weaned_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Weaned"])
        match_sold_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Sold"])
        match_hot_weight_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Hot Weight"])
        match_sighting_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Sighting"])
        # Initializing data which needs to be returned from the API
        birth_date = None
        visual_id = None
        application_id = None
        wean_data = None
        wean_date = None
        wean_strategy = None
        creep_feed = None
        first_14_method = None
        marketing_date = None
        marketing_method = None
        number_of_calves = None
        sale_data = None
        sale_location = None
        hot_weight = None
        zip_code = None
        # Preparing data to be returned
        if len(match_birth_date_row) > 0:
            birth_date = datetime.utcfromtimestamp(match_birth_date_row[0]['time']).strftime('%Y-%m-%d %H:%M:%S')
        if len(match_visual_id_row) > 0:
            visual_id = match_visual_id_row[0]['visual_id']
        if len(match_weaned_row) > 0:
            if match_weaned_row[0]['data'] is not None:
                wean_data = json.loads(match_weaned_row[0]['data'])
                if "creep_feed" in wean_data and wean_data["creep_feed"] is not None:
                    creep_feed = wean_data["creep_feed"]
                if "first_14_method" in wean_data and wean_data["first_14_method"] is not None:
                    first_14_method = wean_data["first_14_method"]
                if "at" in wean_data and wean_data["at"] is not None:
                    wean_strategy = wean_data["at"]
            if match_weaned_row[0]['time'] is not None:
                wean_date = datetime.utcfromtimestamp(match_weaned_row[0]['time']).strftime('%Y-%m-%d %H:%M:%S')
        if len(match_sold_row) > 0:
            if match_sold_row[0]['data'] is not None:
                sale_data = json.loads(match_sold_row[0]['data'])
                if "location" in sale_data and sale_data["location"] is not None:
                    sale_location = sale_data["location"]
                if "method" in sale_data and sale_data["method"] is not None:
                    marketing_method = sale_data["method"]
                if "group_size" in sale_data and sale_data["group_size"] is not None:
                    number_of_calves = sale_data["group_size"]
            if match_sold_row[0]['time'] is not None:
                marketing_date = datetime.utcfromtimestamp(match_sold_row[0]['time']).strftime('%Y-%m-%d %H:%M:%S')
            if match_sold_row[0]['grouping_id'] is not None:
                application_id = match_sold_row[0]['grouping_id']
        if len(match_hot_weight_row) > 0:
            if match_hot_weight_row[0]['data'] is not None:
                hot_weight = match_hot_weight_row[0]['data']
        if len(match_sighting_row) > 0:
            if match_sighting_row[0]['debug'] is not None:
                debug_data = json.loads(match_sighting_row[0]['data'])
                if "zip" in debug_data and debug_data["zip"] is not None:
                    zip_code = debug_data["zip"]
        animal_data = {
            "eid": eid,
            "birthDate": birth_date,
            "visualID": visual_id,
            "application_id": application_id,
            "creep_feed": creep_feed,
            "first_14_method": first_14_method,
            "marketing_date": marketing_date,
            "marketing_method": marketing_method,
            "number_of_calves": number_of_calves,
            "sale_location": sale_location,
            "wean_date": wean_date,
            "wean_strategy": wean_strategy,
            "hot_weight": hot_weight,
            "zip_code": zip_code
        }
        return animal_data
    except ExportException as e:
        raise e
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("External API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500
