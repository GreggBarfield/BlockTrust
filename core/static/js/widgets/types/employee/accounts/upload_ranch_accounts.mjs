import { Widget } from '../../../widget.mjs';
import { AsyncForm } from '../../../../../global/async_form.mjs';

export class UploadRanchAccountsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () =>{
        this.frame.innerHTML = "";
        let partnerId = this.frame.getAttribute("data-widget-partner-id");
        let uploadRanchAccountsContainer = this.makeUploadRanchAccountsContainer(partnerId);
        this.frame.append(uploadRanchAccountsContainer);
    }

    makeUploadRanchAccountsContainer = (partnerId) =>{
        let uploadRanchAccountsContainer = document.createElement("div");
        uploadRanchAccountsContainer.className = "card";

        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header p-1";
        let cardHeaderText = document.createElement("h5");
        cardHeaderText.className = "mt-2 p-2";
        cardHeaderText.textContent = "UPLOAD RANCH ACCOUNTS FOR ACCOUNT " + partnerId;
        cardHeader.append(cardHeaderText);
        uploadRanchAccountsContainer.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body row d-block";

        let form  = document.createElement("form");

        let uploadInputContainer  = document.createElement("div");
        uploadInputContainer.className = "col-md-6 m-3 p-3";
        let uploadInput = document.createElement("input");
        uploadInput.type = "file";
        uploadInput.multiple = false;
        uploadInput.required = true;
        uploadInput.name = "upload_input";
        uploadInputContainer.append(uploadInput);
        form.append(uploadInputContainer);
        
        let uploadAccountsButton = document.createElement("button");
        uploadAccountsButton.className = "btn btn-outline-primary rounded m-2";
        uploadAccountsButton.textContent = "Upload Accounts";
        form.append(uploadAccountsButton);

        let statusMessage = document.createElement("p");
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.className = "mt-2 mb-0";
        form.append(errorMessage);

        let uploadAccountsForm = new AsyncForm({
            action: "/employee/upload-accounts-for-partner",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    partner_id: partnerId,
                    accounts_data: accountsData
                };
            }
        });
        cardBody.append(form);
        uploadRanchAccountsContainer.append(cardBody);

        let accountsData = [];
        uploadAccountsButton.onclick = (e) =>{
            e.preventDefault();
            let uploadedFiles = uploadInput.files;
            if(Object.entries(uploadedFiles).length > 0){
                let uploadedFile = uploadedFiles[0];
                
                var reader = new FileReader();
                reader.readAsText(uploadedFile);
                reader.onload = (event) =>{

                    let textData = event.target.result;
                    let allTextLines = textData.split(/\r\n|\n/);
                    let headers = allTextLines[0].split(',');

                    for(let i=1; i<allTextLines.length; i++){
                        let textLine = allTextLines[i];
                        let data = textLine.split(',');
                        if(data.length === headers.length){
                            let accountObject = {};
                            for(let j=0; j<headers.length; j++){
                                accountObject[headers[j]] = data[j];
                            }
                            accountsData.push(accountObject);
                        }
                    }
                    uploadAccountsForm.submit();
                }
            }
        }
        return uploadRanchAccountsContainer;
    }
}