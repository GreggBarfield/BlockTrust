import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { packerQuestionnaireData } from "../../utilities/sustainability_constants.mjs";

export class PackerQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.frame.innerHTML = "";
        this.createQuestionnaire(packerQuestionnaireData);
    }
}