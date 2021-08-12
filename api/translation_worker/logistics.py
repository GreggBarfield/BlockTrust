from time import sleep
from .exceptions import ExecutionException
from core.reports.query import execute_query
from core.common_exceptions import ExportException
from .insert_handler import handle_insert
import traceback


def run(db, inserts_model, verbose=False, insert_id=None):
    """Starts the translation worker.

    Params:
        db: A Database object
    """

    while True:
        if insert_id is not None:
            insert = inserts_model.get_by_id(insert_id)
        else:
            insert = inserts_model.get_next()

        if insert is None:
            if insert_id is not None:
                if verbose:
                    print("Failed to find the insert!")
                break
            print("Sleeping")
            sleep(10)
        else:
            print("Running insert", insert['id'])
            try:
                #raise Exception('HiThere')
                handle_insert(db, inserts_model, insert)
            except Exception as e:
                #max col size to store exception is 5000
                inserts_model.set_status(insert['id'], "Exception",  e.__class__.__name__ + ": " + str(e) + ", Stacktrace: " + traceback.format_exc())

                if verbose:
                    print("ExecutionException",  str(e))

        if insert_id is not None:
            break
