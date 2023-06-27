import { Widget } from '../../widget.mjs';
import { makeShoppingCartTotalsContainer, generateCheckoutFormTextInput } from '../../utilities/tag_store_utilities.mjs';

export class CheckoutPaymentWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        let publishableKey = this.frame.getAttribute("data-widget-stripe-key");
        let checkoutPaymentCard = this.makeCheckoutPaymentCard();
        this.frame.append(checkoutPaymentCard);
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
        checkoutPaymentCardBody.className = "card-body d-flex";

        let paymentContainer = document.createElement("div");
        paymentContainer.className = "col-md-6 p-0 m-0";
        
        let totalsContainer = document.createElement("div");
        totalsContainer.className = "col-md-6 p-0 m-0";

        let cartTotalsContainer = makeShoppingCartTotalsContainer();
        totalsContainer.append(cartTotalsContainer);

        let checkoutPaymentNameInputContainer = generateCheckoutFormTextInput("*Name", "text", "name", true);
        paymentContainer.append(checkoutPaymentNameInputContainer);

        let checkoutPaymentCardElement = document.createElement("div");
        checkoutPaymentCardElement.id = "checkout-card-element";
        checkoutPaymentCardElement.className = "p-3 m-3 border rounded";
        paymentContainer.append(checkoutPaymentCardElement);

        let checkoutPaymentSubmitButton = document.createElement("button");
        checkoutPaymentSubmitButton.className = "btn btn-primary m-3";
        checkoutPaymentSubmitButton.id = "checkout-payment-submit-button"
        checkoutPaymentSubmitButton.textContent = "SUBMIT";
        paymentContainer.append(checkoutPaymentSubmitButton);
        checkoutPaymentSubmitButton.onclick = () =>{
            this.performStripePaymentActions();
        }

        let checkoutPaymentStatusMessage = document.createElement("div");
        checkoutPaymentStatusMessage.className = "d-none";
        checkoutPaymentStatusMessage.id = "checkout-payment-status-message";
        paymentContainer.append(checkoutPaymentStatusMessage);
        checkoutPaymentCardBody.append(paymentContainer);
        checkoutPaymentCardBody.append(totalsContainer);

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
            this.updatePaymentStatusMessage(error, "d-block mt-2 mb-0 alert alert-danger");
            this.updatePaymentButton("Pay", false);
            return;
        }
        // Creating payment intent
        let {error: backendError, clientSecret} = await fetch(
            '/stripe/create-payment-intent',{
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
            this.updatePaymentStatusMessage(backendError.message, "d-block mt-2 mb-0 alert alert-danger");
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
            this.updatePaymentStatusMessage(stripeError.message, "d-block mt-2 mb-0 alert alert-danger");
            this.updatePaymentButton("Pay", false);
            return;
        }
        // Updating order as paid
        if(paymentIntent.status === 'succeeded'){
            let response = await fetch(
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
            );
            if(response.ok){
                this.updatePaymentButton("Success! Redirecting...", true);
            }
        }
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