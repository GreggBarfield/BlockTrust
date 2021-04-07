from flask import (
    Flask, Blueprint, jsonify, request, g
)
import stripe
from ..database.tables.accounts import AccountsException
from ..database.objects.account import AccountException
from ..common_exceptions import ExportException
from core.config import SUBSCRIPTION_WEBHOOK_SECRET

bp = Blueprint('stripe_bp', __name__)

@bp.route('/stripe/test', methods=['GET'])
def serve_stripe_test():
    return ('<h1>Hello World</h1>')


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
        return jsonify({'error': str(e)})
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': str(e)})

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
        return jsonify({'status': 'This event ' + event.type + ' is not supported.'})

    return jsonify({'status': 'Success'})

def get_account_of_stripe_customer(event):
    #read the customer id and get the account
    customer_id = event.data.object.customer      
    try:
        return g.db.accounts.get_by_stripe_customer_id(customer_id)
    except AccountsException:
        raise ExportException('No customer found with the stripe customer id: ' + customer_id)