import json
from flask import (
    Flask, request, session, Blueprint, g, redirect, render_template
)

from ..sectors import sectors_by_name, sectors_by_id
from ..match_types import match_types_by_name, match_types_by_id

from ..common_exceptions import ExportException

from ..database.tables.account_users import NoAccountUserFound
from ..database.tables.accounts import AccountsException
from ..database.objects.account import AccountException
from ..database.tables.sales_group_eids import SalesGroupEIDs
from ..database.tables import zip_codes
from ..database.tables.usda_favorites_for_accounts import USDAFavoritesForAccounts

from ..database.const.spatial_math import meters_to_miles, distance
from ..database.const.zip_codes_data import ZIP_CODES

from ..renderers.email import render_email
from ..utilities.email import send_email

from ..config import ROOT as WEBSITE_ROOT

from ..utilities import crut

from ..data_requests.router import unauth_route

from time import time

bp = Blueprint('widgets_bp', __name__)


@bp.route('/widgets/data/direct/<name>', methods=['POST'])
@crut.require_user
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
        "eids": list(map(lambda item: item['eid'], SalesGroupEIDs(g.db).get_sales_group_eids(sales_group_id=sales_group_row["id"]))),
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
        "companyId": g.account.id(),
        "company": g.account.name(),
        "is_archived":sales_group_row["is_archived"]
    }


@bp.route('/widgets/data/search_sales_groups', methods=['POST'])
@crut.require_account
def serve_search_sales_groups():
    sales_group_rows = []

    # TODO: Optimize and fix
    sales_group_rows = g.db.sales_groups.get_sales_groups(account_id=request.json["search"]["params"]["ID"])

    results = []

    for sales_group_row in sales_group_rows:
        if sales_group_row["account"] == g.account.id():
            results.append({
                "id": sales_group_row["id"],
                "reported": sales_group_row["reported"],
                "published": sales_group_row["published"],
                "account": sales_group_row["account"],
                "account_name": sales_group_row["account_name"],
                "eids": list(map(lambda item: item['eid'], SalesGroupEIDs(g.db).get_sales_group_eids(sales_group_id=sales_group_row["id"]))),
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
        start=0,
        end=9999999999,
        is_archived=0,
        breed=request.json["search"]["breed"],
        minimum_weight=request.json["search"]["minimum_weight"],
        preconditioning_program=request.json["search"]["preconditioning_program"],
        process_verified_program=request.json["search"]["process_verified_program"],
    )

    results = []

    for sales_group_row in sales_group_rows:
        results.append({
            "id": sales_group_row["id"],
            "reported": sales_group_row["reported"],
            "published": sales_group_row["published"],
            "account": sales_group_row["account"],
            "account_name": sales_group_row["account_name"],
            "eids": list(map(lambda item: item['eid'], SalesGroupEIDs(g.db).get_sales_group_eids(sales_group_id=sales_group_row["id"]))),
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
            "is_archived":sales_group_row["is_archived"]          
        })

    return {
        "sales_groups": results
    }


@bp.route('/widgets/data/search_by_eid_and_visual_id', methods=['POST'])
@crut.require_account
def serve_search_by_eid_and_visual_id():
    eid_number = int(request.json["search"]["eid"])
    rows = g.db.matches.get_matches_by_eid_or_visual_id(eid_number,g.account.id())
    if len(rows) > 0:
        return {
            "matches": rows
        }
    else:
        return {
                "matches": []
        }


@bp.route('/widgets/data/save_sales_group', methods=['POST'])
@crut.require_account
def serve_save_sales_group():
    # Check that the account selected is the owner of the sales group
    original_row = g.db.sales_groups.get_sales_group_by_id(request.json["id"])
    if original_row["account"] != g.account.id():
        raise ExportException("Insufficient permissions to edit this sales group.")
    # Verify that the images provided are allowed
    if 'images' in request.json["reported"]:
        for image in request.json["reported"]["images"]:
            if not g.db.files.is_owner(None, g.account.id(), image):
                raise ExportException("Image " + str(image) + " is not owned by the selected account.")
    # Checking if required values are present
    if request.json["zip"] is None:
        raise ExportException("Zip code does not have a value")
    if request.json["start"] is None:
        raise ExportException("Start date is not selected")
    if request.json["end"] is None:
        raise ExportException("End date is not selected")
    if len(request.json["delivery_location"].strip()) == 0:
        raise ExportException("Delivery Location does not have a value")
    if request.json["reported"]["count"] is None:
        raise ExportException("Total animals cannot be 0")
    if request.json["reported"]["weight"] is None:
        raise ExportException("Base weight does not have a value")
    if len(request.json["reported"]["weight_variance"].strip()) == 0:
        raise ExportException("Weight variance does not have a value")
    if len(request.json["reported"]["breeds"]) == 0:
        raise ExportException("Please select one or more breeds")
    if request.json["reported"]["usda_frame_size"] is None:
        raise ExportException("Please select frame size")
    if request.json["reported"]["muscling"] is None:
        raise ExportException("Please select relevant muscling")
    if request.json["reported"]["horns"] is None:
        raise ExportException("Please select horns or no horns")

    if request.json["zip"] not in ZIP_CODES:
        raise ExportException("Sorry, that zip code could not be found.")

    if request.json["start"] is None or request.json["end"] is None:
        raise ExportException("Sorry, start or end date missing.")

    if request.json["start"] > request.json["end"]:
        raise ExportException("Sorry, check the market start and end dates (specifically the order).")

    if (
        request.json["auction_sale"] is not None
        and original_row['auction_sale'] != request.json["auction_sale"]
    ):
        # it was changed to a non-None value, verify new is published
        if not g.db.auction_sales.get_auction_sale_by_id(request.json["auction_sale"])["published"]:
            raise ExportException("Auction sale specified is not published yet.")

    # Alright, go ahead...
    g.db.sales_groups.update_sales_group(
        request.json["id"],
        request.json["reported"],
        request.json["published"],
        request.json["zip"],
        request.json["delivery_location"],
        request.json["start"],
        request.json["end"],
        request.json["auction_sale"],
        request.json["group_name"],
        request.json["is_archived"]
    )

    return {
        "redirect": "/dashboard/sales-groups/view/" + str(request.json["id"])
    }

@bp.route('/widgets/data/unarchive_sales_group', methods=['POST'])
@crut.require_account
def unarchive_sales_group():
    original_row = g.db.sales_groups.get_sales_group_by_id(request.json["params"]["id"])
    g.db.sales_groups.update_sales_group(
        original_row["id"],
        original_row["reported"],
        original_row["published"],
        original_row["zip"],
        original_row["delivery_location"],
        original_row["start"],
        original_row["end"],
        original_row["auction_sale"],
        original_row["group_name"],
        0
    )
    return {}, 200


@bp.route('/widgets/data/archived_sales_group', methods=['POST'])
@crut.require_account
def serve_archived_sales_group():
    sales_group_rows = []
    sales_group_rows = g.db.sales_groups.get_sales_groups(account_id=request.json["search"]["params"]["ID"], is_archived=1)

    results = []

    for sales_group_row in sales_group_rows:
        results.append({
            "id": sales_group_row["id"],
            "reported": sales_group_row["reported"],
            "published": sales_group_row["published"],
            "account": sales_group_row["account"],
            "account_name": sales_group_row["account_name"],
            "eids": list(map(lambda item: item['eid'], SalesGroupEIDs(g.db).get_sales_group_eids(sales_group_id=sales_group_row["id"]))),
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
    sales_group_row = g.db.sales_groups.get_sales_group_by_id(request.json["sales_group"])
    if not (sales_group_row["published"] > 0 or sales_group_row["account"] == g.account.id()):
        raise ExportException("Insufficient Permissions")
    # Getting eids owned by the account
    distinct_eids = g.db.matches.get_distinct_eids_by_account(account_id=g.account.id(), number_of_years=1)
    # Getting sales groups owned by account and corresponding eid's
    account_sales_groups_ids = list(map(lambda item: item['id'], g.db.sales_groups.get_sales_groups(account_id=g.account.id())))
    assigned_eids_for_account = []
    for sales_group_id in account_sales_groups_ids:
        assigned_eids = list(map(lambda item: item['eid'], SalesGroupEIDs(g.db).get_sales_group_eids(sales_group_id=sales_group_id)))
        if len(assigned_eids) > 0:
            assigned_eids_for_account.extend(assigned_eids)
    available_eids = []
    for distinct_eid in distinct_eids:
        if distinct_eid["eid"] not in assigned_eids_for_account:
            available_eids.append(distinct_eid["eid"])
    return {
        "id": sales_group_row["id"],
        "assigned_eids": list(map(lambda item: item['eid'], SalesGroupEIDs(g.db).get_sales_group_eids(sales_group_id=sales_group_row["id"]))),
        "available_eids": available_eids
    }


@bp.route('/widgets/data/save_eids_for_sales_group', methods=['POST'])
@crut.require_account
def serve_save_eids_for_sales_group():
    original_row = g.db.sales_groups.get_sales_group_by_id(request.json["id"])
    SalesGroupEIDs(g.db).delete_sales_group_eids(sales_group_id=original_row["id"])
    SalesGroupEIDs(g.db).insert_sales_group_eids(sales_group_id=original_row["id"], eids=request.json["eids"])
    return {"redirect": "/dashboard/sales-groups/manage"}


@bp.route('/widgets/data/save_sustainability', methods=['POST'])
@crut.require_account
def serve_save_sustainability():
    g.db.sustainability.insert(
        g.account.id(),
        request.json["response"],
        request.json["sectorScoreCounter"]
    )
    return { "redirect": "/dashboard/sustainability"}


@bp.route('/widgets/data/get_sustainability', methods=['POST'])
@crut.require_account
def serve_get_sustainability():
    return { 
        "results": g.db.sustainability.get_sustainability_by_account(g.account.id())
    }, 200


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
@crut.require_account
def serve_data_request():
    return unauth_route(request.json['request']), 200


@bp.route('/widgets/data/get_market_data/<slug_id>', methods=['POST'])
@crut.require_account
def serve_get_market_data(slug_id):
    return {
        'market_data': g.db.usda_reports.get_all_by_slug_id(slug_id)
    }, 200


@bp.route('/widgets/data/get_sustainability_timeline_data', methods=['POST'])
@crut.require_account
def serve_get_sustainability_timeline_data():
    account_link = g.db.account_links.get_by_account_id(g.account.id())

    if account_link is None:
        return {
            "Account link not available"
        }, 400
    else:
        matched_accounts = g.db.matches.get_matched_accounts_for_account_and_type(
                account_link[0].id()
            )

        data = {}
        #ordering list is used to display the timeline data in the correct order
        ordering = []
        for account_data in matched_accounts:
            response = g.db.sustainability.get_sustainability_by_account(account_data['account'], True)
            if response == []:
                account = g.db.accounts.get_account_by_id(account_data['account'])
                response = {
                    'sector': account.sector_id(),
                    'name': account.name(),
                    'response': None
                }
            else:
                response = response[0]
            #below line appends/updates elements of response dictionary into account_data dictionary
            account_data.update(response)
            data[str(account_data['account'])] = account_data
            ordering.append(str(account_data['account']))

        return {
            'timeline_data': data,
            'order': ordering
        }, 200

@bp.route('/widgets/data/get_usda_favorites_for_account', methods=['POST'])
@crut.require_account
def serve_get_usda_favorites():
    return { 'favorites': USDAFavoritesForAccounts(g.db).get_by_account_with_names(g.account.id()) }

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
