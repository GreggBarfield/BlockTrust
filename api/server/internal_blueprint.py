import json
import os
import gzip


from flask import (
    Flask, jsonify, request, session, Blueprint, g, redirect
)


from core.database.tables.job_runs import JobRuns
from core.database.database import Database
from core.config import MYSQL_CONFIG, API_MYSQL_CONFIG, INTERNAL_API_SECRET
from core.common_exceptions import ExportException
import time

bp = Blueprint('internal_blueprint', __name__)
THREE_YEARS = 60 * 60 * 24 * 365 * 3


@bp.before_request
def before_request():
    """Per-request setup."""
    g.db = Database(MYSQL_CONFIG)

# this is not a good solution ... actually the start date has to be determined by the intermediate program not over here in the API
# intermediate has to send us the unix time from which the window starts

@bp.route('/api/ils-eids/<secret>', methods=["POST", "GET"])
def serve_ils_eids(secret):

    if secret != INTERNAL_API_SECRET:
        print(secret)
        raise ExportException("Bad internal API secret")

    window_start = request.args.get('WindowStart', None)

    
    # job_runs_data_access = JobRuns(g.db)
    # last_job_run = job_runs_data_access.get_job_runs(routine="serve_ils_eids", job_ended_successfully=True, selectColumns=("id", "routine", "unix_timestamp(created_timestamp) AS created"),
    #                     sort_and_order="id DESC", limit=1)
    # print("last job run", last_job_run)
    # if len(last_job_run) > 0:
    #     # datetime.datetime.strptime()
    #     window_start = last_job_run[0]["created"]
    # else:
    #     window_start = time.time() - THREE_YEARS
    
    # job_run_id = job_runs_data_access.insert(request.path, "internal_blueprint.py", "serve_ils_eids")
    eids = g.db.matches.get_ils_eids(window_start)
    # job_runs_data_access.update_job_run(job_run_id, end_timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))
    # list_of_eid_tuples =  list(map(lambda x: (x), eids))
    # update_matches_as_sent_to_ils(list_of_eid_tuples)

    return {
        "eids": eids
    }, 200
