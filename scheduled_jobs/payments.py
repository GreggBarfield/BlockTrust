from datetime import datetime
import os
import time
import traceback
import stripe

from core.config import STRIPE_SECRET_KEY, ROOT
from core.database.combinations import send_email_to_admin_users
from core.database.tables.animals import Animals
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.job_runs import JobRuns
from core.database.tables.matches import Matches
from core.database.tables.payments import PAYMENT_STATUS_NAMES_TO_IDS, Payments
from core.match_types import MATCH_TYPES_NAME_TO_ID
stripe.api_key = STRIPE_SECRET_KEY


def run_payment_tasks(job_run_id, db):
    email_body = """
        <div>
            <p>
                Hello,
                <br><br>
                We wanted to inform you that the following payment has failed:
                <table border="0">
                    <tr><td>Card (last 4): {last_4}</td></tr>
                    <tr><td>Amount: ${amount:.2f}</td></tr>
                    <tr><td>Reason: {reason}</td></tr>
                </table>
            </p>
            <p>
                Please update your card information on the <a href="{link}">payment page</a>
                to continue paying for your cattle in the system.
            </p>
            <p>Thank you.</p>
        </div>
    """
    try:
        accounts_for_charge = db.accounts.get_accounts_for_charge()
        for account in accounts_for_charge:
            if account["stripe_customer_id"]:
                payment_methods = stripe.PaymentMethod.list(
                    customer=account["stripe_customer_id"],
                    type="card",
                )["data"]
                if payment_methods:
                    paid = False
                    payment_intent = None
                    for method in payment_methods:
                        if not paid:
                            try:
                                payment_intent = stripe.PaymentIntent.create(
                                    amount=account["count_eid"]*100,
                                    currency='usd',
                                    customer=account["stripe_customer_id"],
                                    payment_method=method["id"],
                                    off_session=True,
                                    confirm=True,
                                )
                            except stripe.error.CardError as e:
                                err = e.error
                                payment_intent_id = err.payment_intent['id']
                                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                                Payments(db).insert(
                                    account_id=account["id"],
                                    amount=account["count_eid"],
                                    status=PAYMENT_STATUS_NAMES_TO_IDS["failed"],
                                    stripe_customer_id=account["stripe_customer_id"],
                                    stripe_payment_intent_id=payment_intent.id,
                                    stripe_error_code=err.code
                                )
                                stripe.PaymentMethod.detach(method["id"])
                            else:
                                payment_id = Payments(db).insert(
                                    account_id=account["id"],
                                    amount=account["count_eid"],
                                    status=PAYMENT_STATUS_NAMES_TO_IDS["paid"],
                                    paid_date=datetime.now(),
                                    stripe_customer_id=account["stripe_customer_id"],
                                    stripe_payment_intent_id=payment_intent.id
                                )
                                matches = Matches(db).get_matches_with_account_links(
                                    account_links_account_id=account["id"],
                                    matches_restrict_type=MATCH_TYPES_NAME_TO_ID["Sighting"],
                                    matches_cols=("eid",)
                                )
                                for m in matches:
                                    Animals(db).update_animal(eid=m["eid"], is_paid=int(True), payment_id=payment_id)
                                paid = True
                    if not paid:
                        send_email_to_admin_users(
                            db=db,
                            account_id=account["id"],
                            subject="Payment failed",
                            body=email_body.format(
                                reason=payment_intent.last_payment_error.message,
                                last_4=payment_intent.last_payment_error.payment_method.card.last4,
                                amount=account["count_eid"],
                                link=ROOT + "/dashboard/payment"
                            )
                        )
                else:
                    send_payment_reminder(db, account["id"], account["count_eid"])
            else:
                send_payment_reminder(db, account["id"], account["count_eid"])
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print(traceback.format_exc())
        ErrorLogs(db).insert_error_log(os.path.basename(__file__).split('.')[0], e.__class__.__name__ + ": " + str(e), traceback.format_exc())
        JobRuns(db).update_job_run(job_run_id, time.strftime("%Y-%m-%d %H:%M:%S"), {"error": str(e)})


def send_payment_reminder(db, account_id, unpaid_cattle):
    email_body = """
        <div>
            <p>
                Hello,
                <br><br>
                We wanted to inform you that the following payment is pending:
                <table border="0">
                    <tr><td>Total number of cattle: {cattle}</td></tr>
                    <tr><td>Total unpaid cattle: {unpaid_cattle}</td></tr>
                    <tr><td>Amount due: ${amount:.2f}</td></tr>
                </table>
            </p>
            <p>
                Please update your card information on the <a href="{link}">payment page</a>
                to continue paying for your cattle in the system.
            </p>
            <p>Thank you.</p>
        </div>
    """
    send_email_to_admin_users(
        db=db,
        account_id=account_id,
        subject="Payment pending",
        body=email_body.format(
            cattle=Matches(db).get_count_eid_distinct_for_accounts(account_id=account_id),
            unpaid_cattle=unpaid_cattle,
            amount=unpaid_cattle,
            link=ROOT + "/dashboard/payment"
        ),
        add_log=True
    )
