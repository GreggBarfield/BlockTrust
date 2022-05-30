from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.emails import Emails
from core.utilities.email import send_email
from core.renderers.email import render_email
import traceback
import datetime
import time


def run_email_tasks(job_run_id, db):
    try:
        # Emails(db).process_pending_emails()
        send_email(
                    "BlockTrust Network Email Confirmation",
                    render_email("verification_email.html", {
                        'confirm_url': "This is a test"
                    }), "nisheet.thakur@blocktrustnetwork.com"
        )
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Emails Job Exiting. Current time: ", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Email", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
