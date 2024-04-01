import { InfoModal } from "../../../core/info_modal.mjs";

export class UploadVaccinationDatesWidget{
    constructor() {
        this.eids = [];
        this.infoModal = null;
    }

    createModalLink = () =>{
        let linkContainer = document.createElement("div");
        linkContainer.className = `d-flex justify-content-center align-items-center`;
        this.link = document.createElement("a");
        this.link.className = "h6";
        this.link.href="#";
        this.link.textContent = "Add Vaccination Dates";
        this.link.onclick = () =>{
            this.displayModal();
        }
        linkContainer.append(this.link);
        return linkContainer;
    }

    displayModal = () =>{
        if(this.infoModal == null){
            let infoModal = new InfoModal("Upload Vaccination Dates", null, true);
            this.infoModal = infoModal;
            let eidsUploadersContainer = this.generateEidsUploadContainer();
            this.infoModal.getBody().append(eidsUploadersContainer);
        }
        else{
            this.infoModal.display();
        }
    }
}