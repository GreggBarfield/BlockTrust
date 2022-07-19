import { Widget } from '../../widget.mjs';
import { CommonQuestionnaireMethods } from './common_questionnaire_methods.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

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

    this.responses = {};
    this.responses.air = [];
    this.responses.land = [];
    this.responses.water = [];
    this.responses.safety = [];
    this.responses.animal = [];
    this.responses.efficiency = [];
    this.responses.improvement = [];
    }
    
    createQuestionnaire = (questionnaireData, sections) =>{
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
        for(let sectionData in questionnaireData){
            let section = this.commonMethods.createQuestionsSection(sections[sectionData]);
            // Getting the questions array based on section
            let questions = questionnaireData[sectionData];
            // Generating question based on question type
            for (let question of questions){
                let questionContainer = "";
                if(question.responseType == "select"){
                    questionContainer = this.commonMethods.createSelectQuestion(question.questionText, sectionData, question.id);
                }
                else if(question.responseType == "input"){
                    questionContainer = this.commonMethods.createInputQuestion(question.questionText, question.inputType, sectionData, question.id);
                }
                else if(question.responseType == "upload"){
                    questionContainer = this.commonMethods.createUploadQuestion(question.questionText, sectionData, question.id);
                }
                section.append(questionContainer);
            }
            form.append(section)
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

        this.internalErrorMessage = document.createElement("p");
        this.internalErrorMessage.style.display = "none";
        this.internalErrorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(this.internalErrorMessage);

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
                    responses: this.responses
                };
            },
        });

        submitButton.addEventListener("click", () => {
            // Getting all response inputs in the form and check if they are answered
            let allQuestionsAnswered = true;
            for(let section in sections){
                let responses = document.getElementsByName(section);
                for(let response of responses){
                    if(response.value == "Please Select" || response.value == ""){
                        allQuestionsAnswered = false;
                    }
                }
            }
            if(allQuestionsAnswered){
                errorMessage.style.display = "none";
                this.calculateScores(sections, questionnaireData);
                this.asyncForm.submit();
            }
            else{
                errorMessage.style.display = "block";
                errorMessage.textContent = "Please complete the questionnaire";
            }
        });
        cardBody.append(form);
        this.frame.append(card);
    }

    calculateScores = (sections, questionnaireData) => {
        for(let section in sections){
            let responses = document.getElementsByName(section);
            let questions = questionnaireData[section];
            for(let response of responses){
                for(let question of questions){
                    // Matching input to questions based on ID
                    if(question.id == response.id){
                        // Generating score based on scoring criteria
                        if(question.scoringCriteria == "confirmation"){
                            if(response.value == "Yes"){
                                this.scores[section]+=question.score;
                            }
                        }
                        else if(question.scoringCriteria == "responsePresent"){
                            if(response.value !== ""){
                                this.scores[section]+=question.score;
                            }
                        }
                        else if(question.scoringCriteria == "roundOff"){
                            if(response.value > 0 && response.value <= 100){
                                this.scores[section]+=response.value/100;
                            }
                        }
                        // Storing the response for each question based on section
                        this.responses[section].push(response.value);
                    }
                }
            }
        }
    }
}