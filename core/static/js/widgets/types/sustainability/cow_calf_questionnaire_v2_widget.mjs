import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import {cowCalfQuestionnaireData } from "../../../core/sustainability_constants.mjs";

export class CowCalfQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }

    //all ids below help to associate the question with the response of the user (in base_questionnaire_v2.mjs)
    initType() {
        this.frame.innerHTML = "";
        this.getData(
            "get_existing_sustainability_responses_and_files"
        ).then((data) => {
            let pendingQuestionnaireID = data.pending_questionnaire_id;
            let pendingQuestionnaireResponses = JSON.parse(data.pending_questionnaire_responses);
            let pendingQuestionnaireUploadedFiles = data.pending_questionnaire_uploaded_files;
            this.createQuestionnaire(cowCalfQuestionnaireData, pendingQuestionnaireID, pendingQuestionnaireResponses, pendingQuestionnaireUploadedFiles);
        });
    }
}