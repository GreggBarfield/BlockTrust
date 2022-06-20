import time
import traceback
from urllib.error import HTTPError
import requests
import datetime
from core.database.tables.debug_logs import DebugLogs
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.config import DOMAIN

#These need to be developed and tested further
def transfer_data_from_ils(db, job_run_id): #2am
    try:
        if DOMAIN == "blocktrustnetwork.com":
            response = requests.get("https://ledgerspace-secure.com/Test/ILS.asmx/SendEIDData")
            DebugLogs(db).insert_debug_log("TransferDataILS:transfer_data_from_ils", "Request Response", response.text)
            response.raise_for_status()
        else:
            print("ILS transfer turned off")
    except HTTPError as e:
        ErrorLogs(db).insert_error_log("Jobs: Transfer Data From ILS Server", e.__class__.__name__ + ", Code: " + e.response.status_code + 
            ", Text: " + e.response.text, traceback.format_exc())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Jobs: Transfer Data From ILS Server", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    finally:
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))

def transfer_data_to_ils(db, job_run_id): #4.30AM
    try:
        if DOMAIN == "blocktrustnetwork.com":
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
            response = requests.get("https://ledgerspace-secure.com/Test/ILS.asmx/ReceiveEIDList", headers={"User-Agent": user_agent})
            DebugLogs(db).insert_debug_log("TransferDataILS:transfer_data_to_ils", "Request Response", response.text)
            response.raise_for_status()
        else:
            print("ILS transfer turned off")
    except HTTPError as e:
        print(e)
        ErrorLogs(db).insert_error_log("Jobs: Transfer Data To ILS Server", e.__class__.__name__ + ", Code: " + e.response.status_code + 
            ", Text: " + e.response.text, traceback.format_exc())
    except Exception as e:
        print(e)
        ErrorLogs(db).insert_error_log("Jobs: Transfer Data To ILS Server", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    finally:
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))


def transfer_data_ils(job_run_id, db):
    try:
        #transfer_data_from_ils(db, job_run_id)
        transfer_data_to_ils(db, job_run_id)
        print("transfer_data_ILS(): Exiting. Current time: ", datetime.datetime.now().time())
    except Exception as e:
        if len(e.args) > 1:
            ErrorLogs(db).insert_error_log("TransferDataILS", e.__class__.__name__ + ": " + str(e.args[0]), traceback.format_exc(), e.args[1])
        else:
            ErrorLogs(db).insert_error_log("TransferDataILS", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    finally:
        db.close()