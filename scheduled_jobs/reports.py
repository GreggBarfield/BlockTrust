from core.database.tables.accounts import Accounts
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.debug_logs import DebugLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.reports import REPORT_STATUS, Reports
import traceback
import time
import datetime
from core.reports.query_types import (
    market_data_cache, sustainability_response_averages
)


def make_missed_reports_for_accounts(db, reports_table):
    """Make reports for those accounts which don't exist in reports table."""
    account_ids = []
    for row in reports_table.get_accounts_with_no_reports():
        print("Reports Thread: Found account with no reports setup: ", row['account_id'])
        reports_table.make_reports_for_account(row["account_id"], row["sector_id"])
        account_ids.append(row['account_id'])
    DebugLogs(db).insert_debug_log(
        component="Reports", short_info="Missing reports created", details={"account_ids": ','.join(str(id) for id in account_ids)}
    )


def make_annual_reports_for_accounts(db, reports_table):
    """ Temporary routine to create annual reports for accounts """
    accounts = Accounts(db).get_accounts()
    account_ids = []
    for account in accounts:
        print("Reports Thread: Setting up annual reports for account: ", account['id'])
        reports_table.make_annual_reports_for_account(account["id"], account["sector"])
        account_ids.append(account['id'])
    DebugLogs(db).insert_debug_log(
        component="Reports", short_info="Annual reports created", details={"account_ids": ','.join(str(id) for id in account_ids)}
    )


def run_report_tasks(job_run_id, db):
    try:
        reports_table = Reports(db)
        reports_table.make_global_reports()
        make_missed_reports_for_accounts(db, reports_table)
        make_annual_reports_for_accounts(db, reports_table)
        reports_table.mark_account_reports_for_reprocessing()

        market_cache_report = reports_table.get_reports(query=market_data_cache.create(), selectColumns=["id"])[0]
        reports_table.update_report(market_cache_report["id"], REPORT_STATUS["Pending"])

        sus_response_averages = reports_table.get_reports(query=sustainability_response_averages.create(), selectColumns=["id"])[0]
        reports_table.update_report(sus_response_averages["id"], REPORT_STATUS["Pending"])

        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Reports Job Exiting. Current time: ", datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Jobs - Reports", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
    finally:
        db._cursor.close()
        db.close()
