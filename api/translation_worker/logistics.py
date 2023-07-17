from time import sleep
from core.config import MYSQL_CONFIG
from core.database.database import Database
from .insert_handler import handle_insert
import traceback
import datetime


def run(inserts_model, verbose=False, insert_id=None):
    """Starts the translation worker.
    """
    db = None
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
            else:
                if db:
                    db.close()
                    db = None
                print("Sleeping for 60 mins. Current time:", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
                sleep(3600)
        else:
            print("Running insert:", insert['id'], ", Partner account:", insert['account'])
            try:
                if not db:
                    db = Database(MYSQL_CONFIG)
                handle_insert(db, inserts_model, insert)
            except Exception as e:
                if str(e) == "Duplicate":
                    inserts_model.set_status(
                        insert['id'],
                        "Duplicate"
                    )
                else:
                    # max col size to store exception is 3000
                    inserts_model.set_status(
                        insert['id'],
                        "Exception",
                        e.__class__.__name__ + ": " + str(e) + ", Stacktrace: " + traceback.format_exc()
                    )

                if verbose:
                    print("ExecutionException",  str(e))

        if insert_id is not None:
            break
