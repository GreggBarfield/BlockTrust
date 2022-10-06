"""Routines which perform changes to the BlockTrustNetwork database to be run manually."""
from ..database.tables.accounts import Accounts
from ..database.tables.account_links import AccountLinks
from ..database.tables.matches import Matches
from ..database.tables.connections import ConnectionException, Connections, connection_status_name_to_id, connection_type_name_to_id
from ..sectors import sectors_by_name
import inspect, sys


def add_connections_for_supply_chain(db):
    ranchers = Accounts(db).get_accounts(sector=sectors_by_name["Cow-Calf"])
    no_account_link_ranchers = []
    new_connections = []
    for ranch in ranchers:
        account_link = AccountLinks(db).get_account_links(account_id=ranch["id"])
        if len(account_link) > 0:
            supply_chain_links = Matches(db).get_matched_accounts_for_account_link(account_link[0]["id"])
            # go through each account in supply chain and add connection if not exists.
            for account_link in supply_chain_links:
                if ranch["id"] != account_link["account"]:
                    new_connections.append((ranch["id"], account_link["account"]))
                    try:
                        Connections(db).create_or_fail_connection(from_account_id=ranch["id"], to_account_id=account_link["account"],
                                                                  status=connection_status_name_to_id["Connected"],
                                                                  connection_type_id=connection_type_name_to_id["Acquired"])
                    except ConnectionException as e:
                        pass
        else:
            no_account_link_ranchers.append(ranch["id"])

    log = {}
    log["new_connections"] = ",".join(str(i) for i in new_connections)
    log["no_account_links_found"] = ",".join(str(i) for i in no_account_link_ranchers)
    return log


def get_available_scripts():
    return [
        name for name, func in inspect.getmembers(sys.modules[__name__]) 
        if (inspect.isfunction(func) and func.__module__ == __name__) and func.__name__ != get_available_scripts.__name__
    ]
