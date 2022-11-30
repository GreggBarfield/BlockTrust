from time import sleep
from core.reports.query import execute_query
from core.database.tables.reports import Reports
import datetime
import traceback


def run(db):
    """Starts the reports worker.

    Params:
        db: A Database object
    """
    reports_data_access = Reports(db)
    report = reports_data_access.work_report()

    if report is None:
        print("Sleeping. Current time:", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
        sleep(3600)
    else:
        print("Running report:", report['id'], "account id:", report['account_id'])
        try:
            result = execute_query(db, report['query'])
            reports_data_access.fulfill_report(
                report['id'],
                result
            )
        except Exception as e:
            reports_data_access.fulfill_report(
                report['id'],
                {
                    "error": str(e), "Traceback": traceback.format_exc()
                },
                status=4
                )
        # No bare except since it also catches ctrlc interrupts
