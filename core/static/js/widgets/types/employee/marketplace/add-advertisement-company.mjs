import { AsyncForm } from '../../../../../global/async_form.mjs';
import { generateDropDownInput, generateTextInput,generateUploadInput, validateFormCompletion } from "../../../utilities/advertisement_utilities.mjs";
import { saveAndUploadFile } from '../../../../files/files.mjs';
import { states } from '../../../../core/common_constants.mjs';
import { Widget } from "../../../widget.mjs";

export class AddAdvertisementCompanyWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        let marketplaceFilesS3Path = this.frame.getAttribute("data-widget-marketplace-files-s3-path");
        let addAdvertisementCompanyContainer = document.createElement("div");
        addAdvertisementCompanyContainer.className = "card";

        let addAdvertisementCompanyContainerHeader = document.createElement("h5");
        addAdvertisementCompanyContainerHeader.className = "card-header";
        addAdvertisementCompanyContainerHeader.textContent = "Add Advertisement Company";
        addAdvertisementCompanyContainer.append(addAdvertisementCompanyContainerHeader);

        let addAdvertisementCompanyContainerBody =  this.makeAddAdvertisementCompanyContainerBody(marketplaceFilesS3Path);
        addAdvertisementCompanyContainer.append(addAdvertisementCompanyContainerBody);

        this.frame.append(addAdvertisementCompanyContainer);
    }

    makeAddAdvertisementCompanyContainerBody = (marketplaceFilesS3Path) =>{
        let addAdvertisementCompanyContainerBody = document.createElement("div");
        addAdvertisementCompanyContainerBody.className = "card-body";
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
        let logoUploadContainer = generateUploadInput("Upload Logo: ");
        inputsRow.append(logoUploadContainer);
        let integratedWithBlockTrustInput = generateTextInput("*Integrated With BlockTrust", "checkbox", "is_integrated_with_blocktrust", false, "col-md-6 d-flex m-1");
        inputsRow.append(integratedWithBlockTrustInput);

        form.append(inputsRow);
        addAdvertisementCompanyContainerBody.append(form);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-outline-primary rounded m-1";
        submitButton.textContent = "SAVE";
        addAdvertisementCompanyContainerBody.append(submitButton);

        let statusMessage = document.createElement("p");
        addAdvertisementCompanyContainerBody.append(statusMessage);
        let errorMessage = document.createElement("p");
        addAdvertisementCompanyContainerBody.append(errorMessage);

        submitButton.onclick = async() =>{
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
            let logoInput = logoUploadContainer.getElementsByTagName("input");
            let isIntegratedWithBlockTrust = document.getElementById("is_integrated_with_blocktrust").checked;
            let formCompletionStatus = validateFormCompletion(formResponseValues);
            let logoFileID = 0;
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
                            logo_file_id: logoFileID,
                            is_integrated_with_blocktrust: isIntegratedWithBlockTrust
                        };
                    }
                });
                let uploadedFiles = logoInput[0].files;
                if(Object.entries(uploadedFiles).length > 0){
                    let uploadedLogoFile = uploadedFiles[0];
                    logoFileID = await saveAndUploadFile(false, false, uploadedLogoFile, null, null, true, marketplaceFilesS3Path);
                }
                    newAdvertisementCompanyAsyncForm.submit();
            }
            else{
                errorMessage.className = "d-block mt-2 mb-0 alert alert-danger";
                errorMessage.textContent = "Please fill in all required fields";
            }
        }

        return addAdvertisementCompanyContainerBody;
    }
}