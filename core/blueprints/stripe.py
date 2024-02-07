from flask import (
    Blueprint, Response, request, g, session, redirect, url_for
)

from core.common_exceptions import ExportException
from core.config import ROOT, SUBSCRIPTION_WEBHOOK_SECRET, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_BASIC_PRICE, ACCOUNT_WEBHOOK_SECRET
from core.database.tables.accounts import Accounts, AccountsException
from core.database.tables.debug_logs import DebugLogs
from core.database.tables.error_logs import ErrorLogs
from core.database.tables.sales_groups import SalesGroups
from core.database.tables.tips import Tips
from core.database.tables.payments import PAYMENT_STATUS_NAMES_TO_IDS, Payments
from core.database.tables.recurring_payments import RECURRING_STATUS_NAMES_TO_IDS, RecurringPayments
from core.renderers.outside import outside_render
from core.utilities.constants import HTTP_NO_CONTENT
from core.utilities.auth import SESSION_STRIPE_ACCOUNT_ID_VAR
from core.utilities import crut

from datetime import datetime
import json
import stripe
import traceback

bp = Blueprint('stripe_bp', __name__)

stripe.api_key = STRIPE_SECRET_KEY


@bp.route('/stripe/test', methods=['GET'])
def serve_stripe_test():
    return ('<h1>Hello World</h1>')


@bp.route('/stripe/config', methods=['GET'])
def serve_stripe_config():
    return {
        'publishableKey': STRIPE_PUBLISHABLE_KEY
    }


@bp.route('/stripe/config/<partner_id>', methods=['GET'])
def serve_stripe_config_for_partner(partner_id):
    account = g.db.accounts.get_account_by_id(partner_id)
    return {
        'publishableKey': account.partner_stripe_publishable_key() 
    }


@bp.route('/stripe/price/<priceLookupKey>', methods=['GET'])
def serve_stripe_price(priceLookupKey):
    try:
        if priceLookupKey == "basic":
            price = stripe.Price.retrieve(
                STRIPE_BASIC_PRICE,
            )
            return {'price': price['unit_amount']}
        else:
            return {'error':{'message': 'Incorrect price key'}}, 400    
    except Exception as e:
        return {'error':{'message': str(e)}}, 400


@bp.route('/stripe/subscription', methods=['POST'])
def serve_stripe_subscription():
    endpoint_secret = SUBSCRIPTION_WEBHOOK_SECRET
    sig_header = request.headers.get('stripe-signature')
    payload = json.loads(request.data)
    DebugLogs(g.db).insert_debug_log(
        component="Stripe",
        short_info=f"Event: {payload.get('type', '')}, customer id: {payload.get('data',{}).get('object',{}).get('customer','')}",
        long_info=f"Function: {serve_stripe_subscription.__name__}, Stripe signature: {sig_header}, Endpoint secret: {endpoint_secret}",
        details=payload
    )

    try:
        event = stripe.Webhook.construct_event(
            request.data, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        ErrorLogs(g.db).insert_error_log("Stripe Webhooks", f"{e.__class__.__name__ } : {str(e)}", traceback.format_exc())
        raise ExportException(str(e))

    error = ""
    if event.type == 'customer.subscription.created':
        if event.data.object.status == 'active':
            # if len(account := Accounts(g.db).get_accounts(stripe_customer_id=customer_id)) > 0:
            #     Accounts(g.db).update_account(account[0]["id"], stripe_paid=1, subscription_start_date=datetime.now(), subscription_end_date=None)
            # else:
            #     error = f"No account for customer id: {customer_id}. Event: {event.type}"
            pass
    elif event.type == 'customer.subscription.deleted':
        # if len(account := Accounts(g.db).get_accounts(stripe_customer_id=customer_id)) > 0:
        #     Accounts(g.db).update_account(account[0]["id"], stripe_paid=0, subscription_end_date=datetime.now())
        # else:
        #     error = f"No account for customer id: {customer_id}. Event: {event.type}"
        subscription_id = event.data.object.id
        recurring_payment = RecurringPayments(g.db).get(stripe_subscription_id=subscription_id)
        if recurring_payment:
            RecurringPayments(g.db).update(
                id=recurring_payment[0]["id"],
                status=RECURRING_STATUS_NAMES_TO_IDS[event.data.object.status],
                end_date=datetime.utcnow()
            )
    elif event.type == 'customer.subscription.updated':
        # if event.data.object.status == 'past_due':
        #     if len(account := Accounts(g.db).get_accounts(stripe_customer_id=customer_id)) > 0:
        #         Accounts(g.db).update_account(account[0]["id"], stripe_paid=0, subscription_end_date=datetime.now())
        #     else:
        #         error = f"No account for customer id: {customer_id}. Event: {event.type}"
        subscription_id = event.data.object.id
        recurring_payment = RecurringPayments(g.db).get(stripe_subscription_id=subscription_id)
        if recurring_payment:
            RecurringPayments(g.db).update(
                id=recurring_payment[0]["id"],
                status=RECURRING_STATUS_NAMES_TO_IDS[event.data.object.status]
            )
    elif event.type == 'invoice.paid':
        subscription_id = event.data.object.subscription
        if subscription_id:
            recurring_payment = RecurringPayments(g.db).get(stripe_subscription_id=subscription_id)
            recurring_payment_id = recurring_payment[0]["id"] if recurring_payment else None
            account_id = recurring_payment[0]["account_id"] if recurring_payment else None
            Payments(g.db).insert(
                account_id=account_id,
                amount=round(event.data.object.amount_paid/100, 2),
                status=PAYMENT_STATUS_NAMES_TO_IDS[event.data.object.status],
                recurring_payment_id=recurring_payment_id,
                paid_date=datetime.utcnow(),
                email=event.data.object.customer_email,
                stripe_customer_id=event.data.object.customer,
                stripe_invoice_id=event.data.object.id
            )
    else:
        raise ExportException('This event type ' + event.type + ' is not supported.')

    if error:
        ErrorLogs(g.db).insert_error_log("Stripe", short_error=error)
        return {'status': error}

    return Response(status=HTTP_NO_CONTENT)


@bp.route('/stripe/create-customer', methods=['POST'])
def create_customer():
    data = json.loads(request.data)
    try:
        if g.account is not None:
            customer = stripe.Customer.create(
                email=data['email'],
                name=data['name'],
                metadata={'account_id': g.account.id(), 'user_id': g.user.id()}
            )
            g.db.accounts.update_account(
                g.account.id(),
                stripe_customer_id=customer.id
            )
            resp = {'customer':customer}
            return resp
        else:
            return {'error':{'message': "No account selected"}}, 400
    except Exception as e:
        return {'error':{'message': str(e)}}, 400


@bp.route('/stripe/create-subscription', methods=['POST'])
def create_subscription():
    data = json.loads(request.data)
    try:
        payment_method = stripe.PaymentMethod.attach(
            data['paymentMethodId'],
            customer=data['customerId'],
        )
        if data['priceLookupKey'] == "basic":
            subscription = stripe.Subscription.create(
                default_payment_method=payment_method.id,
                customer=data['customerId'],
                items=[{
                    'price': STRIPE_BASIC_PRICE
                }],
                expand=['latest_invoice.payment_intent'],
            )
            return {'subscription': subscription}
        else:
            return {'error':{'message': 'No or incorrect price selected'}}, 400
    except Exception as e:
        return {'error':{'message': str(e)}}, 400


@bp.route('/stripe/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = json.loads(request.data)
    try:
        if 'sales_group_id' in data:
            sales_group_id = data['sales_group_id']
            sales_group = SalesGroups(g.db).get_sales_groups(id=sales_group_id)[0]
            customer_id = g.account.stripe_customer_id() if g.account.stripe_customer_id() else _create_customer()
            intent = _create_payment_intent_for_sales_group(
                count=sales_group["reported"]["count"],
                customer_id=customer_id,
                metadata={"sales_group_id": sales_group_id},
                setup_future_usage="off_session"
            )
            payment_id = Payments(g.db).insert(
                account_id=g.account.id(),
                amount=sales_group["reported"]["count"],
                status=PAYMENT_STATUS_NAMES_TO_IDS["unpaid"],
                stripe_customer_id=g.account.stripe_customer_id(),
                stripe_payment_intent_id=intent.id,
            )
            return {'client_secret': intent.client_secret, 'payment_id': payment_id}
        else:
            if 'partner_id' in data:
                account = g.db.accounts.get_account_by_id(data['partner_id'])
                if account is not None:
                    stripe.api_key = account.partner_stripe_secret_key()
                else:
                    raise Exception("Incorrect partner id.")
            else:
                stripe.api_key = STRIPE_SECRET_KEY
            payment_method_type = data['paymentMethodType']
            currency = data['currency']
            order_id = data['orderId']
            amount = float(data['amount'])*100
            amount = int(amount)
            params = {
                'payment_method_types': [payment_method_type],
                'amount': amount,
                'currency': currency,
                'metadata': {'order_id': order_id}
            }
            intent = stripe.PaymentIntent.create(**params)

            return {'clientSecret': intent.client_secret}
    except stripe.error.StripeError as e:
        return {'error': {'message': str(e)}}, 400
    except Exception as e:
        return {'error': {'message': str(e)}}, 400


@bp.route('/stripe/create-payment-intent/sales-group', methods=['POST'])
def create_sales_group_payment():
    data = json.loads(request.data)
    try:
        if len(account := g.db.accounts.get_accounts(id=data['account_id'])) > 0 and account[0]["stripe_account_id"] is not None \
         and account[0]["is_stripe_payouts_enabled"] == 1:
            intent = _create_intent_for_transfer_to_connected_account(
                amount=int(float(data['amount'])*100)*0.96,
                charged_amount=int(float(data['amount'])*100),
                account=account,
                metadata={'sales_group_id': data['sales_group_id']},
                currency=data['currency']
            )
            return {'clientSecret': intent.client_secret}
        else:
            raise Exception("There is a problem with this sales group transaction. Please try later.")
    except stripe.error.StripeError as e:
        return {'error': {'message': str(e)}}, 400
    except Exception as e:
        return {'error': {'message': str(e)}}, 400


@bp.route('/stripe/create-payment-intent/tip/<account_id>', methods=['POST'])
def create_account_payment(account_id):
    input_post_data = json.loads(request.data)
    try:
        if len(account := g.db.accounts.get_accounts(id=account_id)) > 0 and account[0]["stripe_account_id"] is not None \
         and account[0]["is_stripe_payouts_enabled"] == 1:
            charged_amount = round((float(input_post_data['amount']) + 0.3)/0.97, 2)
            tip_id = Tips(g.db).insert_tip(
                account_id, input_post_data['amount'],
                charged_amount, input_post_data["name"],
                input_post_data["email"] if input_post_data["email"] else None,
                input_post_data["phone"] if input_post_data["phone"] else None
            )
            intent = _create_intent_for_transfer_to_connected_account(
                amount=int(float(input_post_data['amount'])*100),
                charged_amount=int(charged_amount*100),
                account=account,
                metadata={'tip_id': tip_id},
                currency=input_post_data['currency']
            )
            Tips(g.db).update_tip(tip_id, stripe_payment_intent_id=intent.id)
            return {'client_secret': intent.client_secret, 'intent_id': intent.id, 'tip_id': tip_id}
        else:
            raise Exception("Your tip cannot be sent currently. Please try later.")
    except stripe.error.StripeError as e:
        Tips(g.db).update_tip(tip_id, stripe_error=str(e))
        return {'error': {'message': str(e)}}, 400
    except Exception as e:
        return {'error': {'message': str(e)}}, 400


def _create_intent_for_transfer_to_connected_account(amount, charged_amount, account, metadata, currency):
    stripe.api_key = STRIPE_SECRET_KEY
    params = {
        'transfer_data': {
            'amount': amount,
            'destination': account[0]["stripe_account_id"]
        },
        'automatic_payment_methods': {
            'enabled': True,
        },
        'amount': charged_amount,
        'currency': currency,
        'metadata': metadata
    }
    return stripe.PaymentIntent.create(**params)


@bp.route('/stripe/onboard-account', methods=['POST'])
def onboard_account():
    try:
        stripe_account = stripe.Account.create(
            type='express',
            country='US',
            capabilities={
                'transfers': {'requested': True}
            },
            business_type='company',
            company={
                'name': g.account.company()
            },
            metadata={'internal_account_id': g.account.id(), 'created_by_user': g.user.id()}
        )

        session[SESSION_STRIPE_ACCOUNT_ID_VAR] = stripe_account.id
        Accounts(g.db).update_account(account_id=g.account.id(), stripe_account_id=stripe_account.id)

        origin = request.headers['origin']
        account_link_url = _generate_account_link(stripe_account.id, origin)  
        return {'url': account_link_url}
    except Exception as e:
        return {'error': str(e)}, 403


@bp.route('/stripe/onboard-account/complete', methods=['GET'])
def onboard_account_complete():
    if SESSION_STRIPE_ACCOUNT_ID_VAR in session:
        account_id = session[SESSION_STRIPE_ACCOUNT_ID_VAR]
    else:
        account_id = g.account.stripe_account_id()

    origin = ('https://' if request.is_secure else 'http://') + request.headers['host']
    account_link_url = _generate_account_link(account_id, origin)
    return {'url': account_link_url}


@bp.route('/stripe/onboard-account/refresh', methods=['GET'])
def onboard_account_refresh():
    if SESSION_STRIPE_ACCOUNT_ID_VAR not in session:
        return redirect(url_for('dashboard_bp.serve_edit_account'))

    account_id = session[SESSION_STRIPE_ACCOUNT_ID_VAR]

    origin = ('https://' if request.is_secure else 'http://') + request.headers['host']
    account_link_url = _generate_account_link(account_id, origin)
    return redirect(account_link_url)


def _generate_account_link(stripe_account_id, origin):
    account_link = stripe.AccountLink.create(
        type='account_onboarding',
        account=stripe_account_id,
        refresh_url=f'{origin}/{url_for("stripe_bp.onboard_account_refresh")}',
        return_url=f'{origin}/{url_for("dashboard_bp.serve_edit_account")}?stripe_onboarding=1',
    )
    return account_link.url


@bp.route('/stripe/connect/account-events', methods=['POST'])
def serve_stripe_account():
    payload = request.data
    endpoint_secret = ACCOUNT_WEBHOOK_SECRET
    sig_header = request.headers.get('stripe-signature')

    DebugLogs(g.db).insert_debug_log("Stripe", "Connect web hook received", f"Stripe signature: {sig_header}, Endpoint secret: {endpoint_secret}",
                                     json.dumps(json.loads(request.data)))

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        ErrorLogs(g.db).insert_error_log("Stripe", "Connect web hook received", str(e), json.dumps(json.loads(request.data)))
        raise ExportException(str(e))
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        ErrorLogs(g.db).insert_error_log("Stripe", "Connect web hook received", str(e))
        raise ExportException(str(e))

    if event.type == 'account.updated':
        stripe_account = event.data.object
        accounts_table = Accounts(g.db)
        if len(account := accounts_table.get_accounts(stripe_account_id=stripe_account.id)) > 0:
            accounts_table.update_account(account_id=account[0]["id"], is_stripe_payouts_enabled=int(stripe_account.charges_enabled))
        else:
            ErrorLogs(g.db).insert_error_log("Stripe", f"An event was received for stripe account id: {stripe_account.id} which doesn't exist")
    else:
        raise ExportException('This event type ' + event.type + ' is not supported.')

    return {}


@bp.route('/payment/', defaults={'payment_id': ''}, methods=['GET'])
@bp.route('/payment/<int:payment_id>', methods=['GET'])
def serve_payment(payment_id):
    if payment_id and (payment := Payments(g.db).get(
        id=payment_id, status=PAYMENT_STATUS_NAMES_TO_IDS["unpaid"]
    )):
        payment = payment[0]
        product_data = {'name': payment["reason"]}
        if payment["description"]:
            product_data["description"] = payment["description"]
        session = stripe.checkout.Session.create(
            client_reference_id=payment['account_id'],
            customer_creation='if_required',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': product_data,
                    'unit_amount': int(payment["amount"])*100,
                },
                'quantity': 1,
            }],
            mode='payment',
            metadata={'payment_id': payment_id},
            success_url=(ROOT + url_for('stripe_bp.serve_payment_success')
                         + "?session_id={CHECKOUT_SESSION_ID}")
        )
        return redirect(session.url, code=303)
    raise ExportException("Invalid Payment Link")


@bp.route('/payment/success', methods=['GET'])
def serve_payment_success():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    if session.metadata.get("payment_id", None):
        Payments(g.db).update(
            id=session.metadata["payment_id"],
            status=PAYMENT_STATUS_NAMES_TO_IDS[session.payment_status],
            stripe_checkout_id=request.args.get('session_id'),
            stripe_customer_id=session.customer,
            paid_date=datetime.utcnow(),
            email=session.customer_details.email
        )
    else:
        recurring_payment = RecurringPayments(g.db).get(id=session.metadata["recurring_payment_id"])[0]
        RecurringPayments(g.db).update(
            id=recurring_payment["id"],
            status=RECURRING_STATUS_NAMES_TO_IDS['active'],
            stripe_checkout_id=session.id,
            stripe_customer_id=session.customer,
            stripe_subscription_id=session.subscription,
            start_date=datetime.utcnow(),
            email=session.customer_details.email
        )
        account = g.db.accounts.get_accounts(id=recurring_payment["account_id"])[0]
        if not account["stripe_customer_id"]:
            g.db.accounts.update_account(account_id=account["id"], stripe_customer_id=session.customer)
        if payment := Payments(g.db).get(stripe_invoice_id=session.invoice):
            Payments(g.db).update(
                id=payment[0]["id"],
                stripe_checkout_id=session.id,
                stripe_customer_id=session.customer,
                paid_date=datetime.utcnow(),
                email=session.customer_details.email,
                recurring_payment_id=session.metadata["recurring_payment_id"]
            )

    return outside_render("message.html", {
            "heading": "Payment successful",
            "sub_heading": f"Thank you for the payment, {session.customer_details.name}!"
        }
    )


@bp.route('/recurring-payment/', defaults={'recurring_payment_id': ''}, methods=['GET'])
@bp.route('/recurring-payment/<int:recurring_payment_id>', methods=['GET'])
def serve_recurring_payment(recurring_payment_id):
    if recurring_payment_id and (recurring_payment := RecurringPayments(g.db).get(
        id=recurring_payment_id, status=RECURRING_STATUS_NAMES_TO_IDS["unpaid"]
    )):
        recurring_payment = recurring_payment[0]
        product_data = {'name': recurring_payment["reason"]}
        if recurring_payment["description"]:
            product_data["description"] = recurring_payment["description"]
        price_data = {
            'currency': 'usd',
            'product_data': product_data,
            'unit_amount': int(recurring_payment["amount"])*100,
            'recurring': {
                'interval': recurring_payment["recurring_interval"]
            }
        }
        account = g.db.accounts.get_accounts(id=recurring_payment["account_id"])[0]
        customer_id = account["stripe_customer_id"] if account["stripe_customer_id"] else None
        session = stripe.checkout.Session.create(
            client_reference_id=recurring_payment['account_id'],
            line_items=[{'price_data': price_data, 'quantity': 1}],
            mode="subscription",
            customer=customer_id,
            metadata={"recurring_payment_id": recurring_payment["id"]},
            subscription_data={"metadata": {"recurring_payment_id": recurring_payment["id"]}},
            success_url=(ROOT + url_for('stripe_bp.serve_payment_success')
                         + "?session_id={CHECKOUT_SESSION_ID}")
        )
        return redirect(session.url, code=303)
    raise ExportException("Invalid Payment Link")


@crut.require_account
@bp.route('/stripe/setup-payment', methods=['GET'])
def setup_payment():
    try:
        payment_methods = []
        if not g.account.stripe_customer_id():
            customer_id = _create_customer()
        else:
            customer_id = g.account.stripe_customer_id()
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card",
            )["data"]

        intent = stripe.SetupIntent.create(customer=customer_id)
        return {'client_secret': intent.client_secret, "number_of_payment_methods": len(payment_methods)}
    except Exception as e:
        raise ExportException(str(e))


@bp.route('/payment/sales_group', methods=['POST'])
@crut.require_account
def serve_sales_group_payment():
    data = json.loads(request.data)
    sales_group_id = int(data["id"])
    if "payment_id" in data:
        payment_id = int(data["payment_id"])
        Payments(g.db).update(id=payment_id, paid_date=datetime.now(), status=PAYMENT_STATUS_NAMES_TO_IDS["paid"])
        SalesGroups(g.db).update_sales_group(
            id=sales_group_id, published=int(True), is_paid=int(True), payment_id=payment_id
        )
        return redirect(url_for("dashboard_bp.serve_view_sales_group", sales_group_id=sales_group_id))
    else:
        if g.account.stripe_customer_id():
            payment_methods = stripe.PaymentMethod.list(
                customer=g.account.stripe_customer_id(),
                type="card",
            )["data"]
            if len(payment_methods):
                sales_group = SalesGroups(g.db).get_sales_groups(id=sales_group_id)[0]
                is_paid = False
                for method in payment_methods:
                    if not is_paid:
                        try:
                            payment_intent = _create_payment_intent_for_sales_group(
                                count=sales_group["reported"]["count"],
                                customer_id=g.account.stripe_customer_id(),
                                metadata={"sales_group_id": sales_group_id},
                                payment_method_id=method["id"],
                                confirm=True
                            )
                            payment_id = Payments(g.db).insert(
                                account_id=g.account.id(),
                                amount=sales_group["reported"]["count"],
                                status=PAYMENT_STATUS_NAMES_TO_IDS["paid"],
                                paid_date=datetime.now(),
                                stripe_customer_id=g.account.stripe_customer_id(),
                                stripe_payment_intent_id=payment_intent.id,
                                stripe_payment_method_id=method["id"]
                            )
                            SalesGroups(g.db).update_sales_group(
                                id=sales_group_id, published=int(True), is_paid=int(True), payment_id=payment_id
                            )
                            is_paid = True
                        except stripe.error.CardError as e:
                            err = e.error
                            payment_intent_id = err.payment_intent['id']
                            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                            Payments(g.db).insert(
                                account_id=g.account.id(),
                                amount=sales_group["reported"]["count"],
                                status=PAYMENT_STATUS_NAMES_TO_IDS["failed"],
                                stripe_customer_id=g.account.stripe_customer_id(),
                                stripe_payment_intent_id=payment_intent.id,
                                stripe_error_code=err.code,
                                stripe_payment_method_id=method["id"]
                            )
                            stripe.PaymentMethod.detach(method["id"])
                if is_paid:
                    return redirect(url_for("dashboard_bp.serve_view_sales_group", sales_group_id=sales_group_id))
        return redirect(url_for("dashboard_bp.serve_payment", id=sales_group_id))


def _create_payment_intent_for_sales_group(count, customer_id, metadata, payment_method_id=None, confirm=False,
                                           setup_future_usage=None):
    params = {
        "amount": count*100,
        "currency": "usd",
        "customer": customer_id,
        "metadata": metadata,
        "payment_method_types": ["card"]
    }
    if payment_method_id:
        params["payment_method"] = payment_method_id
    if confirm:
        params["confirm"] = True
    if setup_future_usage:
        params["setup_future_usage"] = setup_future_usage

    return stripe.PaymentIntent.create(**params)


def _create_customer():
    customer_id = stripe.Customer.create(
        email=g.user.email() if g.user.is_email_verified() else None,
        name=g.account.company(),
        metadata={'account_id': g.account.id(), 'user_id': g.user.id()}
    ).id
    g.db.accounts.update_account(
        g.account.id(),
        stripe_customer_id=customer_id
    )
    return customer_id
