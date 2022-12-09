from flask import g
from ....match_types import convert_match_type_names_to_ids


def unauth(params):
    result = auth(params)
    return {
        'matches': result['matches']
    }


def auth(params):
    """Authenticated matches_by_eids data request.

    Params:
        params:
            A dictionary of
                eids: A list of EIDs to retrieve
                types: Restrict types (optional list of strings)
                ljoin_account_links: Whether to LJOIN account links (optional boolean)
                    (results as account_links.column_name)
    """
    ljoin_account_links = False
    if "ljoin_account_links" in params:
        ljoin_account_links = params["ljoin_account_links"]

    restrict_types = ()
    if 'types' in params:
        restrict_types = convert_match_type_names_to_ids(params['types'])

    return {
        "matches": g.db.matches.get_by_eids(
            params["eids"],
            restrict_types=restrict_types,
            ljoin_account_links=ljoin_account_links
        )
    }
