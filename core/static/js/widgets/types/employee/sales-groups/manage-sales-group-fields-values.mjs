import { AsyncForm } from '../../../../../global/async_form.mjs';
import { Widget } from "../../../widget.mjs";
import { InfoModal } from '../../../../core/info_modal.mjs';

export class ManageSalesGroupFieldsValuesWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";
        let salesGroupFieldsValues = JSON.parse(this.frame.getAttribute("data-widget-sales-group-fields-values"));
        let salesGroupFieldsIdsToNames = JSON.parse(this.frame.getAttribute("data-widegt-sales-group-field-ids-to-names"));

        let salesGroupFieldsValuesContainer  = this.createSalesGroupFieldsValuesContainer(salesGroupFieldsValues, salesGroupFieldsIdsToNames);
        this.frame.append(salesGroupFieldsValuesContainer);
    }

    createSalesGroupFieldsValuesContainer = (salesGroupFieldsValues, salesGroupFieldsIdsToNames) =>{
        let salesGroupFieldIdsAndValues = {}
        let salesGroupFieldsValuesContainer = document.createElement("div");

        for(const salesGroupFieldValue of salesGroupFieldsValues){
            if(salesGroupFieldValue.field_id in salesGroupFieldIdsAndValues){
                salesGroupFieldIdsAndValues[salesGroupFieldValue.field_id].push(salesGroupFieldValue);
            }
            else{
                salesGroupFieldIdsAndValues[salesGroupFieldValue.field_id] = [salesGroupFieldValue]
            }
        }

        for(const [fieldId, fieldValues] of Object.entries(salesGroupFieldIdsAndValues)){
            let fieldContainer = this.createFieldContainer(fieldId, fieldValues, salesGroupFieldsIdsToNames);
            salesGroupFieldsValuesContainer.append(fieldContainer);
        }
        return salesGroupFieldsValuesContainer;
    }

    createFieldContainer = (fieldId, fieldValues, salesGroupFieldsIdsToNames) =>{
        let fieldContainer = document.createElement("div");
        fieldContainer.className = "card";

        let fieldHeader = document.createElement("h5");
        fieldHeader.className = "card-header";
        fieldHeader.textContent = salesGroupFieldsIdsToNames[fieldId].replaceAll("_", " ").toUpperCase();
        fieldContainer.append(fieldHeader);

        let fieldBody = document.createElement("div");
        fieldBody.className = "card-body";

        let fieldValuesList = document.createElement("div");
        fieldValuesList.className = "row";
        for(let fieldValue of fieldValues){
            let fieldValueElement = document.createElement("ul");
            fieldValueElement.textContent = fieldValue.value;
            fieldValuesList.append(fieldValueElement);
        }
        fieldBody.append(fieldValuesList);

        let fieldOptionsList = document.createElement("div");
        fieldOptionsList.className = "row m-2 p-2";
        let addOptionsButton = this.createAddOptionsButton(fieldId, salesGroupFieldsIdsToNames);
        fieldOptionsList.append(addOptionsButton);
        let removeOptionButton = this.createRemoveOptionsButton(fieldId, fieldValues, salesGroupFieldsIdsToNames);
        fieldOptionsList.append(removeOptionButton);
        fieldBody.append(fieldOptionsList);

        fieldContainer.append(fieldBody);
        return fieldContainer;

    }

    createRemoveOptionsButton = (fieldId, fieldValues, salesGroupFieldsIdsToNames) =>{
        let button = document.createElement("button");
        button.className = "btn btn-danger";
        button.textContent = "Remove Options";
        let fieldValuesList = []
        for(let fieldValue of fieldValues){
            fieldValuesList.push({id: fieldValue.id, text: fieldValue.value});
        }
        button.onclick = () =>{
            let modal = new InfoModal("Remove Options from " + salesGroupFieldsIdsToNames[fieldId].replaceAll("_", " ").toUpperCase(), null, true);
            let modalBody = modal.getBody();
            let optionsSelect = document.createElement("select");      
            optionsSelect.className = "form-control";
            modalBody.append(optionsSelect);
            $(optionsSelect).select2({data: fieldValuesList, dropdownParent: $(modalBody), multiple: true, placeholder: "Select Options to Remove"});
        }
        return button;
    }

    createAddOptionsButton = (fieldId, salesGroupFieldsIdsToNames) =>{
        let button = document.createElement("button");
        button.className = "btn btn-primary";
        button.textContent = "Add Options";
        button.onclick = () =>{
            let modal = new InfoModal("Add Options to " + salesGroupFieldsIdsToNames[fieldId].replaceAll("_", " ").toUpperCase(), null, true);
            let modalBody = modal.getBody();
            let inputLabel = document.createElement("label");
            inputLabel.textContent = "*Enter new values to be added separated by commas";
            modalBody.append(inputLabel);
            let input = document.createElement("input");
            input.type = "text";
            input.size = "100";
            modalBody.append(input);
        }
        return button;
    }
}