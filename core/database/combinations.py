"""Reusable functions which perform actions using multiple table routines"""
import os
from datetime import datetime
from core.database.tables.account_links import AccountLinks
from core.database.tables.account_users import AccountUsers
from core.database.tables.accounts import Accounts
from core.database.tables.auction_markets import AuctionMarkets
from core.database.tables.connection_invites import ConnectionInvites
from core.database.tables.event_logs import EventLogs, EVENT_TYPE_NAMES_TO_IDS
from core.database.tables.reports import Reports
from core.database.tables.sent_emails import SentEmails
from core.database.tables.transactions import TRANSACTION_TYPE_NAMES_TO_IDS, Transactions
from core.database.tables.users import Users
from core.renderers.email import render_email
from core.utilities.email import send_email
from .tables.matches import Matches
from .tables.connections import (
    Connections, ConnectionException, CONNECTION_STATUS_NAME_TO_ID, CONNECTION_TYPE_NAME_TO_ID
)
from core.match_types import MATCH_TYPES_NAME_TO_ID
from core.sectors import SECTORS_NAME_TO_ID
from .tables.scheduled_emails import ScheduledEmails, EMAILS, SCHEDULED_EMAIL_STATUS_NAME_TO_ID
from .tables.debug_logs import DebugLogs
from core.config import ADMIN_EMAIL, SECONDARY_EMAIL_RECIPIENT_FOR_MATCH_FOUND


def create_connections_for_supply_chain(db, cow_calf_account_link_id, cow_calf_account_id, dry_run=False):
    new_connections = []
    supply_chain_links = Matches(db).get_sighted_match_accounts_for_account_link(cow_calf_account_link_id)
    for match_account_link in supply_chain_links:
        if cow_calf_account_id != match_account_link["account_id"]:
            if not dry_run:
                try:
                    Connections(db).create_or_fail_connection(
                        from_account_id=cow_calf_account_id, to_account_id=match_account_link["account_id"],
                        status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
                        connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Acquired"],
                        details={"created_by_operation": create_connections_for_supply_chain.__name__,
                                 "eid": match_account_link["eid"]})
                except ConnectionException:
                    pass
                else:
                    new_connections.append((cow_calf_account_id, match_account_link["account_id"], match_account_link["eid"]))
            else:
                # for dry_run
                existing_connection = Connections(db).get_connection_between(cow_calf_account_id, match_account_link["account"])
                if not existing_connection:
                    new_connections.append((cow_calf_account_id, match_account_link["account_id"], match_account_link["eid"]))
    return new_connections


def schedule_match_found_email(db, owner_match_account_link):
    scheduled_emails_data_access = ScheduledEmails(db)

    if len(match_account_admin_users := db.account_users.get_account_users(account=owner_match_account_link["account"], is_admin=1)) > 0:
        for account_user in match_account_admin_users:
            if len(user := db.users.get_users(id=account_user["user"], is_email_verified=1)) > 0:
                # if same email is not yet to be sent, add the scheduled email. Scheduled emails are processed once a day.
                if len(scheduled_emails_data_access.get_scheduled_emails(
                    user_id=user[0]["id"],
                    account_id=owner_match_account_link["account"],
                    subject=EMAILS["MATCH FOUND"]["SUBJECT"],
                    status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"]
                )) == 0:
                    scheduled_emails_data_access.insert_scheduled_email(
                        user_id=user[0]["id"], account_id=owner_match_account_link["account"], subject=EMAILS["MATCH FOUND"]["SUBJECT"],
                        body=EMAILS["MATCH FOUND"]["BODY"], status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"]
                    )
                    if SECONDARY_EMAIL_RECIPIENT_FOR_MATCH_FOUND:
                        notification_email = f"A match has been found for account: <strong>{owner_match_account_link['company']}</strong>"
                        scheduled_emails_data_access.insert_scheduled_email(
                            email_address=SECONDARY_EMAIL_RECIPIENT_FOR_MATCH_FOUND, account_id=owner_match_account_link["account"], subject="Match found",
                            body=notification_email, status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"]
                        )


def perform_feeder_packer_data_received_actions(db, eid, schedule_email=False, feeder_account_id=None, packer_account_id=None, api_insert_id=None):
    """
    Performs actions when new data is received from a feeder/packer
    """
    if len(sightings := Matches(db).get_matches_with_account_links(
        matches_eid=eid, matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
        account_links_sector=SECTORS_NAME_TO_ID["Cow-Calf"], matches_order_by="created"
    )) > 0:
        owner_match_account_link = sightings[0]

        debug_log = {"schedule_email": schedule_email, "owner_account_id": owner_match_account_link['account'],
                     "feeder_account_id": feeder_account_id, "packer_account_id": packer_account_id, 
                     "api_insert_id": api_insert_id, "eid": eid}
        DebugLogs(db).insert_debug_log(perform_feeder_packer_data_received_actions.__name__, "Function execution", None, debug_log)

        if schedule_email:
            schedule_match_found_email(db, owner_match_account_link)
        try:
            if feeder_account_id:
                Connections(db).create_or_fail_connection(
                    from_account_id=owner_match_account_link["account"],
                    to_account_id=feeder_account_id,
                    status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
                    connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Acquired"],
                    details={"created_by_operation": perform_feeder_packer_data_received_actions.__name__,
                             "eid": eid, "api_insert_id": api_insert_id}
                )
        except ConnectionException:
            pass

        try:
            if packer_account_id:
                Connections(db).create_or_fail_connection(
                    from_account_id=owner_match_account_link["account"],
                    to_account_id=packer_account_id,
                    status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
                    connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Acquired"],
                    details={"created_by_operation": perform_feeder_packer_data_received_actions.__name__,
                             "eid": eid,  "api_insert_id": api_insert_id}
                )
        except ConnectionException:
            pass

def perform_rancher_data_received_actions(db, eid, schedule_email=False, cow_calf_account_id=None, packer_account_id=None, api_insert_id=None):
    """
        Performs actions when data is received from Rancher
    """
    if len(sightings := Matches(db).get_matches_with_account_links(
        matches_eid=eid, matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
        account_links_sector=SECTORS_NAME_TO_ID["Packer"], matches_order_by="created"
    )) > 0:
        packer_match_account_link = sightings[0]
        debug_log = {"schedule_email": schedule_email, "owner_account_id": packer_match_account_link['account'],
                     "cow_calf_account_id": cow_calf_account_id, "packer_account_id": packer_account_id, 
                     "api_insert_id": api_insert_id, "eid": eid}
        DebugLogs(db).insert_debug_log(perform_rancher_data_received_actions.__name__, "Function execution", None, debug_log)
        if schedule_email:
            schedule_match_found_email(db, packer_match_account_link)

def perform_new_account_actions(db, account_id, user_id, event_type_id, sector_id, partner_id=None, email=None,
                                employee_id=None):
    """
        Performs multiple actions needed whenever a new account is created    
    """
    if email:
        ConnectionInvites(db).convert_invites_to_connections(email, account_id)
    Reports(db).make_reports_for_account(account_id, sector_id)
    account_link_id = AccountLinks(db).get_account_links(account_id=account_id)[0]["id"]
    new_connections = create_connections_for_supply_chain(db, account_link_id, account_id)

    # Retained
    # if partner_id:
    #     partner = Accounts(db).get_partners(id=partner_id)[0]
    #     if partner["partner_subscription_credits"]:
    #         update_partner_payment_of_account(db, partner, account_id, True, employee_id)

    event_details = {"connections": ",".join(str(n) for n in new_connections)}
    if employee_id:
        event_details["employee_id"] = employee_id
    EventLogs(db).insert(
        account_id=account_id, user_id=user_id, event_type_id=event_type_id, details=event_details
    )


def update_partner_payment_of_account(db, partner, account_id, paid_by_partner, employee_id=None):
    change_in_credits = -1 if paid_by_partner else 1
    Accounts(db).update_partner(
        partner["id"],
        partner_subscription_credits=partner["partner_subscription_credits"] + change_in_credits
    )
    Transactions(db).insert(
        transaction_type_id=TRANSACTION_TYPE_NAMES_TO_IDS["Subscription Credits"],
        partner_id=partner["id"],
        account_id=account_id,
        subscription_credits=change_in_credits,
        employee_id=employee_id
    )
    if paid_by_partner:
        Accounts(db).update_account(
            account_id=account_id, partner_paid=int(paid_by_partner),
            subscription_start_date=datetime.utcnow(), subscription_end_date=None
        )
    else:
        Accounts(db).update_account(
            account_id=account_id, partner_paid=int(paid_by_partner),
            subscription_end_date=datetime.utcnow()
        )


def send_connection_request_email_to_admin_users(db, to_account_id, from_account_id):
    if len(admin_account_users := AccountUsers(db).get_account_users(account=to_account_id, is_admin=1)) > 0:
        for admin_account_user in admin_account_users:
            if len(email_verified_user := Users(db).get_users(id=admin_account_user["user"], is_email_verified=1)) > 0:
                send_email(
                    "BlockTrust Network New Connection Request",
                    render_email("new_connection_request.html", {
                        "connection_receiving_user": email_verified_user[0],
                        "requesting_account": Accounts(db).get_accounts(id=from_account_id)[0]
                    }), email_verified_user[0]["email"]
                )


def send_email_to_admin_users(db, account_id, subject, body, add_log=False):
    if len(admin_account_users := AccountUsers(db).get_account_users(account=account_id, is_admin=1)) > 0:
        for admin_account_user in admin_account_users:
            if len(email_verified_user := Users(db).get_users(id=admin_account_user["user"], is_email_verified=1)) > 0:
                send_email(subject, body, email_verified_user[0]["email"])
                if add_log:
                    SentEmails(db).insert(
                        account_id=account_id,
                        user_id=email_verified_user[0]["id"],
                        email_address=email_verified_user[0]["email"],
                        subject=subject, file=os.path.basename(__file__),
                        routine=send_email_to_admin_users.__name__
                    )


def create_connection_with_eid_owner(db, eid, connecting_account_id, details=None):
    if len(sightings := Matches(db).get_matches_with_account_links(
        matches_eid=eid, matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
        account_links_sector=SECTORS_NAME_TO_ID["Cow-Calf"], matches_order_by="created"
    )) > 0:
        owner_match_account_link = sightings[0]
        try:
            if connecting_account_id and connecting_account_id != owner_match_account_link["account"]:
                Connections(db).create_or_fail_connection(
                    from_account_id=connecting_account_id,
                    to_account_id=owner_match_account_link["account"],
                    status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
                    connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Acquired"],
                    details=details
                )
        except ConnectionException:
            pass


def create_connection_with_all_sighted_accounts_for_eid(db, eid, connecting_account_id, details):
    sightings_match_als = Matches(db).get_matches_with_account_links(
                            matches_eid=eid,
                            matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"]
                        )
    for match_account_link in sightings_match_als:
        if match_account_link["account"] != connecting_account_id:
            try:
                Connections(db).create_or_fail_connection(
                    from_account_id=connecting_account_id,
                    to_account_id=match_account_link["account"],
                    status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
                    connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Acquired"],
                    details=details
                )
            except ConnectionException:
                pass


def convert_auction_market_to_account(db, auction_market_id, group_name):
    am = AuctionMarkets(db).get_auction_markets(id=auction_market_id)[0]
    account = Accounts(db).get_accounts(auction_market_id=am["id"])
    if not account:
        account_obj = Accounts(db).create_account(
                phone=None,
                company=am["name"],
                partner=None,
                affiliate_id=None,
                sector=SECTORS_NAME_TO_ID["Auction"],
                address=am["address"],
                city=am["city"],
                state=am["state"],
                zip=am["zip_code"],
                auction_market_id=am["id"]
        )
        user_id = Users(db).create_pseudo_user(account_obj.id(), False)
        AccountUsers(db).insert_account_user(user_id, account_obj.id(), int(True))
        send_email(
            "New Auction Market Account",
            render_email("internal/new_auction_market_account.html", {
                "account_id": account_obj.id(),
                "market_name": am["name"],
                "group_name": group_name
            }), ADMIN_EMAIL
        )
        perform_new_account_actions(
            db=db, account_id=account_obj.id(), user_id=user_id,
            event_type_id=EVENT_TYPE_NAMES_TO_IDS["Auction Market Account Created"],
            sector_id=account_obj.sector_id()
        )
