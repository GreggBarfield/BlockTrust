import { Widget } from '../../widget.mjs';

export class SubscribeWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    async initType() {
        this.frame.innerHTML = "";

        this.inputs = {};

        await this.generate();
    }

    async generate() {     
        const params = new URLSearchParams(window.location.search);
        const priceLookupKey = params.get('price');
        let priceHeader = document.createElement("h5")
        priceHeader.className = "text-warning";
        let {price} = await fetch("/stripe/price/" + priceLookupKey).then(r => r.json());
        if(price) {
          priceHeader.textContent = "You will be charged: " + price;
        }
        this.frame.append(priceHeader);

        this.form = document.createElement("form");
   
        let firstFormRow = document.createElement("div");
        firstFormRow.className = "form-row";
        this.form.append(firstFormRow);

        let nameFormGroup = document.createElement("div");
        nameFormGroup.className = "form-group col-md-6";
        firstFormRow.append(nameFormGroup);
        
        let nameLabel = document.createElement("label");
        nameLabel.textContent = "Name";
        nameFormGroup.append(nameLabel);
        
        this.inputs.name = document.createElement("input");
        this.inputs.name.className = "form-control";
        this.inputs.name.placeholder = "Name";
        nameFormGroup.append(this.inputs.name);

        let emailFormGroup = document.createElement("div");
        emailFormGroup.className = "form-group col-md-6";
        firstFormRow.append(emailFormGroup);

        let emailLabel = document.createElement("label");
        emailLabel.textContent = "Email";
        emailFormGroup.append(emailLabel);

        this.inputs.email = document.createElement("input");
        this.inputs.email.className = "form-control";
        this.inputs.email.placeholder = "Email";
        emailFormGroup.append(this.inputs.email);

        let cardFormGroup = document.createElement("div");
        cardFormGroup.className = "form-group col-md-6";
        firstFormRow.append(cardFormGroup);

        let cardLabel = document.createElement("label");
        cardLabel.textContent = "Credit card";
        cardFormGroup.append(cardLabel);
        let cardElementDiv = document.createElement("div");
        cardElementDiv.id = "card-element";
        cardFormGroup.append(cardElementDiv);
              
        // Initialize an instance of Stripe
        const {publishableKey} = await fetch("/stripe/config").then(r => r.json());
        const stripe = Stripe(publishableKey);

        // Create and mount the single line card element
        this.frame.append(this.form);
        const elements = stripe.elements();
        const cardElement = elements.create('card');
        cardElement.mount(cardElementDiv);

        let termsAndConditionsFormGroup = document.createElement("div");
        termsAndConditionsFormGroup.className = "col-md-12 m-1";
        firstFormRow.append(termsAndConditionsFormGroup);

        let termsAndConditionsLabel = document.createElement("label");
        termsAndConditionsLabel.className = "row m-1";
        termsAndConditionsLabel.textContent = "Please read these documents and check the box saying you understand and agree with the terms and conditions within: ";
        termsAndConditionsFormGroup.append(termsAndConditionsLabel);

        let documentsList = document.createElement("ul");
        let firstDocument = document.createElement("li");
        firstDocument.appendChild(this.generateLinkElement("BlockTrust Network EULA", "/dashboard/files/BTN_EULA.pdf"));
        documentsList.append(firstDocument);
        let secondDocument = document.createElement("li");
        secondDocument.appendChild(this.generateLinkElement("BlockTrust Network Privacy", "/dashboard/files/BTN_PRIVACY.pdf"));
        documentsList.append(secondDocument);
        let thirdDocument = document.createElement("li");
        thirdDocument.appendChild(this.generateLinkElement("BlockTrust Network Terms of Service", "/dashboard/files/BTN_TERMS_OF_SERVICE.pdf"));
        documentsList.append(thirdDocument);
        termsAndConditionsFormGroup.append(documentsList);

        let termsAndConditionsCheckboxGroup = document.createElement("div");
        termsAndConditionsCheckboxGroup.className = "row m-1";
        this.inputs.termsAndConditionsCheckbox = document.createElement("input");
        this.inputs.termsAndConditionsCheckbox.type = "checkbox";
        termsAndConditionsCheckboxGroup.append(this.inputs.termsAndConditionsCheckbox);

        let termsAndConditionsCheckboxLabel = document.createElement("label");
        termsAndConditionsCheckboxLabel.className = "m-1";
        termsAndConditionsCheckboxLabel.textContent = "I have read these documents and agree.";
        termsAndConditionsCheckboxGroup.append(termsAndConditionsCheckboxLabel);

        termsAndConditionsFormGroup.append(termsAndConditionsCheckboxGroup);

      
        this.submitButton = document.createElement("button");
        this.submitButton.className = "btn btn-primary";
        this.submitButton.textContent = "Subscribe";
        this.submitButton.addEventListener("click", (e)=>{
            e.preventDefault();
            this.subscribe(stripe, cardElement, priceLookupKey);
        });        
        this.form.append(this.submitButton);
      
        this.loadingAction = document.createElement("div");
        this.loadingAction.style.display = "none";
        this.form.append(this.loadingAction);

        this.searchErrorAlert = document.createElement("div");
        this.searchErrorAlert.className = "alert alert-danger";
        this.searchErrorAlert.style.display = "none";
        this.form.append(this.searchErrorAlert);    
        
        this.disableSubmitButtonIfIncorrectPrice(priceLookupKey);   
    }

    showError(error) {
        this.searchErrorAlert.style.display = "block";
        this.searchErrorAlert.textContent = error;
    }

    generateLinkElement(linkText, linkURL){
      let link = document.createElement("a");
      link.className = "m-1";
      link.href = linkURL;
      link.textContent  = linkText;
      link.target = "_blank";
      return link;
    }

    disableSubmitButtonIfIncorrectPrice(priceLookupKey) {
      //only supporting basic price right now
      if(priceLookupKey != "basic") {
        this.submitButton.disabled = true;
        this.showError("No or incorrect price selected.");
      }
    }

    async subscribe(stripe, cardElement, priceLookupKey) {

        if (this.inputs.name.value == "") {
            this.showError("Name is required.");
            return;
        }
        if(this.inputs.email.value == "") {
            this.showError("Email is required.");
            return;
        }
        if(this.inputs.termsAndConditionsCheckbox.checked == false){
            this.showError("Please check the Terms and Conditions");
            return;
        }
        //display appropriate alerts
        this.loadingAction.style.display = "inline-block";
        this.loadingAction.innerHTML = '\
          <div class="d-flex justify-content-center">\
              <div class="spinner-border" role="status">\
                  <span class="sr-only">Loading...</span>\
              </div>\
          </div>';
        this.submitButton.textContent = "Subscribing..."

        var error, paymentMethod, customer, subscription, paymentIntent;
        // Tokenize the payment method.
        // This makes a client side API call to Stripe to pass the payment
        // details and returns either an error or a new paymentMethod object that
        // we'll pass when creating the Subscription.
         let {} = {error, paymentMethod} = await stripe.createPaymentMethod({
          type: 'card',
          card: cardElement,
          billing_details: {
            name: this.inputs.name.value,
          }
        });

        if(error) {
            // show error and collect new card details.
            this.showError(error.message);
            this.loadingAction.style.display = "none";
        } else {

            // Create a customer. 
            let {} = {error, customer} = await fetch('/stripe/create-customer', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                email: this.inputs.email.value,
                name: this.inputs.name.value
              }),
            }).then(r => r.json());   
            
            if(error) {
              this.showError(error.message);
              this.loadingAction.style.display = "none";
              return;
            }

            // Create the subscription.
             let {} = {error, subscription} = await fetch('/stripe/create-subscription', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                priceLookupKey,
                paymentMethodId: paymentMethod.id,
                customerId : customer.id
              }),
            }).then((response) => response.json());
            
            if(error) {
                this.showError(error.message);
                this.loadingAction.style.display = "none";
                return;
            }

            switch(subscription.status) {
                case 'active':
                    this.submitButton.textContent = "Subscribed! Redirecting…";
                    break;
                case 'incomplete':
                    this.showError("Please confirm the payment.");
                    // Handle next actions
                    // If the status of the subscription is `incomplete` that means
                    // there are some further actions required by the customer. In
                    // the case of upfront payment the payment is confirmed
                    // by passing the client_secret of the subscription's latest_invoice's
                    // payment_intent.
                    let {} = {error, paymentIntent} = await stripe.confirmCardPayment(
                    subscription.latest_invoice.payment_intent.client_secret,
                    )
                    if(error) {
                        this.showError(error.message);
                    } else {
                        this.submitButton.textContent = "Subscribed! Redirecting…";
                    }
                    break;
                default:
                    this.showError(`Unknown Subscription status: ${subscription.status}`);
            }
            this.loadingAction.style.display = "none";     
        }
    }
}
