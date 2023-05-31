import { AsyncForm } from '../../../../../global/async_form.mjs';
import { Widget } from "../../../widget.mjs";
import { generateDropDownInput, generateTextInput, validateFormCompletion } from "../../../utilities/advertisement_utilities.mjs";
import { states } from '../../../../core/common_constants.mjs';

export class AddAdvertisementCompanyWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        let addAdvertisementCompanyContainer = document.createElement("div");
        addAdvertisementCompanyContainer.className = "card";

        let addAdvertisementCompanyContainerHeader = document.createElement("h5");
        addAdvertisementCompanyContainerHeader.className = "card-header";
        addAdvertisementCompanyContainerHeader.textContent = "Add Advertisement Company";
        addAdvertisementCompanyContainer.append(addAdvertisementCompanyContainerHeader);

        let addAdvertisementCompanyContainerBody = document.createElement("div");
        addAdvertisementCompanyContainerBody.className = "card-body";
        let addAdvertisementCompanyForm = this.makeAddAdvertisementCompanyForm();
        addAdvertisementCompanyContainerBody.append(addAdvertisementCompanyForm);
        addAdvertisementCompanyContainer.append(addAdvertisementCompanyContainerBody);

        this.frame.append(addAdvertisementCompanyContainer);
    }

    makeAddAdvertisementCompanyForm = () =>{
        let form = document.createElement("form");

        let inputsRow = document.createElement("div");
        inputsRow.className = "row";
        let nameInput = generateTextInput("*Company Name", "text", "name", true, "col-md-6");
        inputsRow.append(nameInput);
        let emailInput = generateTextInput("*Email", "email", "email", true, "col-md-6");
        inputsRow.append(emailInput);
        let contactNameInput = generateTextInput("*Contact Name", "text", "contact_name", true, "col-md-6");
        inputsRow.append(contactNameInput);
        let addressInput = generateTextInput("*Address", "text", "address", true, "col-md-6");
        inputsRow.append(addressInput);
        let cityInput = generateTextInput("*City", "text", "city", true, "col-md-6");
        inputsRow.append(cityInput);
        let stateInput = generateDropDownInput("state", states, "-Please select State-", true);
        inputsRow.append(stateInput);
        let zipInput = generateTextInput("*Zip", "text", "zip_code", true, "col-md-6");
        inputsRow.append(zipInput);
        let phoneInput = generateTextInput("*Phone", "text", "phone", true, "col-md-6");
        inputsRow.append(phoneInput);
        let integratedWithBlockTrustInput = generateTextInput("*Integrated With BlockTrust", "checkbox", "is_integrated_with_blocktrust", true, "col-md-6 d-flex m-1");
        inputsRow.append(integratedWithBlockTrustInput);
        form.append(inputsRow);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-outline-primary rounded m-1";
        submitButton.textContent = "SAVE";
        form.append(submitButton);

        let statusMessage = document.createElement("p");
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        form.append(errorMessage);

        submitButton.onclick = () =>{
            let formResponseValues = [];
            let name = document.getElementById("name").value;
            formResponseValues.push(name);
            let email = document.getElementById("email").value;
            formResponseValues.push(email);
            let contactName = document.getElementById("contact_name").value;
            formResponseValues.push(contactName);
            let address = document.getElementById("address").value;
            formResponseValues.push(address);
            let city = document.getElementById("city").value;
            formResponseValues.push(city);
            let state = document.getElementById("state").value;
            formResponseValues.push(state);
            let zipCode = document.getElementById("zip_code").value;
            formResponseValues.push(zipCode);
            let phone = document.getElementById("phone").value;
            formResponseValues.push(phone);
            let isIntegratedWithBlockTrust = document.getElementById("is_integrated_with_blocktrust").checked;
            let formCompletionStatus = validateFormCompletion(formResponseValues);
            if(formCompletionStatus){
                errorMessage.className = "d-none";
                let newAdvertisementCompanyAsyncForm = new AsyncForm({
                    action: window.location.href,
                    form: form,
                    status: statusMessage,
                    error: errorMessage,
                    redirectMessage: "Saved!",
                    loadingMessage: "Saving...",
                    getData: () => {
                        return {
                            name: name,
                            email: email,
                            contact_name: contactName,
                            address: address,
                            city: city,
                            state: state,
                            zip_code: zipCode,
                            phone: phone,
                            is_integrated_with_blocktrust: isIntegratedWithBlockTrust
                        };
                    }
                });
                newAdvertisementCompanyAsyncForm.submit();
            }
            else{
                errorMessage.className = "d-block mt-2 mb-0 alert alert-danger";
                errorMessage.textContent = "Please fill in all required fields";
            }
        }
        return form;
    }
}