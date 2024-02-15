import os
from usda_data_retriever import get_usda_data
from blockchain import run_bc_tasks
from reports import run_report_tasks
from emails import run_email_tasks
from partners import run_partner_tasks
from sales_groups_search_summary_emails import run_sales_group_search_summary_emails
from tag_store import run_tag_store_tasks
import payments
from threading import Thread
import traceback
import time
import datetime
from core.database.database import Database
from core.config import HERDWHISTLE_FETCH_EIDS_FROM_API, MYSQL_CONFIG, PAYMENTS
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns

try:
    scheduled_jobs = {
        "USDAData": "usda_data_retriever.py|get_usda_data",
        "Blockchain": "blockchain.py|run_bc_routines",
        "Reports": "reports.py|run_report_tasks",
        "Emails": "emails.py|run_email_tasks",
        "Partners": "partners.py|run_partner_tasks",
        "Tag Store": "tag_store.py|run_tag_store_tasks",
        "Payments": (payments, payments.run_payment_tasks),
        "Sales Groups Search Summary Emails": "sales_group_search_summary_emails.py|run_sales_group_search_summary_emails"
    }
    print("Executing main.py")
    db = Database(MYSQL_CONFIG)
    threads = []
    while True:
        # remove any threads that are done executing
        for t in threads:
            if not t.is_alive():
                t.handled = True
            else:
                t.handled = False
        threads = [t for t in threads if not t.handled]

        current_time = datetime.datetime.now().time()

        # this will run once between 2 and 3 AM
        if datetime.time(2, 0, 0) <= current_time < datetime.time(3, 0, 0):
            if not any(t.getName() == "Blockchain" for t in threads):
                job_run_id = JobRuns(db).insert("Blockchain", scheduled_jobs["Blockchain"].split('|')[0], scheduled_jobs["Blockchain"].split('|')[1])
                t = Thread(target=run_bc_tasks, name="Blockchain", args=[job_run_id, Database(MYSQL_CONFIG)])
                t.start()
                threads.append(t)
                print('Main: Appended thread Blockchain', 'Total number of threads:', len(threads), 'Current time:', current_time)
            else:
                print('Main: Blockchain thread already exists. Not appending again.')

        # this will run once between 10 and 11 AM
        if datetime.time(10, 0, 0) <= current_time < datetime.time(11, 0, 0):
            if not any(t.getName() == "Reports" for t in threads):
                job_run_id = JobRuns(db).insert("Reports", scheduled_jobs["Reports"].split('|')[0], scheduled_jobs["Reports"].split('|')[1])
                t = Thread(target=run_report_tasks, name="Reports", args=[job_run_id, Database(MYSQL_CONFIG)])
                t.start()
                threads.append(t)
                print('Main: appended thread Reports', 'Total number of threads:', len(threads), 'Current time:', current_time)

        # this will run once between 7 and 8 AM
        if datetime.time(7, 0, 0) <= current_time < datetime.time(8, 0, 0):
            if not any(t.getName() == "Emails" for t in threads):
                job_run_id = JobRuns(db).insert("Emails", scheduled_jobs["Emails"].split('|')[0], scheduled_jobs["Emails"].split('|')[1])
                t = Thread(target=run_email_tasks, name="Emails", args=[job_run_id, Database(MYSQL_CONFIG)])
                t.start()
                threads.append(t)
                print('Main: appended thread Emails', 'Total number of threads:', len(threads), 'Current time:', current_time)

        # this will run once between 8 and 9 AM
        # if PAYMENTS and datetime.datetime.today().day == 5 and (datetime.time(8, 0, 0) <= current_time < datetime.time(9, 0, 0)):
        #     if not any(t.getName() == "Payments" for t in threads):
        #         job_run_id = JobRuns(db).insert("Payments", scheduled_jobs["Payments"][0].__name__ + ".py", scheduled_jobs["Payments"][1].__name__)
        #         t = Thread(target=scheduled_jobs["Payments"][1], name="Payments", args=[job_run_id, Database(MYSQL_CONFIG), os.path.join(os.getcwd(), "core/templates")])
        #         t.start()
        #         threads.append(t)
        #         print('Main: appended thread Payments', 'Total number of threads:', len(threads), 'Current time:', current_time)

        # this will run once between 9 and 10 AM
        if datetime.time(9, 0, 0) <= current_time < datetime.time(10, 0, 0):
            if not any(t.getName() == "Partners" for t in threads):
                job_run_id = JobRuns(db).insert("Partners", scheduled_jobs["Partners"].split('|')[0], scheduled_jobs["Partners"].split('|')[1])
                t = Thread(target=run_partner_tasks, name="Partners", args=[job_run_id, Database(MYSQL_CONFIG)])
                t.start()
                threads.append(t)
                print('Main: appended thread Partners', 'Total number of threads:', len(threads), 'Current time:', current_time)

        # this will run once between 10 and 11 AM
        if datetime.time(10, 0, 0) <= current_time < datetime.time(11, 0, 0):
            if not any(t.getName() == "Tag Store" for t in threads):
                if HERDWHISTLE_FETCH_EIDS_FROM_API:
                    job_run_id = JobRuns(db).insert("Tag Store", scheduled_jobs["Tag Store"].split('|')[0], scheduled_jobs["Tag Store"].split('|')[1])
                    t = Thread(target=run_tag_store_tasks, name="Tag Store", args=[job_run_id, Database(MYSQL_CONFIG)])
                    t.start()
                    threads.append(t)
                    print('Main: appended thread Tag Store', 'Total number of threads:', len(threads), 'Current time:', current_time)
                else:
                    print("Tag Store thread: Tag Store HerdWhistle EID fetch turned off. Exiting")
                
        # this will run once between 6 and 7 AM
        if datetime.time(6, 0, 0) <= current_time < datetime.time(7, 0, 0):
            if not any(t.getName() == "Tag Store" for t in threads):
                job_run_id = JobRuns(db).insert(
                    "Sales Groups Search Summary Emails",
                    scheduled_jobs["Sales Groups Search Summary Emails"].split('|')[0],
                    scheduled_jobs["Sales Groups Search Summary Emails"].split('|')[1]
                )
                t = Thread(target=run_sales_group_search_summary_emails, name="Sales Groups Search Summary Emails", args=[job_run_id, Database(MYSQL_CONFIG)])
                t.start()
                threads.append(t)
                print('Main: appended thread Sales Groups Search Summary Emails', 'Total number of threads:', len(threads), 'Current time:', current_time)

        print("Main: Sleeping for 60 mins. Current_time:", datetime.datetime.today().strftime('%Y-%m-%d'), current_time)
        time.sleep(3600)
except Exception as e:
    print("Main:", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
    ErrorLogs(db).insert_error_log("Scheduled Jobs (Main thread)", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
finally:
    db.close()
