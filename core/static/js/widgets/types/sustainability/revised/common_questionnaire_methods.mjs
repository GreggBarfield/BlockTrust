export class CommonQuestionnaireMethods{
    createSelectQuestion = (questionSection, questionText, inputName) => {
        let questionContainer = document.createElement("div");
        questionContainer.className = "row p-1 border-bottom"

        let questionTextContainer = document.createElement("div");
        questionTextContainer.className = "col-md-8";
        let label = document.createElement("label");
        label.textContent = questionText;
        questionTextContainer.append(label);

        let questionInputContainer = document.createElement("div");
        questionInputContainer.className = "col-md-4 p-1"
        let input = document.createElement("select");
        input.className = "form-control";
        input.name = inputName;

        let defaultOption = new Option("Please Select", "Please Select");
        defaultOption.selected = true;
        defaultOption.disabled = true;
        input.appendChild(defaultOption);
        let options = ["Yes", "No"];

        for(const option of options){
            var inputOption = new Option(option, option);
            input.appendChild(inputOption);
        }
        questionInputContainer.append(input);

        questionContainer.append(questionTextContainer);
        questionContainer.append(questionInputContainer);
        questionSection.append(questionContainer);
    }
    createInputQuestion = (questionSection, questionText, inputType, inputName, setMaxNumber=100) =>{
        let questionContainer = document.createElement("div");
        questionContainer.className = "row p-1 border-bottom"

        let questionTextContainer = document.createElement("div");
        questionTextContainer.className = "col-md-8";
        let label = document.createElement("label");
        label.textContent = questionText;
        questionTextContainer.append(label);

        let questionInputContainer = document.createElement("div");
        questionInputContainer.className = "col-md-4 p-1"
        let input = document.createElement("input");
        input.type = inputType;
        input.className = "form-control";
        input.name = inputName;
        if(inputType == "number"){
            input.max = setMaxNumber;
        }
        questionInputContainer.append(input);

        questionContainer.append(questionTextContainer);
        questionContainer.append(questionInputContainer);
        questionSection.append(questionContainer);
    }
    createUploadQuestion = (questionSection, questionText, inputName) => {
        let questionContainer = document.createElement("div");
        questionContainer.className = "row p-1 border-bottom"

        let questionTextContainer = document.createElement("div");
        questionTextContainer.className = "col-md-8";
        let label = document.createElement("label");
        label.textContent = questionText;
        questionTextContainer.append(label);

        let questionInputContainer = document.createElement("div");
        questionInputContainer.className = "col-md-2 p-1"
        let input = document.createElement("select");
        input.className = "form-control";
        input.name = inputName;
        let options = ["Yes", "No"];

        let defaultOption = new Option("Please Select", "Please Select");
        defaultOption.selected = true;
        defaultOption.disabled = true;
        input.appendChild(defaultOption);
        
        for(const option of options){
            var inputOption = new Option(option, option);
            input.appendChild(inputOption);
        }
        questionInputContainer.append(input);
        
        let questionUploadContainer = document.createElement("div");
        questionUploadContainer.className = "col-md-2 p-1";
        let uploadButton = document.createElement("button");
        uploadButton.className = "btn btn-primary";
        uploadButton.textContent = "Upload";
        questionUploadContainer.append(uploadButton);

        questionContainer.append(questionTextContainer);
        questionContainer.append(questionInputContainer);
        questionContainer.append(questionUploadContainer);
        input.onchange = () => {
            if(input.value == "Yes"){
                questionUploadContainer.style.display = 'block';
            }
            else{
                questionUploadContainer.style.display = 'none';
            }
        }
        
        questionSection.append(questionContainer);
    }
    createQuestionsSection = (questionsSectionHeaderText) => {
        let section = document.createElement("div");
        section.className = "card col-xl-10 border border-dark";

        let sectionHeader = document.createElement("div");
        sectionHeader.className = "card-header border-bottom border-dark";
        section.append(sectionHeader);

        let sectionHeaderText = document.createElement("div");
        sectionHeaderText.className = "h6 text-bold";
        sectionHeaderText.textContent = questionsSectionHeaderText;
        sectionHeader.append(sectionHeaderText);
        
        let sectionBody = document.createElement("div");
        sectionBody.className = "card-body";
        //section.append(sectionBody);
        return section;
    }
}