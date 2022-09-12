from flask import (
    request, Blueprint, g
)
from core.database.database import Database
from core.database.tables.connections import Connections, ConnectionException, connection_status
from core.database.tables.api_data_requests import APIDataRequests
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.sustainability_responses import SustainabilityResponses
from core.database.tables.view_logs import ViewLogs, DATA_TYPE_NAME_TO_ID
from core.config import MYSQL_CONFIG
from core.common_exceptions import ExportException
from core.match_types import match_types_by_name
from core.renderers.email import render_email
from core.sectors import sectors_by_name
from core.utilities.email import send_email
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
        if "eid" not in request_data or "token" not in request_data:
            raise ExportException("Bad request")
        eid = request_data["eid"]
        token = request_data["token"]
        requesting_account_list = g.db.accounts.get_accounts(token=token)
        if len(requesting_account_list) == 0:
            APIDataRequests(g.db).insert_api_data_request(api_route=request.path, request_data=request_data)
            raise ExportException("Bad token. You are not authorized")
        else:
            requesting_account = requesting_account_list[0]
        APIDataRequests(g.db).insert_api_data_request(account_id=requesting_account["id"], api_route=request.path, request_data=request_data)

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
        sustainability = {}

        match_ranch_sightings = g.db.matches.get_matches_with_account_links(matches_eid=eid, matches_restrict_type=match_types_by_name["Sighting"],
            account_links_sector=sectors_by_name["Cow-Calf"], matches_order_by="created")
        unauthorized_message = "Access to this EID is not allowed at this time"
        if len(match_ranch_sightings) == 0:
            return {"error": unauthorized_message}, 401
        else:
            match = match_ranch_sightings[0]
            account_id = match["account"]

            # check if connection is established
            if Connections(g.db).get_connection_between(account_id, requesting_account["id"], connection_status["Connected"]) is None:
                # create a new pending connection
                try:
                    Connections(g.db).create_connection(
                        from_account_id=requesting_account["id"],
                        to_account_id=account_id,
                        status=connection_status["Pending"]
                    )
                except ConnectionException as e:
                    pass
                else:
                    # send an email to admin of match account
                    if len(match_account_admin_users := g.db.account_users.get_account_users(account=account_id, is_admin=1)) > 0:
                        if len(email_verified_admin_user := g.db.users.get_users(id=match_account_admin_users[0]["user"], is_email_verified=1)) > 0:
                            send_email(
                                "BlockTrust Network New Connection Request",
                                render_email("new_connection_request.html", {
                                    "connection_receiving_user": email_verified_admin_user[0],
                                    "requesting_account": requesting_account
                                }), email_verified_admin_user[0]["email"]
                            )
                finally:
                    return {"error": unauthorized_message}, 401

            match_birth_date_row = g.db.matches.get_matches(eid=eid, restrict_type=match_types_by_name["Born"])
            if len(match_birth_date_row) > 0:
                birth_date = datetime.utcfromtimestamp(match_birth_date_row[0]['time']).strftime('%Y-%m-%d %H:%M:%S')

            if match["data"] is not None:
                data = loads(match["data"])
                birth_weight = data.get("birth_weight", None)
                description = data.get("description", None)
                sex = data.get("sex", None)
            visual_id = match["visual_id"]
            if match["debug"] is not None:
                zip_code = loads(match["debug"]).get("zip", None)

            sustainability_responses = SustainabilityResponses(g.db).get_sustainability_responses(account_id=account_id)
            if len(sustainability_responses) > 0:
                latest_response = sustainability_responses[0]
                sustainability["airAndGHGemissions"] = latest_response.get("air_points", 0)
                sustainability["landResources"] = latest_response.get("land_points", 0)
                sustainability["waterResources"] = latest_response.get("water_points", 0)
                sustainability["employeeSafetyAndWellBeing"] = latest_response.get("safety_points", 0)
                sustainability["animalHealthAndWellBeing"] = latest_response.get("animal_points", 0)
                sustainability["efficiencyAndYield"] = latest_response.get("efficiency_points", 0)
                sustainability["improvement"] = latest_response.get("improvement_points", 0)
                sustainability["totalScore"] = latest_response["score"]

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
                if match['time'] is not None:
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
                "saleLocation": sale_location,
                "second31DayFeedMethod": second_31_day_feed_method,
                "sex": sex,
                "visualID": visual_id,
                "weanDate": wean_date,
                "weanWeight": wean_weight,
                "weaningStrategy": weaning_strategy,
                "usdaYieldGrade": yield_grade,
                "zipCode": zip_code,
                "sustainabilityScores": sustainability if sustainability != {} else None
            }

            ViewLogs(g.db).insert_view_logs(owner_account_id=account_id, viewer_account_id=requesting_account["id"],
                                            viewer_account_display_name=requesting_account["name"], data_type_id=DATA_TYPE_NAME_TO_ID["EID"],
                                            eid=eid)

            if len(sustainability_responses) > 0:
                ViewLogs(g.db).insert_view_logs(owner_account_id=account_id, viewer_account_id=requesting_account["id"],
                                                viewer_account_display_name=requesting_account["name"],
                                                data_type_id=DATA_TYPE_NAME_TO_ID["Sustainability Score"],
                                                sustainability_response_id=latest_response["id"])

            return animal_data
    except ExportException as e:
        raise e
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("External API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500
