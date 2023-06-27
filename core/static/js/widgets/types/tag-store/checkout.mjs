import { Widget } from '../../widget.mjs';
import { states } from '../../../core/common_constants.mjs';
import { generateButtonLink, makeShoppingCartTotalsContainer, validateFormCompletion } from '../../utilities/tag_store_utilities.mjs';

export class CheckoutWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
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
        let firstNameInput = this.generateCheckoutFormTextInput("*First Name", "text", "first_name", true, first_name);
        personalDetailsInputsRow.append(firstNameInput);
        let lastNameInput = this.generateCheckoutFormTextInput("*Last Name", "text", "last_name", true, last_name);
        personalDetailsInputsRow.append(lastNameInput);
        let companyInput = this.generateCheckoutFormTextInput("*Company", "text", "company", true, company_name);
        personalDetailsInputsRow.append(companyInput);
        checkoutForm.append(personalDetailsInputsRow);

        let shippingAddressDetailsInputsRow = document.createElement("div");
        shippingAddressDetailsInputsRow.className = "row";
        let addressInput = this.generateCheckoutFormTextInput("*Address", "text", "address", true, address);
        shippingAddressDetailsInputsRow.append(addressInput);
        let cityInput = this.generateCheckoutFormTextInput("*City", "text", "city", true, city);
        shippingAddressDetailsInputsRow.append(cityInput);
        let stateInput = this.generateCheckoutFormDropDownInput("state", states, "---Please select shipping state---", true, state);
        shippingAddressDetailsInputsRow.append(stateInput);
        let zipCodeInput = this.generateCheckoutFormTextInput("*Zip Code", "text", "zip_code", true, zip);
        shippingAddressDetailsInputsRow.append(zipCodeInput);
        checkoutForm.append(shippingAddressDetailsInputsRow);

        let contactDetailsInputsRow = document.createElement("div");
        contactDetailsInputsRow.className = "row";
        let phoneInput = this.generateCheckoutFormTextInput("*Phone", "text", "phone", true, phone);
        contactDetailsInputsRow.append(phoneInput);
        let emailInput = this.generateCheckoutFormTextInput("*Email", "email", "email", true);
        contactDetailsInputsRow.append(emailInput);
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

    generateCheckoutFormTextInput = (inputText, inputType, inputId, inputRequired, inputValue="") =>{
        let inputContainer = document.createElement("div");
        inputContainer.className = "col-md-6";
        let input = document.createElement("input");
        input.placeholder = inputText;
        input.type = inputType;
        input.id = inputId;
        input.value = inputValue;
        input.className = "form-control m-1";
        input.required = inputRequired;
        inputContainer.append(input);
        return inputContainer;
    }

    generateCheckoutFormDropDownInput = (inputId, inputOptions, defaultOptionText, inputRequired, selectedInputValue="") =>{
        let inputContainer = document.createElement("div");
        inputContainer.className = "col-md-6";
        let selectInput = document.createElement("select");
        selectInput.id = inputId;
        selectInput.required = inputRequired;
        selectInput.className = "form-control m-1";

        let defaultDisabledOption = document.createElement("option");
        defaultDisabledOption.selected = true;
        defaultDisabledOption.disabled = true;
        defaultDisabledOption.textContent = defaultOptionText;
        selectInput.appendChild(defaultDisabledOption);
        for(let [optionValue, optionTextContent] of Object.entries(inputOptions)){
            let option = document.createElement("option");
            option.value = optionValue;
            option.textContent = optionTextContent;
            selectInput.appendChild(option);
        }
        selectInput.value = selectedInputValue;
        inputContainer.append(selectInput);
        return inputContainer;
    }

    generateProceedToPaymentButton = (errorMessage) =>{
        let proceedToPaymentButton = document.createElement("button");
        proceedToPaymentButton.className = "btn btn-outline-primary rounded m-1";
        proceedToPaymentButton.textContent = "PROCEED TO PAYMENT  ";
        let icon = document.createElement("i");
        icon.className = "fas fa-credit-card";
        proceedToPaymentButton.appendChild(icon);
        proceedToPaymentButton.onclick = () =>{
            let checkoutFormCompletionStatus = this.validateCheckoutFormInputs();
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
            first_name: document.getElementById("first_name").value,
            last_name: document.getElementById("last_name").value,
            company: document.getElementById("company").value,
            address_line: document.getElementById("address").value,
            city: document.getElementById("city").value,
            state: document.getElementById("state").value,
            zip_code: document.getElementById("zip_code").value,
            phone: document.getElementById("phone").value,
            email: document.getElementById("email").value,
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

    validateCheckoutFormInputs = () =>{
        let checkoutFormResponseValues = [];
        checkoutFormResponseValues.push(document.getElementById("first_name").value);
        checkoutFormResponseValues.push(document.getElementById("last_name").value);
        checkoutFormResponseValues.push(document.getElementById("company").value);
        checkoutFormResponseValues.push(document.getElementById("address").value);
        checkoutFormResponseValues.push(document.getElementById("city").value);
        checkoutFormResponseValues.push(document.getElementById("state").value);
        checkoutFormResponseValues.push(document.getElementById("zip_code").value);
        checkoutFormResponseValues.push(document.getElementById("phone").value);
        checkoutFormResponseValues.push(document.getElementById("email").value);
        return validateFormCompletion(checkoutFormResponseValues);
    }
}