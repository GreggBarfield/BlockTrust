from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.sales_group_searches import SalesGroupSearches
from core.database.tables.sales_groups import SalesGroups
from core.database.tables.scheduled_emails import ScheduledEmails, EMAILS, SCHEDULED_EMAIL_STATUS_NAME_TO_ID
from core.database.tables.users import Users
import traceback
import datetime
import time

def run_sales_group_search_summary_emails(job_run_id, db):
    try:

        searches = SalesGroupSearches(db).get()
        user_based_sales_group_searches = {}
        user_based_sales_group_search_results = {}
        for search in searches:
            if search['user_id'] not in user_based_sales_group_searches:
                user_based_sales_group_searches[search['user_id']] = [search]
                user_based_sales_group_search_results[search['user_id']] = []
            else:
                user_based_sales_group_searches[search['user_id']].append(search)
        results = []
        for user_id, searches in user_based_sales_group_searches.items():
            user_data = Users(db).get_users(id=user_id)
            print(user_data)
            if len(user_data) > 0:
                user_search_results = []
                for search in searches:
                    sales_group_rows = SalesGroups(db).search_within(
                        zip_code=int(search["zip"]),
                        miles=search["radius"],
                        sale_date=time.time(),
                        is_archived=0,
                        categories=search["multi_select_fields"].get("categories", None) if search["multi_select_fields"] else None,
                        breeds=search["multi_select_fields"].get("breeds", None) if search["multi_select_fields"] else None,
                        minimum_weight=search["minimum_weight"] if search["minimum_weight"] else None,
                        maximum_weight=search["maximum_weight"] if search["maximum_weight"] else None,
                        preconditioning_program=search["preconditioning_program"],
                        programs=search["multi_select_fields"].get("programs", None) if search["multi_select_fields"] else None,
                        target_date_description=search["target_date_description"]
                    )
                    user_search_results.extend(list(filter(lambda row: not any(item["id"] == row["id"] for item in results), sales_group_rows)))
                # Convert datetime object so that it is compatible with json.dumps()
                ScheduledEmails(db).insert_scheduled_email(
                    user_id=user_data[0]["id"],
                    email_address=user_data[0]["email"],
                    subject=EMAILS["SALES GROUP SEARCH RESULTS"]["SUBJECT"],
                    variables=user_search_results,
                    template_name="sales_group_search_summary.html",
                    status_id=SCHEDULED_EMAIL_STATUS_NAME_TO_ID["Not Sent"]
                )
                user_based_sales_group_search_results[user_id] = user_search_results
        print(user_based_sales_group_search_results)

        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Emails Job Exiting. Current time: ", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Sales Group Search Summary Email", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})