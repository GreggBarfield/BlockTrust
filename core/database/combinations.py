"""Reusable functions which perform actions using multiple table routines"""
from core.database.tables.account_links import AccountLinks
from core.database.tables.account_users import AccountUsers
from core.database.tables.accounts import Accounts
from core.database.tables.event_logs import EventLogs
from core.database.tables.users import Users
from core.renderers.email import render_email
from core.utilities.email import send_email
from .tables.matches import Matches
from .tables.connections import Connections, ConnectionException, CONNECTION_STATUS_NAME_TO_ID, CONNECTION_TYPE_NAME_TO_ID
from core.match_types import match_types_by_name
from core.sectors import sectors_by_name
from .tables.scheduled_emails import ScheduledEmails, EMAILS, SCHEDULED_EMAIL_STATUS_NAME_TO_ID
from .tables.debug_logs import DebugLogs
from core.config import SECONDARY_EMAIL_RECIPIENT_FOR_MATCH_FOUND


def create_connections_for_supply_chain(db, cow_calf_account_link_id, cow_calf_account_id, dry_run=False):
    new_connections = []
    supply_chain_links = Matches(db).get_matched_accounts_for_account_link(cow_calf_account_link_id)
    for account_link in supply_chain_links:
        if cow_calf_account_id != account_link["account"]:
            new_connections.append((cow_calf_account_id, account_link["account"]))
            if not dry_run:
                try:
                    Connections(db).create_or_fail_connection(from_account_id=cow_calf_account_id, to_account_id=account_link["account"],
                                                              status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
                                                              connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Acquired"])
                except ConnectionException:
                    pass
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


def perform_feeder_packer_data_received_actions(db, eid, schedule_email=False, feeder_account_id=None, packer_account_id=None):
    """
    Performs actions when new data is received from a feeder/packer
    """
    if len(sightings := Matches(db).get_matches_with_account_links(
        matches_eid=eid, matches_restrict_type=match_types_by_name["Sighting"],
        account_links_sector=sectors_by_name["Cow-Calf"], matches_order_by="created"
    )) > 0:
        owner_match_account_link = sightings[0]

        debug_log = {"schedule_email": schedule_email, "owner_account_id": owner_match_account_link['account'],
                     "feeder_account_id": feeder_account_id, "packer_account_id": packer_account_id}
        DebugLogs(db).insert_debug_log(perform_feeder_packer_data_received_actions.__name__, "Function execution", None, debug_log)

        if schedule_email:
            schedule_match_found_email(db, owner_match_account_link)
        try:
            if feeder_account_id:
                Connections(db).create_or_fail_connection(from_account_id=owner_match_account_link["account"],
                                                          to_account_id=feeder_account_id,
                                                          status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
                                                          connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Acquired"])
        except ConnectionException:
            pass

        try:
            if packer_account_id:
                Connections(db).create_or_fail_connection(from_account_id=owner_match_account_link["account"],
                                                          to_account_id=packer_account_id,
                                                          status=CONNECTION_STATUS_NAME_TO_ID["Connected"],
                                                          connection_type_id=CONNECTION_TYPE_NAME_TO_ID["Acquired"])
        except ConnectionException:
            pass


def perform_new_account_actions(db, account_id, user_id, event_type_id, employee_id=None):
    account_link_id = AccountLinks(db).get_account_links(account_id=account_id)[0]["id"]
    new_connections = create_connections_for_supply_chain(db, account_link_id, account_id)

    event_details = {"connections": ",".join(str(n) for n in new_connections)}
    if employee_id:
        event_details["employee_id"] = employee_id
    EventLogs(db).insert_event_log(account_id=account_id, user_id=user_id, event_type_id=event_type_id,
                                   details=event_details)


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


def send_email_to_admin_users(db, account_id, subject, body):
    if len(admin_account_users := AccountUsers(db).get_account_users(account=account_id, is_admin=1)) > 0:
        for admin_account_user in admin_account_users:
            if len(email_verified_user := Users(db).get_users(id=admin_account_user["user"], is_email_verified=1)) > 0:
                send_email(subject, body, email_verified_user[0]["email"])
