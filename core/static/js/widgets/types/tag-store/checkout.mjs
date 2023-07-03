import { Widget } from '../../widget.mjs';
import { states } from '../../../core/common_constants.mjs';
import { generateButtonLink, makeShoppingCartTotalsContainer, validateFormCompletion } from '../../utilities/tag_store_utilities.mjs';

export class CheckoutWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        this.inputs = {};
        this.inputs.firstNameInput = {};
        this.inputs.lastNameInput = {}
        this.inputs.companyInput = {};
        this.inputs.addressInput = {};
        this.inputs.cityInput = {};
        this.inputs.stateInput = {};
        this.inputs.zipCodeInput = {};
        this.inputs.phoneInput = {};
        this.inputs.emailInput = {};
        this.inputValues = {};
        this.inputValues.firstName = this.frame.getAttribute("data-widget-first-name");
        this.inputValues.lastName = this.frame.getAttribute("data-widget-last-name");
        this.inputValues.company = this.frame.getAttribute("data-widget-company-name");
        this.inputValues.address = this.frame.getAttribute("data-widget-address");
        this.inputValues.city = this.frame.getAttribute("data-widget-city");
        this.inputValues.state = this.frame.getAttribute("data-widget-state");
        this.inputValues.zipCode = this.frame.getAttribute("data-widget-zip");
        this.inputValues.phone = this.frame.getAttribute("data-widget-phone");
        let checkoutPage = this.makeCheckoutPage();
        this.frame.append(checkoutPage);
    }

    makeCheckoutPage = () =>{
        let checkoutPageCard = document.createElement("div");
        checkoutPageCard.className = "card border rounded";

        let checkoutPageCardHeader = document.createElement("div");
        checkoutPageCardHeader.className = "card-header d-flex justify-content-center p-1";
        let checkoutPageCardHeaderText = document.createElement("h3");
        checkoutPageCardHeaderText.className = "mt-2 p-1";
        checkoutPageCardHeaderText.textContent = "CHECKOUT";
        checkoutPageCardHeader.append(checkoutPageCardHeaderText);
        checkoutPageCard.append(checkoutPageCardHeader);

        let checkoutPageCardBody = document.createElement("div");
        checkoutPageCardBody.className = "card-body row";

        let checkoutFormContainer = document.createElement("div");
        checkoutFormContainer.className = "col-md-9";
        let checkoutForm = this.makeCheckoutForm();
        checkoutFormContainer.append(checkoutForm);
        checkoutPageCardBody.append(checkoutFormContainer);

        let checkoutPageTotalsAndLinksContainer = document.createElement("div");
        checkoutPageTotalsAndLinksContainer.className = "col-md-3 col";
        let shoppingCartTotals = makeShoppingCartTotalsContainer();
        checkoutPageTotalsAndLinksContainer.append(shoppingCartTotals);
        let checkoutPageLinksContainer = this.makeCheckoutPageLinksContainer();
        checkoutPageTotalsAndLinksContainer.append(checkoutPageLinksContainer);
        checkoutPageCardBody.append(checkoutPageTotalsAndLinksContainer);
        
        checkoutPageCard.append(checkoutPageCardBody);
        return checkoutPageCard;
    }

    makeCheckoutForm = () =>{
        let checkoutFormContainer = document.createElement("div");

        let checkoutFormContainerHeader = document.createElement("h4");
        checkoutFormContainerHeader.className = "card-header p-3";
        checkoutFormContainerHeader.textContent = "SHIPPING INFORMATION";
        checkoutFormContainer.append(checkoutFormContainerHeader);

        let checkoutFormContainerBody = document.createElement("div");
        checkoutFormContainerBody.className = "card-body";

        let checkoutForm = document.createElement("form");
        
        let personalDetailsInputsRow = document.createElement("div");
        personalDetailsInputsRow.className = "row";
        this.inputs.firstNameInput = this.generateCheckoutFormTextInput("*First Name", "text", "first_name", true, this.inputValues.firstName);
        let firstNameInputContainer = this.generateContainer(this.inputs.firstNameInput, "col-md-6");
        personalDetailsInputsRow.append(firstNameInputContainer);
        this.inputs.lastNameInput = this.generateCheckoutFormTextInput("*Last Name", "text", "last_name", true, this.inputValues.lastName);
        let lastNameInputContainer = this.generateContainer(this.inputs.lastNameInput, "col-md-6");
        personalDetailsInputsRow.append(lastNameInputContainer);
        this.inputs.companyInput = this.generateCheckoutFormTextInput("*Company", "text", "company", true, this.inputValues.company);
        let companyInputContainer = this.generateContainer(this.inputs.companyInput, "col-md-6");
        personalDetailsInputsRow.append(companyInputContainer);
        checkoutForm.append(personalDetailsInputsRow);

        let shippingAddressDetailsInputsRow = document.createElement("div");
        shippingAddressDetailsInputsRow.className = "row";
        this.inputs.addressInput = this.generateCheckoutFormTextInput("*Address", "text", "address", true, this.inputValues.address);
        let addressInputContainer = this.generateContainer(this.inputs.addressInput, "col-md-6");
        shippingAddressDetailsInputsRow.append(addressInputContainer);
        this.inputs.cityInput = this.generateCheckoutFormTextInput("*City", "text", "city", true, this.inputValues.city);
        let cityInputContainer = this.generateContainer(this.inputs.cityInput, "col-md-6");
        shippingAddressDetailsInputsRow.append(cityInputContainer);
        this.inputs.stateInput = this.generateCheckoutFormDropDownInput("state", states, "---Please select shipping state---", true, this.inputValues.state);
        let stateInputContainer = this.generateContainer(this.inputs.stateInput, "col-md-6");
        shippingAddressDetailsInputsRow.append(stateInputContainer);
        this.inputs.zipCodeInput = this.generateCheckoutFormTextInput("*Zip Code", "text", "zip_code", true, this.inputValues.zipCode);
        let zipCodeInputContainer = this.generateContainer(this.inputs.zipCodeInput, "col-md-6");
        shippingAddressDetailsInputsRow.append(zipCodeInputContainer);
        checkoutForm.append(shippingAddressDetailsInputsRow);

        let contactDetailsInputsRow = document.createElement("div");
        contactDetailsInputsRow.className = "row";
        this.inputs.phoneInput = this.generateCheckoutFormTextInput("*Phone", "text", "phone", true, this.inputValues.phone);
        let phoneInputContainer = this.generateContainer(this.inputs.phoneInput, "col-md-6");
        contactDetailsInputsRow.append(phoneInputContainer);
        this.inputs.emailInput = this.generateCheckoutFormTextInput("*Email", "email", "email", true);
        let emailInputContainer = this.generateContainer(this.inputs.emailInput, "col-md-6");
        contactDetailsInputsRow.append(emailInputContainer);
        checkoutForm.append(contactDetailsInputsRow);

        if(localStorage.isPremiseIdRequired !== null && localStorage.isPremiseIdRequired == 1){
            let premiseIdInputRow = document.createElement("div");
            premiseIdInputRow.className = "row";
            let premiseIdInput = this.generateCheckoutFormTextInput("*Premise ID", "text", "premise_id", true);
            premiseIdInputRow.append(premiseIdInput);
            checkoutForm.append(premiseIdInputRow);
        }
        checkoutFormContainerBody.append(checkoutForm);

        let errorMessage = document.createElement("p");
        let proceedToPaymentButton = this.generateProceedToPaymentButton(errorMessage);
        checkoutFormContainerBody.append(proceedToPaymentButton);
        checkoutFormContainerBody.append(errorMessage);

        checkoutFormContainer.append(checkoutFormContainerBody);
        return checkoutFormContainer;
    }

    makeCheckoutPageLinksContainer = () =>{
        let linksContainer = document.createElement("div");
        let backToCartButton = generateButtonLink("BACK TO CART  ", "/shop/shopping-cart", true, "fas fa-shopping-cart");
        linksContainer.append(backToCartButton);
        let continueShoppingButton = generateButtonLink("CONTINUE SHOPPING  ", "/shop/tag-store", true, "fas fa-shopping-cart");
        linksContainer.append(continueShoppingButton);
        return linksContainer;
    }

    generateContainer = (input, inputSize) =>{
        let inputContainer = document.createElement("div");
        inputContainer.className = inputSize;
        inputContainer.append(input);
        return inputContainer;
    }

    generateCheckoutFormTextInput = (inputText, inputType, inputId, inputRequired, inputValue="") =>{
        let input = document.createElement("input");
        input.placeholder = inputText;
        input.type = inputType;
        input.id = inputId;
        input.value = inputValue;
        input.className = "form-control m-1";
        input.required = inputRequired;
        return input;
    }

    generateCheckoutFormDropDownInput = (inputId, inputOptions, defaultOptionText, inputRequired, selectedInputValue="") =>{
        let selectInput = document.createElement("select");
        selectInput.id = inputId;
        selectInput.required = inputRequired;
        selectInput.className = "form-control m-1";

        let defaultDisabledOption = document.createElement("option");
        defaultDisabledOption.selected = true;
        defaultDisabledOption.disabled = true;
        defaultDisabledOption.value = -1;
        defaultDisabledOption.textContent = defaultOptionText;
        selectInput.appendChild(defaultDisabledOption);
        for(let [optionValue, optionTextContent] of Object.entries(inputOptions)){
            let option = document.createElement("option");
            option.value = optionValue;
            option.textContent = optionTextContent;
            selectInput.appendChild(option);
        }
        selectInput.value = selectedInputValue;
        return selectInput;
    }

    generateProceedToPaymentButton = (errorMessage) =>{
        let proceedToPaymentButton = document.createElement("button");
        proceedToPaymentButton.className = "btn btn-outline-primary rounded m-1";
        proceedToPaymentButton.textContent = "PROCEED TO PAYMENT  ";
        let icon = document.createElement("i");
        icon.className = "fas fa-credit-card";
        proceedToPaymentButton.appendChild(icon);
        proceedToPaymentButton.onclick = () =>{
            let checkoutFormCompletionStatus = validateFormCompletion(Object.values(this.inputs));
            if(checkoutFormCompletionStatus){
                errorMessage.className = "d-none";
                this.updateOrderDetailsInLocalStorage();
            }
            else{
                errorMessage.className = "d-block mt-2 mb-0 alert alert-danger";
                errorMessage.textContent = "Please fill in all required fields";
            }
                
        }
        return proceedToPaymentButton;
    }

    updateOrderDetailsInLocalStorage = () =>{
        let shoppingCartString = localStorage.getItem("shoppingCart");
        let shoppingCart = JSON.parse(shoppingCartString);
        if(shoppingCart == null){
            window.location.href = "/shop/tag-store";
            return;
        }
        let orderDetails ={
            first_name: this.inputs.firstNameInput.value,
            last_name: this.inputs.lastNameInput.value,
            company: this.inputs.companyInput.value,
            address_line: this.inputs.addressInput.value,
            city: this.inputs.cityInput.value,
            state: this.inputs.stateInput.value,
            zip_code: this.inputs.zipCodeInput.value,
            phone: this.inputs.phoneInput.value,
            email: this.inputs.emailInput.value,
            premise_id: localStorage.getItem("isPremiseIdRequired") == 1 ? document.getElementById("premise_id").value : "",
            shopping_cart: localStorage.getItem("shoppingCart"),
            total_price: localStorage.getItem("totalPrice"),
            total_tax: localStorage.getItem("totalTax"),
            discount: localStorage.getItem("discount"),
            shipping: localStorage.getItem("shipping"),
            grand_total: localStorage.getItem("grandTotal")
        }
        localStorage.setItem("orderDetails", JSON.stringify(orderDetails));
        window.location.href = "/shop/checkout-payment";
    }
}