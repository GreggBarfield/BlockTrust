import { InfoModal } from "../../../core/info_modal.mjs";
import { AsyncForm } from "../../../../global/async_form.mjs";

export class UploadVaccinationDatesWidget{
    constructor(vaccinations, vaccinationsAndDatesValues) {
        this.eids = [];
        this.infoModal = null;
        this.vaccinations = vaccinations;
        this.rowCounter = 1;
        this.vaccinationsAndDates = [];
        this.vaccinationAndDateElements = {};
        this.vaccinationsAndDatesValues = vaccinationsAndDatesValues;
    }

    createModalLink = () =>{
        let linkContainer = document.createElement("div");
        linkContainer.className = `d-flex justify-content-center align-items-center`;
        this.link = document.createElement("a");
        this.link.className = "h6";
        this.link.href="#";
        this.link.textContent = "Add Vaccination Details";
        this.link.onclick = () =>{
            this.displayModal();
        }
        linkContainer.append(this.link);
        return linkContainer;
    }

    displayModal = () =>{
        if(this.infoModal == null){
            let infoModal = new InfoModal("Enter Vaccination Details", null, true);
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

        let addNewVaccineLink = this.createAddNewVaccineLink();
        modalBodyContainer.append(addNewVaccineLink);

        let headerContainer = this.createHeaderContainer();
        modalBodyContainer.append(headerContainer);

        let uploadContainer = document.createElement("div");
        modalBodyContainer.append(uploadContainer);

        if(this.vaccinationsAndDatesValues){
            for(let vaccinationAndDateValue of this.vaccinationsAndDatesValues){
                let newRowElement = this.createVaccinationAndDateRow(vaccinationAndDateValue.vaccination, vaccinationAndDateValue.date);
                uploadContainer.append(newRowElement);
            }
        }

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

    createHeaderContainer = () =>{
        let headerContainer = document.createElement("div");
        headerContainer.className = "row m-1 p-1";

        let vaccinationHeader = document.createElement("div");
        vaccinationHeader.className = "col-md-4 h5 text-primary";
        vaccinationHeader.textContent = "Vaccination"
        headerContainer.append(vaccinationHeader);

        let dateHeader = document.createElement("div");
        dateHeader.className = "col-md-4 h5 text-primary";
        dateHeader.textContent = "Date";
        headerContainer.append(dateHeader);
        return headerContainer;
    }

    createAddNewVaccineLink = () =>{
        let newVaccineContainer = document.createElement("div");
        newVaccineContainer.className = "row m-1 p-1";

        let widgetLink = document.createElement("a");
        widgetLink.className = "form-label text-primary";
        widgetLink.textContent = "Don't see yours?";
        widgetLink.onclick = () => {
            this.createNewVaccinationModal();
        }
        newVaccineContainer.append(widgetLink);
        return newVaccineContainer; 
    }

    updateFooter = () =>{
        let modalFooter = this.infoModal.getFooter();
        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.onclick = () =>{  
            for(let [containerId, vaccinationAndDateElement] of Object.entries(this.vaccinationAndDateElements)){
                if(vaccinationAndDateElement.vaccinationInput.value == "" && vaccinationAndDateElement.dateInput.value == ""){
                    this.removeVaccinationAndDateRow(containerId);
                }
            }
            this.closeUploadModal();
        }
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
        $(vaccinationInput).val("").trigger("change");
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
            $(vaccinationInput).val(vaccinationValue).trigger("change");
        }
        if(dateValue !== null && dateValue.length >=0){
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

        this.vaccinationAndDateElements[containerId] = {"vaccinationInput": vaccinationInput, "dateInput": dateInput}
        this.rowCounter++;
        return container;
    }

    removeVaccinationAndDateRow = (containerId) =>{
        let rowElement = document.getElementById(containerId);
        if(rowElement){
            rowElement.remove();
        }
        delete this.vaccinationAndDateElements.containerId;
    }

    getVaccinationAndDateValues = () =>{
        let vaccinationAndDateValues = [];
        for(let vaccinationAndDateElement of Object.values(this.vaccinationAndDateElements)){
            if(vaccinationAndDateElement.vaccinationInput.value !== "" || vaccinationAndDateElement.dateInput.value !== ""){
                vaccinationAndDateValues.push({
                    "vaccination": vaccinationAndDateElement.vaccinationInput.value,
                    "date": vaccinationAndDateElement.dateInput.value
                });
            }
        }
        return vaccinationAndDateValues;
    }

    updateErrorMessage = (errorMessageText, errorMessageClass) =>{
        this.errorMessage.textContent = errorMessageText;
        this.errorMessage.className = errorMessageClass;
    }

    closeUploadModal = () =>{
        this.infoModal.close();
    }

    createNewVaccinationForm = () =>{
        let form = document.createElement("form");

        let firstFormRow = document.createElement("div");
        firstFormRow.className = "form-row";
        form.append(firstFormRow);

        let required = document.createElement("span");
        required.textContent = "*Required"
        required.style = "color: red;";
        firstFormRow.append(required);

        let vaccinationFormGroup = document.createElement("div");
        vaccinationFormGroup.className = "form-group col-md-12";
        
        let requiredIconName = document.createElement("span");
        requiredIconName.textContent = "*"
        requiredIconName.style = "color:red";
        let vaccinationName = document.createElement("label");
        vaccinationName.textContent = "Vaccination Name";
        vaccinationFormGroup.append(vaccinationName);
        vaccinationFormGroup.append(requiredIconName);
        let vaccinationNameInput = document.createElement("input");
        vaccinationNameInput.className = "form-control";
        vaccinationNameInput.type = "text";
        vaccinationFormGroup.append(vaccinationNameInput);
        form.append(vaccinationFormGroup);

        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.addEventListener("click", (e)=>{
            this.asyncForm.submit();
        });
        this.addVaccinationModalFooter.prepend(submitButton);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/add_new_sales_group_field_value",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            getData: () => {
                return {
                    field_name: "vaccination",
                    new_field_value: vaccinationNameInput.value          
                }
            },
            onFinished: (data) =>{
                let newVaccinationOption = new Option(data.new_field_value, data.new_field_value, false, false);
                let maintenanceVaccinations = document.getElementById(salesGroupFormInputIds.maintenanceVaccinations);
                $(maintenanceVaccinations).append(newVaccinationOption).trigger('change');
                this.infoModal.close();
            }
        });
        return form;
    }

    createNewVaccinationModal = () =>{
        let infoModal = new InfoModal("Add Vaccination");
        let modalBody = infoModal.getBody();

        let form = document.createElement("form");
        let firstFormRow = document.createElement("div");
        firstFormRow.className = "form-row";
        form.append(firstFormRow);

        let required = document.createElement("span");
        required.textContent = "*Required"
        required.style = "color: red;";
        firstFormRow.append(required);

        let vaccinationFormGroup = document.createElement("div");
        vaccinationFormGroup.className = "form-group col-md-12";
        
        let requiredIconName = document.createElement("span");
        requiredIconName.textContent = "*"
        requiredIconName.style = "color:red";
        let vaccinationName = document.createElement("label");
        vaccinationName.textContent = "Vaccination Name";
        vaccinationFormGroup.append(vaccinationName);
        vaccinationFormGroup.append(requiredIconName);
        let vaccinationNameInput = document.createElement("input");
        vaccinationNameInput.className = "form-control";
        vaccinationNameInput.type = "text";
        vaccinationFormGroup.append(vaccinationNameInput);
        form.append(vaccinationFormGroup);

        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.addEventListener("click", (e)=>{
            this.asyncForm.submit();
        });
        infoModal.getFooter().prepend(submitButton);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/add_new_sales_group_field_value",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            getData: () => {
                return {
                    field_name: "vaccination",
                    new_field_value: vaccinationNameInput.value          
                }
            },
            onFinished: (data) =>{
                this.updateVaccinationOptions(data.new_field_value);
                infoModal.close();
            }
        });
        modalBody.append(form);
    }

    updateVaccinationOptions = (vaccinationName) =>{
        this.vaccinations.push(vaccinationName);
        let newVaccinationOption = new Option(vaccinationName, vaccinationName, false, false);
        for(let vaccinationAndDateElement of Object.values(this.vaccinationAndDateElements)){
            $(vaccinationAndDateElement.vaccinationInput).append(newVaccinationOption).trigger('change');
        }
    }
}