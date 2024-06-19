import { Widget } from '../../widget.mjs';

export class GeneticTestingWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () => {
        this.frame.innerHTML = "";
        let geneticTestingContainer = this.createGeneticTrestingContainer();
        this.frame.append(geneticTestingContainer);
    }

    createInput = (inputLabeltext, inputType) =>{
        let inputContainer = document.createElement("div");
        inputContainer.className = "col-md-3";

        let inputLabel = document.createElement("div");
        inputLabel.textContent = inputLabeltext;
        inputLabel.className = "m-1 p-1";
        inputContainer.append(inputLabel);

        let input = document.createElement("input");
        input.className = "form-control"
        input.type = inputType;
        if(inputType == "number"){
            input.min = 0;
        }
        inputContainer.append(input);
        return inputContainer;
    }

    createSelectInput = (inputLabel, inputValues) =>{
        let inputContainer = document.createElement("div");
        inputContainer.className = "col-md-3";

        let inputLabel = document.createElement("div");
        inputLabel.textContent = inputLabeltext;
        inputLabel.className = "m-1 p-1";
        inputContainer.append(inputLabel);

        let select = document.createElement("select");
        select.className = "form-control";
        inputContainer.append(select);
        return inputContainer;
    }

    createNewDataInputRow = () =>{
        let dataInputRow = document.createElement("div");
        dataInputRow.className = "row d-flex m-1 p-1";

        let sampleBarcode = this.createInput("Sample Barcode", "number");
        dataInputRow.append(sampleBarcode);
        let animalId = this.createInput("Animal ID", "number");
        dataInputRow.append(animalId);
        this.dataInputRowsContainer.append(dataInputRow);
    }

    createGeneticTrestingContainer = () =>{
        let geneticTestingContainer = document.createElement("div");
        geneticTestingContainer.className = "card";
        this.dataInputRowsContainer = document.createElement("div");
        this.dataInputRowsContainer.className = "col";
        geneticTestingContainer.append(this.dataInputRowsContainer);
        this.createNewDataInputRow();

        let addNewRowButtonContainer = document.createElement("div");
        addNewRowButtonContainer.className = "m-1 p-1";
        let addNewRowButton = document.createElement("button");
        addNewRowButton.className = "btn btn-primary m-1 p-1";
        addNewRowButton.textContent = "Add New Row";
        addNewRowButton.onclick = () =>{
            this.createNewDataInputRow();
        }
        addNewRowButtonContainer.append(addNewRowButton);
        geneticTestingContainer.append(addNewRowButtonContainer);

        return geneticTestingContainer;
    }
}