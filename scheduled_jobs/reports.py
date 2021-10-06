from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.reports import Reports
import traceback
import time
import datetime

from core.reports.query_types import (
    count_distribution, count_distribution_global, count_eid_distinct,
    count_eid_distinct_by_account
)


def make_global_reports(db):
    queries = [
        count_distribution_global.create("USDA Yield Grade"),
        count_distribution_global.create("USDA Quality Grade"),
        count_eid_distinct.create(),
    ]
    for query in queries:
        Reports(db).insert_query(None, query)


def make_report(db, account_id):
    queries = [
        count_distribution.create(account_id, "USDA Yield Grade"),
        count_distribution.create(account_id, "USDA Quality Grade"),
        count_eid_distinct_by_account.create(account_id)
    ]

    for query in queries:
        Reports(db).insert_query(account_id, query)


def make_missed_reports_for_accounts(db):
    """Make reports for those accounts which don't exist in reports table.

    """
    for row in db.execute_d("SELECT id FROM accounts WHERE accounts.id NOT IN (SELECT account_id FROM reports WHERE account_id IS NOT NULL)"):
        print("Reports Thread: Found account with no reports setup: ", row['id'])
        make_report(db, row['id'])


def run_report_tasks(job_run_id, db):
    try:
        make_global_reports(db)
        make_missed_reports_for_accounts(db)
        Reports(db).mark_reports_for_reprocessing()
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Reports Job Exiting. Current time: ", datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Jobs - Reports", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
    finally:
        db._cursor.close()
        db.close()
