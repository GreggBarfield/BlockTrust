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

const advertisementFormFields = ["ad_company", "ad_category", "short_description", "long_description"];

const advertisementCompanyFormFields = ["name", "email", "contact_name", "address", "city", "state", "zip_code", "phone"];

const validateFormCompletion = (formFieldIds) =>{
    let formCompletionStatus = true;
    for(let fieldId of formFieldIds){
        let fieldValue = document.getElementById(fieldId).value;
        if(fieldValue == "" || fieldValue == -1){
            formCompletionStatus = false;
        }
    }
    return formCompletionStatus;
}

export {
    generateTextInput,
    generateDropDownInput,
    validateFormCompletion,
    advertisementFormFields,
    advertisementCompanyFormFields
}