from time import sleep
from core.reports.query import execute_query
import datetime
import traceback


def run(db):
    """Starts the reports worker.

    Params:
        db: A Database object
    """
    report = db.reports.work_report()

    if report is None:
        print("Sleeping. Current time:", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
        sleep(3600)
    else:
        print("Running report:", report['id'], "account id:", report['account_id'])
        try:
            result = execute_query(db, report['query'])
            db.reports.fulfill_report(
                report['id'],
                result
            )
        except Exception as e:
            db.reports.fulfill_report(
                report['id'],
                {
                    "error": str(e), "Traceback": traceback.format_exc()
                },
                status=4
                )
        # No bare except since it also catches ctrlc interrupts
