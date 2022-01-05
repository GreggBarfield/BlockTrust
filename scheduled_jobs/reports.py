from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.reports import REPORT_STATUS, Reports
import traceback
import time
import datetime

from core.reports.query_types import (
    count_distribution, count_distribution_global, count_eid_distinct,
    count_eid_distinct_by_account, market_data_cache, sustainability_averages,
    eid_list_global
)


def make_global_reports(db):
    queries = [
        count_distribution_global.create("USDA Yield Grade"),
        count_distribution_global.create("USDA Quality Grade"),
        count_eid_distinct.create(),
        eid_list_global.create()
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
        reports_table = Reports(db)
        reports_table.mark_account_reports_for_reprocessing()

        market_cache_report = reports_table.get_reports(query=market_data_cache.create(), selectColumns=["id"])[0]
        reports_table.update_report(market_cache_report["id"], REPORT_STATUS["Pending"])

        sus_averages = reports_table.get_reports(query=sustainability_averages.create(), selectColumns=["id"])[0]
        reports_table.update_report(sus_averages["id"], REPORT_STATUS["Pending"])

        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Reports Job Exiting. Current time: ", datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Jobs - Reports", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
    finally:
        db._cursor.close()
        db.close()
