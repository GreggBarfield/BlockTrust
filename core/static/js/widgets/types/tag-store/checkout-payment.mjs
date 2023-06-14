import { Widget } from '../../widget.mjs';

export class CheckoutPaymentWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        let publishableKey = this.frame.getAttribute("data-widget-stripe-key");
        let checkoutPaymentPage = this.makeCheckoutPaymentCard();
        this.frame.append(checkoutPaymentPage);
        this.generateStripePaymentElements(publishableKey)
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

        let checkoutPaymentCardbody = document.createElement("div");
        checkoutPaymentCardbody.className = "card-body";
        checkoutPaymentCardbody.id = "checkout-card-element";
        checkoutPaymentCard.append(checkoutPaymentCardbody);

        return checkoutPaymentCard;
    }

    generateStripePaymentElements = (publishableKey) =>{
        const stripe = Stripe(publishableKey);  
        const elements = stripe.elements();
        const card = elements.create('card');
        card.mount('#checkout-card-element');
    }
}