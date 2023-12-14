from os.path import join
from flask import (Flask, render_template)
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.scheduled_emails import ScheduledEmails
from core.utilities.email import send_email
import traceback
import datetime
import time

app = Flask(__name__)

def run_email_tasks(job_run_id, db):
    try:
        # ScheduledEmails(db).process_pending_emails()
        with app.app_context():
            print(join("email", "contact_us.html"))
            send_email(
            "New Email",
            render_template(join("email/internal", "sales_group_search_summary.html"), **{
                "test": "test"
            }),
            "nisheet.thakur@blocktrustnetwork.com"
            )
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Emails Job Exiting. Current time: ", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Email", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
