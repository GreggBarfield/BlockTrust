from time import sleep
from .exceptions import ExecutionException
from core.reports.query import execute_query
from core.common_exceptions import ExportException
from .insert_handler import handle_insert


def run(db, inserts_model):
    """Starts the translation worker.

    Params:
        db: A Database object
    """

    while True:
        insert = inserts_model.get_next()

        if insert is None:
            print("Sleeping")
            sleep(10)
        else:
            print("Running insert", insert['id'])
            try:
                handle_insert(db, inserts_model, insert)
            except ExecutionException:
                inserts_model.set_status(insert['id'], "Exception")
