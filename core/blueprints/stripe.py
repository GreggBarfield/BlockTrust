from flask import (
    Blueprint, request, g, session, redirect, url_for
)
from ..utilities.auth import SESSION_STRIPE_ACCOUNT_ID_VAR
import stripe
import json
import traceback
from ..database.tables.accounts import Accounts
from ..database.tables.debug_logs import DebugLogs
from ..database.tables.error_logs import ErrorLogs
from ..common_exceptions import ExportException
from core.config import SUBSCRIPTION_WEBHOOK_SECRET, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_BASIC_PRICE, ACCOUNT_WEBHOOK_SECRET 

bp = Blueprint('stripe_bp', __name__)

stripe.api_key = STRIPE_SECRET_KEY


@bp.route('/stripe/test', methods=['GET'])
def serve_stripe_test():
    return ('<h1>Hello World</h1>')


@bp.route('/stripe/config', methods=['GET'])
def serve_stripe_config():
    return  {
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
            return {
                'price': "${:,.2f}".format(price['unit_amount']/100)
            }
        else:
            return {'error':{'message': 'Incorrect price key'}}, 400    
    except Exception as e:
        return {'error':{'message': str(e)}}, 400


# events to subscribe to: customer.subscription.created, customer.subscription.deleted, customer.subscription.updated
@bp.route('/stripe/subscription', methods=['POST'])
def serve_stripe_subscription():
    endpoint_secret = SUBSCRIPTION_WEBHOOK_SECRET
    sig_header = request.headers.get('stripe-signature')
    payload = json.loads(request.data)
    DebugLogs(g.db).insert_debug_log(
        component="Stripe Webhooks", short_info=f"Event: {payload['type']}",
        long_info=f"Function: {serve_stripe_subscription.__name__}, Stripe signature: {sig_header}, Endpoint secret: {endpoint_secret}",
        details=payload
    )

    try:
        event = stripe.Webhook.construct_event(
            request.data, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise ExportException(str(e))
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise ExportException(str(e))

    try:
        customer_id = event.data.object.customer
        if event.type == 'customer.subscription.created':
            if event.data.object.status == 'active':
                account = g.db.accounts.get_by_stripe_customer_id(customer_id)
                g.db.accounts.update_account(
                    account.id(),
                    stripe_paid=1
                )
        elif event.type == 'customer.subscription.deleted':
            account = g.db.accounts.get_by_stripe_customer_id(customer_id)
            g.db.accounts.update_account(
                account.id(),
                stripe_paid=0
            )
        elif event.type == 'customer.subscription.updated':
            account = g.db.accounts.get_by_stripe_customer_id(customer_id)
            if event.data.object.status == 'past_due':
                g.db.accounts.update_account(
                    account.id(),
                    stripe_paid=0
                )
        else:
            raise ExportException('This event type ' + event.type + ' is not supported.')
    except Exception as e:
        print("Event:", event)
        ErrorLogs(g.db).insert_error_log("Stripe Webhooks", f"No account for customer id: {customer_id}. Event: {event.type}", traceback.format_exc())
        return {'status': 'No customer found with the stripe customer id: ' + customer_id}

    return {'status': 'Success'}


@bp.route('/stripe/create-customer', methods=['POST'])
def create_customer():
    data = json.loads(request.data)
    try:
        if g.account is not None:
            # Create a new customer object
            customer = stripe.Customer.create(
                email=data['email'],
                name=data['name'],
                metadata={'account_id': g.account.id(), 'user_id': g.user.id()}
            )
            # At this point, associate the ID of the Customer object with your
            # own internal representation of a customer, if you have one.            
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
        # Create the subscription
        # only supporting basic price right now       
        if data['priceLookupKey'] == "basic":
            subscription = stripe.Subscription.create(
                default_payment_method=payment_method.id,
                customer=data['customerId'],
                items=[{
                    'price': STRIPE_BASIC_PRICE
                }],
                expand=['latest_invoice.payment_intent'],
            )
            return {'subscription':subscription}
        else:
            return {'error':{'message': 'No or incorrect price selected'}}, 400
    except Exception as e:
        return {'error':{'message': str(e)}}, 400


@bp.route('/stripe/create-payment-intent/<partner_id>', methods=['POST'])
def create_payment(partner_id):
    data = json.loads(request.data)
    try:
        account = g.db.accounts.get_account_by_id(partner_id)
        if account is not None:
            stripe.api_key = account.partner_stripe_secret_key()
            # Some example payment method types include `card`, `ideal`, and `alipay`.
            payment_method_type = data['paymentMethodType']
            currency = data['currency']
            order_id = data['orderId']
            amount = float(data['amount'])*100
            amount = int(amount)
            # Create a PaymentIntent with the amount, currency, and a payment method type.
            params = {
                'payment_method_types': [payment_method_type],
                'amount': amount,
                'currency': currency,
                'metadata': {'order_id':order_id}
            }
            intent = stripe.PaymentIntent.create(**params)

            # Send PaymentIntent details to the front end.
            return {'clientSecret': intent.client_secret}
        else:
            raise Exception("Incorrect partner id.")
    except stripe.error.StripeError as e:
        return {'error': {'message': str(e)}}, 400
    except Exception as e:
        return {'error': {'message': str(e)}}, 400


@bp.route('/stripe/create-payment-intent/sales-group', methods=['POST'])
def create_sales_group_payment():
    data = json.loads(request.data)
    try:
        if len(account := g.db.accounts.get_accounts(id=data['account_id'])) > 0 and account[0]["stripe_account_id"] is not None \
         and account[0]["is_stripe_charges_enabled"] == 1:
            stripe.api_key = STRIPE_SECRET_KEY
            currency = data['currency']
            sales_group_id = data['sales_group_id']
            amount = int(float(data['amount'])*100)
            params = {
                'transfer_data': {
                    'destination': account[0]["stripe_account_id"]
                },
                'automatic_payment_methods': {
                    'enabled': True,
                },
                'application_fee_amount': int(0.1*amount),
                'amount': amount,
                'currency': currency,
                'metadata': {'sales_group_id': sales_group_id}
            }
            intent = stripe.PaymentIntent.create(**params)
            return {'clientSecret': intent.client_secret}
        else:
            raise Exception("There is a problem with this sales group transaction. Please try later.")
    except stripe.error.StripeError as e:
        return {'error': {'message': str(e)}}, 400
    except Exception as e:
        return {'error': {'message': str(e)}}, 400


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
            accounts_table.update_account(account_id=account[0]["id"], is_stripe_charges_enabled=int(stripe_account.charges_enabled))
        else:
            ErrorLogs(g.db).insert_error_log("Stripe", f"An event was received for stripe account id: {stripe_account.id} which doesn't exist")
    else:
        raise ExportException('This event type ' + event.type + ' is not supported.')

    return {}
