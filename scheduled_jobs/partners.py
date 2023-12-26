from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.api_inserts import ApiInserts
from core.database.tables.accounts import RED_ANGUS_PARTNER_COMPANY
from core.utilities.email import send_email
from core.config import ADMIN_EMAIL, RUN_NOTIFY_IF_NO_DATA_RECEIVED_FROM_PARTNER
import traceback
import datetime
import time
from pathlib import Path


def notify_admin_if_no_data_received_from_partner(db):
    partners = [RED_ANGUS_PARTNER_COMPANY]
    for partner in partners:
        api_insert_count = ApiInserts(db).get_partner_api_inserts_count(partner_company_name=partner, interval=7)
        if api_insert_count == 0:
            email_subject = "API Update"
            email_body = "No API data received in the last 1 week for account: " + partner
            send_email(email_subject, email_body, ADMIN_EMAIL)


def run_partner_tasks(job_run_id, db):
    try:
        log = {}
        if RUN_NOTIFY_IF_NO_DATA_RECEIVED_FROM_PARTNER:
            notify_admin_if_no_data_received_from_partner(db)
        else:
            log["RUN_NOTIFY_IF_NO_DATA_RECEIVED_FROM_PARTNER"] = False
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), log if log else None)
        print(Path(__file__).stem.capitalize() + " Job Exiting. Current time: ", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log(Path(__file__).stem.capitalize(), e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
    finally:
        db.close()
