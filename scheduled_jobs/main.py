from usda_data_retriever import get_usda_data
from threading import Thread
import traceback
import time
import datetime
from core.database.database import Database
from core.config import (MYSQL_CONFIG)
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns

try:
    scheduled_jobs = {
        "USDAData": "usda_data_retriever|get_usda_data",
    }
    print("Executing main.py")
    db = Database(MYSQL_CONFIG)
    threads=[]
    while(True):
        #remove any threads that are done executing
        for t in threads:
            if not t.is_alive():
                t.handled = True
            else:
                t.handled = False
        threads = [t for t in threads if not t.handled]

        current_time = datetime.datetime.now().time()
        print("current_time:", current_time)
        #this will run once between 7 and 7.10 AM UTC time
        if datetime.time(7,0,0) <= current_time < datetime.time(7,10,0):
            #check if this thread is already running 
            if not any(t.getName() == "USDAData" for t in threads):
                #proceed to create a new thread
                JobRuns(db).insert("USDAData", scheduled_jobs["USDAData"].split('|')[0], scheduled_jobs["USDAData"].split('|')[1])
                t = Thread(target=get_usda_data, name="USDAData", args=[Database(MYSQL_CONFIG)])
                t.start()
                threads.append(t) 
                print('Appended thread USDAData','Total number of threads:', len(threads), 'Current time:', current_time)

        #sleep for 10 minutes
        #print("going to sleep")
        time.sleep(600)
except Exception as e:
    print(e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    ErrorLogs(db).insert_error_log("Scheduled Jobs", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
finally:
     db.close()