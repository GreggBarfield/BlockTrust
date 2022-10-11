"""Functions which perform actions using multiple tables"""
from .tables.matches import Matches
from .tables.connections import Connections, ConnectionException, connection_status_name_to_id, connection_type_name_to_id
from core.match_types import match_types_by_name
from core.sectors import sectors_by_name
from .tables.scheduled_emails import ScheduledEmails, EMAILS, SCHEDULED_EMAIL_STATUS_NAME_TO_ID
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


def schedule_match_found_email(self, owner_match_account_link):
    scheduled_emails_data_access = ScheduledEmails(self._db)
    # if same email is not yet to be sent, add the scheduled email. Scheduled emails are processed once a day.
    if len(scheduled_emails_data_access.get_scheduled_emails(
        subject=EMAILS["MATCH FOUND"]["SUBJECT"],
        status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"]
    )) == 0:
        if len(match_account_admin_users := self._db.account_users.get_account_users(account=owner_match_account_link["account"], is_admin=1)) > 0:
            if len(users := self._db.users.get_users(id=match_account_admin_users[0]["user"], is_email_verified=1)) > 0:
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
                    #add connection to ranch
                    #when a new account joins as well, you need to add connection since they might have been just accountlinks
                    #when this happened.


def perform_packer_data_found_actions(db, eid, account_id):
    if len(sightings := Matches(db).get_matches_with_account_links(
        matches_eid=eid, matches_restrict_type=match_types_by_name["Sighting"],
        account_links_sector=sectors_by_name["Cow-Calf"], matches_order_by="created"
    )) > 0:
        owner_match_account_link = sightings[0]
        schedule_match_found_email(owner_match_account_link)
        try:
            Connections(db).create_or_fail_connection(from_account_id=owner_match_account_link["account"], 
                                                      to_account_id=account_id,
                                                      status=connection_status_name_to_id["Connected"],
                                                      connection_type_id=connection_type_name_to_id["Acquired"])
        except ConnectionException:
            pass

