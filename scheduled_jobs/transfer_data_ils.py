import time
import traceback
from urllib.error import HTTPError
import requests
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns

#These need to be developed and tested further
def transfer_data_from_ils(db, job_run_id): #2am
    try:
        response = requests.get("https://ledgerspace-secure.com/Test/ILS.asmx/SendEIDData")
        response.raise_for_status()
    except HTTPError as e:
        ErrorLogs(db).insert_error_log("Jobs: Transfer Data To ILS", e.__class__.__name__ + ", Code: " + e.response.status_code + 
            ", Text: " + e.response.text, traceback.format_exc())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Jobs: Transfer Data To ILS", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    finally:
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))

def transfer_data_to_ils(db, job_run_id): #4.30AM
    try:
        response = requests.get("https://ledgerspace-secure.com/Test/ILS.asmx/ReceiveEIDList")
        response.raise_for_status()
    except HTTPError as e:
        ErrorLogs(db).insert_error_log("Jobs: Transfer Data From ILS", e.__class__.__name__ + ", Code: " + e.response.status_code + 
            ", Text: " + e.response.text, traceback.format_exc())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Jobs: Transfer Data From ILS", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    finally:
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
