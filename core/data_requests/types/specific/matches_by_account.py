from flask import g
from core.database.tables.connections import Connections

from core.sectors import SECTORS_NAME_TO_ID
from ....match_types import MATCH_TYPES_NAME_TO_ID, convert_match_type_names_to_ids
from ....common_exceptions import ExportException


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
    if params.get("account_id", 0):
        if g.account.is_partner():
            account = g.db.accounts.get_accounts(id=params["account_id"])[0]
            if account["partner_account"] == g.account.id():
                matches = g.db.matches.get_matches(
                        account_link=g.db.account_links.get_account_links(account_id=account["id"])[0]["id"],
                        restrict_type=convert_match_type_names_to_ids(params['types'])[0],
                        selectColumns=["eid", "visual_id"]
                )
                if matches and account["sector"] != SECTORS_NAME_TO_ID["Cow-Calf"]:
                    owner_data = g.db.matches.get_matches_with_account_links(
                        matches_eids=tuple(match["eid"] for match in matches),
                        matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
                        account_links_sector=SECTORS_NAME_TO_ID["Cow-Calf"], matches_order_by="created"
                    )
                    for match in matches:
                        owner = list(filter(lambda o: o["eid"] == match["eid"], owner_data))
                        match["name"] = owner[0]["name"] if owner else None
                        match["visual_id"] = owner[0]["visual_id"] if owner else match["visual_id"]

                return {
                    "matches": matches
                }

            else:
                raise ExportException("Unauthorized")
        else:
            account = g.db.accounts.get_accounts(id=params["account_id"])[0]
            account_link_id = g.db.account_links.get_account_links(account_id=account["id"])[0]["id"]
            logged_in_account_link_id = g.db.account_links.get_account_links(account_id=g.account.id())[0]["id"]
            return {
                "matches": g.db.matches.get_common_eid_data(logged_in_account_link_id, account_link_id)
            }
    else:
        if 'sighted_animals' in params:
            return {
                "matches": g.db.matches.get_sightings_in_auction_house_feedlot_packer_stocker(g.account.id(), g.account.is_partner())
            }
        elif 'all_matches' in params:
            if g.account.is_partner():
                # no matches for a partner account
                return {"matches": []}
            else:
                account_link_id = g.db.account_links.get_account_links(account_id=g.account.id())[0]["id"]
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
            account_ids = []
            if g.account.is_partner():
                if g.account.sector_id() == SECTORS_NAME_TO_ID["Producer Service"]:
                    account_ids = Connections(g.db).get_connected_account_ids(g.account.id())
                else:
                    accounts = g.db.accounts.get_accounts(partner_account=g.account.id())
                    account_ids = [account["id"] for account in accounts]
            else:
                account_ids = [g.account.id()]
            return {
                "matches": g.db.matches.get_distinct_match_locations_for_account(
                    account_ids, restrict_types, g.account.is_partner()
                )
            }
