import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { saveAndUploadFile } from '../../../files/files.mjs';
import { generateTextInput, generateUploadInput, generateDropDownInput, validateFormCompletion } from "../../utilities/advertisement_utilities.mjs";


export class AddSeedstockProducerDataWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        let marketplaceFilesS3Path = this.frame.getAttribute("data-widget-marketplace-files-s3-path");
        let seedstockAccounts = this.formatAccountsData(JSON.parse(this.frame.getAttribute("data-widget-seedstock-accounts")));
        let addForm = this.createAddForm(marketplaceFilesS3Path, seedstockAccounts);
        this.frame.append(addForm);
    }

    formatAccountsData = (accountsData) =>{
        let formattedData = {};
        for(const accountData of accountsData){
            formattedData[accountData.id] = accountData.name;
        }
        return formattedData;
    }

    createAddForm = (marketplaceFilesS3Path, seedstockAccounts) =>{
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


        let accountInput = generateDropDownInput("account_id", seedstockAccounts, "-Please select Seedstock Account-", true);
        inputsRow.append(accountInput);
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
            let accountId = document.getElementById("account_id").value;
            formResponseValues.push(accountId);
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
                            account_id: accountId,
                            name: name,
                            email: email,
                            contact_name: contactName,
                            phone: phone,
                            short_description: shortDescription,
                            long_description: longDescription,
                            logo_file_id: logoFileID
                        };
                    }
                });
                if(Object.entries(uploadedFile).length > 0){
                    let uploadedLogoFile = uploadedFile[0];
                    logoFileID = await saveAndUploadFile(false, false, uploadedLogoFile, null, null, true, marketplaceFilesS3Path);
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
}