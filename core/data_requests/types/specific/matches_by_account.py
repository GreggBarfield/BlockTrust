from flask import g
from ....match_types import name_to_id


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
    account = g.db.accounts.get_account_by_id(g.account.id())
    account_link_id = 0
    if len(account.account_links()) > 0:
        account_link_id = account.account_links()[0].id()
    if 'sighted_animals' in params:
        return {
            "matches": g.db.matches.get_sighted_matches_for_account(account_link_id)
        }
    elif 'all_matches' in params:
        restrict_types = ()
        if 'types' in params:
            restrict_types = name_to_id(params['types'])
        return {
            "matches": g.db.matches.get_matches(account_link=account_link_id, restrict_type = restrict_types[0], selectColumns=["eid", "visual_id"])
        }
    else:
        ljoin_account_links = False
        if "ljoin_account_links" in params:
            ljoin_account_links = params["ljoin_account_links"]

        restrict_types = ()
        if 'types' in params:
            restrict_types = name_to_id(params['types'])

        return {
            "matches": g.db.matches.get_distinct_match_locations_for_account(
                account_link_id,
                restrict_types
            )
        }
