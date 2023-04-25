import { Widget } from '../../widget.mjs';
import { states } from '../../../core/common_constants.mjs';

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

        let checkoutForm = this.makeCheckoutForm();
        checkoutPageCardBody.append(checkoutForm);
        
        checkoutPageCard.append(checkoutPageCardBody);
        return checkoutPageCard;
    }

    makeCheckoutForm = () =>{
        let checkoutFormContainer = document.createElement("div");
        checkoutFormContainer.className = "card col-md-9";

        let checkoutFormContainerHeader = document.createElement("h4");
        checkoutFormContainerHeader.className = "card-header";
        checkoutFormContainerHeader.textContent = "SHIPPING INFORMATION";
        checkoutFormContainer.append(checkoutFormContainerHeader);

        let checkoutFormContainerBody = document.createElement("div");
        checkoutFormContainerBody.className = "card-body";

        let checkoutForm = document.createElement("form");
        
        let personalDetailsInputsRow = document.createElement("div");
        personalDetailsInputsRow.className = "row";
        let firstNameInput = this.generateCheckoutFormTextInput("*First Name", "text", "first_name", true);
        personalDetailsInputsRow.append(firstNameInput);
        let lastNameInput = this.generateCheckoutFormTextInput("*Last Name", "text", "last_name", true);
        personalDetailsInputsRow.append(lastNameInput);
        let companyInput = this.generateCheckoutFormTextInput("*Company", "text", "company", true);
        personalDetailsInputsRow.append(companyInput);
        checkoutForm.append(personalDetailsInputsRow);

        let shippingAddressDetailsInputsRow = document.createElement("div");
        shippingAddressDetailsInputsRow.className = "row";
        let addressInput = this.generateCheckoutFormTextInput("*Address", "text", "address", true);
        shippingAddressDetailsInputsRow.append(addressInput);
        let cityInput = this.generateCheckoutFormTextInput("*City", "text", "city", true);
        shippingAddressDetailsInputsRow.append(cityInput);
        let stateInput = this.generateCheckoutFormDropDownInput("state", states, "---Please select shipping state---", true);
        shippingAddressDetailsInputsRow.append(stateInput);
        let zipCodeInput = this.generateCheckoutFormTextInput("*Zip Code", "text", "zip_code", true);
        shippingAddressDetailsInputsRow.append(zipCodeInput);
        checkoutForm.append(shippingAddressDetailsInputsRow);

        let contactDetailsInputsRow = document.createElement("div");
        contactDetailsInputsRow.className = "row";
        let phoneInput = this.generateCheckoutFormTextInput("*Phone", "text", "phone", true);
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

        let proceedToPaymentButton = this.generateProceedToPaymentButton();
        checkoutForm.append(proceedToPaymentButton);
        
        checkoutFormContainerBody.append(checkoutForm);
        checkoutFormContainer.append(checkoutFormContainerBody);
        return checkoutFormContainer;
    }

    generateCheckoutFormTextInput = (inputText, inputType, inputId, inputRequired) =>{
        let inputContainer = document.createElement("div");
        inputContainer.className = "col-md-6";
        let input = document.createElement("input");
        input.placeholder = inputText;
        input.type = inputType;
        input.id = inputId;
        input.className = "form-control m-1";
        input.required = inputRequired;
        inputContainer.append(input);
        return inputContainer;
    }

    generateCheckoutFormDropDownInput = (inputId, inputOptions, defaultOptionText, inputRequired) =>{
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
        for(let inputOption of inputOptions){
            let option = document.createElement("option");
            option.value = inputOption.value;
            option.textContent = inputOption.name;
            selectInput.appendChild(option);
        }
        inputContainer.append(selectInput);
        return inputContainer;
    }

    generateProceedToPaymentButton = () =>{
        let proceedToPaymentButton = document.createElement("button");
        proceedToPaymentButton.className = "btn btn-outline-primary rounded m-1";
        proceedToPaymentButton.textContent = "PROCEED TO PAYMENT  ";
        let icon = document.createElement("i");
        icon.className = "fas fa-credit-card";
        proceedToPaymentButton.appendChild(icon);
        proceedToPaymentButton.onclick = () =>{
            this.updateOrderDetailsInLocalStorage();
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
        console.log(orderDetails);
        localStorage.setItem("orderDetails", JSON.stringify(orderDetails));
    }

}