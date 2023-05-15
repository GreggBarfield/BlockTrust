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

        let form = document.createElement("form");

        let uploadInputContainer  = document.createElement("div");
        uploadInputContainer.className = "col-md-6 m-3 p-3";
        let uploadInput = document.createElement("input");
        uploadInput.type = "file";
        uploadInput.multiple = false;
        uploadInput.size = "60";
        uploadInputContainer.append(uploadInput);
        form.append(uploadInputContainer);
        
        let uploadAccountsButton = document.createElement("button");
        uploadAccountsButton.className = "btn btn-outline-primary rounded m-2";
        uploadAccountsButton.textContent = "Upload Accounts";
        form.append(uploadAccountsButton);

        let statusMessage = document.createElement("p");
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        form.append(errorMessage);

        uploadAccountsButton.onclick = async() =>{
            let uploadAccountsForm = new AsyncForm({
                action: "/employee/upload-accounts-for-partner",
                form: form,
                status: statusMessage,
                error: errorMessage,
                redirectMessage: "Saved!",
                loadingMessage: "Saving...",
                getData: () => {
                    return {
                        partner_id: partnerId,
                        file: uploadInput.files[0]
                    };
                }
            });
            if(uploadInput.files.length() > 0){
                uploadAccountsForm.submit();
            }
        }

        cardBody.append(form);
        uploadRanchAccountsContainer.append(cardBody);
        return uploadRanchAccountsContainer;
    }
}