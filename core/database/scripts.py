"""Routines which can be run individually to perform specific changes to the database."""
from .tables.accounts import Accounts
from .tables.account_links import AccountLinks
from core.database.tables.account_users import AccountUsers
from core.database.tables.users import Users
from ..sectors import SECTORS_NAME_TO_ID
from .combinations import create_connections_for_supply_chain
import inspect
import sys


def add_connections_for_supply_chain(db, dry_run=False):
    cow_calf_accounts = Accounts(db).get_accounts(sector=SECTORS_NAME_TO_ID["Cow-Calf"])
    no_account_link_ranchers = []
    new_connections = []
    for ranch in cow_calf_accounts:
        account_link = AccountLinks(db).get_account_links(account_id=ranch["id"])
        if len(account_link) > 0:
            if len(new_connections_for_ranch := create_connections_for_supply_chain(
                db, account_link[0]["id"], ranch["id"], dry_run)
            ) > 0:
                new_connections.append(new_connections_for_ranch)
        else:
            no_account_link_ranchers.append(ranch["id"])

    log = {
        "dry_run": dry_run,
        "new_connections": ",".join(str(i) for i in new_connections),
        "no_account_links_found": ",".join(str(i) for i in no_account_link_ranchers)
    }
    return log


def add_default_user_for_partners(db, dry_run=False):
    partners = Accounts(db).get_partners()
    log = {}
    partners_users = []
    if not dry_run:
        for partner in partners:
            try:
                user_id = Users(db).create_pseudo_user(f"DefaultUserPartner#{partner['id']}", "Default", "User")
                AccountUsers(db).create_account_user(user_id, partner["id"])
            except Exception:
                pass
            else:
                partners_users.append((partner["id"], user_id))
    log = {
        "dry_run": dry_run,
        "partner_ids_to_user_ids": ",".join(str(i) for i in partners_users)
    }
    return log


def get_available_scripts():
    return [
        name for name, func in inspect.getmembers(sys.modules[__name__]) 
        if (inspect.isfunction(func) and func.__module__ == __name__) and func.__name__ != get_available_scripts.__name__
    ]
