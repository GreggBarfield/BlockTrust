from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect, render_template
)

from sectors import sectors_by_name, sectors_by_id
from match_types import match_types_by_name, match_types_by_id

from common_exceptions import ExportException

from database.tables.account_users import NoAccountUserFound
from database.tables.accounts import AccountsException
from database.objects.account import AccountException

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
        eids = [row["eid"] for row in g.db.sales_group_eids.rows_by_sales_group(sales_group_row["id"])]
        return jsonify({
            "reported": sales_group_row["reported"],
            "published": sales_group_row["published"],
            "eids": eids
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

        g.db.sales_group_eids.delete_sales_group(params["id"])
        g.db.sales_group_eids.insert_multiple(params["eids"], params["id"])
        
        g.db.sales_groups.update(
            params["id"],
            params["reported"],
            params["published"]
        )

        return jsonify({
            "redirect": "/dashboard/sales-groups/view/" + str(params["id"])
        })
    else:
        return "Unknown action " + action, 400

