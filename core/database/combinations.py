"""Reusable functions which perform actions using multiple tables"""
from .tables.matches import Matches
from .tables.connections import Connections, ConnectionException, connection_status_name_to_id, connection_type_name_to_id
from core.match_types import match_types_by_name
from core.sectors import sectors_by_name
from .tables.scheduled_emails import ScheduledEmails, EMAILS, SCHEDULED_EMAIL_STATUS_NAME_TO_ID
from .tables.debug_logs import DebugLogs
from core.config import SECONDARY_EMAIL_RECIPIENT_FOR_MATCH_FOUND


def create_connections_for_supply_chain(db, cow_calf_account_link_id, cow_calf_account_id):
    new_connections = []
    supply_chain_links = Matches(db).get_matched_accounts_for_account_link(cow_calf_account_link_id)
    for account_link in supply_chain_links:
        if cow_calf_account_id != account_link["account"]:
            new_connections.append((cow_calf_account_id, account_link["account"]))
            try:
                Connections(db).create_or_fail_connection(from_account_id=cow_calf_account_id, to_account_id=account_link["account"],
                                                          status=connection_status_name_to_id["Connected"],
                                                          connection_type_id=connection_type_name_to_id["Acquired"])
            except ConnectionException:
                pass
    return new_connections


def schedule_match_found_email(db, owner_match_account_link):
    scheduled_emails_data_access = ScheduledEmails(db)
    # if same email is not yet to be sent, add the scheduled email. Scheduled emails are processed once a day.
    if len(scheduled_emails_data_access.get_scheduled_emails(
        subject=EMAILS["MATCH FOUND"]["SUBJECT"],
        status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"]
    )) == 0:
        if len(match_account_admin_users := db.account_users.get_account_users(account=owner_match_account_link["account"], is_admin=1)) > 0:
            if len(users := db.users.get_users(id=match_account_admin_users[0]["user"], is_email_verified=1)) > 0:
                scheduled_emails_data_access.insert_scheduled_email(
                    user_id=users[0]["id"], account_id=owner_match_account_link["account"], subject=EMAILS["MATCH FOUND"]["SUBJECT"],
                    body=EMAILS["MATCH FOUND"]["BODY"], status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"]
                )
                if SECONDARY_EMAIL_RECIPIENT_FOR_MATCH_FOUND:
                    notification_email = f"A match has been found for account: <strong>{owner_match_account_link['company']}</strong>"
                    scheduled_emails_data_access.insert_scheduled_email(
                        email_address=SECONDARY_EMAIL_RECIPIENT_FOR_MATCH_FOUND, account_id=owner_match_account_link["account"], subject="Match found",
                        body=notification_email, status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"]
                    )


def perform_feeder_packer_actions(db, eid, schedule_email=False, feeder_account_id=None, packer_account_id=None):
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
        DebugLogs(db).insert_debug_log(perform_feeder_packer_actions.__name__, "Function execution", None, debug_log)

        if schedule_email:
            schedule_match_found_email(db, owner_match_account_link)
        try:
            if feeder_account_id:
                Connections(db).create_or_fail_connection(from_account_id=owner_match_account_link["account"],
                                                          to_account_id=feeder_account_id,
                                                          status=connection_status_name_to_id["Connected"],
                                                          connection_type_id=connection_type_name_to_id["Acquired"])
        except ConnectionException:
            pass

        try:
            if packer_account_id:
                Connections(db).create_or_fail_connection(from_account_id=owner_match_account_link["account"],
                                                          to_account_id=packer_account_id,
                                                          status=connection_status_name_to_id["Connected"],
                                                          connection_type_id=connection_type_name_to_id["Acquired"])
        except ConnectionException:
            pass
