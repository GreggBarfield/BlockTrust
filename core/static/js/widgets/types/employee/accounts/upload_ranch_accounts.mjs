import { Widget } from '../../../widget.mjs';
import { FileUploader } from '../../../../files/file_uploader.mjs';

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
        cardBody.className = "card-body row";
        let fileUploader = new FileUploader(cardBody, ["application/xls"]);
        uploadRanchAccountsContainer.append(cardBody);

        return uploadRanchAccountsContainer;
    }
}