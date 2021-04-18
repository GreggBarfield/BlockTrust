from flask import (
    Flask, Blueprint, jsonify, request, g
)
import stripe
import json
from ..database.tables.accounts import AccountsException
from ..database.objects.account import AccountException
from ..common_exceptions import ExportException
from core.config import SUBSCRIPTION_WEBHOOK_SECRET, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_BASIC_PRICE

bp = Blueprint('stripe_bp', __name__)

stripe.api_key = STRIPE_SECRET_KEY


@bp.route('/stripe/test', methods=['GET'])
def serve_stripe_test():
    return ('<h1>Hello World</h1>')


@bp.route('/stripe/config', methods=['GET'])
def serve_stripe_config():
    return jsonify(
        publishableKey=STRIPE_PUBLISHABLE_KEY
    )


#events to subscribe to: customer.subscription.created, customer.subscription.deleted, customer.subscription.updated
@bp.route('/stripe/subscription', methods=['POST'])
def serve_stripe_subscription():
    payload = request.data
    #this should match the signing secret of the webhook set up in Stripe Dashboard
    endpoint_secret = SUBSCRIPTION_WEBHOOK_SECRET
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise ExportException(str(e))
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise ExportException(str(e))

    if event.type == 'customer.subscription.created':
        if event.data.object.status == 'active':
            account = get_account_of_stripe_customer(event)
            g.db.accounts.update_account(
                account.id(),
                stripe_paid=1
            )
    elif event.type == 'customer.subscription.deleted':
        account = get_account_of_stripe_customer(event)
        g.db.accounts.update_account(
            account.id(),
            stripe_paid=0
        )
    elif event.type == 'customer.subscription.updated':
        account = get_account_of_stripe_customer(event)
        if event.data.object.status == 'past_due':
            g.db.accounts.update_account(
                account.id(),
                stripe_paid=0
            )
    else:
        raise ExportException('This event type ' + event.type + ' is not supported.')

    return jsonify({'status': 'Success'})


def get_account_of_stripe_customer(event):
    #read the stripe customer id and get the account
    customer_id = event.data.object.customer      
    try:
        return g.db.accounts.get_by_stripe_customer_id(customer_id)
    except AccountsException:
        raise ExportException('No customer found with the stripe customer id: ' + customer_id)


@bp.route('/stripe/create-customer', methods=['POST'])
def create_customer():
    data = json.loads(request.data)
    try:
        if g.account is not None:
            # Create a new customer object
            customer = stripe.Customer.create(email=data['email'], name=data['name'], metadata={'AccountId':g.account.id()})
            # At this point, associate the ID of the Customer object with your
            # own internal representation of a customer, if you have one.            
            g.db.accounts.update_account(
                g.account.id(),
                stripe_customer_id=customer.id
            )
            resp = jsonify(customer=customer)
            return resp
        else:
            return jsonify(error={'message': "No account selected"}), 400
    except Exception as e:
        return jsonify(error=str(e)), 400


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
            return jsonify(subscription=subscription)
        else:
            return jsonify(error={'message': 'No or incorrect price selected'}), 400
    except Exception as e:
        return jsonify(error={'message': str(e)}), 400