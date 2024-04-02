import { InfoModal } from "../../../core/info_modal.mjs";

export class UploadVaccinationDatesWidget{
    constructor(vaccinations) {
        this.eids = [];
        this.infoModal = null;
        this.vaccinations = vaccinations;
        this.vaccinationsAndDates = [];
        console.log(this.vaccinations);
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
            let vaccinationDatesUploadContainer = this.generateVaccinationDatesUploadContainer();
            this.infoModal.getBody().append(vaccinationDatesUploadContainer);
        }
        else{
            this.infoModal.display();
        }
    }

    generateVaccinationDatesUploadContainer = () =>{
        let uploadContainer = document.createElement("div");
        let testdiv = this.createVaccinationAndDateRow();
        uploadContainer.append(testdiv);
        return uploadContainer;
    }

    createVaccinationAndDateRow = (vaccinationValue=null, dateValue=null) =>{
        let container = document.createElement("div");
        container.className = "row";
        let vaccinationInputContainer = document.createElement("div");
        vaccinationInputContainer.className = "col-md-4";
        let vaccinationInput = document.createElement("select");
        vaccinationInput.className = "form-control";
        //$(vaccinationInput).select2({data: this.vaccinations, dropdownParent: $(this.infoModal.getBody()), multiple: false, placeholder: "Select Vaccination"});
        vaccinationInputContainer.append(vaccinationInput);
        container.append(vaccinationInputContainer)

        let dateInputContainer = document.createElement("div");
        dateInputContainer.className = "col-md-4";
        let dateInput = document.createElement("input");
        dateInput.className = "form-control";
        dateInput.type = "date";
        dateInputContainer.append(dateInput);
        container.append(dateInputContainer);

        return container;



    }
}