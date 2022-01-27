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
from core.sectors import sectors_by_name
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
        account = g.db.accounts.get_accounts(token=token)
        if len(account) == 0:
            APIDataRequests(g.db).insert_api_data_request(api_route=request.path, request_data=request_data)
            raise ExportException("Bad token. You are not authorized.")
        APIDataRequests(g.db).insert_api_data_request(account_id=account[0]["id"], api_route=request.path, request_data=request_data)
        birth_date = None
        visual_id = None
        birth_weight = None
        description = None
        hot_weight = None
        yield_grade = None
        quality_grade = None
        sex = None
        creep_feed = None
        first_14_day_feed_method = None
        marketing_date = None
        marketing_method_name = None
        number_of_calves = None
        sale_location = None
        second_31_day_feed_method = None
        wean_date = None
        weaning_strategy = None
        wean_weight = None
        zip_code = None

        match_birth_date_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Born"])
        if len(match_birth_date_row) > 0:
            birth_date = datetime.utcfromtimestamp(match_birth_date_row[0]['time']).strftime('%Y-%m-%d %H:%M:%S')

        match_ranch_sightings = g.db.matches.get_matches_with_account_links(matches_eid=eid, matches_restrict_type=match_types_by_name["Sighting"],
            account_links_sector=sectors_by_name["Cow-Calf"], matches_order_by="created")
        if len(match_ranch_sightings) > 0:
            match = match_ranch_sightings[0]
            if match["data"] is not None:
                data = loads(match["data"])
                birth_weight = data.get("birth_weight", None)
                description = data.get("description", None)
                sex = data.get("sex", None)
            visual_id = match["visual_id"]
            if match["debug"] is not None:
                zip_code = loads(match["debug"]).get("zip", None)

        match_wean_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Weaned"])
        if len(match_wean_row) > 0:
            match = match_wean_row[0]
            wean_date = datetime.utcfromtimestamp(match['time']).strftime('%Y-%m-%d %H:%M:%S')
            if match["data"] is not None:
                data = loads(match["data"])
                creep_feed = data.get("creep_feed", None)
                first_14_day_feed_method = data.get("first_14_method", None)
                second_31_day_feed_method = data.get("second_31_method", None)
                weaning_strategy = data.get("at", None)
                wean_weight = data.get("wean_weight", None)

        match_sold_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Sold"])
        if len(match_sold_row) > 0:        
            match = match_sold_row[0]
            marketing_date = datetime.utcfromtimestamp(match['time']).strftime('%Y-%m-%d %H:%M:%S')
            if match["data"] is not None:
                data = loads(match["data"])
                marketing_method_name = data.get("method", None)
                sale_location = data.get("location", None)
                number_of_calves = data.get("group_size", None)

        match_weight_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Hot Weight"])
        if len(match_weight_row) > 0:
            hot_weight = match_weight_row[0]['data']

        match_quality_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["USDA Quality Grade"])
        if len(match_quality_row) > 0:
            quality_grade = match_quality_row[0]['data']

        match_yield_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["USDA Yield Grade"])
        if len(match_yield_row) > 0:
            yield_grade = match_yield_row[0]['data']

        animal_data = {
            "birthDate": birth_date,
            "birthWeight": birth_weight,
            "calfDescription": description,
            "creepFeed": creep_feed,
            "electronicID": eid,
            "first14DayFeedMethod": first_14_day_feed_method,
            "hotWeight": hot_weight,
            "usdaQualityGrade": quality_grade,
            "marketingDate": marketing_date,
            "marketingMethodName": marketing_method_name,
            "numberOfCalves": number_of_calves,
            "sale_location": sale_location,
            "second31DayFeedMethod": second_31_day_feed_method,
            "sex": sex,
            "visualID": visual_id,
            "weanDate": wean_date,
            "weanWeight": wean_weight,
            "weaningStrategy": weaning_strategy,
            "usdaYieldGrade": yield_grade,
            "zipCode": zip_code
        }
        return animal_data
    except ExportException as e:
        raise e
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("External API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500
