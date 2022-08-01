import { Widget } from '../../widget.mjs';
import { CommonQuestionnaireMethods } from './common_questionnaire_methods.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { sections, scoringCriteria, questionType } from '../../../core/sustainability_constants.mjs'

export class BaseQuestionnaireV2Widget extends Widget{
    constructor(frame) {
        super(frame);
        this.scores = {};
        this.scores.air = 0;
        this.scores.land = 0;
        this.scores.water = 0;
        this.scores.safety = 0;
        this.scores.animal = 0;
        this.scores.efficiency = 0;
        this.scores.improvement = 0;
        this.documentUploadInputs = [];
        this.uploadedDocumentIDs = [];
    }
    
    createQuestionnaire = (questionnaireData) =>{
        this.commonMethods = new CommonQuestionnaireMethods();
        this.frame.innerHTML = "";
        let card = document.createElement("div");
        card.className = "card";
    
        let sustainabilityHeaderText = document.createElement("h4");
        sustainabilityHeaderText.className = "mt-2";
        sustainabilityHeaderText.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;"
    
        sustainabilityHeaderText.textContent = "Cow-Calf Sustainability Questionnaire";
    
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between";
        cardHeader.style = "padding:5px;padding-left: 15px;"
        
        cardHeader.append(sustainabilityHeaderText);
        card.append(cardHeader)
    
        let cardBody = document.createElement("div");
        cardBody.className = "card-body justify-content-center";
        card.append(cardBody);

        let form = document.createElement("form");
        for(let section of Object.values(sections)) {
            let questionsSection = this.commonMethods.createQuestionsSection(section.header);
            let questions = questionnaireData[section.name];
            for (let question of questions){
                let questionContainer = "";
                if(question.responseType == questionType.select){
                    questionContainer = this.commonMethods.createSelectQuestion(question.questionText, section.name, question.id);
                    questionsSection.append(questionContainer);
                }
                else if(question.responseType == questionType.input){
                    questionContainer = this.commonMethods.createInputQuestion(question.questionText, question.inputType, section.name, question.id);
                    questionsSection.append(questionContainer);
                }
                else if(question.responseType == questionType.upload){
                    const {questionContainer, uploadInput} = this.commonMethods.createUploadQuestion(question.questionText, section.name, question.id);
                    questionsSection.append(questionContainer);
                    this.documentUploadInputs.push(uploadInput);
                }
            }
            form.append(questionsSection)
        }
        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        form.append(submitFormGroup);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Submit";
        submitButton.type = "button";
        submitFormGroup.append(submitButton);
        
        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);

        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/save_sustainability_questionnaire",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    scores: this.scores,
                    uploaded_document_ids: this.uploadedDocumentIDs
                };
            },
        });

        submitButton.addEventListener("click", () => {
            // Getting all response inputs in the form and check if they are answered
            let allQuestionsAnswered = true;
            let allDocumentsUploaded = true;
            for(let section of Object.values(sections)){
                let responses = document.getElementsByName(section.name);
                for(let response of responses){
                    if(response.value == "Please Select" || response.value == ""){
                        allQuestionsAnswered = false;
                        break;
                    }
                }
                if(allQuestionsAnswered == false){break;}
            }
            for(let uploadInput of this.documentUploadInputs){
                if(!(uploadInput.checkForUploadDeclined())){
                    if(!uploadInput.checkForUploadedFile()){
                        allDocumentsUploaded=false;
                        break;
                    }
                }
            }
            
            if(allQuestionsAnswered && allDocumentsUploaded){
                errorMessage.style.display = "none";
                this.uploadDocuments()
                .then(() =>{
                    this.calculateScores(questionnaireData);
                    this.asyncForm.submit();
                });
            }
            else{
                errorMessage.style.display = "block";
                errorMessage.textContent = "Please complete the questionnaire/ Upload all required documents";
            }
        });
        cardBody.append(form);
        this.frame.append(card);
    }

    calculateScores = (questionnaireData) => {
        for(let section of Object.values(sections)){
            let questions = questionnaireData[section.name];
            for (let question of questions){
                let response = document.getElementById(question.id);
                if(question.scoringCriteria == scoringCriteria.confirmation){
                    if(response.value == "Yes"){
                        this.scores[section.name]+=question.score;
                    }
                }
                else if(question.scoringCriteria == scoringCriteria.responsePresent){
                    if(response.value !== ""){
                        this.scores[section.name]+=question.score;
                    }
                }
                else if(question.scoringCriteria == scoringCriteria.roundOff){
                    if(response.value > 0 && response.value <= 100){
                        this.scores[section.name]+=response.value/100;
                    }
                }
            }
        }
    }

    uploadDocuments = () =>{
        return new Promise((resolve, reject) =>{
            for(let uploadInput of this.documentUploadInputs){
                uploadInput.upload()
                .then((id) =>{
                    this.uploadedDocumentIDs.push(id);
                    if(this.uploadedDocumentIDs.length == this.documentUploadInputs.length){
                        resolve(true);
                    }
                });
            }
        });
    }
}