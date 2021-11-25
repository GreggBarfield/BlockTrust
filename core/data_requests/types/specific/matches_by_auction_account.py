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
    ljoin_account_links = False
    if "ljoin_account_links" in params:
        ljoin_account_links = params["ljoin_account_links"]

    restrict_types = ()
    if 'types' in params:
        restrict_types = name_to_id(params['types'])

    return {
        "matches": g.db.matches.get_by_auction_sale_account(
            g.account.id(),
            restrict_types=restrict_types,
            ljoin_account_links=ljoin_account_links
        )
    }
