from time import sleep
from core.reports.query import execute_query
from core.common_exceptions import ExportException


def run(db):
    """Starts the reports worker.

    Params:
        db: A Database object
    """
    while True:
        report = db.reports.work_report()

        if report is None:
            print("Sleeping")
            sleep(10)
        else:
            print("Running report", report['id'])
            try:
                result = execute_query(db, report['query'])
                db.reports.fulfill_report(
                    report['id'],
                    result
                )
            except ExportException as e:
                db.reports.fulfill_report(
                    report['id'],
                    {
                        "error": str(e)
                    },
                    status=4
                )
            # No bare except since it also catches ctrlc interrupts
