import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { packerQuestionnaireData } from "../../../core/sustainability_constants.mjs";

export class PackerQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.frame.innerHTML = "";
        this.getData(
            "get_existing_sustainability_responses_and_files"
        ).then((data) => {
            let pendingQuestionnaireID = data.pending_questionnaire_id;
            let pendingQuestionnaireResponses = JSON.parse(data.pending_questionnaire_responses);
            let pendingQuestionnaireUploadedFiles = data.pending_questionnaire_uploaded_files;
            this.createQuestionnaire(packerQuestionnaireData, pendingQuestionnaireID, pendingQuestionnaireResponses, pendingQuestionnaireUploadedFiles);
        });
    }
}