from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, render_template
)

from ..sectors import sectors_by_name, sectors_by_id
from ..match_types import match_types_by_name, match_types_by_id

from ..common_exceptions import ExportException

from ..database.tables.account_users import NoAccountUserFound
from ..database.tables.accounts import AccountsException
from ..database.objects.account import AccountException

from ..database.const.spatial_math import meters_to_miles, distance
from ..database.const.zip_codes_data import ZIP_CODES

from ..renderers.email import render_email
from ..utilities.email import send_email

from ..config import ROOT as WEBSITE_ROOT

bp = Blueprint('widgets_bp', __name__)

@bp.route('/widgets/data', methods=['POST'])
def serve_data():
    """Serves data.

    Post:
        JSON data.
        action: What data to get
        params: Configuration of the data to get

    Actions & params:
        matches
            account: Account ID to get matches for
            types: Optional list of types to get (by string)
    """
    # TODO: How to handle not signed in?
    data = request.json

    if data == None:
        return "Missing JSON (application/json not specified perhaps)", 400
    
    if 'action' not in data:
        return "Missing action", 400
    
    if 'params' not in data:
        return "Missing params", 400

    # Serve actions

    action = data['action']
    params = data['params']

    direct_export = {
        "match_types_by_id": match_types_by_id,
        "match_types_by_name": match_types_by_name,
        "sectors_by_id": sectors_by_id,
        "sectors_by_name": sectors_by_name
    }

    try:

        if action == "matches":
            restrict_types = []
            if 'types' in params:
                restrict_types = [match_types_by_name[n] for n in params['types']]
            ljoin_account_links = False
            if "ljoin_account_links" in params:
                ljoin_account_links = params["ljoin_account_links"]
            ljoin_data_str = False
            if "ljoin_data_str" in params:
                ljoin_data_str = params["ljoin_data_str"]
            
            if 'account' in params:
                account_user = g.db.account_users.get_by_user_and_account_id(g.user, params['account'])
                account = account_user.account()
                account_links = account.account_links()
                matches = g.db.matches.get_by_account_links_spread(account_links, restrict_types=restrict_types, ljoin_account_links=ljoin_account_links)
                
            else:
                matches = g.db.matches.get_by_eid(params["animal"], restrict_types=restrict_types, ljoin_account_links=ljoin_account_links, ljoin_data_str=ljoin_data_str)

            if len(matches) > 2000:
                # TODO: Remove
                #raise ValueError("Remove me later")
                pass
            return jsonify({
                "match_rows": [match.row() for match in matches]
            })
        elif action in direct_export:
            return jsonify({
                action: direct_export[action]
            })
        elif action == "get_count_eid_distinct":
            return jsonify({
                "count_eid_distinct": g.db.matches.get_count_eid_distinct()
            })
        elif action == "sales_group":
            sales_group_row = g.db.sales_groups.row_by_id(params["sales_group"])
            if not (sales_group_row["published"] > 0 or sales_group_row["account"] == g.account.id()):
                raise ExportException("Insufficient Permissions")
            eids = [row["eid"] for row in g.db.sales_group_eids.rows_by_sales_group(sales_group_row["id"])]
            return jsonify({
                "id": sales_group_row["id"],
                "reported": sales_group_row["reported"],
                "published": sales_group_row["published"],
                "account": sales_group_row["account"],
                "account_name": sales_group_row["account_name"],
                "eids": eids,
                "file_auths": g.db.files.get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None),
                "zip": sales_group_row["zip"],
                "start": sales_group_row["start"],
                "end": sales_group_row["end"]
            })
        elif action == "search_sales_groups":
            sales_group_rows = []

            # TODO: Optimize and fix
            sales_group_rows = g.db.sales_groups.rows_by_account(params["search"]["params"]["ID"])

            results = []

            for sales_group_row in sales_group_rows:
                eids = [row["eid"] for row in g.db.sales_group_eids.rows_by_sales_group(sales_group_row["id"])]
                if sales_group_row["account"] == g.account.id():
                    results.append({
                        "id": sales_group_row["id"],
                        "reported": sales_group_row["reported"],
                        "published": sales_group_row["published"],
                        "account": sales_group_row["account"],
                        "account_name": sales_group_row["account_name"],
                        "eids": eids,
                        "file_auths": g.db.files.get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None) if params["file_auths"] else [],
                        "zip": sales_group_row["zip"],
                        "start": sales_group_row["start"],
                        "end": sales_group_row["end"]
                    })

            return jsonify({
                "sales_groups": results
            })
        elif action == "search_sales_groups_2":
            sales_group_rows = []

            sales_group_rows = g.db.sales_groups.search_within(
                zip_code=params["search"]["zip"],
                miles=params["search"]["radius"],
                start=0,
                end=9999999999,
                breed=params["search"]["breed"],
                minimum_weight=params["search"]["minimum_weight"],
                preconditioning_program=params["search"]["preconditioning_program"],
                process_verified_program=params["search"]["process_verified_program"],
            )

            results = []

            for sales_group_row in sales_group_rows:
                eids = [row["eid"] for row in g.db.sales_group_eids.rows_by_sales_group(sales_group_row["id"])]
                results.append({
                    "id": sales_group_row["id"],
                    "reported": sales_group_row["reported"],
                    "published": sales_group_row["published"],
                    "account": sales_group_row["account"],
                    "account_name": sales_group_row["account_name"],
                    "eids": eids,
                    "file_auths": g.db.files.get_auths(sales_group_row["reported"]["images"] if "images" in sales_group_row["reported"] else None),
                    "zip": sales_group_row["zip"],
                    "start": sales_group_row["start"],
                    "end": sales_group_row["end"],
                    "context": {
                        "milesAway": meters_to_miles(distance(ZIP_CODES[params["search"]["zip"]]["ecef"], ZIP_CODES[sales_group_row["zip"]]["ecef"]))
                    }
                })

            return jsonify({
                "sales_groups": results
            })
        elif action == "get_count_distribution":
            join_str = False
            account_links = None
            if "type" not in params:
                return "Missing params.type", 400
            if 'join_str' in params:
                join_str = params['join_str']
            if 'account' in params:
                account_user = g.db.account_users.get_by_user_and_account_id(g.user, params['account'])
                account = account_user.account()
                account_links = account.account_links()
                if len(account_links) == 0:
                    return jsonify({"count_distribution":[]})
                    
            return jsonify({
                "count_distribution": g.db.matches.get_count_distribution(match_types_by_name[params["type"]], account_links=account_links, join_str=join_str)
            })
        elif action == "save_sales_group":
            # Check that the account selected is the owner of the sales group
            original_row = g.db.sales_groups.row_by_id(params["id"])
            if original_row["account"] != g.account.id():
                raise ExportException("Insufficient permissions to edit this sales group.")

            # Verify that the images provided are allowed
            if 'images' in params["reported"]:
                for image in params["reported"]["images"]:
                    if not g.db.files.is_owner(None, g.account.id(), image):
                        raise ExportException("Image " + str(image) + " is not owned by the selected account.")

            if params["zip"] not in ZIP_CODES:
                raise ExportException("Sorry, that zip code could not be found.")
        
            if params["start"] is None or params["end"] is None:
                raise ExportException("Sorry, start or end date missing.")
        
            if params["start"] > params["end"]:
                raise ExportException("Sorry, check the market start and end dates (specifically the order).")

            # Alright, go ahead...

            g.db.sales_group_eids.delete_sales_group(params["id"])
            g.db.sales_group_eids.insert_multiple(params["eids"], params["id"])
            
            g.db.sales_groups.update(
                params["id"],
                params["reported"],
                params["published"],
                params["zip"],
                params["start"],
                params["end"]
            )

            return jsonify({
                "redirect": "/dashboard/sales-groups/view/" + str(params["id"])
            })
        elif action == "get_upload_config":
            user_owns = params["user_owns"] == True
            account_owns = params["account_owns"] == True
            if not user_owns and not account_owns:
                raise ExportException("Someone must own the file.")

            file_id, file_config = g.db.files.get_post(params["file_name"], g.user.id() if user_owns else None, g.account.id() if account_owns else None)

            return jsonify({
                "id": file_id,
                "config": file_config
            })
        elif action == "get_account_messages":
            return jsonify({
                "messages": g.db.messages.get(g.account.id(), g.account.id())
            })
        elif action == "send_message":
            message_id = g.db.messages.insert_message(
                g.account.id(),
                params["to_account"],
                params["data"]
            )
            send_to_users = g.db.users.get_rows_by_account(params["to_account"])
            for user in send_to_users:
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
            return jsonify({}), 200
        else:
            return "Unknown action " + action, 400
    except ExportException as e:
        return jsonify({"error":str(e)}), 500
