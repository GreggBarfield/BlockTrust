import { Widget } from '../../../widget.mjs';
import { CommonQuestionnaireMethods } from './common_questionnaire_methods.mjs';

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


        let airGFGLandWaterSection = this.commonMethods.createQuestionsSection("Air, GHG, Land and Water");
        let firstQuestion = this.commonMethods.createSelectQuestion("Do you have a Grazing Management Plan (GMP)?", [{text: "Yes", score: 1}, {text: "No", score:0}]);
        let secondQuestion = this.commonMethods.createSelectQuestion("Is your grazing management plan written?", [{text: "Yes", score: 1}, {text: "No", score:0}]);
        let thirdQuestion = this.commonMethods.createSelectQuestion("Are you willing to share the plan? If so, please upload", [{text: "Yes", score: 0.5}, {text: "No", score:0}]);
        let fourthQuestion = this.commonMethods.createSelectQuestion("Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?", [{text: "Yes", score: 1}, {text: "No", score:0}]);
        let fifthQuestion = this.commonMethods.createSelectQuestion("Are you willing to share data or information related to that active management? If so, please upload", [{text: "Yes", score: 0.5}, {text: "No", score:0}])
        let sixthQuestion = this.commonMethods.createInputQuestion("How many acres are under your grazing management plan?");
        let seventhQuestion = this.commonMethods.createInputQuestion("What percent of your grazing land does this cover?");
        secondQuestion.onchange = () => {
            if(secondQuestion.value == 0){
                //thirdQuestion.style.display = "none"
                $(thirdQuestion).hide();
            }
            else{
                //thirdQuestion.style.display = "block"
                $(thirdQuestion).show();
            }
        }
        fourthQuestion.onchange = () => {
            if(fourthQuestion.value == 0){
            }
        }
        airGFGLandWaterSection.append(firstQuestion);
        airGFGLandWaterSection.append(secondQuestion);
        airGFGLandWaterSection.append(thirdQuestion);
        airGFGLandWaterSection.append(fourthQuestion);
        airGFGLandWaterSection.append(fifthQuestion);
        airGFGLandWaterSection.append(sixthQuestion);
        airGFGLandWaterSection.append(seventhQuestion);

        let employeeSafetyAndWellBeingSection = this.commonMethods.createQuestionsSection("Employee Safety and Well Being");
        let firstQuestionB = this.commonMethods.createSelectQuestion("Do you conduct stockmanship and/or safety training?", [{text: "Yes", score: 1}, {text: "No", score:0}]);
        let secondQuestionB = this.commonMethods.createInputQuestion("If yes, what training? Please upload training")
        employeeSafetyAndWellBeingSection.append(firstQuestionB);
        employeeSafetyAndWellBeingSection.append(secondQuestionB);
        
        cardBody.append(airGFGLandWaterSection);
        cardBody.append(employeeSafetyAndWellBeingSection);

        this.frame.append(card);
    }
        
}