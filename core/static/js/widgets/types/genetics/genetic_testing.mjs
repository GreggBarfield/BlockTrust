import { Widget } from '../../widget.mjs';
import { breedOptions, sexOptions, parentageTestingOptions, sampleTypeOptions } from '../../utilities/genetic_testing_constants.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class GeneticTestingWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () => {
        this.frame.innerHTML = "";
        let geneticTestingContainer = document.createElement("div");
        geneticTestingContainer.className = "card";
        let geneticTestingContainerHeader = document.createElement("h5");
        geneticTestingContainerHeader.className = "card-header";
        geneticTestingContainerHeader.textContent = "Genetic Testing";
        geneticTestingContainer.append(geneticTestingContainerHeader);
        geneticTestingContainer.append(this.createInfoText());
        let geneticTestingForm = this.createGeneticTestingForm();
        geneticTestingContainer.append(geneticTestingForm);
        this.frame.append(geneticTestingContainer);
    }

    createInfoText = () => {
        let container = document.createElement("p");
        container.classList = "card-header";
        let image = document.createElement("img");
        image.src = "/static/images/partners/logos/neogen-logo.png";
        image.classList = "float-left";
        container.append(image);
        let div = document.createElement("div");
        div.classList = "mt-2";
        div.innerHTML = "Genetics testing is available through our partner, Neogen.    To start genetics testing, please enter your tags using the form below.  The data will be transferred to Neogen so all you have to do is retrieve your DNA samples and send them in. Results will come back through your dashboard and we will notify you of the next steps.";
        container.append(div);
        return container;
    }

    createInput = (inputLabeltext, inputType, inputId, inputRequired=false, inputSize="col-md-3") =>{
        let inputContainer = document.createElement("div");
        inputContainer.className = inputSize;

        let inputLabel = document.createElement("div");
        inputLabel.textContent = inputLabeltext;
        inputLabel.className = "m-1 p-1 font-weight-bold";
        inputContainer.append(inputLabel);

        let input = document.createElement("input");
        input.className = "form-control"
        input.type = inputType;
        input.id = inputId;
        input.required = inputRequired;
        if(inputType == "number"){
            input.min = 0;
        }
        inputContainer.append(input);
        return inputContainer;
    }

    createSelectInput = (inputLabelText, inputOptions, inputId, inputRequired=false, inputSize="col-md-3") =>{
        let inputContainer = document.createElement("div");
        inputContainer.className = inputSize;

        let inputLabel = document.createElement("div");
        inputLabel.textContent = inputLabelText;
        inputLabel.className = "m-1 p-1 font-weight-bold";
        inputContainer.append(inputLabel);

        let select = document.createElement("select");
        select.className = "form-control";
        select.id = inputId;
        select.required = inputRequired;
        let defaultOption = document.createElement("option");
        defaultOption.textContent = "Select";
        defaultOption.value = "-1";
        defaultOption.disabled = true;
        defaultOption.selected = true;
        select.appendChild(defaultOption);
        for(let inputOption of inputOptions){
            let option = document.createElement("option");
            option.textContent = inputOption.text;
            option.value = inputOption.value;
            select.appendChild(option);
        }
        inputContainer.append(select);
        return inputContainer;
    }

    createRemoveButton = (uid) =>{
        let removeButton = document.createElement("button");
        removeButton.className = "btn btn-danger btn-sm";
        removeButton.textContent = "Remove";
        removeButton.onclick = () =>{
            this.dataInputRowsContainer.removeChild(document.getElementById(uid));
        }
        return removeButton;
    }

    checkValue = (value) =>{
        if(value !== "" && value !== null && value !== "-1"){
            return true;
        }
        return false;
    }

    saveAndSubmitData = () =>{
        let geneticData = [];
        let dataInputRows = document.getElementsByName("data-input-row");
        for(let inputRow of dataInputRows){
            let id = inputRow.id;
            let barcodeInput = document.getElementById("barcode-"+id);
            let animalIdInput = document.getElementById("animal-id-"+id);
            let breedInput = document.getElementById("breed-"+id);
            let sexInput = document.getElementById("sex-"+id);
            let parentageInput = document.getElementById("parentage-"+id);
            let sampleTypeInput = document.getElementById("sample-type-"+id);
            geneticData.push({
                sample_barcode: this.checkValue(barcodeInput.value) ? barcodeInput.value : "",
                animal_id: this.checkValue(animalIdInput.value) ? animalIdInput.value : "",
                breed: this.checkValue(breedInput.value) ? breedInput.value : "",
                sex: this.checkValue(sexInput.value) ? sexInput.value : "",
                parentage_testing: this.checkValue(parentageInput.value) ? parentageInput.value : "",
                sample_type: this.checkValue(sampleTypeInput.value) ? sampleTypeInput.value : ""
            })
        }
        
        let geneticTestingForm = new AsyncForm({
            action: window.location.href,
            form: this.geneticTestingForm,
            status: this.statusMessage,
            error: this.errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    genetic_testing_data: geneticData
                };
            }
        });
    }

    createNewDataInputRow = () =>{
        let dataInputRow = document.createElement("div");
        dataInputRow.className = "row d-flex m-2 p-2 border rounded";
        dataInputRow.setAttribute("name", "data-input-row");
        const uid = Math.random().toString(36).substring(2, 9);
        dataInputRow.id = uid;

        let removeButtonContainer = document.createElement("div");
        removeButtonContainer.className = "col-md-12 d-flex flex-row-reverse";
        let removeButton = this.createRemoveButton(uid);
        removeButtonContainer.append(removeButton);
        dataInputRow.append(removeButtonContainer);

        let sampleBarcode = this.createInput("Sample Barcode", "number", "barcode-"+uid, true);
        dataInputRow.append(sampleBarcode);
        let animalId = this.createInput("Animal ID", "number", "animal-id-"+uid, true);
        dataInputRow.append(animalId);
        let breedSelect = this.createSelectInput("Breed", breedOptions, "breed-"+uid);
        dataInputRow.append(breedSelect);
        let sexOptionsSelect = this.createSelectInput("Sex", sexOptions, "sex-"+uid);
        dataInputRow.append(sexOptionsSelect);
        let parentageSelect = this.createSelectInput("Parentage Testing", parentageTestingOptions, "parentage-"+uid);
        dataInputRow.append(parentageSelect);
        let sampleTypeSelect = this.createSelectInput("Sample Type", sampleTypeOptions, "sample-type-"+uid);
        dataInputRow.append(sampleTypeSelect);
        this.dataInputRowsContainer.append(dataInputRow);
    }

    createGeneticTestingForm = () =>{
        this.geneticTestingForm = document.createElement("form");
        let geneticTestingContainer = document.createElement("div");
        geneticTestingContainer.className = "card border border-white m-0 p-0";
        this.dataInputRowsContainer = document.createElement("div");
        this.dataInputRowsContainer.className = "col";
        geneticTestingContainer.append(this.dataInputRowsContainer);
        this.createNewDataInputRow();

        let addNewRowButtonContainer = document.createElement("div");
        addNewRowButtonContainer.className = "m-1 p-1";
        let addNewRowButton = document.createElement("button");
        addNewRowButton.className = "btn btn-primary m-1 p-1";
        addNewRowButton.textContent = "Add New Row";
        addNewRowButton.onclick = (event) =>{
            event.preventDefault();
            this.createNewDataInputRow();
        }
        addNewRowButtonContainer.append(addNewRowButton);
        geneticTestingContainer.append(addNewRowButtonContainer);

        let submitButtonContainer = document.createElement("div");
        submitButtonContainer.className = "m-2 p-2";
        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.onclick = () =>{
            this.saveAndSubmitData();
        }
        submitButtonContainer.append(submitButton);
        geneticTestingContainer.append(submitButtonContainer);

        this.statusMessage = document.createElement("p");
        this.statusMessage.className = "text-success";
        geneticTestingContainer.append(this.statusMessage);
        this.errorMessage = document.createElement("p");
        this.errorMessage.className = "text-danger";
        geneticTestingContainer.append(this.errorMessage);

        this.geneticTestingForm.append(geneticTestingContainer)
        return this.geneticTestingForm;
    }
}