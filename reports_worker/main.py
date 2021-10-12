import os
import json
import random
import sys
import traceback

sys.path = [
        os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
    ] + sys.path

try:

    __name__ = "reports_worker.main"
    from core.database.database import Database  # noqa
    from core.config import *  # noqa
    from core.database.tables.error_logs import ErrorLogs
    from .logistics import run  # noqa
    db = Database(MYSQL_CONFIG)
    while True:
        run(db)
except Exception as e:
    print("Reports worker", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    ErrorLogs(db).insert_error_log("Reports worker", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
finally:
    db._cursor.close()
    db.close()
