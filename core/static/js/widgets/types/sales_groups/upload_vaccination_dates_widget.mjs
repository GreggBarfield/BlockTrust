import { InfoModal } from "../../../core/info_modal.mjs";

export class UploadVaccinationDatesWidget{
    constructor(vaccinations) {
        this.eids = [];
        this.infoModal = null;
        this.vaccinations = vaccinations;
        this.rowCounter = 1;
        this.vaccinationsAndDates = [];
        this.vaccinationAndDateELements = {}
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
            this.updateFooter();
        }
        else{
            this.infoModal.display();
        }
    }

    generateVaccinationDatesUploadContainer = () =>{
        let modalBodyContainer = document.createElement("div");
        let uploadContainer = document.createElement("div");
        modalBodyContainer.append(uploadContainer);

        let optionsRow = document.createElement("div");
        let addNewRowButtonContainer = document.createElement("div");
        let addNewRowButton = document.createElement("button");
        addNewRowButton.className = "btn btn-primary";
        addNewRowButton.textContent = "Add New Vaccination";
        addNewRowButton.onclick = () =>{
            let newRowElement = this.createVaccinationAndDateRow();
            uploadContainer.append(newRowElement);
        }
        addNewRowButtonContainer.append(addNewRowButton);
        optionsRow.append(addNewRowButtonContainer);
        modalBodyContainer.append(optionsRow);

        this.statusMessage = document.createElement("p");
        this.statusMessage.style.display = "none";
        this.statusMessage.className = "mt-2 mb-0";
        modalBodyContainer.append(this.statusMessage);

        this.errorMessage = document.createElement("p");
        this.errorMessage.style.display = "none";
        this.errorMessage.className = "mt-2 mb-0 alert alert-danger";
        modalBodyContainer.append(this.errorMessage);
        return modalBodyContainer;
    }

    updateFooter = () =>{
        let modalFooter = this.infoModal.getFooter();
        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        modalFooter.prepend(submitButton);
    }

    createVaccinationAndDateRow = (vaccinationValue=null, dateValue=null) =>{
        let vaccinationsList = [];
        let containerId = "data-row-" + this.rowCounter;
        for(let vaccination of this.vaccinations){
            vaccinationsList.push({id: vaccination, text: vaccination});
        }
        let container = document.createElement("div");
        container.className = "row m-1 p-1";
        container.id = containerId; 

        let vaccinationInputContainer = document.createElement("div");
        vaccinationInputContainer.className = "col-md-4";
        let vaccinationInput = document.createElement("select");
        vaccinationInput.className = "form-control";
        vaccinationInputContainer.append(vaccinationInput);
        $(vaccinationInput).select2({data: vaccinationsList, dropdownParent: $(this.infoModal.getBody()), multiple: false, placeholder: "Select Vaccination"});
        vaccinationInputContainer.append(vaccinationInput);
        container.append(vaccinationInputContainer);

        let dateInputContainer = document.createElement("div");
        dateInputContainer.className = "col-md-4";
        let dateInput = document.createElement("input");
        dateInput.className = "form-control";
        dateInput.type = "date";
        dateInputContainer.append(dateInput);
        container.append(dateInputContainer);
        if(vaccinationValue !== null){
            $(vaccinationInput).val(vaccinationValue).trigger('change');
        }
        if(dateValue !== null){
            dateInput.value = dateValue;
        }

        let removeButtonContainer = document.createElement("div");
        removeButtonContainer.className = "col-md-4";
        let removeButton = document.createElement("button");
        removeButton.className = "btn btn-danger btn-sm";
        removeButton.textContent = "Remove";
        removeButtonContainer.append(removeButton);
        removeButton.onclick = () =>{
            this.removeVaccinationAndDateRow(containerId)
        }
        container.append(removeButtonContainer);

        this.vaccinationAndDateELements.containerId = {"vaccinationInput": vaccinationInput, "dateInput": dateInput}
        this.rowCounter++;
        return container;
    }


    removeVaccinationAndDateRow = (containerId) =>{
        let rowElement = document.getElementById(containerId);
        if(rowElement){
            rowElement.remove();
        }
        delete this.vaccinationAndDateELements.containerId;
    }

    getVaccinationAndDateValues = () =>{
        let vaccinationAndDateValues = [];
        for(let vaccinationAndDateElement in Object.values(this.vaccinationAndDateELements)){
            vaccinationAndDateValues.push({
                "vacccination": vaccinationAndDateElement.vaccinationInput,
                "date": vaccinationAndDateElement.dateInput
            })
        }
    }

    updateErrorMessage = (errorMessageText, errorMessageClass) =>{
        this.errorMessage.textContent = errorMessageText;
        this.errorMessage.className = errorMessageClass;
    }
}