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
        this.questionIDToFileUploaderObjectList = [];
        this.questionIDToUploadedFileIDList = [];
        this.totalScore = 0;
        this.partialResponse = true;
        
        this.responses = {};
        this.responses.air = {};
        this.responses.land = {};
        this.responses.water = {};
        this.responses.safety = {};
        this.responses.animal = {};
        this.responses.efficiency = {};
        this.responses.improvement = {};
        this.progressBar = new ProgressBar();
        this.statusMessage = document.createElement("p");
        this.statusMessage.className = "d-none p-2 mt-2 mb-0";
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
                        const {questionContainer, fileUploaderObject} = this.commonMethods.createUploadQuestion(question.questionText, section.name, question.id);
                        questionsSection.append(questionContainer);
                        this.questionIDToFileUploaderObjectList.push({questionID: question.id, fileUploader: fileUploaderObject});
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

        let saveForLaterButton = document.createElement("button");
        saveForLaterButton.className = "btn btn-secondary";
        saveForLaterButton.textContent = "Save For Later";
        saveForLaterButton.type = "button";
        submitFormGroup.append(saveForLaterButton);

        this.progressBar.attach(form);
        this.progressBar.hide();
        
        form.append(this.statusMessage);

        let errorMessage = document.createElement("p");
        errorMessage.className = "d-none mt-2 mb-0 alert alert-danger";
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
                    uploaded_file_ids: this.questionIDToUploadedFileIDList,
                    total_score: this.totalScore,
                    responses: this.responses,
                    partial_response: this.partialResponse
                };
            }
        });

        submitButton.addEventListener("click",async () => {
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
            for(let questionIDToFileUploaderObject of this.questionIDToFileUploaderObjectList){
                let fileUploader = questionIDToFileUploaderObject.fileUploader;
                if(!(fileUploader.uploadDeclinedByUser)){
                    if(!fileUploader.isFileAttached()){
                        allDocumentsUploaded=false;
                        break;
                    }
                }
            }

            if(allQuestionsAnswered && allDocumentsUploaded){
                errorMessage.className = "d-none";
                await this.uploadDocuments();
                this.calculateScores(questionnaireData);
                this.partialResponse = false;
                this.asyncForm.submit();
            }
            else{
                if(allQuestionsAnswered == false){
                    errorMessage.className = "d-block mt-2 mb-0 alert alert-danger";
                    errorMessage.textContent = "Please complete the following section: " + incompleteSection;
                }
                else{
                    errorMessage.className = "d-block mt-2 mb-0 alert alert-danger";
                    errorMessage.textContent = "Please upload all required documents";
                }
            }
        });

        saveForLaterButton.addEventListener("click",async () => {
            await this.uploadDocuments();
            for(let section of Object.values(sections)){
                let questions = questionnaireData[section.name];
                if(questions != null){
                    for (let question of questions){
                        let response = document.getElementById(question.id);
                        if(response.value != "Please Select" && response.value != ""){
                            this.responses[section.name][question.id]=response.value;
                        }
                    }
                }
            }
            this.asyncForm.submit();
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
                    this.responses[section.name][question.id]=response.value;
                }
            }
            this.totalScore+= this.scores[section.name];
        }
    }

    uploadDocuments = async () =>{
        this.questionIDToUploadedFileIDList = [];
        let uploadedFiles = 0;
        let numberOfFilesToBeUploaded = 0;
        this.progressBar.show();
        this.statusMessage.className= "d-block";
        this.statusMessage.textContent = "Uploading documents...";
        for(let questionIDToFileUploaderObject of this.questionIDToFileUploaderObjectList){
            let fileUploader = questionIDToFileUploaderObject.fileUploader;
            if(!fileUploader.uploadDeclinedByUser && fileUploader.isFileAttached()){
                numberOfFilesToBeUploaded++;
            }
        }
        for(let questionIDToFileUploaderObject of this.questionIDToFileUploaderObjectList){
            let fileUploader = questionIDToFileUploaderObject.fileUploader;
            let id=0;
            if(!fileUploader.uploadDeclinedByUser && fileUploader.isFileAttached()){
                id = await fileUploader.upload();
                uploadedFiles++;
            }
            this.questionIDToUploadedFileIDList.push({question_id: questionIDToFileUploaderObject.questionID, file_id: id});
            this.progressBar.setProgress(uploadedFiles/numberOfFilesToBeUploaded);
            if(this.questionIDToUploadedFileIDList.length == this.questionIDToFileUploaderObjectList.length){
                this.statusMessage.textContent = "All documents uploaded";
            }
        }
    }
}