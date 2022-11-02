import { Widget } from '../../widget.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class EditAccountRetailDataWidget extends Widget{
    constructor(frame) {
        super(frame);
    }
    
    initType = () => {
        let retailName = this.frame.getAttribute("data-widget-retail-name");
        let retailDescription = this.frame.getAttribute("data-widget-retail-description"); 
        this.createEditForm(retailName, retailDescription);
    }

    createTextInput = (inputLabel, inputID, maxLength, inputValue) => {
        let textInputContainer = document.createElement("div");
        textInputContainer.className = "row p-1 border-bottom";
        let inputLabelContainer = document.createElement("div");
        inputLabelContainer.className = "col-md-2";
        let label = document.createElement("label");
        label.textContent = inputLabel;
        inputLabelContainer.append(label);

        let inputContainer = document.createElement("div");
        inputContainer.className = "col-md-8 p-1";
        let input = document.createElement("input");
        input.type = "text";
        input.className = "form-control";
        input.id = inputID;
        input.maxLength = maxLength;
        input.value = inputValue;
        inputContainer.append(input);

        textInputContainer.append(inputLabelContainer);
        textInputContainer.append(inputContainer);
        return textInputContainer;
    }

    createTextAreaInput = (inputLabel, inputID, maxLength, inputValue) => {
        let textInputContainer = document.createElement("div");
        textInputContainer.className = "row p-1 border-bottom";
        let inputLabelContainer = document.createElement("div");
        inputLabelContainer.className = "col-md-2";
        let label = document.createElement("label");
        label.textContent = inputLabel;
        inputLabelContainer.append(label);

        let inputContainer = document.createElement("div");
        inputContainer.className = "col-md-8 p-1"
        let textArea = document.createElement("textArea");
        textArea.className = "form-control";
        textArea.id = inputID;
        textArea.rows=5;
        textArea.maxLength = maxLength;
        textArea.value = inputValue;
        inputContainer.append(textArea);

        textInputContainer.append(inputLabelContainer);
        textInputContainer.append(inputContainer);
        return textInputContainer;
    }

    createEditForm = (retailName, retailDescription) => {
        this.frame.innerHTML = "";
        let card = document.createElement("div");
        card.className = "card";
    
        let headerText = document.createElement("h3");
        headerText.className = "mt-2";
        headerText.textContent = "Edit Retail Data";
    
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between";
        cardHeader.append(headerText);
        card.append(cardHeader)
    
        let cardBody = document.createElement("div");
        cardBody.className = "card-body justify-content-center";
        card.append(cardBody);  
        
        let form = document.createElement("form");
        
        let retailNameInput = this.createTextInput("Account Retail Name", "retailName", "100", retailName);
        let retailDescriptionInput = this.createTextAreaInput("Retail Description", "retailDescription", "250", retailDescription);

        let imageUploadContainer = document.createElement("div");
        imageUploadContainer.className = "p-1 col-md-8";
        let imageUploader = new BasicFileEditor({filetype:["image"]}, imageUploadContainer);
        
        form.append(retailNameInput);
        form.append(retailDescriptionInput);
        form.append(imageUploadContainer);
        
        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group p-2";
        form.append(submitFormGroup);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Submit";
        submitButton.type = "button";
        submitFormGroup.append(submitButton);
        
        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);

        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/save_account_retail_data",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    retail_name: document.getElementById("retailName").value,
                    retail_description: document.getElementById("retailDescription").value,
                    uploaded_images: imageUploader.getFileIDs()
                };
            },
        });
       
        submitButton.addEventListener("click", () => {
            if(imageUploader.getNumberOfAttachedFiles() < 4){
                this.uploadFilesAndSubmit(imageUploader);
            }
            else{
                errorMessage.style.display = "block";
                errorMessage.textContent = "Please upload a maximum of 3 images.";
            }
        });

        cardBody.append(form);
        this.frame.append(card);
    }

    uploadFilesAndSubmit = async (imageUploader) => {
        function progress(){};
        await imageUploader.upload(progress)
        this.asyncForm.submit();
    }
}