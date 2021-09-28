from flask import g
from ....match_types import name_to_id
from ...security.matches_visibility import apply_visibility


def unauth(params):
    result = auth(params)
    #visible_matches, blocked_matches = apply_visibility(result['matches'], [g.account.id()])
    return {
        'matches': result['matches'] #visible_matches
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

    # account_user = g.db.account_users.get_by_user_and_account_id(
    #     g.user,
    #     g.account.id()
    # )
    account = g.db.accounts.get_by_id(g.account.id())  # account_user.account()
    account_links = account.account_links()

    # return {
    #     "matches": g.db.matches.get_by_account_links_spread(
    #         account_links,
    #         restrict_types=restrict_types,
    #         ljoin_account_links=ljoin_account_links
    #     )
    # }

    return {
        "matches": g.db.matches.get_all_matches_for_an_account(
            account_links,
            restrict_types=restrict_types,
            ljoin_account_links=ljoin_account_links,
            match_cols=["lat", "lon", "time", "eid"]
        )
    }
