from flask import g
from ....match_types import name_to_id
from ...security.matches_visibility import apply_visibility


def unauth(params):
    result = auth(params)
    # visible_matches, blocked_matches = apply_visibility(result['matches'], [g.account.id()])   
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
    account = g.db.accounts.get_by_id(g.account.id())
    account_link_id = 0
    if len(account.account_links()) > 0:
        account_link_id = account.account_links()[0].id()
    if 'animals_with_data' in params:
        return {
            "matches": g.db.matches.get_animals_with_data_for_account(account_link_id)
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
