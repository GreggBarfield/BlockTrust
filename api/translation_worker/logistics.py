from time import sleep
from .exceptions import ExecutionException
from core.reports.query import execute_query
from core.common_exceptions import ExportException
from .insert_handler import handle_insert


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
                handle_insert(db, inserts_model, insert)
            except ExecutionException as e:
                inserts_model.set_status(insert['id'], "Exception")

                if verbose:
                    print("ExecutionException", str(e))

        if insert_id is not None:
            break
