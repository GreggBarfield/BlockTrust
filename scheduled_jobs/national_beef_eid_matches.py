from core.database.combinations import perform_feeder_packer_data_received_actions, schedule_match_found_email
from core.database.tables.accounts import Accounts, NATIONAL_BEEF_COMPANY
from core.database.tables.animals import Animals, ANIMALS_PAGINATION_LIMIT
from core.database.tables.debug_logs import DebugLogs
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.matches import Matches, MATCH_TYPES_NAME_TO_ID
from core.database.tables.scheduled_emails import ScheduledEmails
from core.sectors import SECTORS_NAME_TO_ID
import traceback
import datetime
import time

START_TIMESTAMP_DATETIME = datetime.datetime(2025, 10, 30, 12, 0, 0)
START_TIMESTAMP = START_TIMESTAMP_DATETIME.strftime("%Y-%m-%d %H:%M:%S")
END_TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run_national_beef_eid_matches_task(job_run_id, db):
    try:
        national_beef_partner = Accounts(db).get_partners(company=NATIONAL_BEEF_COMPANY)[0]
        total_animal_pages = Animals(db).get_animals_total_pages(
            account_id=national_beef_partner["id"],
            created_start_time=START_TIMESTAMP,
            created_end_time=END_TIMESTAMP
        )
        print(total_animal_pages)
        for page_number in range(1, total_animal_pages + 1):
            offset = (page_number - 1) * ANIMALS_PAGINATION_LIMIT
            packer_animals = Animals(db).get_animals_by_packer_api_insert_ids(
                account_id=national_beef_partner["id"],
                created_start_time=START_TIMESTAMP,
                created_end_time=END_TIMESTAMP,
                offset=offset
            )
            print(len(packer_animals))
            for packer_animal in packer_animals:
                sightings = Matches(db).get_matches_with_account_links(
                    matches_eid=packer_animal["eid"],
                    matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
                    account_links_sector=SECTORS_NAME_TO_ID["Cow-Calf"],
                    matches_order_by="created"
                )
                if len(sightings) > 0:
                    owner_match_account_link = sightings[0]
                    existing_debug_logs = DebugLogs(db).get(
                        component=perform_feeder_packer_data_received_actions.__name__,
                        details_owner_account_id=owner_match_account_link["account"],
                        details_eid=packer_animal["eid"]
                    )
                    if(len(existing_debug_logs)) == 0:
                        schedule_match_found_email(db, owner_match_account_link)
            break

        print("National Beef EID matches Job Exiting. Current time: ", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("National Beef EID matches job", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
