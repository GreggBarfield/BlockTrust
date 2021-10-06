from core.config import (BLOCKCHAIN_BATCH_SIZE, BLOCKCHAIN_UPLOADS)
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
import traceback
from core.utilities.blockchain import blockchain_helper
import datetime
import time


class Blockchain:
    """Class for blockchain related tasks"""

    def __init__(self, db):
        self._db = db

    def insert_matches_to_bc(self):
        if not BLOCKCHAIN_UPLOADS:
            print("Blockchain thread: Blockchain uploads turned off, exiting")
            return
        while(True):
            matches_to_be_uploaded = self.get_next_batch_of_matches(BLOCKCHAIN_BATCH_SIZE)
            if len(matches_to_be_uploaded) > 0:
                hashes = []
                hash_and_match_ids = []
                for m in matches_to_be_uploaded:
                    match = {
                            "eid": m["eid"],
                            "visual_id": m["visual_id"],
                            "type": m["type"],
                            "grouping_id": m["grouping_id"],
                            "data": m["data"],
                            "partner_account": m["partner_account"],
                            "account_link": m["account_link"],
                            "lat": m["lat"],
                            "lon": m["lon"],
                            "time": m["time"]
                        }
                    hash = blockchain_helper.generate_bc_hash(match)
                    hashes.append(hash)
                    hash_and_match_ids.append((hash, m["id"]))

                bc_transaction_id = blockchain_helper.transmit(hashes)
                # update matches rows with corresponding transaction id and hash
                hash_transaction_and_match_ids = list(map(lambda x: (x[0], bc_transaction_id, x[1]), hash_and_match_ids))
                self.update_matches_with_bc_data(hash_transaction_and_match_ids)
            else:
                print("Blockchain thread: No records left to upload and so exiting")
                break

    def get_next_batch_of_matches(self, size):
        query = "SELECT * FROM matches WHERE bc_upload=0 ORDER BY id LIMIT " + str(size)
        match_rows = self._db.execute_d(query)
        return match_rows

    def update_matches_with_bc_data(self, hash_and_ids):
        query = "UPDATE matches SET bc_hash=%s, bc_transaction_id=%s, bc_upload=1 WHERE id=%s"
        self._db.execute_many(query, hash_and_ids)
        return self._db.row_count()


def run_bc_tasks(job_run_id, db):
    try:
        bc = Blockchain(db)
        bc.insert_matches_to_bc()
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Blockchain Job Exiting. Current time: ",  datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Blockchain", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
    finally:
        db.close()
