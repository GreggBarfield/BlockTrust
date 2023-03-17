import {CoreModal} from "./core_modal.mjs";

export class InfoModal extends CoreModal {
    /**
     * Constructs the info modal.
     * 
     * @param {string} headerText Text for the header
     * @param {string|null} [contentText] Text for the content, or null for nothing
     * @param {boolean} [wide] Whether to make the modal wide. Default false
     */
    constructor(headerText, contentText=null, wide=false) {
        super(wide);
        let that = this;

        let modalHeader = document.createElement("div");
        modalHeader.className = "modal-header";
        
        let modalHeaderH5 = document.createElement("h5");
        modalHeaderH5.className = "modal-title";
        modalHeaderH5.innerHTML = headerText;
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
        this.modalBody = modalBody;
        modalBody.className = "modal-body";

        if (contentText !== null) {
            // Sometimes stuff is just appended to body manually
            let modalBodyP = document.createElement("p");
            modalBodyP.textContent = contentText;
            modalBody.append(modalBodyP);
        }

        this.modalContent.append(modalBody);

        let modalFooter = document.createElement("div");
        this.modalFooter = modalFooter;
        modalFooter.className = "modal-footer";

        this.actionButtonDiv = document.createElement("div");
        modalFooter.append(this.actionButtonDiv);

        let closeButton = document.createElement("button");
        closeButton.className = "btn btn-secondary";
        closeButton.textContent = "Close";
        closeButton.addEventListener("click", ()=>{
            that.close();
        });
        modalFooter.append(closeButton);

        this.modalContent.append(modalFooter);
    }

    getBody() {
        return this.modalBody;
    }

    getActionButtonDiv() {
        return this.actionButtonDiv;
    }

    getFooter() {
        return this.modalFooter;
    }

}