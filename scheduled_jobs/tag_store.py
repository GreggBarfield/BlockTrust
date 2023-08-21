from core.database.tables.animals import Animals
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.account_links import AccountLinks
from core.database.tables.orders import Orders
from core.utilities.shop.herdwhistle_api import HerdWhistleAPI
import traceback
import datetime
import time


def run_tag_store_tasks(job_run_id, db):
    try:
        unprocessed_orders_for_eids = Orders(db).get_orders(has_eids_been_retrieved=0)
        for unprocessed_order in unprocessed_orders_for_eids:
            if unprocessed_order["herdwhistle_sale_order_id"] is not None:
                order_details = HerdWhistleAPI().get_sales_order_details(unprocessed_order["herdwhistle_sale_order_id"])
                if len(order_details) > 0:
                    herdwhistle_order_line_id = order_details[0]["order_line"]
                    products_order_details_with_eids = HerdWhistleAPI().get_sale_order_details_with_eids(herdwhistle_order_line_id)
                    for product_details in products_order_details_with_eids:
                        if product_details['x_studio_tag_sequence_start']:
                            account_links = AccountLinks(db).get_by_account_id(unprocessed_order["account_id"])
                            if len(account_links) > 0:
                                account_link = account_links[0]
                                for eid in range(int(product_details["x_studio_tag_sequence_start"]), int(product_details["x_studio_tag_sequence_end"])+1):
                                    db.matches.types.insert_sighting(
                                        eid=eid,
                                        account_link=account_link.id(),
                                        lat=None,
                                        lon=None,
                                        partner_account=account_link.partner_account_id()
                                    )
                                    Animals(db).create_or_fail_animal(eid=eid)
                                Orders(db).update(id=unprocessed_order["id"], has_eids_been_retrieved=1)
            else:
                Orders(db).update(id=unprocessed_order["id"], has_eids_been_retrieved=1)
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Tag Store Job Exiting. Current time: ", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.now().time())
    except Exception as e:
        ErrorLogs(db).insert_error_log("Tag Store", e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})
