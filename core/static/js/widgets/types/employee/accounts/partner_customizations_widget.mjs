import { Widget } from '../../../widget.mjs';
import { FileUploader } from '../../../../files/file_uploader.mjs';
import { generateUploadInput } from '../../../utilities/advertisement_utilities.mjs';
import { saveAndUploadFile } from '../../../../files/files.mjs';
import { AsyncForm } from '../../../../../global/async_form.mjs';

export class PartnerCustomizationsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () =>{
        this.frame.innerHTML = "";
        let partnerId = this.frame.getAttribute("data-widget-partner-id");
        let logoFilesS3Path = this.frame.getAttribute("data-widget-logo-files-s3-path");
        let partnerCustomizationsForm = this.createPartnerCustomizationsForm(partnerId, logoFilesS3Path);
        this.frame.append(partnerCustomizationsForm);
    }

    createPartnerCustomizationsForm = (partnerId, logoFilesS3Path) =>{
        let card = document.createElement("div");
        card.className = "card";
        
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header p-1 d-flex";
        let cardHeaderText = document.createElement("h5");
        cardHeaderText.className = "mt-2 p-2 col-md-6";
        cardHeaderText.textContent = "Customization options for Partner " + partnerId;
        cardHeader.append(cardHeaderText);
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body row d-block";

        let form = document.createElement("form");
        let colorFormRow = document.createElement("div");
        colorFormRow.className = "col-md-5 d-inline-flex";
        let colorInputText = document.createElement("label");
        colorInputText.className = "h6 m-2 p-1 text-dark";
        colorInputText.textContent = "Select Color Scheme: ";
        colorFormRow.append(colorInputText);
        let colorInput = document.createElement("input");
        colorInput.type = "color";
        colorInput.className = "form-control form-control-color";
        colorInput.value = "#563d7c";
        colorInput.title = "Choose your color";
        colorFormRow.append(colorInput);
        form.append(colorFormRow);

        let logoInputRow = document.createElement("div");
        let logoUploadContainer = generateUploadInput("Upload Private Logo: ")
        logoInputRow.append(logoUploadContainer);
        form.append(logoInputRow);
        
        let saveFormGroup = document.createElement("div");
        saveFormGroup.className = "form-group m-1 p-1";
        form.append(saveFormGroup);

        let saveButton = document.createElement("button");
        saveButton.className = "btn btn-primary";
        saveButton.textContent = "Save";
        saveButton.type = "button";
        saveFormGroup.append(saveButton);

        let statusMessage = document.createElement("p");
        statusMessage.className = "d-none mt-2 mb-0";
        form.append(statusMessage);
        
        let errorMessage = document.createElement("p");
        errorMessage.className = "d-none mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);
        cardBody.append(form);
        card.append(cardBody);

        let uploadedLogoFileId = undefined;
        let partnerCustomizationForm = new AsyncForm({
            action: "/widgets/data/save_partner_customizations",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    partner_id: partnerId,
                    color_hex: colorInput.value,
                    uploaded_logo_file_id: uploadedLogoFileId
                };
            }
        });
        

        saveButton.onclick = async() =>{
            let logoInput = logoUploadContainer.getElementsByTagName("input");
            let uploadedFiles = logoInput[0].files;
            if(Object.entries(uploadedFiles).length > 0){
                let uploadedLogoFile = uploadedFiles[0];
                uploadedLogoFileId = await saveAndUploadFile(false, false, uploadedLogoFile, null, null, true, logoFilesS3Path);
            }
            partnerCustomizationForm.submit();
        }

        return card;
    }
}