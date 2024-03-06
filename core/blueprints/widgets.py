import json
from flask import (
    Response, request, Blueprint, g, url_for
)

from ..sectors import SECTORS_NAME_TO_ID, SECTORS_ID_TO_NAME
from ..match_types import MATCH_TYPES_NAME_TO_ID, MATCH_TYPES_ID_TO_NAME

from ..common_exceptions import ExportException

from ..database.combinations import convert_auction_market_to_account, send_connection_request_email_to_admin_users
from ..database.tables.account_links import AccountLinks
from ..database.tables.accounts import HEALTH_TRACK_PARTNER_COMPANY
from ..database.tables.advertisement_companies import AdvertisementCompanies
from ..database.tables.advertisements import ADVERTISEMENT_CATEGORY_IDS_TO_NAMES, Advertisements
from ..database.tables.auction_markets import AuctionMarkets
from ..database.tables.connections import Connections, CONNECTION_STATUS_NAME_TO_ID, CONNECTION_TYPE_NAME_TO_ID
from ..database.tables.connection_invites import ConnectionInvites
from ..database.tables.files import Files, DEFAULT_FILES_S3_PATH
from ..database.tables.matches import Matches
from ..database.tables.messages import Messages
from ..database.tables.not_interested_sales_group_ids_for_accounts import NotInterestedSalesGroupIdsForAccounts
from ..database.tables.reports import Reports
from ..database.tables.sales_group_animals import SalesGroupAnimals
from ..database.tables.sales_group_fields_values import SalesGroupFieldsValues, SALES_GROUP_FIELD_NAMES_TO_IDS
from ..database.tables.sales_group_searches import SalesGroupSearches
from ..database.tables.sustainability_responses import SustainabilityResponses, QUESTIONNAIRE_STATUS_NAMES_TO_IDS
from ..database.tables.usda_favorites_for_accounts import USDAFavoritesForAccounts
from ..database.tables.usda_reports import USDAReports
from ..database.tables.sales_groups import SalesGroups

from ..reports.query_types import count_eid_distinct, count_distribution

from ..renderers.email import render_email
from ..utilities.constants import HTTP_CREATED, HTTP_NO_CONTENT
from ..utilities.email import send_email
from ..utilities.general_utilities import format_field
from ..utilities.spatial_math import meters_to_miles, distance
from ..utilities.data.zip_codes_data import ZIP_CODES

from ..config import ROOT as WEBSITE_ROOT

from ..utilities import crut

from ..data_requests.router import unauth_route

import time

bp = Blueprint('widgets_bp', __name__)


@bp.route('/widgets/data/direct/<name>', methods=['POST'])
@crut.require_user_or_employee
def serve_direct(name):
    direct_export = {
        "match_types_id_to_name": MATCH_TYPES_ID_TO_NAME,
        "match_types_name_to_id": MATCH_TYPES_NAME_TO_ID,
        "sectors_id_to_name": SECTORS_ID_TO_NAME,
        "sectors_name_to_id": SECTORS_NAME_TO_ID
    }

    if name in direct_export:
        return {
            name: direct_export[name]
        }
    raise ExportException("Unable to directly export the requested value")


@bp.route('/widgets/data/sales_group', methods=['POST'])
@crut.require_account
def serve_sales_group():
    sales_group_row = SalesGroups(g.db).get_sales_group_by_id(request.json["sales_group"])
    if not (sales_group_row["published"] > 0 or sales_group_row["account"] == g.account.id()):
        raise ExportException("Insufficient Permissions")
    return {
        "id": sales_group_row["id"],
        "reported": sales_group_row["reported"],
        "published": sales_group_row["published"],
        "account": sales_group_row["account"],
        "account_name": sales_group_row["account_name"],
        "is_account_payouts_enabled": sales_group_row["is_account_payouts_enabled"],
        "eids": list(map(lambda item: item['eid'], SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_row["id"]))),
        "file_auths": Files(g.db).get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None),
        "zip": sales_group_row["zip"],
        "market_location": sales_group_row["market_location"],
        "delivery_location_type": sales_group_row["delivery_location_type"],
        "delivery_location": sales_group_row["delivery_location"],
        "sale_date": sales_group_row["sale_date"],
        "auction_sale": sales_group_row["auction_sale"],
        "auction_sale_name": sales_group_row["auction_sale_name"],
        "group_name": sales_group_row["group_name"],
        "userID": g.user.id(),
        "name": g.user.first_name() + ' ' + g.user.last_name(),
        "companyId": g.account.id(),
        "company": g.account.name(),
        "is_archived": sales_group_row["is_archived"],
        "price": sales_group_row["price"],
        "is_sold": sales_group_row["is_sold"],
        "category": sales_group_row["category"],
        "breed_comments": sales_group_row["breed_comments"],
        "weighing_conditions": sales_group_row["weighing_conditions"],
        "show_account_carcass_data": sales_group_row["show_account_carcass_data"],
        "auction_market_id": sales_group_row["auction_market_id"],
        "created_date": sales_group_row["created_timestamp"].strftime("%m/%d/%Y"),
        "is_paid": sales_group_row["is_paid"]
    }


@bp.route('/widgets/data/auction_markets', methods=['POST'])
@crut.require_account
def serve_auction_markets():
    auction_markets = AuctionMarkets(g.db).get_auction_markets(
        is_archived=0,
        auction_markets_order_by="name",
        auction_markets_sort_by="ASC"
    )
    return {"auction_markets": auction_markets}


@bp.route('/widgets/data/search_sales_groups', methods=['POST'])
@crut.require_account
def serve_search_sales_groups():
    sales_group_rows = []

    # TODO: Optimize and fix
    sales_group_rows = SalesGroups(g.db).get_sales_groups_and_data(account_id=request.json["search"]["params"]["ID"], is_archived=0)

    results = []

    for sales_group_row in sales_group_rows:
        if sales_group_row["account"] == g.account.id():
            results.append({
                "id": sales_group_row["id"],
                "reported": sales_group_row["reported"],
                "published": sales_group_row["published"],
                "account": sales_group_row["account"],
                "account_name": sales_group_row["account_name"],
                "eids": list(map(lambda item: item['eid'], SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_row["id"]))),
                "file_auths": Files(g.db).get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None) if request.json["file_auths"] else [],
                "zip": sales_group_row["zip"],
                "market_location": sales_group_row["market_location"],
                "delivery_location": sales_group_row["delivery_location"],
                "sale_date": sales_group_row["sale_date"],
                "auction_sale": sales_group_row["auction_sale"],
                "auction_sale_name": sales_group_row["auction_sale_name"],
                "group_name": sales_group_row["group_name"],
                "is_archived":sales_group_row["is_archived"]
            })

    return {
        "sales_groups": results
    }


@bp.route('/widgets/data/search_sales_groups_2', methods=['POST'])
@crut.require_account
def serve_search_sales_groups_2():
    sales_group_rows = []

    sales_group_rows = SalesGroups(g.db).search_within(
        zip_code=request.json["search"]["zip"],
        miles=request.json["search"]["radius"],
        sale_date=time.time(),
        is_archived=0,
        categories=request.json["search"]["categories"],
        breeds=request.json["search"]["breeds"],
        minimum_weight=request.json["search"]["minimum_weight"],
        maximum_weight=request.json["search"]["maximum_weight"],
        preconditioning_program=request.json["search"]["preconditioning_program"],
        programs=request.json["search"]["programs"],
        target_date_description=request.json["search"]["target_date"]
    )

    results = []

    for sales_group_row in sales_group_rows:
        owner_account_sustainability_averages = SustainabilityResponses(g.db).get_sustainability_response_averages(account_id=sales_group_row["account"])
        owner_account_sustainability_score_average = float(owner_account_sustainability_averages["score_average"]) if owner_account_sustainability_averages["score_average"] else 0
        results.append({
            "id": sales_group_row["id"],
            "reported": sales_group_row["reported"],
            "published": sales_group_row["published"],
            "group_name": sales_group_row["group_name"],
            "account": sales_group_row["account"],
            "account_name": sales_group_row["account_name"],
            "eids": list(map(lambda item: item['eid'], SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_row["id"]))),
            "file_auths": Files(g.db).get_auths(
                sales_group_row["reported"]["images"]
                if "images" in sales_group_row["reported"]
                else None
            ),
            "zip": sales_group_row["zip"],
            "market_location": sales_group_row["market_location"],
            "delivery_location":sales_group_row["delivery_location"],
            "sale_date": sales_group_row["sale_date"],
            "context": {
                "milesAway": meters_to_miles(distance(
                    ZIP_CODES[request.json["search"]["zip"]]["ecef"],
                    ZIP_CODES[sales_group_row["zip"]]["ecef"]
                ))
            },
            "auction_sale": sales_group_row["auction_sale"],
            "auction_sale_name": sales_group_row["auction_sale_name"],
            "is_archived": sales_group_row["is_archived"],
            "price": sales_group_row["price"],
            "is_sold": sales_group_row["is_sold"],
            "is_account_payouts_enabled": sales_group_row["is_account_payouts_enabled"],
            "category": sales_group_row["category"],
            "breed_comments": sales_group_row["breed_comments"],
            "weighing_conditions": sales_group_row["weighing_conditions"],
            "owner_account_sustainability_score_average": owner_account_sustainability_score_average
        })

    return {
        "sales_groups": results
    }


@bp.route('/widgets/data/sales_group_searches', methods=['GET', 'POST'])
@crut.require_account
def serve_sales_group_searches():
    if request.method == 'POST':
        multi_select_fields = {}
        if request.json["search"]["categories"]:
            multi_select_fields["categories"] = request.json["search"]["categories"]
        if request.json["search"]["breeds"]:
            multi_select_fields["breeds"] = request.json["search"]["breeds"]
        if request.json["search"]["programs"]:
            multi_select_fields["programs"] = request.json["search"]["programs"]
        id = SalesGroupSearches(g.db).insert(
            name=request.json["search"]["name"],
            user_id=g.user.id(),
            zip=request.json["search"]["zip"],
            radius=request.json["search"]["radius"],
            minimum_weight=request.json["search"]["minimum_weight"],
            maximum_weight=request.json["search"]["maximum_weight"],
            preconditioning_program=request.json["search"]["preconditioning_program"],
            multi_select_fields=multi_select_fields,
            target_date_description=request.json["search"]["target_date"]
        )
        return Response(str(id), status=HTTP_CREATED)
    return SalesGroupSearches(g.db).get(user_id=g.user.id())


@bp.route('/widgets/data/sales_group_searches/<int:id>', methods=['PUT', 'DELETE'])
@crut.require_account
def sales_group_search(id):
    if request.method == 'PUT':
        multi_select_fields = {}
        if request.json["search"]["categories"]:
            multi_select_fields["categories"] = request.json["search"]["categories"]
        if request.json["search"]["breeds"]:
            multi_select_fields["breeds"] = request.json["search"]["breeds"]
        if request.json["search"]["programs"]:
            multi_select_fields["programs"] = request.json["search"]["programs"]
        SalesGroupSearches(g.db).update(
            id=id,
            name=request.json["search"]["name"],
            zip=request.json["search"]["zip"],
            radius=request.json["search"]["radius"],
            minimum_weight=request.json["search"]["minimum_weight"],
            maximum_weight=request.json["search"]["maximum_weight"],
            preconditioning_program=request.json["search"]["preconditioning_program"],
            multi_select_fields=multi_select_fields,
            target_date_description=request.json["search"]["target_date"]
        )
        return Response(status=HTTP_NO_CONTENT)
    else:
        SalesGroupSearches(g.db).delete(id=id)
        return Response(status=HTTP_NO_CONTENT)


@bp.route('/widgets/data/search_summary', methods=['GET'])
@crut.require_account
def search_summary():
    searches = SalesGroupSearches(g.db).get(user_id=g.user.id())
    results = []
    filtered_results = []
    not_interested = NotInterestedSalesGroupIdsForAccounts(g.db).get(account_id=g.account.id())
    for search in searches:
        sales_group_rows = SalesGroups(g.db).search_within(
            zip_code=int(search["zip"]),
            miles=search["radius"],
            sale_date=time.time(),
            is_archived=0,
            categories=search["multi_select_fields"].get("categories", None) if search["multi_select_fields"] else None,
            breeds=search["multi_select_fields"].get("breeds", None) if search["multi_select_fields"] else None,
            minimum_weight=search["minimum_weight"] if search["minimum_weight"] else None,
            maximum_weight=search["maximum_weight"] if search["maximum_weight"] else None,
            preconditioning_program=search["preconditioning_program"],
            programs=search["multi_select_fields"].get("programs", None) if search["multi_select_fields"] else None,
            target_date_description=search["target_date_description"]
        )
        results.extend(list(filter(lambda row: not any(item["id"] == row["id"] for item in results), sales_group_rows)))
    filtered_results = list(filter(lambda row: not any(item["sales_group_id"] == row["id"] for item in not_interested), results))
    return filtered_results


@bp.route('/widgets/data/search_by_eid_and_visual_id_for_account', methods=['POST'])
@crut.require_account
def serve_search_by_eid_and_visual_id():
    eid_number = int(request.json["search"]["eid"])
    available_account_ids = [g.account.id()] if g.account.sector_id() == SECTORS_NAME_TO_ID["Cow-Calf"] else []
    available_account_ids += Connections(g.db).get_connected_account_ids(g.account.id(), SECTORS_NAME_TO_ID["Cow-Calf"])
    rows = Matches(g.db).get_matches_by_eid_or_visual_id(
        eid_or_visual_id=eid_number,
        account_ids=available_account_ids
    )
    redirect_route = url_for('dashboard_bp.serve_animal_eid')
    if len(rows) > 0:
        return {
            "redirect_route": redirect_route,
            "matches": rows
        }
    else:
        return {
                "redirect_route": redirect_route,
                "matches": []
        }


@bp.route('/widgets/data/create_sales_group', methods=["POST"])
@crut.require_account
def serve_create_sales_group():
    images = []
    if 'images' in request.json["reported"]:
        images = request.json["reported"]["images"]
    SalesGroups(g.db).validate_or_fail_sales_group(
        account_id=g.account.id(),
        group_name=request.json["group_name"],
        zip=request.json["zip"],
        delivery_location_type=request.json["delivery_location_type"],
        count=request.json["reported"]["count"],
        weight=request.json["reported"]["weight"],
        category=request.json["category"],
        breeds=request.json["reported"]["breeds"],
        sale_date=request.json["sale_date"],
        delivery_location=request.json["delivery_location"],
        auction_market_location=request.json["auction_market_location"],
        images=images,
        price=request.json["price"],
        slide=request.json["reported"]["marketing_slide"],
        weighing_conditions=request.json["reported"]["marketing_weighing_conditions"]
    )
    # Alright, go ahead...
    delivery_location = ""
    auction_market_id = None
    if request.json["delivery_location_type"] == "Direct/Off Ranch":
        delivery_location = request.json["delivery_location"]
    else:
        delivery_location = request.json["auction_market_location"]
        if request.json["delivery_location_type"] == "Auction":
            auction_market_id = request.json["auction_market_id"]
            convert_auction_market_to_account(g.db, auction_market_id, request.json["group_name"])
    partner_pays = False
    if g.account.partner_account_id():
        partner = g.db.accounts.get_partners(id=g.account.partner_account_id())[0]
        if partner["partner_pays_sales_groups"]:
            partner_pays = True
    sales_group_id = SalesGroups(g.db).insert_sales_group(
        account=g.account.id(),
        reported=request.json["reported"],
        published=request.json["published"] if partner_pays else int(False),
        zip_code=request.json["zip"],
        delivery_location=delivery_location,
        auction_market_id=auction_market_id,
        sale_date=request.json["sale_date"],
        group_name=request.json["group_name"],
        is_archived=0,
        delivery_location_type=request.json["delivery_location_type"],
        price=request.json["price"],
        category=request.json["category"],
        breed_comments=request.json["breed_comments"],
        weighing_conditions=request.json["weighing_conditions"],
        show_account_carcass_data=request.json["show_account_carcass_data"],
        is_api_insert=0
    )
    return {"id": sales_group_id}


@bp.route('/widgets/data/update_sales_group', methods=['POST'])
@crut.require_account
def serve_update_sales_group():
    # Check that the account selected is the owner of the sales group
    original_row = SalesGroups(g.db).get_sales_group_by_id(request.json["id"])
    if original_row["account"] != g.account.id():
        raise ExportException("Insufficient permissions to edit this sales group.")
    # Validate sales group fields
    images = []
    if 'images' in request.json["reported"]:
        images = request.json["reported"]["images"]
    SalesGroups(g.db).validate_or_fail_sales_group(
        account_id=g.account.id(),
        group_name=request.json["group_name"],
        zip=request.json["zip"],
        delivery_location_type=request.json["delivery_location_type"],
        count=request.json["reported"]["count"],
        weight=request.json["reported"]["weight"],
        category=request.json["category"],
        breeds=request.json["reported"]["breeds"],
        sale_date=request.json["sale_date"],
        delivery_location=request.json["delivery_location"],
        auction_market_location=request.json["auction_market_location"],
        images=images,
        price=request.json["price"],
        slide=request.json["reported"]["marketing_slide"],
        weighing_conditions=request.json["reported"]["marketing_weighing_conditions"]
    )
    delivery_location = ""
    auction_market_id = None
    if request.json["delivery_location_type"] == "Direct/Off Ranch":
        delivery_location = request.json["delivery_location"]
    else:
        delivery_location = request.json["auction_market_location"]
        if request.json["delivery_location_type"] == "Auction":
            auction_market_id = request.json["auction_market_id"]
            convert_auction_market_to_account(g.db, auction_market_id, request.json["group_name"])
    partner_pays = False
    if g.account.partner_account_id():
        partner = g.db.accounts.get_partners(id=g.account.partner_account_id())[0]
        if partner["partner_pays_sales_groups"]:
            partner_pays = True
    SalesGroups(g.db).update_sales_group(
        id=request.json["id"],
        reported=request.json["reported"],
        published=request.json["published"] if (request.json["is_paid"] or partner_pays) else int(False),
        zip_code=request.json["zip"],
        delivery_location=delivery_location,
        auction_market_id=auction_market_id,
        sale_date=request.json["sale_date"],
        group_name=request.json["group_name"],
        is_archived=0,
        delivery_location_type=request.json["delivery_location_type"],
        price=request.json["price"],
        category=request.json["category"],
        breed_comments=request.json["breed_comments"],
        weighing_conditions=request.json["weighing_conditions"],
        show_account_carcass_data=request.json["show_account_carcass_data"]
    )
  
    return Response(status=HTTP_NO_CONTENT)


@bp.route('/widgets/data/archive_sales_group', methods=['POST'])
@crut.require_account
def serve_archive_sales_group():
    SalesGroups(g.db).update_sales_group(id=request.json["sales_group_id"], is_archived=1)
    return {}, 200


@bp.route('/widgets/data/unarchive_sales_group', methods=['POST'])
@crut.require_account
def unarchive_sales_group():
    SalesGroups(g.db).update_sales_group(id=request.json["params"]["id"], is_archived=0)
    return {}, 200


@bp.route('/widgets/data/archived_sales_group', methods=['POST'])
@crut.require_account
def serve_archived_sales_group():
    sales_group_rows = []
    sales_group_rows = SalesGroups(g.db).get_sales_groups_and_data(account_id=request.json["search"]["params"]["ID"], is_archived=1)

    results = []

    for sales_group_row in sales_group_rows:
        results.append({
            "id": sales_group_row["id"],
            "reported": sales_group_row["reported"],
            "published": sales_group_row["published"],
            "account": sales_group_row["account"],
            "account_name": sales_group_row["account_name"],
            "eids": list(map(lambda item: item['eid'], SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_row["id"]))),
            "file_auths": Files(g.db).get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None),
            "zip": sales_group_row["zip"],
            "market_location": sales_group_row["market_location"],
            "delivery_location": sales_group_row["delivery_location"],
            "sale_date": sales_group_row["sale_date"],
            "auction_sale": sales_group_row["auction_sale"],
            "auction_sale_name": sales_group_row["auction_sale_name"],
            "group_name": sales_group_row["group_name"],
            "userID": g.user.id(),
            "name": g.user.first_name() + ' ' + g.user.last_name(),
            "companyId": request.json["search"]["params"]["ID"],
            "company": g.account.company(),
            "is_archived": sales_group_row["is_archived"]
        })

    return {
        "sales_groups": results
    }


@bp.route('/widgets/data/get_eids_for_sales_group', methods=['POST'])
@crut.require_account
def serve_get_eids_for_sales_group():
    healthtrack_partner_row = g.db.accounts.get_accounts(company=HEALTH_TRACK_PARTNER_COMPANY, is_partner=1)[0]
    is_healthtrack_partner_account = False
    if g.account.partner_account_id() == healthtrack_partner_row["id"]:
        is_healthtrack_partner_account = True
    sales_group_row = SalesGroups(g.db).get_sales_group_by_id(request.json["sales_group"])
    if not (sales_group_row["published"] > 0 or sales_group_row["account"] == g.account.id()):
        raise ExportException("Insufficient Permissions")
    # Getting eids owned by the account
    distinct_eids = Matches(g.db).get_distinct_eids_and_visual_ids_by_account(account_id=g.account.id(), number_of_years=1)
    # Getting sales groups owned by account and corresponding eid's
    account_sales_groups_ids = list(map(lambda item: item['id'], SalesGroups(g.db).get_sales_groups_and_data(account_id=g.account.id())))
    assigned_eids_for_account = []
    for sales_group_id in account_sales_groups_ids:
        assigned_eids = list(map(lambda item: item['eid'], SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_id)))
        if len(assigned_eids) > 0:
            assigned_eids_for_account.extend(assigned_eids)
    available_eids_with_visual_ids = []
    for distinct_eid in distinct_eids:
        if distinct_eid["eid"] not in assigned_eids_for_account:
            available_eids_with_visual_ids.append({
                "eid": distinct_eid["eid"],
                "visual_id": distinct_eid["visual_id"]
            })
    assigned_animals = SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_row["id"])
    return {
        "id": sales_group_row["id"],
        "assigned_animals": assigned_animals,
        "available_eids_with_visual_ids": available_eids_with_visual_ids,
        "is_healthtrack_partner_account": is_healthtrack_partner_account
    }


@bp.route('/widgets/data/save_eids_for_sales_group', methods=['POST'])
@crut.require_account
def serve_save_eids_for_sales_group():
    original_row = SalesGroups(g.db).get_sales_group_by_id(request.json["id"])
    SalesGroupAnimals(g.db).delete_sales_group_eids(sales_group_id=original_row["id"])
    SalesGroupAnimals(g.db).insert_sales_group_eids(sales_group_id=original_row["id"], eids_and_visual_ids=request.json["eids_and_visual_ids"])
    return {"redirect": "/dashboard/sales-groups/manage"}


@bp.route('/widgets/data/save_file_and_get_upload_config', methods=['POST'])
@crut.require_user_or_employee
def serve_save_file_get_upload_config():
    user_owns = request.json["user_owns"] is True
    account_owns = request.json["account_owns"] is True
    employee_owns = request.json["employee_owns"] is True
    question_id = request.json.get("question_id", None)
    file_s3_path = request.json["file_s3_path"] if request.json["file_s3_path"] is not None else DEFAULT_FILES_S3_PATH
    if not user_owns and not account_owns and not employee_owns:
        raise ExportException("Someone must own the file.")

    file_id, file_config = Files(g.db).insert_file_and_get_post_configuration(
        request.json["file_name"],
        g.user.id() if user_owns else None,
        g.account.id() if account_owns else None,
        g.employee.id() if employee_owns else None,
        question_id,
        file_s3_path=file_s3_path
    )

    return {
        "id": file_id,
        "config": file_config
    }


@bp.route('/widgets/data/get_accounts_list', methods=['POST'])
@crut.require_account
def serve_get_accounts_list():
    return {
        "accounts": g.db.accounts.get_accounts(is_partner=0)
    }

@bp.route('/widgets/data/get_account_messages', methods=['POST'])
@crut.require_account
def serve_get_account_messages():
    return {
        "messages": Messages(g.db).get(g.account.id(), g.account.id())
    }


@bp.route('/widgets/data/send_message', methods=['POST'])
@crut.require_account
def serve_send_message():
    message_id = Messages(g.db).insert_message(
        g.account.id(),
        request.json["params"]["to_account"],
        request.json["params"]["data"]
    )
    send_to_users = g.db.users.get_rows_by_account(request.json["params"]["to_account"])
    for user in send_to_users:
        if user["is_email_verified"] == 1:
            send_email(
                "New Message",
                render_email(
                    "new_message.html",
                    {
                        'new_message': {
                            'link': (
                                WEBSITE_ROOT + "/dashboard/messages/"
                                + str(message_id)
                            ),
                            'receiver': user['account_name'],
                            'sender': g.account.name()
                        }
                    }
                ),
                user["email"]
            )
    return {}, 200


@bp.route('/widgets/data/data_request', methods=['POST'])
@crut.require_user_or_employee
def serve_data_request():
    return unauth_route(request.json['request']), 200


@bp.route('/widgets/data/get_market_data/<slug_id>', methods=['POST'])
@crut.require_account
def serve_get_market_data(slug_id):
    return {
        'market_data': USDAReports(g.db).get_by_slug_id(slug_id)
    }, 200


@bp.route('/widgets/data/get_employee_summary_graphs_data', methods=['POST'])
@crut.require_employee
def get_employee_summary_graphs_data():
    ranches = g.db.accounts.get_accounts(sector=SECTORS_NAME_TO_ID["Cow-Calf"], accounts_order_by="created_timestamp")
    feedyards = g.db.accounts.get_accounts(sector=SECTORS_NAME_TO_ID["Feedlot"], accounts_order_by="created_timestamp")
    tags_count_list = Reports(g.db).get_reports(query=count_eid_distinct.create(), selectColumns=["result", "created_timestamp"])
    return {
        "ranches": ranches,
        "feedyards": feedyards,
        "tags_count_list": tags_count_list
    }


@bp.route('/widgets/data/get_usda_favorites_for_account', methods=['POST'])
@crut.require_account
def serve_get_usda_favorites():
    return { 'favorites': USDAFavoritesForAccounts(g.db).get_favorites_for_account(g.account.id()) }

@bp.route('/widgets/data/save_usda_favorites_for_account', methods=['POST'])
@crut.require_account
def serve_save_usda_favorites():
    request_json = json.loads(request.data)
    USDAFavoritesForAccounts(g.db).insert_usda_favorites_for_accounts(g.account.id(), request_json["state"], request_json["slug_id"])
    return {}, 200

@bp.route('/widgets/data/remove_usda_favorites_for_account', methods=['POST'])
@crut.require_account
def serve_remove_usda_favorite():
    request_json = json.loads(request.data)
    USDAFavoritesForAccounts(g.db).delete_usda_favorites_for_accounts(g.account.id(), request_json["state"], request_json["slug_id"])
    return {}, 200

@bp.route('/widgets/data/get_invitable_accounts', methods=['POST'])
@crut.require_account
def serve_get_invitable_accounts():
    invitable_account_rows = Connections(g.db).get_unconnected_accounts(account_id=g.account.id())
    return {"account_rows": invitable_account_rows}

@bp.route('/widgets/data/create-auction-market', methods=["POST"])
def serve_create_auction_market():
    if len(request.form["name"].strip()) == 0:
        raise ExportException("Auction market Name cannot be blank")
    if len(request.form["city"].strip()) == 0:
        raise ExportException("Auction market City cannot be blank")
    if len(request.form["state"].strip()) == 0:
        raise ExportException("Auction market State cannot be blank")
    new_auction_market_id = AuctionMarkets(g.db).insert_auction_market(
        name=format_field(request.form["name"]),
        address=format_field(request.form["address"]),
        city=format_field(request.form["city"]),
        state=format_field(request.form["state"]),
        zip_code=format_field(request.form["zip"]),
        phone=format_field(request.form["phone"]),
        email=format_field(request.form["email"])
    )
    new_auction_market_name = request.form["name"] + ", " + request.form["city"] + ", " + request.form["state"]
    return {
        "new_auction_market_name": new_auction_market_name,
        "new_auction_market_id": new_auction_market_id
    }

@bp.route('/widgets/data/add-connection-request', methods=["POST"])
@crut.require_account
def serve_add_connection_request():
    try:
        invited_accounts = request.json["invited_account_ids_list"]
        for invited_account_id in invited_accounts:
            Connections(g.db).create_or_fail_connection(g.account.id(), invited_account_id, CONNECTION_STATUS_NAME_TO_ID["Pending"],
                                                        connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Created"])
            send_connection_request_email_to_admin_users(g.db, invited_account_id, g.account.id())
        if request.json["unlisted_company"]:
            ConnectionInvites(g.db).add_connection_invite(
                from_account=g.account.id(),
                company_sector=request.json["new_account_sector"],
                company_name=request.json["new_account_name"],
                company_contact=request.json["new_account_contact_name"],
                company_email=request.json["new_account_email"]
            )
            send_email(
                "BlockTrust Network Connection Invite",
                render_email("send_connection_invite.html", {
                    'new_company_contact': request.json["new_account_contact_name"],
                    'account_company': g.account.name()
                }), request.json["new_account_email"]
            )
        return {"redirect": "/dashboard/connections"}
    except Exception as e:
        raise ExportException(str(e))

@bp.route('/widgets/data/search_by_eid_and_visual_id', methods=['POST'])
@crut.require_employee
def serve_employee_search_by_eid_and_visual_id():
    eid_number = int(request.json["search"]["eid"])
    rows = Matches(g.db).get_matches_by_eid_or_visual_id(eid_or_visual_id=eid_number)
    redirect_route = url_for('employee_bp.serve_animal_eid')
    if len(rows) > 0:
        return {
            "redirect_route": redirect_route,
            "matches": rows
        }
    else:
        return {
            "redirect_route": redirect_route,
            "matches": []
        }

@bp.route('/widgets/data/get_animals_and_grouping_ids_for_account', methods=["POST"])
@crut.require_account
def get_animals_and_grouping_ids_for_account():
    animals_and_grouping_ids = Matches(g.db).get_matches_with_account_links(
        account_links_account_id=g.account.id(),
        matches_partner_account_id=g.account.partner_account_id(),
        is_distinct=True,
        matches_cols=("eid", "visual_id", "grouping_id")
    )
    # Getting sales groups owned by account and corresponding eid's
    account_sales_groups_ids = SalesGroups(g.db).get_sales_groups(account_id=g.account.id(), sales_group_cols=["id"])
    assigned_eids_for_account = []
    for sales_group_id in account_sales_groups_ids:
        assigned_eids = list(map(lambda item: item['eid'], SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_id["id"])))
        if len(assigned_eids) > 0:
            assigned_eids_for_account.extend(assigned_eids)
    available_animals_and_grouping_ids = []
    for animal_and_grouping_id in animals_and_grouping_ids:
        if animal_and_grouping_id["eid"] not in assigned_eids_for_account:
            available_animals_and_grouping_ids.append(animal_and_grouping_id)
    return {"available_animals_and_grouping_ids": available_animals_and_grouping_ids}

@bp.route('/widgets/data/save_eids_by_application_id_for_sales_group', methods=["POST"])
@crut.require_account
def serve_save_eids_by_application_id():
    SalesGroupAnimals(g.db).delete_sales_group_eids(sales_group_id=request.json["sales_group_id"])
    SalesGroupAnimals(g.db).insert_sales_group_eids(sales_group_id=request.json["sales_group_id"], eids_and_visual_ids=request.json["eids_and_visual_ids_list"])
    return {"redirect": "/dashboard/sales-groups/manage"}

@bp.route('/widgets/data/save_sustainability_questionnaire', methods=["POST"])
@crut.require_account
def serve_save_sustainability_questionnaire():
    if request.json["sustainability_response_id"] is not None:
        SustainabilityResponses(g.db).update_sustainability_response(
            id=request.json["sustainability_response_id"],
            air_points=round(request.json["scores"]["air"], 1),
            land_points=round(request.json["scores"]["land"], 1),
            water_points=round(request.json["scores"]["water"], 1),
            animal_points=round(request.json["scores"]["animal"], 1),
            safety_points=round(request.json["scores"]["safety"], 1),
            efficiency_points=round(request.json["scores"]["efficiency"], 1),
            improvement_points=round(request.json["scores"]["improvement"], 1),
            score=request.json["total_score"],
            response=request.json["responses"],
            sector_id=g.account.sector_id(),
            questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Pending"] if request.json["is_partial_response"] else QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Completed"]
        )
        previously_uploaded_files = Files(g.db).get_files(sustainability_response_id=request.json["sustainability_response_id"])
        previously_uploaded_file_ids = [file["id"] for file in previously_uploaded_files]
        removed_file_ids = [id for id in previously_uploaded_file_ids if id not in request.json["uploaded_file_ids"]]
        newly_uploaded_file_ids = [id for id in request.json["uploaded_file_ids"] if id != 0 and id not in previously_uploaded_file_ids]
        if len(removed_file_ids) > 0:
            Files(g.db).update_multiple_files(removed_file_ids, sustainability_response_id=None)
        if len(newly_uploaded_file_ids) > 0:
            Files(g.db).update_multiple_files(newly_uploaded_file_ids, sustainability_response_id=request.json["sustainability_response_id"])
    else:
        sustainability_response_id = SustainabilityResponses(g.db).insert_sustainabilty_response(
            account_id=g.account.id(),
            user_id=g.user.id(),
            air_points=round(request.json["scores"]["air"], 1),
            land_points=round(request.json["scores"]["land"], 1),
            water_points=round(request.json["scores"]["water"], 1),
            animal_points=round(request.json["scores"]["animal"], 1),
            safety_points=round(request.json["scores"]["safety"], 1),
            efficiency_points=round(request.json["scores"]["efficiency"], 1),
            improvement_points=round(request.json["scores"]["improvement"], 1),
            score=request.json["total_score"],
            response=request.json["responses"],
            sector_id=g.account.sector_id(),
            questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Pending"] if request.json["is_partial_response"] else QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Completed"]
        )
        uploaded_file_ids = [file_id for file_id in request.json["uploaded_file_ids"] if file_id != 0]
        if len(uploaded_file_ids) > 0:
            Files(g.db).update_multiple_files(uploaded_file_ids, sustainability_response_id=sustainability_response_id)
    return {"redirect": "/dashboard/sustainability"}


@bp.route('/widgets/data/get_account_sustainability_data', methods=["POST"])
@crut.require_user
def serve_get_sustainability_response_averages():
    if request.json.get("scores_only", None):
        account_id = request.json["account_id"]
        scores_only = True
    else:
        account_id = g.account.id()
        scores_only = False
    account_sustainability_responses = SustainabilityResponses(g.db).get_sustainability_responses(account_id=account_id, questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Completed"])
    # default all 0s
    account_sustainability_section_and_scores = {
        "air_score": 0,
        "land_score": 0,
        "water_score": 0,
        "animal_score": 0,
        "safety_score": 0,
        "efficiency_score": 0,
        "improvement_score": 0,
        "total_score": 0
    }
    if len(account_sustainability_responses) > 0:
        latest_account_sustainability_response = account_sustainability_responses[0]
        account_sustainability_section_and_scores = {
            "air_score": latest_account_sustainability_response["air_points"] if latest_account_sustainability_response["air_points"] else 0,
            "land_score": latest_account_sustainability_response["land_points"] if latest_account_sustainability_response["land_points"] else 0,
            "water_score": latest_account_sustainability_response["water_points"] if latest_account_sustainability_response["water_points"] else 0,
            "animal_score": latest_account_sustainability_response["animal_points"] if latest_account_sustainability_response["animal_points"] else 0,
            "safety_score": latest_account_sustainability_response["safety_points"] if latest_account_sustainability_response["safety_points"] else 0,
            "efficiency_score": latest_account_sustainability_response["efficiency_points"] if latest_account_sustainability_response["efficiency_points"] else 0,
            "improvement_score": latest_account_sustainability_response["improvement_points"] if latest_account_sustainability_response["improvement_points"] else 0,
            "total_score": latest_account_sustainability_response["score"] if latest_account_sustainability_response["score"] else 0
        }
    if scores_only:
        account_data = g.db.accounts.get_accounts(id=account_id)
        account_sector = account_data[0]["sector"] if len(account_data) > 0 else SECTORS_NAME_TO_ID["Cow-Calf"]
        return {"account_sector_id": account_sector, "account_sustainability_section_and_scores": account_sustainability_section_and_scores}
    account_sustainability_responses = SustainabilityResponses(g.db).get_sustainability_responses(account_id=account_id, questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Completed"])
    return {"account_sustainability_responses": account_sustainability_responses, "account_sustainability_section_and_scores": account_sustainability_section_and_scores}


@bp.route('/widgets/data/get_sustainability_response_timeline_data', methods=['POST'])
@crut.require_account
def serve_get_sustainability_response_timeline_data():
    account_link = g.db.account_links.get_by_account_id(g.account.id())
    if account_link is None:
        return {"Account link not available"}, 400
    else:
        matched_accounts = Matches(g.db).get_sighted_match_accounts_for_account_link(account_link[0].id())
        for account_data in matched_accounts:
            account_sustainability_score = 0
            account_sustainability_responses = SustainabilityResponses(g.db).get_sustainability_responses(account_id=account_data["account_id"], questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Completed"])
            if len(account_sustainability_responses) > 0:
                latest_sustainability_response = account_sustainability_responses[0]
                account_sustainability_score = latest_sustainability_response["score"]
            account_data["account_sustainability_score"] = account_sustainability_score

        return {'timeline_data': matched_accounts}, 200


@bp.route('/widgets/data/save_account_retail_data', methods=["POST"])
@crut.require_account
def serve_save_account_retail_data():
    g.db.accounts.update_account(account_id=g.account.id(), retail_name=request.json["retail_name"], retail_description=request.json["retail_description"])
    previous_uploaded_retail_image_files = Files(g.db).get_files(retail_page_account_id=g.account.id())
    previous_uploaded_retail_image_ids = [image["id"] for image in previous_uploaded_retail_image_files]
    removed_image_ids = [id for id in previous_uploaded_retail_image_ids if id not in request.json["uploaded_images"]]
    newly_uploaded_image_ids = [id for id in request.json["uploaded_images"] if id not in previous_uploaded_retail_image_ids]
    if len(removed_image_ids) > 0:
        Files(g.db).update_multiple_files(removed_image_ids, None)
    if len(newly_uploaded_image_ids) > 0:
        Files(g.db).update_multiple_files(newly_uploaded_image_ids, g.account.id())
    return {"redirect": "/dashboard"}


@bp.route('/widgets/data/get_existing_sustainability_response', methods=["POST"])
@crut.require_account
def serve_get_existing_sustainability_responses():
    pending_questionnaires = SustainabilityResponses(g.db).get_sustainability_responses(
        account_id=g.account.id(),
        user_id=g.user.id(),
        questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Pending"]
    )
    sustainability_response_id = None
    sustainability_responses = None
    sustainability_response_uploaded_files = None
    if len(pending_questionnaires) > 0:
        sustainability_response_id = pending_questionnaires[0]["id"]
        sustainability_responses = pending_questionnaires[0]["response"]
        sustainability_response_uploaded_files = Files(g.db).get_files(sustainability_response_id=pending_questionnaires[0]["id"])
    return {
        "sustainability_response_id": sustainability_response_id,
        "sustainability_responses": sustainability_responses,
        "sustainability_response_uploaded_files": sustainability_response_uploaded_files
    }


@bp.route('/widgets/data/get_advertisement_companies_and_categories', methods=["POST"])
@crut.require_employee
def serve_get_advertising_companies():
    advertisement_companies = AdvertisementCompanies(g.db).get()
    return {
        "advertisement_companies": advertisement_companies,
        "advertisement_category_ids_to_names": ADVERTISEMENT_CATEGORY_IDS_TO_NAMES
    }


@bp.route('/widgets/data/get_advertisements', methods=["POST"])
@crut.require_account
def serve_get_advertisements():
    advertisements = Advertisements(g.db).get(is_archived=0, get_related_advertising_company=True, include_logo_images=True)
    return {
        "advertisements": advertisements,
        "advertisement_category_ids_to_names": ADVERTISEMENT_CATEGORY_IDS_TO_NAMES
    }


@bp.route('/widgets/data/get_count_distribution_for_account', methods=["POST"])
@crut.require_account
def serve_get_count_distribution_for_account():
    count_distribution_data = Reports(g.db).get_ready_by_query(count_distribution.create(
        request.json["account_id"],
        "USDA Quality Grade",
        0
    ))
    if count_distribution_data is not None:
        return count_distribution_data
    return {}


@bp.route('/widgets/data/get_yield_and_quality_grades_for_owned_eids', methods=["POST"])
@crut.require_user
def serve_get_all_matches_for_an_account():
    eids_carcass_data = {}
    account_links = AccountLinks(g.db).get_account_links(account_id=g.account.id())
    for account_link in account_links:
        account_matches = Matches(g.db).get_matches(account_link=account_link["id"])
        for account_match in account_matches:
            if account_match["type"] == MATCH_TYPES_NAME_TO_ID["USDA Quality Grade"]:
                if account_match["eid"] in eids_carcass_data:
                    eids_carcass_data[account_match["eid"]]["quality_grade"] = account_match["data"]
                else:
                    eids_carcass_data[account_match["eid"]] = {"quality_grade": account_match["data"]}
            if account_match["type"] == MATCH_TYPES_NAME_TO_ID["USDA Yield Grade"]:
                if account_match["eid"] in eids_carcass_data:
                    eids_carcass_data[account_match["eid"]]["yield_grade"] = account_match["data"]
                else:
                    eids_carcass_data[account_match["eid"]] = {"yield_grade": account_match["data"]}
    return eids_carcass_data


@bp.route('/widgets/data/add_new_sales_group_field_value', methods=["POST"])
@crut.require_account
def serve_add_new_sales_group_field_value():
    try:
        if len(request.form["new_field_value"].strip()) == 0:
            raise ExportException("Field cannot be blank")
        SalesGroupFieldsValues(g.db).insert(
            field_id=SALES_GROUP_FIELD_NAMES_TO_IDS[request.form["field_name"]],
            value=format_field(request.form["new_field_value"].strip())
        )
        return {"new_field_value": format_field(request.form["new_field_value"].strip())}
    except ExportException as e:
        return {"error": str(e)}
    except Exception as e:
        raise e


@bp.route('/widgets/not-interested-in-sales-group', methods=["POST"])
@crut.require_account
def serve_not_interested_in_sales_group():
    NotInterestedSalesGroupIdsForAccounts(g.db).insert(
        account_id=g.account.id(),
        sales_group_id=request.json["sales_group_id"]
    )
    return Response(status=HTTP_NO_CONTENT)


@bp.route('/widgets/add-new-sales-group-field-values', methods=["POST"])
@crut.require_employee
def serve_add_new_sales_group_field_values():
    for new_field_value in request.json["new_field_values"]:
        SalesGroupFieldsValues(g.db).insert(field_id=request.json["field_id"], value=new_field_value)
    return Response(status=HTTP_NO_CONTENT)


@bp.route('/widgets/remove-sales-group-field-values', methods=["POST"])
@crut.require_employee
def serve_remove_sales_group_field_values():
    for sales_group_field_value_id in request.json["sales_group_field_value_ids"]:
        SalesGroupFieldsValues(g.db).update(id=sales_group_field_value_id, is_archived=1)
    return Response(status=HTTP_NO_CONTENT)