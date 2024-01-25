import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { saveAndUploadFile } from '../../../files/files.mjs';
import { generateTextInput, generateUploadInput, validateFormCompletion } from "../../utilities/advertisement_utilities.mjs";


export class EditSeedstockProducerDataWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        let marketplaceFilesS3Path = this.frame.getAttribute("data-widget-marketplace-files-s3-path");
        let seedstockProducerData = await this.getData("get_seedstock_producer_data");
        let editForm = this.createEditForm(marketplaceFilesS3Path);
        this.frame.append(editForm);

        this.existingAdAvailable = false;
        this.existingAdID = null;
        if(Object.entries(seedstockProducerData).length !== 0){
            this.existingAdAvailable = true;
            this.existingAdID = seedstockProducerData.id;
            this.seedstockProducerData = seedstockProducerData;
            this.prefillFormFields(seedstockProducerData);
        }
    }

    createEditForm = (marketplaceFilesS3Path) =>{
        let card = document.createElement("div");
        card.className = "card col-md-12";

        let cardHeader = document.createElement("h5");
        cardHeader.className = "card-header";
        cardHeader.textContent = "Edit Seedstock Producer MarketPlace Data";
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body";

        let form = document.createElement("form");
        let inputsRow = document.createElement("row");


        let nameInput = generateTextInput("*MarketPlace Company Name", "text", "account_name", true, "col-md-6");
        inputsRow.append(nameInput);
        let emailInput = generateTextInput("*MarketPlace Company Email", "text", "account_email", true, "col-md-6");
        inputsRow.append(emailInput);
        let contactNameInput = generateTextInput("*MarketPlace Company Contact Name", "text", "account_contact_name", true, "col-md-6");
        inputsRow.append(contactNameInput);
        let phoneInput = generateTextInput("*MarketPlace Company Phone", "text", "account_phone", true, "col-md-6");
        inputsRow.append(phoneInput);
        let shortDescriptionInput = generateTextInput("*Short Description", "text", "short_description", true, "col-md-12");
        inputsRow.append(shortDescriptionInput);
        let longDescriptionInput = generateTextInput("*Long Description", "text", "long_description", true, "col-md-12");
        inputsRow.append(longDescriptionInput);
        let logoUploadContainer = generateUploadInput("Upload Logo: ");
        inputsRow.append(logoUploadContainer);
        this.inputsRow = inputsRow;
        form.append(inputsRow);
        cardBody.append(form);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-outline-primary rounded m-1";
        submitButton.textContent = "SAVE";
        cardBody.append(submitButton);

        let statusMessage = document.createElement("p");
        cardBody.append(statusMessage);
        let errorMessage = document.createElement("p");
        cardBody.append(errorMessage);

        submitButton.onclick = async() =>{
            let formResponseValues = [];
            let name = document.getElementById("account_name").value;
            formResponseValues.push(name);
            let email = document.getElementById("account_email").value;
            formResponseValues.push(email);
            let contactName = document.getElementById("account_contact_name").value;
            formResponseValues.push(contactName);
            let phone = document.getElementById("account_phone").value;
            formResponseValues.push(phone);
            let shortDescription = document.getElementById("short_description").value;
            formResponseValues.push(shortDescription);
            let longDescription = document.getElementById("long_description").value;
            formResponseValues.push(longDescription);
            let logoInput = logoUploadContainer.getElementsByTagName("input");
            let formValidationStatus = validateFormCompletion(formResponseValues);
            if(formValidationStatus){
                let logoFileID = undefined;
                let uploadedFile = logoInput[0].files;
                errorMessage.className = "d-none";
                let seedstockProducerDataForm = new AsyncForm({
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
                            phone: phone,
                            short_description: shortDescription,
                            long_description: longDescription,
                            logo_file_id: logoFileID,
                            existing_ad_available: this.existingAdAvailable,
                            existing_ad_id: this.existingAdID
                        };
                    }
                });
                if(Object.entries(uploadedFile).length > 0){
                    let uploadedLogoFile = uploadedFile[0];
                    logoFileID = await saveAndUploadFile(true, true, uploadedLogoFile, null, null, false, marketplaceFilesS3Path);
                }
                seedstockProducerDataForm.submit();
            }
            else{
                errorMessage.className = "d-block mt-2 mb-0 alert alert-danger";
                errorMessage.textContent = "Please fill in all required fields";
            }
        }
        card.append(cardBody);
        return card;
    }

    prefillFormFields = (seedstockProducerData) =>{
        document.getElementById("account_name").value = seedstockProducerData.marketplace_account_name;
        document.getElementById("account_email").value = seedstockProducerData.marketplace_account_email;
        document.getElementById("account_contact_name").value = seedstockProducerData.marketplace_account_contact_name;
        document.getElementById("account_phone").value = seedstockProducerData.marketplace_account_phone;
        document.getElementById("short_description").value = seedstockProducerData.short_description;
        document.getElementById("long_description").value = seedstockProducerData.long_description;
        if(this.existingAdAvailable && this.seedstockProducerData.logo_file_id !== null){
            let existingLogoMessage = document.createElement("p");
            existingLogoMessage.className = "text-primary font-italic ml-2";
            existingLogoMessage.textContent = "*You have already uploaded a MarketPlace Logo. Upload a new one if you would like to replace it.";
            this.inputsRow.append(existingLogoMessage);
        }
    }
}