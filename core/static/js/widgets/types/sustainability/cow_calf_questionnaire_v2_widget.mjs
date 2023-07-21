import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { cowCalfQuestionnaireData } from "../../utilities/sustainability_constants.mjs";


export class CowCalfQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }

    //all ids below help to associate the question with the response of the user (in base_questionnaire_v2.mjs)
    initType() {
        this.frame.innerHTML = "";
        this.createQuestionnaire(cowCalfQuestionnaireData);
    }
}