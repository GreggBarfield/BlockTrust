import { Widget } from '../../widget.mjs';
import { CommonQuestionnaireMethods } from './common_questionnaire_methods.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { sections, scoringCriteria, questionType } from '../../../core/sustainability_constants.mjs'
import { ProgressBar } from '../../../core/progress_bar.mjs';

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
        this.totalScore = 0;
        
        this.responses = {};
        this.responses.air = [];
        this.responses.land = [];
        this.responses.water = [];
        this.responses.safety = [];
        this.responses.animal =[];
        this.responses.efficiency = [];
        this.responses.improvement = [];
    }
    
    createQuestionnaire = (questionnaireData) =>{
        this.commonMethods = new CommonQuestionnaireMethods();
        this.frame.innerHTML = "";
        let card = document.createElement("div");
        card.className = "card";
    
        let sustainabilityHeaderText = document.createElement("h4");
        sustainabilityHeaderText.className = "mt-2";
        sustainabilityHeaderText.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;"
    
        sustainabilityHeaderText.textContent = "Sustainability Questionnaire";
    
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
            let questions = questionnaireData[section.name];
            //Below check is needed since not all sections might have questions for a particular questionnaire
            if(questions != null){
                let questionsSection = this.commonMethods.createQuestionsSection(section.header);
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
        }
        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        form.append(submitFormGroup);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Submit";
        submitButton.type = "button";
        submitFormGroup.append(submitButton);

        this.progressBar = new ProgressBar();
        this.progressBar.attach(form);
        this.progressBar.hide();
        
        this.statusMessage = document.createElement("p");
        this.statusMessage.style.display = "none";
        this.statusMessage.className = "mt-2 mb-0";
        form.append(this.statusMessage);

        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/save_sustainability_questionnaire",
            form: form,
            status: this.statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    scores: this.scores,
                    uploaded_document_ids: this.uploadedDocumentIDs,
                    total_score: this.totalScore,
                    responses: this.responses
                };
            },
        });

        submitButton.addEventListener("click", () => {
            // Getting all response inputs in the form and check if they are answered
            let allQuestionsAnswered = true;
            let incompleteSection = "";
            let allDocumentsUploaded = true;
            for(let section of Object.values(sections)){
                let responses = document.getElementsByName(section.name);
                for(let response of responses){
                    if(response.value == "Please Select" || response.value == ""){
                        allQuestionsAnswered = false;
                        incompleteSection = section.header;
                        break;
                    }
                }
                if(allQuestionsAnswered == false){break;}
            }
            for(let uploadInput of this.documentUploadInputs){
                if(!(uploadInput.uploadDeclinedByUser)){
                    if(!uploadInput.isFileAttached()){
                        allDocumentsUploaded=false;
                        break;
                    }
                }
            }
            
            if(allQuestionsAnswered && allDocumentsUploaded){
                errorMessage.style.display = "none";
                this.progressBar.show();
                this.uploadDocuments()
                .then(() =>{
                    this.calculateScores(questionnaireData);
                    this.asyncForm.submit();
                });
            }
            else{
                if(allQuestionsAnswered == false){
                    errorMessage.style.display = "block";
                    errorMessage.textContent = "Please complete the following section: " + incompleteSection;
                }
                else{
                    errorMessage.style.display = "block";
                    errorMessage.textContent = "Please upload all required documents";
                }
            }
        });
        cardBody.append(form);
        this.frame.append(card);
    }

    calculateScores = (questionnaireData) => {
        for(let section of Object.values(sections)){
            let questions = questionnaireData[section.name];
            //Below check is needed since not all sections might have questions for a particular questionnaire
            if(questions != null){
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
                    this.responses[section.name].push(response.value);
                }
            }
            this.totalScore+= this.scores[section.name];
        }
    }

    uploadDocuments = () =>{
        this.statusMessage.style.display = "block";
        this.statusMessage.textContent = "Uploading documents...";
        return new Promise((resolve, reject) =>{     
            this.uploadedDocumentIDs = [];
            let uploadedFiles = 0;
            let numberOfFilesToBeUploaded = 0;
            for(let uploadInput of this.documentUploadInputs){
                if(!uploadInput.uploadDeclinedByUser && uploadInput.isFileAttached()){
                    numberOfFilesToBeUploaded++;
                }
            }
            for(let uploadInput of this.documentUploadInputs){
                uploadInput.upload()
                .then((id) =>{
                    this.uploadedDocumentIDs.push(id);
                    uploadedFiles++;
                    this.progressBar.setProgress(uploadedFiles/numberOfFilesToBeUploaded);
                    //below check is necessary in case any document upload failed
                    if(this.uploadedDocumentIDs.length == this.documentUploadInputs.length){
                        this.statusMessage.style.display = "block";
                        this.statusMessage.textContent = "All documents uploaded";
                        resolve(true);
                    }
                });
            }
        });
    }
}