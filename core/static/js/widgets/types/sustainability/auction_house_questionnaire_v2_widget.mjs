import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { auctionHouseQuestionnaireData } from "../../../core/sustainability_constants.mjs";

export class AuctionHouseQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.frame.innerHTML = "";
        this.createQuestionnaire(auctionHouseQuestionnaireData);
    }
}