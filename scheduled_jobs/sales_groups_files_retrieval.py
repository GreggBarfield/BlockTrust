from core.config import AWS_S3_BUCKET
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.files import Files, SALES_GROUP_FILES_S3_PATH
from core.database.tables.job_runs import JobRuns
from core.database.tables.sales_groups import SalesGroups, SalesGroupsException
from core.database.tables.sales_group_files import SalesGroupFiles
from core.database.tables.users import Users
from core.utilities.aws import aws

import re
import requests
import traceback
import datetime
import time

def run_sales_groups_files_retrieval(job_run_id, db):
    try:
        pending_files = SalesGroupFiles(db).get_sales_group_files_pending_upload()
        for pending_file in pending_files:
            sales_group = SalesGroups(db).get_sales_group_by_id(row_id=pending_file["sales_group_id"])
            if len(pending_file["link"]) != 0 and pending_file["file_id"] is None:
                file_response = requests.get(pending_file["link"])
                if file_response.ok:
                    # Get file name
                    file_content_disposition = file_response.headers["content-disposition"]
                    file_name = re.findall("filename=(.+)",  file_content_disposition)[0]

                    file_id, file_config = Files(db).insert_file_and_get_post_configuration(
                        file_name=file_name,
                        user_id=None,
                        account_id=sales_group["account"],
                        employee_id=None,
                        file_s3_path=SALES_GROUP_FILES_S3_PATH
                    )
                    file_upload_url = file_config["url"]
                    file_upload_fields = file_config["fields"]
                    file_upload_fields["file"] = file_response.content
                    file_upload_to_s3 = requests.post(
                        file_upload_url,
                        files=file_upload_fields
                    )
                    if file_upload_to_s3.ok:
                        SalesGroupFiles(db).update_sales_group_files(id=pending_file["id"], file_id=file_id)
                    else:
                        raise Exception(file_upload_to_s3.text)


        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Sales Groups Files Retrieval Job Exiting. Current time: ", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
    except (SalesGroupsException, Exception) as e:
        ErrorLogs(db).insert_error_log("Sales Groups Files Retrieval", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})