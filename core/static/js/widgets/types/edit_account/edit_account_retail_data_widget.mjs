import { Widget } from '../../widget.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class EditAccountRetailDataWidget extends Widget{
    constructor(frame) {
        super(frame);
    }
    
    initType = () => {
        this.retailName = "";
        this.reatilDescription = "";
        this.createEditForm();
    }

    createEditForm = () => {

        function createTextInput(inputLabel, inputID, maxLength){
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
            inputContainer.append(input);

            textInputContainer.append(inputLabelContainer);
            textInputContainer.append(inputContainer);
            return textInputContainer;
        }

        function createTextAreaInput(inputLabel, inputID, maxLength){
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
            inputContainer.append(textArea);

            textInputContainer.append(inputLabelContainer);
            textInputContainer.append(inputContainer);
            return textInputContainer;
        }

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
        
        let retailNameInput = createTextInput("Account Retail Name", "retailName", "100");
        let retailDescriptionInput = createTextAreaInput("Retail Description", "retailDescription", "250");

        let imageUploadContainer = document.createElement("div");
        imageUploadContainer.className = "p-1 col-md-8";
        this.imageUploader = new BasicFileEditor({filetype:["image"]}, imageUploadContainer);
        
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
                    retail_name: this.retailName,
                    retail_description: this.retailDescription,
                    uploaded_images: this.imageUploader.getFileIDs()
                };
            },
        });
       
        submitButton.addEventListener("click", () => {
            function progress(){}
            this.retailName = document.getElementById("retailName").value;
            this.retailDescription = document.getElementById("retailDescription").value;
            this.imageUploader.upload(progress)
                .then(() => {
                    if(this.imageUploader.getFileIDs().length < 4){
                        this.asyncForm.submit();
                    }
                    else{
                        errorMessage.style.display = "block";
                        errorMessage.textContent = "Please upload a maximum of 3 images.";
                    }
            });
        });

        cardBody.append(form);
        this.frame.append(card);
    }
}