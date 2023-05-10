import { AsyncForm } from '../../../../../global/async_form.mjs';
import { Widget } from "../../../widget.mjs";
import { generateDropDownInput, generateTextInput } from "../../../utilities/advertisement_utilities.mjs";
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
        let integratedWithBlockTrustInput = generateTextInput("*Integrated With BlockTrust", "checkbox", "integrated_with_blocktrust", true, "col-md-6 d-flex m-1");
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
            let allQuestionsAnswered = true;
            let name = document.getElementById("name").value;
            let email = document.getElementById("email").value;
            let contact_name = document.getElementById("contact_name").value;
            let address = document.getElementById("address").value;
            let city = document.getElementById("city").value;
            let state = document.getElementById("state").value;
            let zip_code = document.getElementById("zip_code").value;
            let phone = document.getElementById("phone").value;
            let integrated_with_blocktrust = document.getElementById("integrated_with_blocktrust").checked;
            if(name == ""){ allQuestionsAnswered=false; }
            if(email == ""){ allQuestionsAnswered=false; }
            if(contact_name == ""){ allQuestionsAnswered=false; }
            if(address == ""){ allQuestionsAnswered=false; }
            if(city == ""){ allQuestionsAnswered=false; }
            if(state == "-Please select State-"){ allQuestionsAnswered=false; }
            if(zip_code == ""){ allQuestionsAnswered=false; }
            if(phone == ""){ allQuestionsAnswered=false; }
            if(allQuestionsAnswered){
                let newAdvertisementCompanyAsyncForm = new AsyncForm({
                    action: "/widgets/data/save_new_advertisement_company",
                    form: form,
                    status: statusMessage,
                    error: errorMessage,
                    redirectMessage: "Saved!",
                    loadingMessage: "Saving...",
                    getData: () => {
                        return {
                            name: name,
                            email: email,
                            contact_name: contact_name,
                            address: address,
                            city: city,
                            state: state,
                            zip_code: zip_code,
                            phone: phone,
                            integrated_with_blocktrust: integrated_with_blocktrust ? 1: 0
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