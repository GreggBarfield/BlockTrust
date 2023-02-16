from flask import g
from ....match_types import convert_match_type_names_to_ids


def unauth(params):
    result = auth(params)
    return {
        'matches': result['matches']
    }


def auth(params):
    """Authenticated matches_by_account data request.

    Params:
        params:
            A dictionary of
                types: restrict types
                ljoin_account_links: Whether to LJOIN account links (boolean)
                    (results as account_links.column_name)
    """
    account_link_id = 0
    if "account_id" in params and params["account_id"]:
        account = g.db.accounts.get_accounts(id=params["account_id"])[0]
        account_link_id = g.db.account_links.get_account_links(account_id=account["id"])[0]["id"]
    else:
        account = g.db.accounts.get_account_by_id(g.account.id())
        if len(account.account_links()) > 0:
            account_link_id = account.account_links()[0].id()
    if 'sighted_animals' in params:
        return {
            "matches": g.db.matches.get_sightings_in_auction_house_feedlot_packer_stocker(account_link_id)
        }
    elif 'all_matches' in params:
        restrict_types = ()
        if 'types' in params:
            restrict_types = convert_match_type_names_to_ids(params['types'])
        return {
            "matches": g.db.matches.get_matches(account_link=account_link_id, restrict_type=restrict_types[0], selectColumns=["eid", "visual_id"])
        }
    else:
        restrict_types = ()
        if 'types' in params:
            restrict_types = convert_match_type_names_to_ids(params['types'])

        return {
            "matches": g.db.matches.get_distinct_match_locations_for_account(
                account_link_id,
                restrict_types
            )
        }
