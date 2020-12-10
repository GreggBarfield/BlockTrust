import {CoreModal} from "./core_modal.mjs";

export class InfoModal extends CoreModal {
    constructor(headerText, contentText) {
        super();
        let that = this;

        let modalHeader = document.createElement("div");
        modalHeader.className = "modal-header";
        
        let modalHeaderH5 = document.createElement("h5");
        modalHeaderH5.className = "modal-title";
        modalHeaderH5.textContent = headerText;
        modalHeader.append(modalHeaderH5);

        let modalHeaderX = document.createElement("button");
        modalHeaderX.className = "close";
        modalHeaderX.addEventListener("click", ()=>{
            that.close();
        });
        modalHeaderX.textContent = "x";
        modalHeader.append(modalHeaderX);
        
        this.modalContent.append(modalHeader);

        let modalBody = document.createElement("div");
        modalBody.className = "modal-body";

        let modalBodyP = document.createElement("p");
        modalBodyP.textContent = contentText;
        modalBody.append(modalBodyP);

        this.modalContent.append(modalBody);

        let modalFooter = document.createElement("div");
        modalFooter.className = "modal-footer";

        let closeButton = document.createElement("button");
        closeButton.className = "btn btn-secondary";
        closeButton.textContent = "Close";
        closeButton.addEventListener("click", ()=>{
            that.close();
        });
        modalFooter.append(closeButton);

        this.modalContent.append(modalFooter);
    }
}