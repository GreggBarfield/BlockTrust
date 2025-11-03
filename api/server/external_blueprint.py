from datetime import datetime
from flask import (
    request, Blueprint, g, jsonify
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import json
from traceback import format_exc
from core.database.combinations import send_connection_request_email_to_admin_users
from core.database.database import Database
from core.database.no_value import NoValue
from core.database.tables.accounts import Accounts, NATIONAL_BEEF_COMPANY
from core.database.tables.account_users import AccountUsers
from core.database.tables.animals import Animals
from core.database.tables.api_data_requests import APIDataRequests
from core.database.tables.api_inserts import ApiInserts, API_INSERTS_PAGINATION_LIMIT
from core.database.tables.connections import Connections, CONNECTION_STATUS_NAME_TO_ID, CONNECTION_TYPE_NAME_TO_ID
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.event_logs import EventLogs, EVENT_TYPE_NAMES_TO_IDS
from core.database.tables.matches import Matches
from core.database.tables.sales_groups import SalesGroups
from core.database.tables.sustainability_responses import SustainabilityResponses
from core.database.tables.users import Users
from core.database.tables.view_logs import ViewLogs, DATA_TYPE_NAME_TO_ID
from core.config import MYSQL_CONFIG
from core.common_exceptions import ExportException
from core.match_types import MATCH_TYPES_NAME_TO_ID
from core.sectors import SECTORS_NAME_TO_ID
from core.utilities.constants import HTTP_UNAUTHORISED
from core.utilities.general_utilities import str_to_bool
from core.utilities import auth
from mysql.connector import IntegrityError

bp = Blueprint('external_blueprint', __name__, url_prefix='/api')

NO_VALUE = NoValue()


@bp.before_request
def before_request():
    """Per-request setup."""
    g.db = Database(MYSQL_CONFIG)


@bp.route("/fetch-animal-data", methods=["POST"])
def serve_get_animal_data():
    try:
        try:
            request_data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return {"error": "Decoding request JSON has failed"}, 400
        if "eid" not in request_data or "token" not in request_data:
            raise ExportException("Bad request")
        eid = request_data["eid"]
        token = request_data["token"]
        dry_run = str_to_bool(request_data.get("dry_run", False))

        requesting_account_list = g.db.accounts.get_accounts(token=token)
        if len(requesting_account_list) == 0:
            if not dry_run:
                APIDataRequests(g.db).insert_api_data_request(api_route=request.path, request_data=request_data)
            raise ExportException("Bad token. You are not authorized")
        else:
            authenticated_account = requesting_account_list[0]
        if not dry_run:
            APIDataRequests(g.db).insert_api_data_request(account_id=authenticated_account["id"], api_route=request.path, request_data=request_data)

        birth_date = None
        visual_id = None
        hot_weight = None
        yield_grade = None
        quality_grade = None
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

        owner_account_sightings = Matches(g.db).get_matches_with_account_links(matches_eid=eid, matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
                                                                              account_links_sector=SECTORS_NAME_TO_ID["Cow-Calf"], matches_order_by="created")
        unauthorized_message = "Access to this EID is not allowed at this time"
        if len(owner_account_sightings) == 0:
            return {"error": unauthorized_message}, 401
        else:
            owner_account_link_and_match = owner_account_sightings[0]
            owner_account_id = owner_account_link_and_match["account"]

            existing_connection = Connections(g.db).get_connection_between(owner_account_id, authenticated_account["id"])
            if existing_connection is None:
                # create a new pending connection
                if not dry_run:
                    Connections(g.db).create_or_fail_connection(
                            from_account_id=authenticated_account["id"],
                            to_account_id=owner_account_id,
                            status=CONNECTION_STATUS_NAME_TO_ID["Pending"],
                            connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Created"],
                            details={"eid": eid, "created_by_operation": serve_get_animal_data.__name__}
                    )
                    send_connection_request_email_to_admin_users(g.db, owner_account_id, authenticated_account["id"])
                else:
                    return {"dry_run": f"Connection doesn't exist between {authenticated_account['name']} and {owner_account_link_and_match['name']}"}
                return {"error": unauthorized_message}, 401
            elif existing_connection["connection_status_id"] != CONNECTION_STATUS_NAME_TO_ID["Connected"]:
                return {"error": unauthorized_message}, 401

            match_birth_date_row = Matches(g.db).get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["Born"])
            if len(match_birth_date_row) > 0:
                birth_date = datetime.utcfromtimestamp(match_birth_date_row[0]['time']).strftime('%Y-%m-%d %H:%M:%S')

            visual_id = owner_account_link_and_match["visual_id"]
            if owner_account_link_and_match["debug"] is not None:
                zip_code = json.loads(owner_account_link_and_match["debug"]).get("zip", None)

            if len(animal := Animals(g.db).get_animals(eid=eid)) > 0:
                animal = animal[0]
                animal_table_data = {
                    ''.join((k if i == 0 else k.capitalize()) for i, k in enumerate(key.split('_'))): value
                    for key, value in animal.items() if ("id" not in key and "timestamp" not in key)
                }
            else:
                animal = Animals(g.db).get_animals()[0]
                animal_table_data = {
                    ''.join((k if i == 0 else k.capitalize()) for i, k in enumerate(key.split('_'))): None
                    for key in animal if ("id" not in key and "timestamp" not in key)
                }

            sustainability_responses = SustainabilityResponses(g.db).get_sustainability_responses(account_id=owner_account_id)
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

            match_wean_row = Matches(g.db).get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["Weaned"])
            if len(match_wean_row) > 0:
                owner_account_link_and_match = match_wean_row[0]
                wean_date = datetime.utcfromtimestamp(owner_account_link_and_match['time']).strftime('%Y-%m-%d %H:%M:%S')
                if owner_account_link_and_match["data"] is not None:
                    data = owner_account_link_and_match["data"]
                    creep_feed = data.get("creep_feed", None)
                    first_14_day_feed_method = data.get("first_14_method", None)
                    second_31_day_feed_method = data.get("second_31_method", None)
                    weaning_strategy = data.get("at", None)
                    wean_weight = data.get("wean_weight", None)

            match_sold_row = Matches(g.db).get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["Sold"])
            if len(match_sold_row) > 0:
                owner_account_link_and_match = match_sold_row[0]
                if owner_account_link_and_match['time'] is not None:
                    marketing_date = datetime.utcfromtimestamp(owner_account_link_and_match['time']).strftime('%Y-%m-%d %H:%M:%S')
                if owner_account_link_and_match["data"] is not None:
                    data = owner_account_link_and_match["data"]
                    marketing_method_name = data.get("method", None)
                    sale_location = data.get("location", None)
                    number_of_calves = data.get("group_size", None)

            match_weight_row = Matches(g.db).get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["Hot Weight"])
            if len(match_weight_row) > 0:
                hot_weight = match_weight_row[0]['data']

            match_quality_row = Matches(g.db).get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"])
            if len(match_quality_row) > 0:
                quality_grade = match_quality_row[0]['data'].strip('"')

            match_yield_row = Matches(g.db).get_matches(eid=eid, restrict_type=MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"])
            if len(match_yield_row) > 0:
                yield_grade = match_yield_row[0]['data']

            result = {
                "birthDate": birth_date,
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
                "visualID": visual_id,
                "weanDate": wean_date,
                "weanWeight": wean_weight,
                "weaningStrategy": weaning_strategy,
                "usdaYieldGrade": yield_grade,
                "zipCode": zip_code,
                "sustainabilityScores": sustainability if sustainability != {} else None
            }
            result.update(animal_table_data)

            if not dry_run:
                ViewLogs(g.db).insert_view_logs(owner_account_id=owner_account_id, viewer_account_id=authenticated_account["id"],
                                                data_type_id=DATA_TYPE_NAME_TO_ID["EID"], eid=eid)

                if len(sustainability_responses) > 0:
                    ViewLogs(g.db).insert_view_logs(owner_account_id=owner_account_id, viewer_account_id=authenticated_account["id"],
                                                    data_type_id=DATA_TYPE_NAME_TO_ID["Sustainability Score"],
                                                    sustainability_response_id=latest_response["id"])

                return result
            else:
                return {"dry_run": "Data fetched successfully"}
    except ExportException as e:
        raise e
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("External API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route("/fetch-all-sales-groups-data", methods=["GET"])
@jwt_required()
def serve_fetch_all_sales_groups_data():
    try:
        APIDataRequests(g.db).insert_api_data_request(api_route=request.path, user_id=get_jwt().get("user_id"), account_id=get_jwt().get("account_id"), employee_id=get_jwt().get("employee_id"))
        sales_groups_data = SalesGroups(g.db).get_sales_groups(is_archived=0, published=int(True))
        for sales_group in sales_groups_data:
            account = g.db.accounts.get_accounts(id=sales_group["account"])[0]
            sales_group["owner"] = account["company"]
            del sales_group["account"]
        sales_groups_data = list(map(lambda x: {k: v for k, v in x.items() if k != "account"}, sales_groups_data))
        return sales_groups_data
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Sales Group Retrieval", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"message": "Internal Server Error"}, 500


@bp.route("/sales-groups/<int:number>", methods=["GET"])
@jwt_required()
def sales_groups(number):
    try:
        APIDataRequests(g.db).insert_api_data_request(api_route=request.path, user_id=get_jwt().get("user_id"), account_id=get_jwt().get("account_id"), employee_id=get_jwt().get("employee_id"))
        sales_group = {}
        if len(sales_groups := SalesGroups(g.db).get_sales_groups(
            id=number, is_archived=int(False), published=int(True)
        )) > 0:
            sales_group = sales_groups[0]
            account = g.db.accounts.get_accounts(id=sales_group["account"])[0]
            sales_group["owner"] = account["company"]
            del sales_group["account"]
        return sales_group
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Sales Group Retrieval", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"message": "Internal Server Error"}, 500


@bp.route("/sales-groups/auction-market/<int:auction_market_id>", methods=["GET"])
@jwt_required()
def sales_groups_by_auction_market(auction_market_id):
    try:
        APIDataRequests(g.db).insert_api_data_request(api_route=request.path, user_id=get_jwt().get("user_id"), account_id=get_jwt().get("account_id"), employee_id=get_jwt().get("employee_id"))
        sales_groups = SalesGroups(g.db).get_sales_groups(
            auction_market_id=auction_market_id, delivery_location_type="Auction", is_archived=int(False), published=int(True)
        )
        for sales_group in sales_groups:
            account = g.db.accounts.get_accounts(id=sales_group["account"])[0]
            sales_group["owner"] = account["company"]
            del sales_group["account"]
        return sales_groups
    except IntegrityError as ie:
        return {"message": "Invalid Token"}, HTTP_UNAUTHORISED
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Sales Group Retrieval", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"message": "Internal Server Error"}, 500


@bp.route("/employee/login", methods=["POST"])
def serve_employee_login():
    try:
        id=auth.employee_login(identifier=request.json["username"], password=request.json["password"], load=False)
        APIDataRequests(g.db).insert_api_data_request(api_route=request.path, employee_id=id)
    except auth.LoginException as e:
        return {"message":str(e)}, HTTP_UNAUTHORISED
    except Exception as e:
        raise ExportException(str(e))
    return {"access_token": create_access_token(identity=id, additional_claims={'employee_id': id})}


@bp.route("/login", methods=["POST"])
def serve_login():
    try:
        id=auth.login(identifier=request.json["username"], password=request.json["password"])
        user = Users(g.db).get_users_and_accounts(user_id=id)[0]
        if not user["has_api_access"]:
            raise auth.LoginException(f"You do not have permission to perform this action. Please contact your account: {user['company']}'s administrator")
        EventLogs(g.db).insert(
            event_type_id=EVENT_TYPE_NAMES_TO_IDS["User Login"],
            account_id=user["account_id"],
            user_id=id
        )
        APIDataRequests(g.db).insert_api_data_request(api_route=request.path, user_id=id, account_id=user["account_id"])
    except auth.LoginException as e:
        return {"message":str(e)}, HTTP_UNAUTHORISED
    except Exception as e:
        raise ExportException(str(e))
    return {"access_token": create_access_token(identity=id, additional_claims={'user_id': id, 'account_id':user["account_id"]})}


@bp.route("/fetch-accounts-data", methods=['POST'])
def serve_fetch_account_data():
    try:
        try:
            request_data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return {"error": "Decoding request JSON has failed"}, 400
        sector = request_data.get('sector', NO_VALUE)
        is_partner = request_data.get('is_partner', NO_VALUE)
        partner_account = request_data.get('partner_account', NO_VALUE)
        affiliate_id = request_data.get('affiliate_id', NO_VALUE)
        auction_market_id = request_data.get('auction_market_id', NO_VALUE)
        generated_paid = request_data.get('generated_paid', NO_VALUE)
        accounts_data = Accounts(g.db).get_accounts(
            sector=sector,
            is_partner=is_partner,
            partner_account=partner_account,
            affiliate_id=affiliate_id,
            auction_market_id=auction_market_id,
            generated_paid=generated_paid
        )
        return accounts_data
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Accounts Data Retrieval", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route("/national-beef/get-latest-logins", methods=["GET"])
@jwt_required()
def serve_get_latest_national_beef_logins():
    try:
        national_beef_partner = Accounts(g.db).get_partners(company=NATIONAL_BEEF_COMPANY)[0]
        national_beef_partner_accounts = Accounts(g.db).get_accounts(partner_account=national_beef_partner["id"])
        latest_login_data = []
        for account in national_beef_partner_accounts:
            account_latest_login_timestamp = None
            account_user = AccountUsers(g.db).get_account_users(account=account["id"])

            account_login_events = EventLogs(g.db).get(
                account_id=account["id"],
                event_type_id=EVENT_TYPE_NAMES_TO_IDS["User Login"],
                event_logs_order_by="created_timestamp",
                event_logs_sort_by="DESC"
            )
            if len(account_login_events) > 0:
                account_latest_login = account_login_events[0]
                account_latest_login_timestamp = account_latest_login["created_timestamp"]
            if len(account_user) > 0:
                user = Users(g.db).get_user_by_id(account_user[0]["user"])
                if user.email() is not None:
                    account_login_data = {
                        "email": user.email(),
                        "created_timestamp": account["created_timestamp"],
                        "latest_login_timestamp": account_latest_login_timestamp
                    }
                    latest_login_data.append(account_login_data)

        return jsonify({"latest_login_data": latest_login_data})
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Fetch Latest Login Data", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route("/fetch-packer-carcass-data", methods=["GET"])
@jwt_required()
def serve_fetch_packer_carcass_data():
    try:
        try:
            request_data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return {"error": "Decoding request JSON has failed"}, 400

        packer_account_id = request_data.get("account_id", None)
        if packer_account_id is None:
            return {"error": "Please provide a Packer Account ID (account_id)."}
        packer_account_data = Accounts(g.db).get_account_by_id(packer_account_id)
        if packer_account_data.sector_id() != SECTORS_NAME_TO_ID["Packer"]:
            return {"error": "Provided account is not a Packer."}

        start_timestamp = request_data.get("start_timestamp", None)
        if start_timestamp is None:
            return {"error": "Please provide a starting timestamp to fetch records from (start_timestamp)."}


        start_timestamp_format = "%m/%d/%Y T:%H:%M:%S"
        start_timestamp_object = datetime.strptime(start_timestamp, start_timestamp_format)
        start_timestamp_string = start_timestamp_object.strftime('%Y-%m-%d %H:%M:%S')

        packer_api_inserts = ApiInserts(g.db).get_api_inserts(
            account=packer_account_id,
            created_start_time=start_timestamp_string
        )

        packer_api_insert_ids = [packer_api_insert["id"] for packer_api_insert in packer_api_inserts]

        packer_animals = Animals(g.db).get_animals_by_packer_insert_ids(
            packer_insert_ids=packer_api_insert_ids
        )
        for packer_animal in packer_animals:
            eid_matches = Matches(g.db).get_animal_by_eid(packer_animal["eid"])
            for eid_match in eid_matches.matches:
                if eid_match["type"] == MATCH_TYPES_NAME_TO_ID["Hot Weight"]:
                    packer_animal["hot_weight"] = eid_match["data"]
                elif eid_match["type"] == MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"]:
                    packer_animal["quality_grade"] = eid_match["data"]
                elif eid_match["type"] == MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"]:
                    packer_animal["yield_grade"] = eid_match["data"]
                elif eid_match["type"] == MATCH_TYPES_NAME_TO_ID["Died"]:
                    packer_animal["kill_date"] = eid_match["data"]
        return {"packer_carcass_data": packer_animals}, 200
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Packer Carcass Data Retrieval", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route("/fetch-packer-carcass-data-total-pages", methods=["GET"])
@jwt_required()
def serve_fetch_packer_carcass_data_total_pages():
    try:
        try:
            request_data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return {"error": "Decoding request JSON has failed"}, 400

        packer_account_id = request_data.get("account_id", None)
        if packer_account_id is None:
            return {"error": "Please provide a Packer Account ID (account_id)."}
        packer_account_data = Accounts(g.db).get_account_by_id(packer_account_id)
        if packer_account_data.sector_id() != SECTORS_NAME_TO_ID["Packer"]:
            return {"error": "Provided account is not a Packer."}

        start_timestamp = request_data.get("start_timestamp", None)
        if start_timestamp is None:
            return {"error": "Please provide a starting timestamp to fetch records from (start_timestamp)."}

        start_timestamp_format = "%m/%d/%Y T:%H:%M:%S"
        start_timestamp_object = datetime.strptime(start_timestamp, start_timestamp_format)
        start_timestamp_string = start_timestamp_object.strftime('%Y-%m-%d %H:%M:%S')
        
        end_timestamp = request_data.get("end_timestamp", None)
        if end_timestamp is None:
            return {"error": "Please provide an ending timestamp to fetch records to (end_timestamp)."}

        end_timestamp_format = "%m/%d/%Y T:%H:%M:%S"
        end_timestamp_object = datetime.strptime(end_timestamp, end_timestamp_format)
        end_timestamp_string = end_timestamp_object.strftime('%Y-%m-%d %H:%M:%S')

        total_pages = ApiInserts(g.db).get_api_inserts_total_pages(
            account=packer_account_id,
            created_start_time=start_timestamp_string,
            created_end_time=end_timestamp_string
        )
        return {"total_pages": total_pages}, 200

    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Packer Carcass Data Page Number Retrieval", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route("/fetch-paginated-packer-carcass-data", methods=["GET"])
@jwt_required()
def serve_fetch_paginated_packer_carcass_data():
    try:
        try:
            request_data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return {"error": "Decoding request JSON has failed"}, 400

        packer_account_id = request_data.get("account_id", None)
        if packer_account_id is None:
            return {"error": "Please provide a Packer Account ID (account_id)."}
        packer_account_data = Accounts(g.db).get_account_by_id(packer_account_id)
        if packer_account_data.sector_id() != SECTORS_NAME_TO_ID["Packer"]:
            return {"error": "Provided account is not a Packer."}

        start_timestamp = request_data.get("start_timestamp", None)
        if start_timestamp is None:
            return {"error": "Please provide a starting timestamp to fetch records from (start_timestamp)."}

        start_timestamp_format = "%m/%d/%Y T:%H:%M:%S"
        start_timestamp_object = datetime.strptime(start_timestamp, start_timestamp_format)
        start_timestamp_string = start_timestamp_object.strftime('%Y-%m-%d %H:%M:%S')
        
        end_timestamp = request_data.get("end_timestamp", None)
        if end_timestamp is None:
            return {"error": "Please provide an ending timestamp to fetch records to (end_timestamp)."}

        end_timestamp_format = "%m/%d/%Y T:%H:%M:%S"
        end_timestamp_object = datetime.strptime(end_timestamp, end_timestamp_format)
        end_timestamp_string = end_timestamp_object.strftime('%Y-%m-%d %H:%M:%S')

        page_number = request_data.get("page_number", None)
        if page_number is None:
            return {"error": "Please provide a page number for the records(page_number)."}
        
        OFFSET = (page_number - 1) * API_INSERTS_PAGINATION_LIMIT

        packer_api_inserts = ApiInserts(g.db).get_api_inserts_with_offset_and_limit(
            account=packer_account_id,
            created_start_time=start_timestamp_string,
            created_end_time=end_timestamp_string,
            offset=OFFSET
        )

        packer_api_insert_ids = [packer_api_insert["id"] for packer_api_insert in packer_api_inserts]

        packer_animals = Animals(g.db).get_animals_by_packer_insert_ids(
            packer_insert_ids=packer_api_insert_ids
        )
        for packer_animal in packer_animals:
            eid_matches = Matches(g.db).get_animal_by_eid(packer_animal["eid"])
            for eid_match in eid_matches.matches:
                if eid_match["type"] == MATCH_TYPES_NAME_TO_ID["Hot Weight"]:
                    packer_animal["hot_weight"] = eid_match["data"]
                elif eid_match["type"] == MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"]:
                    packer_animal["quality_grade"] = eid_match["data"]
                elif eid_match["type"] == MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"]:
                    packer_animal["yield_grade"] = eid_match["data"]
                elif eid_match["type"] == MATCH_TYPES_NAME_TO_ID["Died"]:
                    packer_animal["kill_date"] = eid_match["data"]
        return {"packer_carcass_data": packer_animals}, 200
    except Exception as e:
        print("API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Paginated Packer Carcass Data Retrieval", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500