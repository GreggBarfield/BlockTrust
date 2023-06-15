import { Widget } from '../../widget.mjs';
import { generateCheckoutFormTextInput } from '../../utilities/tag_store_utilities.mjs';

export class CheckoutPaymentWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        this.partner_id = 739;
        let  {publishableKey} = await fetch('/stripe/config/'+this.partner_id).then((r) => r.json());
        let checkoutPaymentPage = this.makeCheckoutPaymentCard();
        this.frame.append(checkoutPaymentPage);
        this.prefilleNameInputAndGenerateStripeElements(publishableKey)
    }

    makeCheckoutPaymentCard = () =>{
        let checkoutPaymentCard = document.createElement("div");
        checkoutPaymentCard.className = "card border rounded";

        let checkoutPaymentCardHeader = document.createElement("div");
        checkoutPaymentCardHeader.className = "card-header d-flex justify-content-center p-1";
        let checkoutPaymentCardHeaderText = document.createElement("h3");
        checkoutPaymentCardHeaderText.className = "mt-2 p-1";
        checkoutPaymentCardHeaderText.textContent = "CHECKOUT PAYMENT";
        checkoutPaymentCardHeader.append(checkoutPaymentCardHeaderText);
        checkoutPaymentCard.append(checkoutPaymentCardHeader);

        let checkoutPaymentCardBody = document.createElement("div");
        checkoutPaymentCardBody.className = "card-body col-md-6";

        let checkoutPaymentNameInputContainer = generateCheckoutFormTextInput("*Name", "text", "name", true);
        checkoutPaymentCardBody.append(checkoutPaymentNameInputContainer);

        let checkoutPaymentCardElement = document.createElement("div");
        checkoutPaymentCardElement.id = "checkout-card-element";
        checkoutPaymentCardElement.className = "p-3 m-3 border rounded";
        checkoutPaymentCardBody.append(checkoutPaymentCardElement);

        let checkoutPaymentSubmitButton = document.createElement("button");
        checkoutPaymentSubmitButton.className = "btn btn-primary";
        checkoutPaymentSubmitButton.id = "checkout-payment-submit-button"
        checkoutPaymentSubmitButton.textContent = "SUBMIT";
        checkoutPaymentCardBody.append(checkoutPaymentSubmitButton);
        checkoutPaymentSubmitButton.onclick = () =>{
            this.performStripePaymentActions();
        }

        let checkoutPaymentStatusMessage = document.createElement("div");
        checkoutPaymentStatusMessage.className = "d-none";
        checkoutPaymentStatusMessage.id = "checkout-payment-status-message";
        checkoutPaymentCardBody.append(checkoutPaymentStatusMessage);

        checkoutPaymentCard.append(checkoutPaymentCardBody);
        return checkoutPaymentCard;
    }

    prefilleNameInputAndGenerateStripeElements = (publishableKey) =>{
        if(localStorage.orderDetails){
            let orderDetailsString=localStorage.getItem("orderDetails");
            let orderDetails = JSON.parse(orderDetailsString);
            let checkoutNameInput = document.getElementById("name");
            checkoutNameInput.value = orderDetails['first_name'] + " " + orderDetails['last_name'];
        }
        this.stripe = Stripe(publishableKey);
        let elements = this.stripe.elements();
        this.card = elements.create('card');
        this.card.mount('#checkout-card-element');
    }

    performStripePaymentActions = async () =>{
        let submitButton = document.getElementById("checkout-payment-submit-button");
        this.updatePaymentButton("Processing...", true);
        // Creating a new order
        let {error, orderId} = await fetch(
            '/shop/create-order',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({orderDetails: localStorage.getItem('orderDetails')})
            }
        ).then((r) => r.json());
        if(error){
            this.updatePaymentStatusMessage(error, "text-danger");
            this.updatePaymentButton("Pay", false);
            return;
        }
        // Creating payment intent
        let {error: backendError, clientSecret} = await fetch(
            '/stripe/create-payment-intent/' + this.partner_id,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    currency: 'usd',
                    paymentMethodType: 'card',
                    amount: localStorage.getItem('grandTotal'),
                    orderId: orderId
                }),
            }
        ).then((r) => r.json());
        if(backendError){
            this.updatePaymentStatusMessage(backendError.message, "text-danger");
            this.updatePaymentButton("Pay", false);
            return;
        }
        // Confirming card payment
        let checkoutNameInput = document.getElementById("name");
        let {error: stripeError, paymentIntent} = await this.stripe.confirmCardPayment(
            clientSecret,{
                payment_method: {
                    card: this.card,
                    billing_details: {
                        name: checkoutNameInput.value
                    }
                }
            }
        );
        if(stripeError){
            this.updatePaymentStatusMessage(stripeError.message, "text-danger");
            this.updatePaymentButton("Pay", false);
            return;
        }
        // Updating order as paid
        if(paymentIntent.status === 'succeeded'){
            let {error, success} = await fetch(
                '/shop/update-order',{
                    method: 'POST',
                    header: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        orderId: orderId,
                        paymentIntent: paymentIntent.id,
                        orderDetails: localStorage.getItem("orderDetails")
                    })
                }
            ).then((r) => r.json());
        }
        this.updatePaymentButton("Success! Redirecting...", true);
        window.location.href = '/shop/invoice';
    }

    updatePaymentStatusMessage = (statusTextContent, statusClassName) =>{
        let paymentStatusMessage = document.getElementById("checkout-payment-status-message");
        paymentStatusMessage.style.display = 'block';
        paymentStatusMessage.className = statusClassName;
        paymentStatusMessage.textContent = statusTextContent;
    }

    updatePaymentButton = (buttonTextContent, buttonDisabledStatus) =>{
        let paymentButton = document.getElementById("checkout-payment-submit-button");
        paymentButton.disabled = buttonDisabledStatus;
        paymentButton.textContent = buttonTextContent;
    }
}