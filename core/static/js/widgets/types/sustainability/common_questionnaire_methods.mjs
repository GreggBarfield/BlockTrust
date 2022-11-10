import { FileUploader } from "../../../files/file_uploader.mjs";
import { resourcesLink } from "../../../core/sustainability_constants.mjs";

export class CommonQuestionnaireMethods{
    /**
     * Creates a question container with the question text and select dropdown
     * @param {String} questionText The question text which needs to be added
     * @param {String} inputName The name of the group of questions
     * @param {String} inputID The unique ID of the question to calculate scores
     * @returns {Element} The element containing the question text and select input 
     */
    createSelectQuestion = (questionText, inputName, inputID) => {
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
        input.id = inputID

        let defaultOption = new Option("Please Select", "Please Select");
        defaultOption.selected = true;
        defaultOption.disabled = true;
        input.appendChild(defaultOption);
        input.appendChild(new Option("Yes", "Yes"));
        input.appendChild(new Option("No", "No"));
        questionInputContainer.append(input);

        questionContainer.append(questionTextContainer);
        questionContainer.append(questionInputContainer);
        return questionContainer;
    }
    /**
     * Creates a question container with the question text and an input field
     * @param {String} questionText The question text which needs to be added
     * @param {String} inputType The name of the group of questions
     * @param {String} inputName The type of input which needs to be accepted
     * @param {String} inputID The unique ID of the question to calculate scores
     * @param {Number} setMaxNumber The maximum number which can be entered as a response
     * @returns {Element} The element containing the question text and input field
     */
    createInputQuestion = (questionText, inputType, inputName, inputID, setMaxNumber=100) =>{
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
        input.id = inputID;
        input.min=0;
        if(inputType == "number"){
            input.max = setMaxNumber;
        }
        questionInputContainer.append(input);

        questionContainer.append(questionTextContainer);
        questionContainer.append(questionInputContainer);
        return questionContainer;
    }
    /**
     * Creates a question container with the question text and inline upload widget
     * @param {String} questionText The question text which needs to be added
     * @param {String} inputName The name of the group of questions
     * @param {String} inputID The unique ID of the question to calculate scores
     * @returns {Element} The element containing the question text and inline upload widget
     */
    createUploadQuestion = (questionText, inputName, inputID) => {
        let questionContainer = document.createElement("div");
        questionContainer.className = "row p-1 border-bottom"

        let questionTextContainer = document.createElement("div");
        questionTextContainer.className = "col-md-8";
        let label = document.createElement("label");
        label.textContent = questionText;
        questionTextContainer.append(label);

        let questionInputContainer = document.createElement("div");
        questionInputContainer.className = "col-md-4 p-1"
        let uploadOptionsDropDown = document.createElement("select");
        uploadOptionsDropDown.className = "form-control";
        uploadOptionsDropDown.name = inputName;
        uploadOptionsDropDown.id = inputID;

        let defaultOption = new Option("Please Select", "Please Select");
        defaultOption.selected = true;
        defaultOption.disabled = true;
        uploadOptionsDropDown.appendChild(defaultOption);
        uploadOptionsDropDown.appendChild(new Option("Yes", "Yes"));
        uploadOptionsDropDown.appendChild(new Option("No", "No"));
        questionInputContainer.append(uploadOptionsDropDown);
        
        let questionUploadContainer = document.createElement("div");
        questionUploadContainer.className = "col-md-12 p-1 justify-content-center";
        let uploadInput = new FileUploader(questionUploadContainer, ["application/pdf"]);

        questionContainer.append(questionTextContainer);
        questionContainer.append(questionInputContainer);
        questionContainer.append(questionUploadContainer);
        uploadOptionsDropDown.onchange = () => {
            if(uploadOptionsDropDown.value == "Yes"){
                questionUploadContainer.style.display = 'flex';
                uploadInput.uploadDeclinedByUser=false;
            }
            else{
                questionUploadContainer.style.display = 'none';
                uploadInput.uploadDeclinedByUser=true;
            }
        }
        uploadOptionsDropDown.onchange();
        return {questionContainer, uploadInput};
    }
    /**
     * Returns a card element with a specified header text for question groups
     * @param {String} questionsSectionHeaderText Headet text for the card element
     * @returns {Element} The card element with a specified header
     */
    createQuestionsSection = (questionsSectionHeaderText) => {
        let section = document.createElement("div");
        section.className = "card col-xl-10 border border-dark";

        let sectionHeader = document.createElement("div");
        sectionHeader.className = "card-header border-bottom border-dark d-flex";
        section.append(sectionHeader);

        let sectionHeaderText = document.createElement("div");
        sectionHeaderText.className = "h6 text-bold col-xl-6";
        sectionHeaderText.textContent = questionsSectionHeaderText;

        let resourcesLinkContainer = document.createElement("div");
        resourcesLinkContainer.className = "col-xl-6";
        
        let link = document.createElement("a");
        link.className = "float-right";
        link.textContent = "Resources";
        link.href = resourcesLink;
        link.target = "_blank";
        resourcesLinkContainer.append(link);

        sectionHeader.append(sectionHeaderText);
        sectionHeader.append(resourcesLinkContainer);
        
        return section;
    }
}