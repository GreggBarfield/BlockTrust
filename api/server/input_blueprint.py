
import gzip
from http import HTTPStatus
import json
import requests


from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, Response
)
from flask_jwt_extended import jwt_required, get_jwt_identity

from core.database.combinations import convert_auction_market_to_account
from core.database.tables.error_logs import ErrorLogs 
from ..database.inserts_model import InsertsModel
from core.database.tables.accounts import AccountsException
from core.database.database import Database
from core.database.tables.account_users import AccountUsers
from core.database.tables.accounts import Accounts
from core.database.tables.api_data_requests import APIDataRequests
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.files import Files, SALES_GROUP_FILES_S3_PATH
from core.database.tables.sales_groups import SalesGroups
from core.database.tables.users import Users, UsersException
from core.config import MYSQL_CONFIG, API_MYSQL_CONFIG, DEV_MYSQL_CONFIG, TEMPORARY_SALES_GROUP_API_TOKEN, TEMPORARY_CREATE_ACCOUNT_API_TOKEN
from core.common_exceptions import ExportException
from core.utilities import auth
from core.utilities.field_lists import SALES_GROUP_REPORTED_FIELDS

from datetime import datetime
from traceback import format_exc
from zoneinfo import ZoneInfo


bp = Blueprint('input_blueprint', __name__)


@bp.before_request
def before_request():
    """Per-request setup."""
    g.db = Database(MYSQL_CONFIG)
    g.dev_db = Database(DEV_MYSQL_CONFIG)


@bp.route('/', methods=["GET", "POST"])
def serve_index():
    raise ExportException("Good endpoint, bad path")


@bp.route('/api', methods=["POST"])
def serve_api():
    try:
        # Decode the data

        data = None
        if request.headers.get('content-encoding', None) is not None:
            print("decompressing")
            gzip_data = gzip.decompress(request.data)
            print("decoding")
            gzip_data_decoded = gzip_data.decode()
            print("freeing gzip_data")
            gzip_data = None
            print("loading json")
            data = json.loads(gzip_data_decoded)
            print("freeing gzip_data_decoded")
            gzip_data_decoded = None

        else:
            data = json.loads(request.data)

        # Check target
        assert data["target"] == "BlockTrust Network Ingestion API"

        # Check version
        version = list(map(int, data["version"].split('.')))
        assert version[0] == 1

        # Check account
        account = g.db.accounts.get_account_by_id(data["account"])
        if account is None:
            raise ExportException("Bad account ID")
        if account.token() != data["token"]:
            raise ExportException("Bad token")

        # Check for bad syntax

        for action in data["actions"]:
            rows = action["data"]["values"]

            for row in rows:
                if len(action["data"]["fields"]) != len(row):
                    raise ExportException("Fields & row length mismatch")

        # Execute actions

        for action in data["actions"]:
            rows = action["data"]["values"]
            left = 0
            size = 5000
            right = 0
            while left < len(rows):
                right = left + size
                if right > len(rows):
                    right = len(rows)

                ss = []

                for row in rows[left:right]:
                    fields = {
                        key: value for key, value in zip(
                            action["data"]["fields"],
                            row
                        )
                    }
                    ss += (
                        data["account"],
                        action["data"]["namespace"],
                        action["data"]["type"],
                        json.dumps(fields)
                    )

                sql = (
                    "INSERT INTO api_inserts (account, namespace, type, fields) VALUES " +
                    ",".join(["(%s, %s, %s, %s)" for i in range(right - left)])
                )

                # TODO: remove once we have a separate dev and prod server for API
                server = data.get("server", "production")

                if server == "development":
                    g.dev_db.execute(
                        sql, ss
                    )
                elif server == "both":
                    g.dev_db.execute(
                        sql, ss
                    )
                    g.db.execute(
                        sql, ss
                    )
                else:
                    g.db.execute(
                        sql, ss
                    )

                left = right


        # All-good
        print("api good")
        return "", 200
    except ExportException as e:
        raise e
    except Exception as e:
        print("Input API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Input API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route('/api/v2', methods=["POST"])
@jwt_required()
def serve_api_v2():
    try:
        # Decode the data

        data = None
        if request.headers.get('content-encoding', None) is not None:
            print("decompressing")
            gzip_data = gzip.decompress(request.data)
            print("decoding")
            gzip_data_decoded = gzip_data.decode()
            print("freeing gzip_data")
            gzip_data = None
            print("loading json")
            data = json.loads(gzip_data_decoded)
            print("freeing gzip_data_decoded")
            gzip_data_decoded = None

        else:
            data = json.loads(request.data)

        # Check target
        assert data["target"] == "BlockTrust Network Ingestion API"

        # Check version
        version = list(map(int, data["version"].split('.')))
        assert version[0] == 1

        # Check account
        account = g.db.accounts.get_account_by_id(data["account"])
        if account is None:
            raise ExportException("Bad account ID")

        # Check for bad syntax

        for action in data["actions"]:
            rows = action["data"]["values"]

            for row in rows:
                if len(action["data"]["fields"]) != len(row):
                    raise ExportException("Fields & row length mismatch")

        # Execute actions

        for action in data["actions"]:
            rows = action["data"]["values"]
            left = 0
            size = 5000
            right = 0
            while left < len(rows):
                right = left + size
                if right > len(rows):
                    right = len(rows)

                ss = []

                for row in rows[left:right]:
                    fields = {
                        key: value for key, value in zip(
                            action["data"]["fields"],
                            row
                        )
                    }
                    ss += (
                        data["account"],
                        action["data"]["namespace"],
                        action["data"]["type"],
                        json.dumps(fields)
                    )

                sql = (
                    "INSERT INTO api_inserts (account, namespace, type, fields) VALUES " +
                    ",".join(["(%s, %s, %s, %s)" for i in range(right - left)])
                )

                # TODO: remove once we have a separate dev and prod server for API
                server = data.get("server", "production")

                if server == "development":
                    g.dev_db.execute(
                        sql, ss
                    )
                elif server == "both":
                    g.dev_db.execute(
                        sql, ss
                    )
                    g.db.execute(
                        sql, ss
                    )
                else:
                    g.db.execute(
                        sql, ss
                    )

                left = right

        APIDataRequests(g.db).insert_api_data_request(api_route=request.path, employee_id=get_jwt_identity())
        # All-good
        print("api good")
        return "", 200
    except ExportException as e:
        raise e
    except Exception as e:
        print("Input API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Input API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route('/api/insert_sales_group', methods=["POST"])
def serve_insert_sales_group():
    try:
        try:
            request_data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return {"error": "Decoding request JSON has failed"}, 400
        if "token" not in request_data:
            raise ExportException("Bad request. Missing token.")
        if request_data["token"] != TEMPORARY_SALES_GROUP_API_TOKEN:
            raise ExportException("Invlaid Token provided")
        accounts_list = Accounts(g.db).get_accounts(id=request_data["account_id"])
        if len(accounts_list) == 0:
            raise ExportException("Account not found.")
        else:
            authenticated_account = accounts_list[0]
        sales_group_data = {
            "sales_group_name": "",
            "total_animals": 0,
            "zip_code": 0,
            "sale_date_string": "",
            "delivery_location_type": "",
            "auction_market": "",
            "delivery_location": "",
            "category": "",
            "breeds": [],
            "breed_comments": "",
            "base_weight": 0,
            "weight_variance": "",
            "weighing_conditions": "",
            "frame": "",
            "muscling": "",
            "horns": "",
            "preconditioning_program": "",
            "feeding_program": [],
            "implants": [],
            "castrated": "",
            "pvp_program": "",
            "publish_sales_group": 1,
            "show_carcass_data_for_account": 1,
            "price": 0,
            "slide": ""
        }

        for sales_group_data_field_name, sales_group_data_field_value in sales_group_data.items():
            if sales_group_data_field_name not in request_data:
                raise ExportException("Missing field: " + sales_group_data_field_name)
            if type(sales_group_data_field_value) != type(request_data[sales_group_data_field_name]):
                raise ExportException(sales_group_data_field_name + " should be " + type(sales_group_data_field_value).__name__)
            sales_group_data[sales_group_data_field_name] = request_data[sales_group_data_field_name]

        sale_date_string = sales_group_data["sale_date_string"] + " 12:00"
        sale_date_format = "%m/%d/%Y %H:%M"
        sale_date_object = datetime.strptime(sale_date_string, sale_date_format)
        # Localizing to Eastern Timezone
        ny_tz = ZoneInfo("America/New_York")
        sale_date_object = sale_date_object.replace(tzinfo=ny_tz)
        sale_epoch_time = int(sale_date_object.timestamp())

        SalesGroups(g.db).validate_or_fail_sales_group(
            account_id=authenticated_account["id"],
            group_name=sales_group_data["sales_group_name"],
            zip=sales_group_data["zip_code"],
            delivery_location_type=sales_group_data["delivery_location_type"],
            count=sales_group_data["total_animals"],
            weight=sales_group_data["base_weight"],
            category=sales_group_data["category"],
            breeds=sales_group_data["breeds"],
            sale_date=sale_epoch_time,
            delivery_location=sales_group_data["delivery_location"],
            auction_market_location=sales_group_data["auction_market"],
            images=[],
            price=sales_group_data["price"],
            slide=sales_group_data["slide"],
            weighing_conditions=sales_group_data["weighing_conditions"],
            published=True if sales_group_data["publish_sales_group"] == 1 else False
        )
        reported_data = {
            "comments": request_data["comments"] if "comments" in request_data else "",
            "count": sales_group_data["total_animals"],
            "weight": sales_group_data["base_weight"],
            "weight_variance": sales_group_data["weight_variance"],
            "breeds": sales_group_data["breeds"],
            "horns": sales_group_data["horns"],
            "muscling": sales_group_data["muscling"],
            "usda_frame_size": sales_group_data["frame"],
            "preconditioning_program": sales_group_data["preconditioning_program"],
            "vaccinations_and_dates": request_data.get("vaccinations_and_dates", []),
            "feeding_program": sales_group_data["feeding_program"],
            "implants": sales_group_data["implants"],
            "castrated": sales_group_data["castrated"],
            "process_verified_program": sales_group_data["pvp_program"],
            "weaned_date": request_data.get("weaned_date", ""),
            "images": [],
            "videos": []
        }
        delivery_location = ""
        if sales_group_data["delivery_location_type"] == "Direct/Off Ranch":
            delivery_location = sales_group_data["delivery_location"]
        else:
            delivery_location = sales_group_data["auction_market"]
        sales_group_id = SalesGroups(g.db).insert_sales_group(
            account=authenticated_account["id"],
            reported=reported_data,
            published=1,
            zip_code=sales_group_data["zip_code"],
            delivery_location=delivery_location,
            sale_date=sale_epoch_time,
            auction_sale=None,
            group_name=sales_group_data["sales_group_name"],
            is_archived=0,
            delivery_location_type=sales_group_data["delivery_location_type"],
            price=sales_group_data["price"],
            category=sales_group_data["category"],
            breed_comments=sales_group_data["breed_comments"],
            weighing_conditions=sales_group_data["weighing_conditions"],
            show_account_carcass_data=1,
            is_api_insert=1,
            auction_market_id=request_data.get("auction_market_id", None),
            upload_file=request_data.get("upload_file", None)
        )
        SalesGroups(g.db).update_sales_group(
            id=sales_group_id, is_paid=request_data.get("is_paid", 1)
        )

        if "sales_group_files" in request_data:
            sales_group_files = request_data["sales_group_files"]
            for file in sales_group_files:
                SalesGroups(g.db).validate_sales_group_file(name=file.get("file_name", None), link=file.get("file_link", None))
                SalesGroups(g.db).upload_sales_group_file(
                    sales_group_id=sales_group_id,
                    account_id=authenticated_account["id"],
                    file_name=file["file_name"],
                    file_link=file["file_link"]
                )

        return {"response": "Sales Group Inserted", "sales_group_id": sales_group_id}, 200
    except ExportException as e:
        raise e
    except Exception as e:
        print("Sales Group API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Sales Group API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route('/api/create_new_account', methods=["POST"])
def serve_create_new_account():
    try:
        try:
            request_data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return {"error": "Decoding request JSON has failed"}, 400
        if "token" not in request_data:
            raise ExportException("Bad request. Missing token.")
        if request_data["token"] != TEMPORARY_CREATE_ACCOUNT_API_TOKEN:
            raise ExportException("Invlaid Token provided")
        required = {
            'company': None, 'sector': None, 'first_name': None, 'last_name': None,
            'username': None, 'email': None, 'password': None, 'confirm_password': None,
            'zip_code': None
        }
        for required_field in required:
            if required_field not in request_data:
                raise ExportException("Missing Required Field: " + required_field)
            required[required_field] = request_data[required_field]
            if len(required[required_field].strip()) == 0:
                raise ExportException("'" + required_field.capitalize().replace("_", " ") + "' does not have a value")

        try:
            account = auth.verified_signup(
                username=required['username'],
                email=required['email'],
                phone=request_data.get("phone", ""),
                first_name=required['first_name'],
                last_name=required['last_name'],
                password=required['password'],
                confirm_password=required['confirm_password'],
                company=required['company'],
                partner=request_data.get("partner", ""),
                affiliate_id=request_data.get('affiliate_id', ""),
                sector=required['sector'],
                address=request_data.get("address", ""),
                city=request_data.get("city", ""),
                state=request_data.get("state", ""),
                zip_code=required["zip_code"],
                personal_phone=request_data.get("personal_phone", ""),
                auction_markets_used=request_data.get("auction_market_ids", []),
                preconditioning_programs=request_data.get("preconditioning_programs", []),
                pvp_programs=request_data.get("pvp_programs", [])
            )
        except UsersException:
            user = Users(g.db).get_by_email(required["email"])
            if user is not None:
                account_user = AccountUsers(g.db).get_by_user(user)
                if len(account_user) > 0:
                    error_message = "Email is being used by Account " + str(account_user[0].account_id())
                    raise ExportException("Signup failed for " + required['company'] +" : " + error_message)
            
            user = Users(g.db).get_by_username(required["username"])
            if user is not None:
                account_user = AccountUsers(g.db).get_by_user(user)
                if len(account_user) > 0:
                    error_message = "Username is being used by Account " + str(account_user[0].account_id())
                raise ExportException("Signup failed for " + required['company'] +" : " + error_message)
        except (auth.SignupFailedException, AccountsException) as e:
            raise ExportException("Signup failed for " + required['company'] +" : " + str(e))

        return {"response": "New Account Created for " + required['company'], "account_id": account.id()}
    except ExportException as e:
        raise e
    except Exception as e:
        print("Create Account API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Create Account API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500


@bp.route('/api/data', methods=["POST"])
def data():
    print(f"Route: {request.path}, Data received: {request.json}")
    return Response(status=HTTPStatus.NO_CONTENT)


@bp.route('/api/update_sales_group', methods=["POST"])
def serve_update_sales_group():
    try:
        try:
            request_data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return {"error": "Decoding request JSON has failed"}, 400
        if "token" not in request_data:
            raise ExportException("Bad request. Missing token.")
        if request_data["token"] != TEMPORARY_SALES_GROUP_API_TOKEN:
            raise ExportException("Invlaid Token provided")
        if "sales_group_id" not in request_data:
            raise ExportException("Sales Group ID needs to be provided.")
        if request_data["token"] != TEMPORARY_SALES_GROUP_API_TOKEN:
            raise ExportException("Invlaid Token provided")
        original_row = SalesGroups(g.db).get_sales_group_by_id(request_data["sales_group_id"])

        accounts_list = Accounts(g.db).get_accounts(id=original_row["account"])
        if len(accounts_list) == 0:
            raise ExportException("Account not found.")
        else:
            authenticated_account = accounts_list[0]

        images = []
        reported = original_row["reported"]

        sale_epoch_time = original_row["sale_date"]
        if "sale_date_string" in request_data and request_data["sale_date_string"] != "":
            sale_date_string = request_data["sale_date_string"] + " 12:00"
            sale_date_format = "%m/%d/%Y %H:%M"
            sale_date_object = datetime.strptime(sale_date_string, sale_date_format)
            # Localizing to Eastern Timezone
            ny_tz = ZoneInfo("America/New_York")
            sale_date_object = sale_date_object.replace(tzinfo=ny_tz)
            sale_epoch_time = int(sale_date_object.timestamp())

        SalesGroups(g.db).validate_or_fail_sales_group(
            account_id=authenticated_account["id"],
            group_name=request_data.get("sales_group_name", original_row["group_name"]),
            zip=request_data.get("zip", original_row["zip"]),
            delivery_location_type=request_data.get("delivery_location_type", original_row["delivery_location_type"]),
            count=request_data.get("count", reported.get("count", 0)),
            weight=request_data.get("weight", reported.get("weight", 0)),
            category=request_data.get("category", original_row["category"]),
            breeds=request_data.get("breeds", reported.get("breeds", [])),
            sale_date=sale_epoch_time,
            delivery_location=request_data.get("delivery_location", original_row["delivery_location"]),
            auction_market_location=request_data.get("auction_market", original_row["delivery_location"]),
            images=images,
            price=request_data.get("price", original_row["price"]),
            slide=request_data.get("slide", reported.get("marketing_slide", "")),
            weighing_conditions=request_data.get("weighing_conditions", reported.get("marketing_weighing_conditions", "")),
            published=request_data.get("published", original_row["published"])
        )
        
        delivery_location = original_row["delivery_location"]
        auction_market_id = original_row["auction_market_id"]
        if "delivery_location_type" in request_data and request_data["delivery_location_type"] == "Direct/Off Ranch":
            delivery_location = request_data["delivery_location"]
        elif "delivery_location_type" in request_data and request_data["delivery_location_type"] == "Auction":
            delivery_location = request_data["auction_market"]
            auction_market_id = request_data.get("auction_market_id", original_row["auction_market_id"])
            convert_auction_market_to_account(g.db, auction_market_id, request_data.get("sales_group_name", None))
        
        for reported_field in SALES_GROUP_REPORTED_FIELDS:
            if reported_field["field_name"] in request_data:
                reported_field_name = reported_field["field_name"]
                reported_field_default = reported_field["field_default"]
                if type(request_data[reported_field_name]) == type(reported_field_default):
                    reported[reported_field_name] = request_data[reported_field_name]
                else:
                    field_name = ' '.join(word.capitalize() for word in reported_field_name.split('_'))
                    field_type = type(reported_field_default).__name__
                    error_message = "Wrong Data type provided for field: " + field_name + ". Please provide: " + field_type
                    raise ExportException(error_message)

        SalesGroups(g.db).update_sales_group(
            id=request_data["sales_group_id"],
            reported=reported,
            published=request_data.get("published", original_row["published"]),
            zip_code=request_data.get("zip", original_row["zip"]),
            delivery_location=delivery_location,
            auction_market_id=auction_market_id,
            sale_date=sale_epoch_time,
            group_name=request_data.get("sales_group_name", original_row["group_name"]),
            is_archived=request_data.get("is_archived", original_row["is_archived"]),
            delivery_location_type=request_data.get("delivery_location_type", original_row["delivery_location_type"]),
            price=request_data.get("price", original_row["price"]),
            category=request_data.get("category", original_row["category"]),
            breed_comments=request_data.get("breed_comments", original_row["breed_comments"]),
            weighing_conditions=request_data.get("weighing_conditions", reported.get("marketing_weighing_conditions", "")),
            show_account_carcass_data=request_data.get("show_account_carcass_data", reported.get("show_account_carcass_data", 1)),
            upload_file=request_data.get("upload_file", original_row["upload_file"])
        )
        if "sales_group_files" in request_data:
            sales_group_files = request_data["sales_group_files"]
            for file in sales_group_files:
                SalesGroups(g.db).validate_sales_group_file(name=file.get("file_name", None), link=file.get("file_link", None))
                existing_file = Files(g.db).get_files(
                    name=file["file_name"],
                    sales_group_id=request_data["sales_group_id"],
                    external_link=file["file_link"]
                )
                if len(existing_file) == 0:
                    SalesGroups(g.db).upload_sales_group_file(
                        sales_group_id=request_data["sales_group_id"],
                        account_id=authenticated_account["id"],
                        file_name=file["file_name"],
                        file_link=file["file_link"]
                    )
        return {"response": "Sales Group Updated"}, 200
    except ExportException as e:
        raise e
    except Exception as e:
        print("Update Sales Group API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Update Sales Group API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500