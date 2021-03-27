from flask import (
    Flask, Blueprint, jsonify, request, g
)
import stripe
from ..database.tables.accounts import AccountsException
from ..database.objects.account import AccountException
from core.config import SUBSCRIPTION_WEBHOOK_SECRET

bp = Blueprint('stripe_bp', __name__)

@bp.route('/stripe/test', methods=['GET'])
def serve_stripe_test():
    return jsonify('<h1>Hello World</h1>')


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

    if event.type != 'customer.subscription.created' and event.type != 'customer.subscription.deleted' \
       and event.type != 'customer.subscription.updated':
        return jsonify({'status': 'This event ' + event.type + ' is not supported.'})

    customer_id = event.data.object.customer  
    #read the customer id and get the account
    try:
        account = g.db.accounts.get_by_stripe_customer_id(customer_id)
    except AccountsException:
        return jsonify({'status': 'No customer found with the stripe customer id: ' + customer_id})

    # found account, now update it as required
    if event.type == 'customer.subscription.created':
        if event.data.object.status == 'active':
            g.db.accounts.update_account(
                account.id(),
                account.name(),
                account.company(),
                account.sector_id(),
                account.token(),
                1,
                account.manual_paid(),
                account.stripe_customer_id()
            )
    elif event.type == 'customer.subscription.deleted':
        g.db.accounts.update_account(
            account.id(),
            account.name(),
            account.company(),
            account.sector_id(),
            account.token(),
            0,
            account.manual_paid(),
            account.stripe_customer_id()
        )
    elif event.type == 'customer.subscription.updated':
        if event.data.object.status == 'past_due':
            g.db.accounts.update_account(
                account.id(),
                account.name(),
                account.company(),
                account.sector_id(),
                account.token(),
                0,
                account.manual_paid(),
                account.stripe_customer_id()
            )

    return jsonify({'status': 'Success'})