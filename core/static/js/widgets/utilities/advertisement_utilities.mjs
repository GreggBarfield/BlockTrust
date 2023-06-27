const generateTextInput = (inputText, inputType, inputId, inputRequired, inputSize) =>{
    let inputContainer = document.createElement("div");
    inputContainer.className = inputSize;
    let input = document.createElement("input");
    input.placeholder = inputText;
    input.type = inputType;
    input.id = inputId;
    input.className = "form-control m-1";
    input.required = inputRequired;
    inputContainer.append(input);
    if(inputType === "checkbox"){
        input.className = "form-control col-md-1 m-1"
        let checkboxText = document.createElement("h6");
        checkboxText.textContent = inputText;
        inputContainer.append(checkboxText);
    }
    return inputContainer;
}

const generateDropDownInput = (inputId, inputOptions, defaultOptionText, inputRequired) =>{
    let inputContainer = document.createElement("div");
    inputContainer.className = "col-md-6";
    let selectInput = document.createElement("select");
    selectInput.id = inputId;
    selectInput.required = inputRequired;
    selectInput.className = "form-control m-1";

    let defaultDisabledOption = document.createElement("option");
    defaultDisabledOption.selected = true;
    defaultDisabledOption.disabled = true;
    defaultDisabledOption.textContent = defaultOptionText;
    defaultDisabledOption.value = -1;
    selectInput.appendChild(defaultDisabledOption);
    for(let [optionValue, optionTextContent] of Object.entries(inputOptions)){
        let option = document.createElement("option");
        option.value = optionValue;
        option.textContent = optionTextContent;
        selectInput.appendChild(option);
    }
    inputContainer.append(selectInput);
    return inputContainer;
}

const generateUploadInput = (inputText) =>{
    let uploadInputContainer  = document.createElement("div");
    uploadInputContainer.className = "col-md-6 d-flex";
    let uploadInputText = document.createElement("h6");
    uploadInputText.textContent = inputText;
    uploadInputText.className = "m-2 p-1";
    let uploadInput = document.createElement("input");
    uploadInput.type = "file";
    uploadInput.multiple = false;
    uploadInput.required = false;
    uploadInput.className = "m-2 p-1";
    uploadInputContainer.append(uploadInputText);
    uploadInputContainer.append(uploadInput);
    return uploadInputContainer;
}

const validateFormCompletion = (formResponseValues) =>{
    let formCompletionStatus = true;
    for(let value of formResponseValues){
        if(value == "" || value == -1){
            formCompletionStatus = false;
        }
    }
    return formCompletionStatus;
}

export {
    generateTextInput,
    generateDropDownInput,
    generateUploadInput,
    validateFormCompletion
}