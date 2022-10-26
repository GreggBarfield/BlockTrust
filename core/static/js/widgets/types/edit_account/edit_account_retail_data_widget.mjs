import { Widget } from '../../widget.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { ProgressBar } from '../../../core/progress_bar.mjs';

export class EditAccountRetailDataWidget extends Widget{
    constructor(frame) {
        super(frame);
    }
    
    initType = () => {
        this.createEditForm();
    }

    createEditForm = () => {

        function createTextInput(inputLabel, inputID){
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
            inputContainer.append(input);

            textInputContainer.append(inputLabelContainer);
            textInputContainer.append(inputContainer);
            return textInputContainer;
        }

        function createTextAreaInput(inputLabel, inputID){
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
        
        let retailNameInput = createTextInput("Account Retail Name", "retailName");
        let retailSubheadingInput = createTextInput("Retail Subheading", "retailSubheading");
        let retailDescriptionInput = createTextAreaInput("Retail Description", "retailDescription");

        let imageUploadContainer = document.createElement("div");
        imageUploadContainer.className = "p-1 col-md-8";
        this.imageUploader = new BasicFileEditor({filetype:["image"]}, imageUploadContainer);
        
        form.append(retailNameInput);
        form.append(retailSubheadingInput);
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
       
        submitButton.addEventListener("click", () => {
            function progress(){} 
            console.log(this.imageUploader.files);
            if(this.imageUploader.files.length < 4){
                this.imageUploader.upload(progress)
                    .then(() => {
                        console.log("uploaded");
                    });
            }
            else{
                errorMessage.style.display = "block";
                errorMessage.textContent = "Please upload a Maximum of 3 images.";
            }
        });

        cardBody.append(form);
        this.frame.append(card);
    }
}