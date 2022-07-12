import { Widget } from '../../../widget.mjs';
import { CommonQuestionnaireMethods } from './common_questionnaire_methods.mjs';
import { AsyncForm } from '../../../../../global/async_form.mjs';

export class RevisedCowCalfQuestionnaireWidget extends Widget{
    constructor(frame) {
    super(frame);
    }
    
    initType = () => {
        this.commonMethods = new CommonQuestionnaireMethods();
        this.createQuestionnaire();
    }
    
    createQuestionnaire = () =>{
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

        // Air and GHG section questions
        let airAndGHGSection = this.commonMethods.createQuestionsSection("Air and GHG");
        this.commonMethods.createSelectQuestion(airAndGHGSection, "Do you have a Grazing Management Plan (GMP)?", "airAndGHG");
        this.commonMethods.createSelectQuestion(airAndGHGSection, "Is your grazing management plan written?", "airAndGHG");
        this.commonMethods.createUploadQuestion(airAndGHGSection, "Are you willing to share the plan? If so, please upload", "airAndGHG");
        this.commonMethods.createSelectQuestion(airAndGHGSection, "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?", "airAndGHG");
        this.commonMethods.createSelectQuestion(airAndGHGSection, "Are you willing to share data or information related to that active management? If so, please upload", "airAndGHG")
        this.commonMethods.createInputQuestion(airAndGHGSection, "How many acres are under your grazing management plan?", "number", "airAndGHG");
        this.commonMethods.createInputQuestion(airAndGHGSection, "What percent of your grazing land does this cover?", "number", "airAndGHG");

        // Land section questions
        let landSection = this.commonMethods.createQuestionsSection("Land");
        this.commonMethods.createSelectQuestion(landSection, "Do you have a Grazing Management Plan (GMP)?", "land");
        this.commonMethods.createSelectQuestion(landSection, "Is your grazing management plan written?", "land");
        this.commonMethods.createUploadQuestion(landSection, "Are you willing to share the plan? If so, please upload", "land");
        this.commonMethods.createSelectQuestion(landSection, "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?", "land");
        this.commonMethods.createSelectQuestion(landSection, "Are you willing to share data or information related to that active management? If so, please upload", "land")
        this.commonMethods.createInputQuestion(landSection, "How many acres are under your grazing management plan?", "number", "land");
        this.commonMethods.createInputQuestion(landSection, "What percent of your grazing land does this cover?", "number", "land");

        // Water section questions
        let waterSection = this.commonMethods.createQuestionsSection("Water");
        this.commonMethods.createSelectQuestion(waterSection, "Do you have a Grazing Management Plan (GMP)?", "water");
        this.commonMethods.createSelectQuestion(waterSection, "Is your grazing management plan written?", "water");
        this.commonMethods.createUploadQuestion(waterSection, "Are you willing to share the plan? If so, please upload", "water");
        this.commonMethods.createSelectQuestion(waterSection, "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?", "water");
        this.commonMethods.createSelectQuestion(waterSection, "Are you willing to share data or information related to that active management? If so, please upload", "water")
        this.commonMethods.createInputQuestion(waterSection, "How many acres are under your grazing management plan?", "number", "water");
        this.commonMethods.createInputQuestion(waterSection, "What percent of your grazing land does this cover?", "number", "water");

        // Employee Safety and Well Being questions 
        let employeeSafetyAndWellBeingSection = this.commonMethods.createQuestionsSection("Employee Safety and Well Being");
        this.commonMethods.createSelectQuestion(employeeSafetyAndWellBeingSection, "Do you conduct stockmanship and/or safety training?", "employeeSafetyAndWellBeing");
        this.commonMethods.createUploadQuestion(employeeSafetyAndWellBeingSection, "If yes, what training? Please upload training", "employeeSafetyAndWellBeing");
        this.commonMethods.createSelectQuestion(employeeSafetyAndWellBeingSection, "Did you conduct employee safety training in the last 12 months?", "employeeSafetyAndWellBeing");
        this.commonMethods.createSelectQuestion(employeeSafetyAndWellBeingSection, "Are 100% of your employees stockmanship & safety training annually?", "employeeSafetyAndWellBeing");
        this.commonMethods.createInputQuestion(employeeSafetyAndWellBeingSection, "What percentage of your employees have undergone stockmanship &/or safety training?", "number", "employeeSafetyAndWellBeing");

        // Animal Health and Well Being questions
        let animalHealthAndWellBeingSection = this.commonMethods.createQuestionsSection("Animal Health and Well Being");
        this.commonMethods.createSelectQuestion(animalHealthAndWellBeingSection, "Does you operation participate in BQA or equivalent programs?", "animalHealthAndWellBeing");
        this.commonMethods.createSelectQuestion(animalHealthAndWellBeingSection, "Is your operation BQA Certified or an equivalent program? Or are you certified?", "animalHealthAndWellBeing")
        this.commonMethods.createInputQuestion(animalHealthAndWellBeingSection, "If yes, what is your BQA certification number? Please upload", "text", "animalHealthAndWellBeing")
        this.commonMethods.createSelectQuestion(animalHealthAndWellBeingSection, "Have you conducted a BQA audit?", "animalHealthAndWellBeing")
        this.commonMethods.createInputQuestion(animalHealthAndWellBeingSection, "If yes, what was your score? Please upload", "text", "animalHealthAndWellBeing");
        this.commonMethods.createInputQuestion(animalHealthAndWellBeingSection, "What percentage of your employees are BQA Certified?", "number", "animalHealthAndWellBeing");

        // Efficiency and Yield questions
        let efficiencyAndYieldSection = this.commonMethods.createQuestionsSection("Efficiency and Yield");
        this.commonMethods.createSelectQuestion(efficiencyAndYieldSection, "Do you measure weaning weight either by individual cow or by unit of land? Neither?", "efficiencyAndYield");
        this.commonMethods.createSelectQuestion(efficiencyAndYieldSection, "Do you track calf weaning percentage per cow exposed?", "efficiencyAndYield");
        this.commonMethods.createInputQuestion(efficiencyAndYieldSection, "What is your calf weaning percentage per cow exposed?", "number", "efficiencyAndYield");
        this.commonMethods.createSelectQuestion(efficiencyAndYieldSection, "Are you/will you making culling decisions based on calf weaning weight or cow reproductive success?", "efficiencyAndYield");
        this.commonMethods.createSelectQuestion(efficiencyAndYieldSection, "When determing mating decisions are you selecting bulls in considerations of your own cowherds strengths and weaknesses?", "efficiencyAndYield");
        this.commonMethods.createUploadQuestion(efficiencyAndYieldSection, "Are you willing to share your breeding plan? If so, please upload", "efficiencyAndYield");

        // Improvement questions
        let improvementSection = this.commonMethods.createQuestionsSection("Improvement");
        this.commonMethods.createSelectQuestion(improvementSection, "Have you or are you planning to examine the environmental impact of your operation? (Water footprint)", "improvement");
        this.commonMethods.createInputQuestion(improvementSection, "If already completed, what was your footprint?", "number", "improvement");
        this.commonMethods.createSelectQuestion(improvementSection, "Have you or are you planning to examine the environmental impact of your operation? (Greenhouse Gas footprint)", "improvement");
        this.commonMethods.createInputQuestion(improvementSection, "If already completed, what was your footprint?", "number", "improvement");
        this.commonMethods.createSelectQuestion(improvementSection, "Is your operation actively participating in ecosystem service markets or convservation programs?", "improvement");
        this.commonMethods.createSelectQuestion(improvementSection, "Do you have a herd health plan developed through a Veterinary-Client Patient Relationship (VCPR)?", "improvement");
        this.commonMethods.createSelectQuestion(improvementSection, "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?", "improvement");
        this.commonMethods.createSelectQuestion(improvementSection, "Do you utilize RFID or alternative traceability technology?", "improvement");
        
        
        form.append(airAndGHGSection);
        form.append(landSection);
        form.append(waterSection);
        form.append(employeeSafetyAndWellBeingSection);
        form.append(animalHealthAndWellBeingSection);
        form.append(efficiencyAndYieldSection);
        form.append(improvementSection);
        
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
            action: "/widgets/data/save_new_cow_calf_sustainability",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    air_and_ghg_score: this.airAndGHGScore,
                    land_score: this.landScore,
                    water_score: this.waterScore,
                    employee_safety_and_well_being_score: this.employeeSafetyAndWellBeingScore,
                    animal_health_and_well_being_score: this.animalHealthAndWellBeingScore,
                    efficiency_and_yield_score: this.efficiencyAndYieldScore,
                    improvement_score: this.improvementScore,
                    all_responses: this.allResponses
                };
            },
        });

        submitButton.addEventListener("click", () => {
            let sustainabilityResponses = document.getElementsByClassName("form-control");
            let allQuestionsAnswered = true;
            for(let sustainabilityResponse of sustainabilityResponses){
                if(sustainabilityResponse.value == "Please Select" || sustainabilityResponse.value == ""){
                    allQuestionsAnswered = false;
                }
            }
            if(allQuestionsAnswered){
                this.internalErrorMessage.style.display = "none";
                this.calculateScores();
                this.asyncForm.submit();
            }
            else{
                this.internalErrorMessage.style.display = "block";
                this.internalErrorMessage.textContent = "Please complete the questionnaire";
            }
        });

        cardBody.append(form);
        this.frame.append(card);
    }  
    
    calculateScores = () => {
        this.allResponses = {
            "air_and_ghg": [],
            "land": [],
            "water": [],
            "employee_safety_and_well_being": [],
            "animal_health_and_well_being": [],
            "efficiency_and_yield": [],
            "improvement": []
        };
        this.airAndGHGScore = 0;
        this.landScore = 0;
        this.waterScore = 0;
        this.employeeSafetyAndWellBeingScore = 0;
        this.animalHealthAndWellBeingScore = 0;
        this.efficiencyAndYieldScore = 0;
        this.improvementScore = 0;

        // Calculating scores for Air and GHG section
        let airAndGHGResponses = document.getElementsByName("airAndGHG");
        if(airAndGHGResponses[0].value == "Yes"){this.airAndGHGScore+=1;}
        if(airAndGHGResponses[1].value == "Yes"){this.airAndGHGScore+=1;}
        if(airAndGHGResponses[2].value == "Yes"){this.airAndGHGScore+=0.5;}
        if(airAndGHGResponses[3].value == "Yes"){this.airAndGHGScore+=1;}
        if(airAndGHGResponses[4].value == "Yes"){this.airAndGHGScore+=0.5;}
        if(airAndGHGResponses[5].value != ""){this.airAndGHGScore+=0.5;}
        if(airAndGHGResponses[6].value != ""){this.airAndGHGScore+=0.5;}
        // Storing the responses provided by the user
        for(let airAndGHGResponse of airAndGHGResponses){
            this.allResponses["air_and_ghg"].push(airAndGHGResponse.value);
        }

        // Calculating scores for Land section
        let landResponses = document.getElementsByName("land");
        if(landResponses[0].value == "Yes"){this.landScore+=1;}
        if(landResponses[1].value == "Yes"){this.landScore+=1;}
        if(landResponses[2].value == "Yes"){this.landScore+=0.5;}
        if(landResponses[3].value == "Yes"){this.landScore+=1;}
        if(landResponses[4].value == "Yes"){this.landScore+=0.5;}
        if(landResponses[5].value != ""){this.landScore+=0.5;}
        if(landResponses[6].value != ""){this.landScore+=0.5;}
        // Storing the responses provided by the user
        for(let landResponse of landResponses){
            this.allResponses["land"].push(landResponse.value);
        }

        // Calculating scores for Water section
        let waterResponses = document.getElementsByName("water");
        if(waterResponses[0].value == "Yes"){this.waterScore+=1;}
        if(waterResponses[1].value == "Yes"){this.waterScore+=1;}
        if(waterResponses[2].value == "Yes"){this.waterScore+=0.5;}
        if(waterResponses[3].value == "Yes"){this.waterScore+=1;}
        if(waterResponses[4].value == "Yes"){this.waterScore+=0.5;}
        if(waterResponses[5].value != ""){this.waterScore+=0.5;}
        if(waterResponses[6].value != ""){this.waterScore+=0.5;}
        // Storing the responses provided by the user
        for(let waterResponse of waterResponses){
            this.allResponses["water"].push(waterResponse.value);
        }

        // Calculating scores for Employee Safety and Well Being section
        let employeeSafetyAndWellBeingResponses = document.getElementsByName("employeeSafetyAndWellBeing");
        if(employeeSafetyAndWellBeingResponses[0].value == "Yes"){this.employeeSafetyAndWellBeingScore+=1;}
        if(employeeSafetyAndWellBeingResponses[1].value == "Yes"){this.employeeSafetyAndWellBeingScore+=0.5;}
        if(employeeSafetyAndWellBeingResponses[2].value == "Yes"){this.employeeSafetyAndWellBeingScore+=1;}
        if(employeeSafetyAndWellBeingResponses[3].value == "Yes"){this.employeeSafetyAndWellBeingScore+=1;}
        if(employeeSafetyAndWellBeingResponses[4].value > 0 && employeeSafetyAndWellBeingResponses[4].value < 100){
            this.employeeSafetyAndWellBeingScore+=employeeSafetyAndWellBeingResponses[4].value/100;
        }
        // Storing the responses provided by the user
        for(let employeeSafetyAndWellBeingResponse of employeeSafetyAndWellBeingResponses){
            this.allResponses["employee_safety_and_well_being"].push(employeeSafetyAndWellBeingResponse.value);
        }

        // Calculating scores for Animal Health and Well Being section
        let animalHealthAndWellBeingResponses = document.getElementsByName("animalHealthAndWellBeing");
        if(animalHealthAndWellBeingResponses[0].value == "Yes"){this.animalHealthAndWellBeingScore+=1;}
        if(animalHealthAndWellBeingResponses[1].value == "Yes"){this.animalHealthAndWellBeingScore+=1;}
        if(animalHealthAndWellBeingResponses[2].value != ""){this.animalHealthAndWellBeingScore+=0.5;}
        if(animalHealthAndWellBeingResponses[3].value == "Yes"){this.animalHealthAndWellBeingScore+=1;}
        if(animalHealthAndWellBeingResponses[4].value != ""){this.animalHealthAndWellBeingScore+=0.5;}
        if(animalHealthAndWellBeingResponses[5].value > 0 && animalHealthAndWellBeingResponses[5].value < 100){
            this.animalHealthAndWellBeingScore+=animalHealthAndWellBeingResponses[5].value/100;
        }
        // Storing the responses provided by the user
        for(let animalHealthAndWellBeingResponse of animalHealthAndWellBeingResponses){
            this.allResponses["animal_health_and_well_being"].push(animalHealthAndWellBeingResponse.value);
        }

        // Calculating scores for Efficiency and Yield section
        let efficiencyAndYieldResponses = document.getElementsByName("efficiencyAndYield");
        if(efficiencyAndYieldResponses[0].value == "Yes"){this.efficiencyAndYieldScore+=1;}
        if(efficiencyAndYieldResponses[1].value == "Yes"){this.efficiencyAndYieldScore+=1;}
        if(efficiencyAndYieldResponses[2].value > 0 && efficiencyAndYieldResponses[2].value < 100){
            this.efficiencyAndYieldScore+=efficiencyAndYieldResponses[2].value/100;
        }
        if(efficiencyAndYieldResponses[3].value == "Yes"){this.efficiencyAndYieldScore+=1;}
        if(efficiencyAndYieldResponses[4].value == "Yes"){this.efficiencyAndYieldScore+=1;}
        if(efficiencyAndYieldResponses[5].value == "Yes"){this.efficiencyAndYieldScore+=0.5;}
        // Storing the responses provided by the user
        for(let efficiencyAndYieldResponse of efficiencyAndYieldResponses){
            this.allResponses["efficiency_and_yield"].push(efficiencyAndYieldResponse.value);
        }

        // Calculating scores for Improvement section
        let improvementResponses = document.getElementsByName('improvement');
        if(improvementResponses[0].value == "Yes"){this.improvementScore+=1;}
        if(improvementResponses[1].value != ""){this.improvementScore+=0.5;}
        if(improvementResponses[2].value == "Yes"){this.improvementScore+=1;}
        if(improvementResponses[3].value != ""){this.improvementScore+=0.5;}
        if(improvementResponses[4].value == "Yes"){this.improvementScore+=0.5;}
        if(improvementResponses[5].value == "Yes"){this.improvementScore+=0.5;}
        if(improvementResponses[6].value == "Yes"){this.improvementScore+=0.5;}
        if(improvementResponses[7].value == "Yes"){this.improvementScore+=0.5;}
        // Storing the responses provided by the user
        for(let improvementResponse of improvementResponses){
            this.allResponses["improvement"].push(improvementResponse.value);
        }
    }

}