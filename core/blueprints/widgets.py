import json
from flask import (
    Flask, request, session, Blueprint, g, redirect, render_template, url_for
)

from ..sectors import sectors_by_name, sectors_by_id
from ..match_types import match_types_by_name, match_types_by_id

from ..common_exceptions import ExportException

from ..database.tables.account_users import NoAccountUserFound
from ..database.tables.accounts import AccountsException, Accounts, HEALTH_TRACK_PARTNER_COMPANY
from ..database.objects.account import AccountException
from ..database.tables.sales_group_animals import SalesGroupAnimals
from ..database.tables.auction_markets import AuctionMarkets
from ..database.tables.connections import Connections, connection_status_name_to_id, CONNECTION_TYPE_NAME_TO_ID
from ..database.tables.connection_invites import ConnectionInvites
from ..database.tables.account_users import AccountUsers
from ..database.tables.sustainability_responses import SustainabilityResponses
from ..database.tables.users import Users

from ..database.tables import zip_codes
from ..database.tables.usda_favorites_for_accounts import USDAFavoritesForAccounts
from ..database.tables.sales_groups import SalesGroups

from ..database.const.spatial_math import meters_to_miles, distance
from ..database.const.zip_codes_data import ZIP_CODES

from ..reports.query_types import count_eid_distinct

from ..renderers.email import render_email
from ..utilities.email import send_email
from ..utilities.general_utilities import format_field

from ..config import ROOT as WEBSITE_ROOT

from ..utilities import crut

from ..data_requests.router import unauth_route

import time

bp = Blueprint('widgets_bp', __name__)


@bp.route('/widgets/data/direct/<name>', methods=['POST'])
@crut.require_account_or_employee
def serve_direct(name):
    direct_export = {
        "match_types_by_id": match_types_by_id,
        "match_types_by_name": match_types_by_name,
        "sectors_by_id": sectors_by_id,
        "sectors_by_name": sectors_by_name
    }

    if name in direct_export:
        return {
            name: direct_export[name]
        }
    raise ExportException("Unable to directly export the requested value")


@bp.route('/widgets/data/sales_group', methods=['POST'])
@crut.require_account
def serve_sales_group():
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(request.json["sales_group"])
    if not (sales_group_row["published"] > 0 or sales_group_row["account"] == g.account.id()):
        raise ExportException("Insufficient Permissions")
    return {
        "id": sales_group_row["id"],
        "reported": sales_group_row["reported"],
        "published": sales_group_row["published"],
        "account": sales_group_row["account"],
        "account_name": sales_group_row["account_name"],
        "is_account_charges_enabled": sales_group_row["is_account_charges_enabled"],
        "eids": list(map(lambda item: item['eid'], SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_row["id"]))),
        "file_auths": g.db.files.get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None),
        "zip": sales_group_row["zip"],
        "market_location": sales_group_row["market_location"],
        "delivery_location_type": sales_group_row["delivery_location_type"],
        "delivery_location": sales_group_row["delivery_location"],
        "start": sales_group_row["start"],
        "end": sales_group_row["end"],
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
        "are_annual_cattle_herd_vaccinations_given": sales_group_row["are_annual_cattle_herd_vaccinations_given"]
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
    sales_group_rows = g.db.sales_groups.get_sales_groups_and_data(account_id=request.json["search"]["params"]["ID"], is_archived=0)

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
                "file_auths": g.db.files.get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None) if request.json["file_auths"] else [],
                "zip": sales_group_row["zip"],
                "market_location": sales_group_row["market_location"],
                "delivery_location": sales_group_row["delivery_location"],
                "start": sales_group_row["start"],
                "end": sales_group_row["end"],
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

    sales_group_rows = g.db.sales_groups.search_within(
        zip_code=request.json["search"]["zip"],
        miles=request.json["search"]["radius"],
        start=time.time(),
        end=9999999999,
        is_archived=0,
        category=request.json["search"]["category"],
        breed=request.json["search"]["breed"],
        minimum_weight=request.json["search"]["minimum_weight"],
        preconditioning_program=request.json["search"]["preconditioning_program"],
        process_verified_program=request.json["search"]["process_verified_program"],
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
            "file_auths": g.db.files.get_auths(
                sales_group_row["reported"]["images"]
                if "images" in sales_group_row["reported"]
                else None
            ),
            "zip": sales_group_row["zip"],
            "market_location": sales_group_row["market_location"],
            "delivery_location":sales_group_row["delivery_location"],
            "start": sales_group_row["start"],
            "end": sales_group_row["end"],
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
            "is_account_charges_enabled": sales_group_row["is_account_charges_enabled"],
            "category": sales_group_row["category"],
            "breed_comments": sales_group_row["breed_comments"],
            "weighing_conditions": sales_group_row["weighing_conditions"],
            "are_annual_cattle_herd_vaccinations_given": sales_group_row["are_annual_cattle_herd_vaccinations_given"],
            "owner_account_sustainability_score_average": owner_account_sustainability_score_average
        })

    return {
        "sales_groups": results
    }


@bp.route('/widgets/data/search_by_eid_and_visual_id_for_account', methods=['POST'])
@crut.require_account
def serve_search_by_eid_and_visual_id():
    eid_number = int(request.json["search"]["eid"])
    rows = g.db.matches.get_matches_by_eid_or_visual_id(eid_or_visual_id=eid_number, account_id=g.account.id())
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
    g.db.sales_groups.validate_or_fail_sales_group(
        account_id=g.account.id(),
        group_name=request.json["group_name"],
        zip=request.json["zip"],
        delivery_location_type=request.json["delivery_location_type"],
        count=request.json["reported"]["count"],
        weight=request.json["reported"]["weight"],
        weight_variance=request.json["reported"]["weight_variance"],
        category=request.json["category"],
        breeds=request.json["reported"]["breeds"],
        start=request.json["start"],
        end=request.json["end"],
        auction_sale=request.json["auction_sale"],
        delivery_location=request.json["delivery_location"],
        auction_market_location=request.json["auction_market_location"],
        images=images,
        price=request.json["price"]
        )
    # Alright, go ahead...
    delivery_location = ""
    if request.json["delivery_location_type"] == "Off Ranch":
        delivery_location = request.json["delivery_location"]
    else:
        delivery_location = request.json["auction_market_location"]
    sales_group_id = g.db.sales_groups.insert_new_sales_group(
        account=g.account.id(),
        reported=request.json["reported"],
        published=request.json["published"],
        zip_code=request.json["zip"],
        delivery_location=delivery_location,
        start=request.json["start"],
        end=request.json["end"],
        auction_sale=request.json["auction_sale"],
        group_name=request.json["group_name"],
        is_archived=0,
        delivery_location_type=request.json["delivery_location_type"],
        price=request.json["price"],
        category=request.json["category"],
        breed_comments=request.json["breed_comments"],
        weighing_conditions=request.json["weighing_conditions"],
        are_annual_cattle_herd_vaccinations_given=request.json["are_annual_cattle_herd_vaccinations_given"]
    )
    return {"redirect": "/dashboard/sales-groups/view/" + str(sales_group_id)}


@bp.route('/widgets/data/update_sales_group', methods=['POST'])
@crut.require_account
def serve_update_sales_group():
    # Check that the account selected is the owner of the sales group
    original_row = g.db.sales_groups.get_sales_group_by_id(request.json["id"])
    if original_row["account"] != g.account.id():
        raise ExportException("Insufficient permissions to edit this sales group.")
    # Validate sales group fields
    images = []
    if 'images' in request.json["reported"]:
        images = request.json["reported"]["images"]
    g.db.sales_groups.validate_or_fail_sales_group(
        account_id=g.account.id(),
        group_name=request.json["group_name"],
        zip=request.json["zip"],
        delivery_location_type=request.json["delivery_location_type"],
        count=request.json["reported"]["count"],
        weight=request.json["reported"]["weight"],
        weight_variance=request.json["reported"]["weight_variance"],
        category=request.json["category"],
        breeds=request.json["reported"]["breeds"],
        start=request.json["start"],
        end=request.json["end"],
        auction_sale=request.json["auction_sale"],
        delivery_location=request.json["delivery_location"],
        auction_market_location=request.json["auction_market_location"],
        images=images,
        price=request.json["price"]
        )
    delivery_location = ""
    if request.json["delivery_location_type"] == "Off Ranch":
        delivery_location = request.json["delivery_location"]
    else:
        delivery_location = request.json["auction_market_location"]
    g.db.sales_groups.update_sales_group(
        id=request.json["id"],
        reported=request.json["reported"],
        published=request.json["published"],
        zip_code=request.json["zip"],
        delivery_location=delivery_location,
        start=request.json["start"],
        end=request.json["end"],
        auction_sale=request.json["auction_sale"],
        group_name=request.json["group_name"],
        is_archived=0,
        delivery_location_type=request.json["delivery_location_type"],
        price=request.json["price"],
        category=request.json["category"],
        breed_comments=request.json["breed_comments"],
        weighing_conditions=request.json["weighing_conditions"],
        are_annual_cattle_herd_vaccinations_given=request.json["are_annual_cattle_herd_vaccinations_given"]
    )

    return {
        "redirect": "/dashboard/sales-groups/view/" + str(request.json["id"])
    }


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
    sales_group_rows = g.db.sales_groups.get_sales_groups_and_data(account_id=request.json["search"]["params"]["ID"], is_archived=1)

    results = []

    for sales_group_row in sales_group_rows:
        results.append({
            "id": sales_group_row["id"],
            "reported": sales_group_row["reported"],
            "published": sales_group_row["published"],
            "account": sales_group_row["account"],
            "account_name": sales_group_row["account_name"],
            "eids": list(map(lambda item: item['eid'], SalesGroupAnimals(g.db).get_sales_group_animals(sales_group_id=sales_group_row["id"]))),
            "file_auths": g.db.files.get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None),
            "zip": sales_group_row["zip"],
            "market_location": sales_group_row["market_location"],
            "delivery_location": sales_group_row["delivery_location"],
            "start": sales_group_row["start"],
            "end": sales_group_row["end"],
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
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(request.json["sales_group"])
    if not (sales_group_row["published"] > 0 or sales_group_row["account"] == g.account.id()):
        raise ExportException("Insufficient Permissions")
    # Getting eids owned by the account
    distinct_eids = g.db.matches.get_distinct_eids_and_visual_ids_by_account(account_id=g.account.id(), number_of_years=1)
    # Getting sales groups owned by account and corresponding eid's
    account_sales_groups_ids = list(map(lambda item: item['id'], g.db.sales_groups.get_sales_groups_and_data(account_id=g.account.id())))
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
    original_row = g.db.sales_groups.get_sales_group_by_id(request.json["id"])
    SalesGroupAnimals(g.db).delete_sales_group_eids(sales_group_id=original_row["id"])
    SalesGroupAnimals(g.db).insert_sales_group_eids(sales_group_id=original_row["id"], eids_and_visual_ids=request.json["eids_and_visual_ids"])
    return {"redirect": "/dashboard/sales-groups/manage"}


@bp.route('/widgets/data/get_upload_config', methods=['POST'])
@crut.require_account
def serve_get_upload_config():
    user_owns = request.json["user_owns"] is True
    account_owns = request.json["account_owns"] is True
    if not user_owns and not account_owns:
        raise ExportException("Someone must own the file.")

    file_id, file_config = g.db.files.get_post(
        request.json["file_name"],
        g.user.id() if user_owns else None,
        g.account.id() if account_owns else None
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
        "messages": g.db.messages.get(g.account.id(), g.account.id())
    }


@bp.route('/widgets/data/send_message', methods=['POST'])
@crut.require_account
def serve_send_message():
    message_id = g.db.messages.insert_message(
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


@bp.route('/widgets/data/get_auction_sales', methods=['POST'])
@crut.require_account
def serve_get_auction_sales():
    return {
        "auction_sales": g.db.auction_sales.get_auction_sales_by_account(g.account.id())
    }


@bp.route('/widgets/data/search_auction_sales', methods=['POST'])
@crut.require_account
def serve_search_auction_sales():
    return {
        "auction_sales": g.db.auction_sales.search_auction_sales(request.json["term"])
    }


@bp.route('/widgets/data/new_auction_sale', methods=['POST'])
@crut.require_account
def serve_new_auction_sale():
    g.db.auction_sales.new_auction_sale(
        name=request.json["name"],
        at=request.json["at"],
        account_id=g.account.id(),
        comments=request.json["comments"],
        published=request.json["published"]
    )
    return {}, 200


@bp.route('/widgets/data/update_auction_sale', methods=['POST'])
@crut.require_account
def serve_update_auction_sale():
    if g.db.auction_sales.get_auction_sale_by_id(request.json["id"])["account"] == g.account.id():
        g.db.auction_sales.update_auction_sale(
            name=request.json["name"],
            at=request.json["at"],
            auction_sale_id=request.json["id"],
            comments=request.json["comments"],
            published=request.json["published"]
        )
        return {}, 200
    else:
        return {
            "Account does not match"
        }, 400


@bp.route('/widgets/data/data_request', methods=['POST'])
@crut.require_account_or_employee
def serve_data_request():
    return unauth_route(request.json['request']), 200


@bp.route('/widgets/data/get_market_data/<slug_id>', methods=['POST'])
@crut.require_account
def serve_get_market_data(slug_id):
    return {
        'market_data': g.db.usda_reports.get_by_slug_id(slug_id)
    }, 200


@bp.route('/widgets/data/get_employee_summary_graphs_data', methods=['POST'])
@crut.require_employee
def get_employee_summary_graphs_data():
    ranches = g.db.accounts.get_accounts(sector=sectors_by_name["Cow-Calf"], accounts_order_by="created_timestamp")
    feedyards = g.db.accounts.get_accounts(sector=sectors_by_name["Feedlot"], accounts_order_by="created_timestamp")
    tags_count_list = g.db.reports.get_reports(query=count_eid_distinct.create(), selectColumns=["result", "created_timestamp"])
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
    AuctionMarkets(g.db).insert_auction_market(
        name=format_field(request.form["name"]),
        address=format_field(request.form["address"]),
        city=format_field(request.form["city"]),
        state=format_field(request.form["state"]),
        zip_code=format_field(request.form["zip"]),
        phone=format_field(request.form["phone"]),
        email=format_field(request.form["email"])
    )
    return {"redirect": request.form['requestRedirectTo']}

@bp.route('/widgets/data/add-connection-request', methods=["POST"])
@crut.require_account
def serve_add_connection_request():
    try:
        invited_accounts = request.json["invited_account_ids_list"]
        for invited_account in invited_accounts:
            Connections(g.db).create_or_fail_connection(g.account.id(), invited_account, connection_status_name_to_id["Pending"],
                                                        connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Created"])
            if len(admin_account_users:=AccountUsers(g.db).get_account_users(account=invited_account, is_admin=1)) > 0:
                if len(email_verified_admin_user:=Users(g.db).get_users(id=admin_account_users[0]["user"],is_email_verified=1)) > 0:
                    send_email(
                        "BlockTrust Network New Connection Request",
                        render_email("new_account_connection_request.html", {
                            'connection_receiving_user': email_verified_admin_user[0],
                            'requesting_account': g.account
                        }), email_verified_admin_user[0]["email"]
                    )
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
    rows = g.db.matches.get_matches_by_eid_or_visual_id(eid_or_visual_id=eid_number)
    redirect_route = url_for('employees_bp.serve_animal_eid')
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
    animals_and_grouping_ids = g.db.matches.get_matches_with_account_links(
        account_links_account_id=g.account.id(),
        matches_partner_account_id=g.account.partner_account_id(),
        is_distinct=True,
        matches_cols=("eid", "visual_id", "grouping_id")
    )
    # Getting sales groups owned by account and corresponding eid's
    account_sales_groups_ids = g.db.sales_groups.get_sales_groups(account_id=g.account.id(), sales_group_cols=["id"])
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
    file_ids_json = {"file_ids": []}
    for file_id in request.json["uploaded_document_ids"]:
        if file_id != 0:
            file_ids_json["file_ids"].append(file_id)
    SustainabilityResponses(g.db).insert_sustainabilty_response(
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
        uploaded_file_ids=file_ids_json,
        response=request.json["responses"],
        sector_id=g.account.sector_id()
    )
    return {"redirect": "/dashboard/sustainability"}

@bp.route('/widgets/data/get_account_sustainability_data', methods=["POST"])
@crut.require_account
def serve_get_sustainability_response_averages():
    account_sustainability_averages = SustainabilityResponses(g.db).get_sustainability_response_averages(account_id=g.account.id())
    account_sustainability_section_and_score_averages = {
        "air_average": float(account_sustainability_averages["air_average"]) if account_sustainability_averages["air_average"] else 0,
        "land_average": float(account_sustainability_averages["land_average"]) if account_sustainability_averages["land_average"] else 0,
        "water_average": float(account_sustainability_averages["water_average"]) if account_sustainability_averages["water_average"] else 0,
        "animal_average": float(account_sustainability_averages["animal_average"]) if account_sustainability_averages["animal_average"] else 0,
        "safety_average": float(account_sustainability_averages["safety_average"]) if account_sustainability_averages["safety_average"] else 0,
        "efficiency_average": float(account_sustainability_averages["efficiency_average"]) if account_sustainability_averages["efficiency_average"] else 0,
        "improvement_average": float(account_sustainability_averages["improvement_average"]) if account_sustainability_averages["improvement_average"] else 0,
        "score_average": float(account_sustainability_averages["score_average"]) if account_sustainability_averages["score_average"] else 0
    }
    account_sustainability_responses = SustainabilityResponses(g.db).get_sustainability_responses(account_id=g.account.id())
    return {"account_sustainability_section_and_score_averages": account_sustainability_section_and_score_averages, "account_sustainability_responses": account_sustainability_responses}


@bp.route('/widgets/data/get_sustainability_response_timeline_data', methods=['POST'])
@crut.require_account
def serve_get_sustainability_response_timeline_data():
    account_link = g.db.account_links.get_by_account_id(g.account.id())
    if account_link is None:
        return {"Account link not available"}, 400
    else:
        matched_accounts = g.db.matches.get_matched_accounts_for_account_link(account_link[0].id())
        for account_data in matched_accounts:
            sustainability_response_averages = SustainabilityResponses(g.db).get_sustainability_response_averages(account_id=account_data["account"])
            account_data["account_score_average"] = float(sustainability_response_averages["score_average"]) if sustainability_response_averages["score_average"] is not None else 0

        return {'timeline_data': matched_accounts}, 200
