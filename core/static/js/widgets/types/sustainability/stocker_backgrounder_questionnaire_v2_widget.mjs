import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { stockerBackGrounderQuestionnaireData } from "../../../core/sustainability_constants.mjs";

export class StockerBackgrounderQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.frame.innerHTML = "";
        this.createQuestionnaire(stockerBackGrounderQuestionnaireData);
    }
}