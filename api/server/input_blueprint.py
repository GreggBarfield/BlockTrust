import json
import os
import gzip


from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)


from core.database.tables.error_logs import ErrorLogs 
from ..database.inserts_model import InsertsModel
from core.database.tables.accounts import AccountsException
from core.database.database import Database
from core.database.tables.accounts import Accounts
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.sales_groups import SalesGroups
from core.database.tables.users import UsersException
from core.config import MYSQL_CONFIG, API_MYSQL_CONFIG, DEV_MYSQL_CONFIG
from core.common_exceptions import ExportException
from core.utilities import auth

from traceback import format_exc


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
                print(left, "/", len(rows))
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
                print(sql)

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

        print("sent to db")

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
        accounts_list = Accounts(g.db).get_accounts(token=request_data["token"])
        if len(accounts_list) == 0:
            raise ExportException("Bad token. You are not authorized to insert a sales group")
        else:
            authenticated_account = accounts_list[0]
        sales_group_data = {
            "sales_group_name": "",
            "total_animals": 0,
            "zip_code": 0,
            "sale_date": 0,
            "end_time": 0,
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
            "vaccinations": [],
            "feeding_program": [],
            "implants": [],
            "castrated": "",
            "pvp_program": "",
            "publish_sales_group": 1,
            "show_carcass_data_for_account": 1,
            "price": 0
        }

        for sales_group_data_field_name, sales_group_data_field_value in sales_group_data.items():
            if sales_group_data_field_name not in request_data:
                raise ExportException("Missing field: " + sales_group_data_field_name)
            if type(sales_group_data_field_value) != type(request_data[sales_group_data_field_name]):
                raise ExportException(sales_group_data_field_name + " should be " + type(sales_group_data_field_value).__name__)
            sales_group_data[sales_group_data_field_name] = request_data[sales_group_data_field_name]

        SalesGroups(g.db).validate_or_fail_sales_group(
            account_id=authenticated_account["id"],
            group_name=sales_group_data["sales_group_name"],
            zip=sales_group_data["zip_code"],
            delivery_location_type=sales_group_data["delivery_location_type"],
            count=sales_group_data["total_animals"],
            weight=sales_group_data["base_weight"],
            category=sales_group_data["category"],
            breeds=sales_group_data["breeds"],
            auction_sale=None,
            sale_date=sales_group_data["sale_date"],
            delivery_location=sales_group_data["delivery_location"],
            auction_market_location=sales_group_data["auction_market"],
            images=[],
            price=sales_group_data["price"]
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
            "vaccinations": sales_group_data["vaccinations"],
            "feeding_program": sales_group_data["feeding_program"],
            "implants": sales_group_data["implants"],
            "castrated": sales_group_data["castrated"],
            "process_verified_program": sales_group_data["pvp_program"],
            "images": [],
            "videos": []
        }
        delivery_location = ""
        if sales_group_data["delivery_location_type"] == "Direct/Off Ranch":
            delivery_location = sales_group_data["delivery_location"]
        else:
            delivery_location = sales_group_data["auction_market"]
        SalesGroups(g.db).insert_sales_group(
            account=authenticated_account["id"],
            reported=reported_data,
            published=sales_group_data["publish_sales_group"],
            zip_code=sales_group_data["zip_code"],
            delivery_location=delivery_location,
            sale_date=sales_group_data["sale_date"],
            auction_sale=None,
            group_name=sales_group_data["sales_group_name"],
            is_archived=0,
            delivery_location_type=sales_group_data["delivery_location_type"],
            price=sales_group_data["price"],
            category=sales_group_data["category"],
            breed_comments=sales_group_data["breed_comments"],
            weighing_conditions=sales_group_data["weighing_conditions"],
            show_account_carcass_data=1,
            is_api_insert=1
        )
        return {"response": "Sales Group Inserted"}, 200
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
        accounts_list = Accounts(g.db).get_accounts(token=request_data["token"])
        if len(accounts_list) == 0:
            raise ExportException("Bad token. You are not authorized to insert a new account")
        required = {
            'company': None, 'sector': None, 'first_name': None, 'last_name': None,
            'address': None, 'city': None, 'state': None, 'zip_code': None,
            'username': None, 'email': None, 'password': None, 'confirm_password': None
        }
        for required_field in required:
            if required_field not in request_data:
                raise ExportException("Missing Required Field: " + required_field)
            required[required_field] = request_data[required_field]
            if len(required[required_field].strip()) == 0:
                raise ExportException("'" + required_field.capitalize().replace("_", " ") + "' does not have a value")
        
        try:
            auth.verified_signup(
                username=required['username'],
                email=required['email'],
                phone=request_data['phone'],
                first_name=required['first_name'],
                last_name=required['last_name'],
                password=required['password'],
                confirm_password=required['confirm_password'],
                company=required['company'],
                partner=request_data['partner'],
                affiliate_id=request_data['affiliate_id'],
                sector=required['sector'],
                address=required['address'],
                city=required['city'],
                state=required['state'],
                zip_code=required['zip_code'],
                personal_phone=request_data['personal_phone']
            )
        except (auth.SignupFailedException, AccountsException, UsersException) as e:
            raise ExportException("Signup failed for " + required['company'] +" : " + str(e))

        return {"response": "New Account Created for " + required['company']}
    except ExportException as e:
        raise e
    except Exception as e:
        print("Create Account API", e.__class__.__name__ + ": " + str(e), format_exc())
        ErrorLogs(g.db).insert_error_log("Sales Group API", e.__class__.__name__ + ": " + str(e), format_exc())
        return {"error": "Internal Server Error"}, 500
