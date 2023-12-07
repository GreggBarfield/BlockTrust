import { InfoModal } from "../../../core/info_modal.mjs";
import { AsyncForm } from "../../../../global/async_form.mjs";
import { Widget } from "../../widget.mjs";
import { salesGroupFormInputIds } from "../../utilities/sales_group_constants.mjs";

export class CreateVaccinationWidget extends Widget{
    constructor(){
        let infoModal = new InfoModal("Add Vaccination");
        super(infoModal.getBody());
        this.addVaccinationModalFooter = infoModal.getFooter();
        this.infoModal = infoModal;
    }

    initType = () =>{
        this.frame.innerHTML = "";
        let addVaccinationForm = this.generateAddVaccinationForm();
        this.frame.append(addVaccinationForm);
    }

    generateAddVaccinationForm = () =>{
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
                    field_name: "Vaccinations",
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
}