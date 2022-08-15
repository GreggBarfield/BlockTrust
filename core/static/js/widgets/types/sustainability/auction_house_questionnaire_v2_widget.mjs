import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { sections, scoringCriteria, questionType } from "../../../core/sustainability_constants.mjs";

export class AuctionHouseQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.frame.innerHTML = "";
        let questionnaireData = {
            [sections.water.name] : [
                {
                    id: "water1",
                    responseType: questionType.select,
                    questionText: "If required, does your facility have a waste water permit and is it in compliance with the permit?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water2",
                    responseType: questionType.upload,
                    questionText: "If yes, are you willing to share it?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water3",
                    responseType: questionType.select,
                    questionText: "Is your facility designed to capture pen runoff and with manure storage areas?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water4",
                    responseType: questionType.select,
                    questionText: "Does your facility have a written water or nutrient management plan?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water5",
                    responseType: questionType.upload,
                    questionText: "If yes, are you willing to share it?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water6",
                    responseType: questionType.select,
                    questionText: "Are employees with environmental responsibilities regularly trained?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
            ],
            [sections.safety.name] : [
                {
                    id: "safety1",
                    responseType: questionType.select,
                    questionText: "Do you have an employee safety program in place?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety2",
                    responseType: questionType.select,
                    questionText: "If yes, do is your safety program written?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety3",
                    responseType: questionType.upload,
                    questionText: "If yes, are you willing to share? Please upload training",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety4",
                    responseType: questionType.input,
                    questionText: "What percentage of your employees have undergone stockmanship &/or safety training?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.roundOff
                },
                {
                    id: "safety5",
                    responseType: questionType.select,
                    questionText: "Are 100% of your employees stockmanship & safety training upon hiring and at least annually?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                }
            ],
            [sections.animal.name] : [
                {
                    id: "animal1",
                    responseType: questionType.select,
                    questionText: "Does you operation participate in BQA, Livestock marketing association training or equivalent programs?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "animal2",
                    responseType: questionType.select,
                    questionText: "Is your operation BQA Certified, Livestock marketing association or an equivalent program? Or are you certified?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "animal3",
                    responseType: questionType.input,
                    questionText: "If yes, what is your BQA certification number? Please upload",
                    inputType: "text",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5
                },
                {
                    id: "animal4",
                    responseType: questionType.select,
                    questionText: "Have you conducted a BQA, Livestock marketing association or equivalent audit?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "animal5",
                    responseType: questionType.input,
                    questionText: "If yes, what was your score? Please enter",
                    inputType: "text",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5
                },
                {
                    id: "animal6",
                    responseType: questionType.input,
                    questionText: "What percentage of your animal hanlding employees are BQA or Livestock marketing association trained?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.roundOff
                }
            ],
            [sections.improvement.name] : [ 
                {
                    id: "improvement1",
                    responseType: questionType.select,
                    questionText: "Have you or are you planning to examine the environmental impact of your operation? (Water or Greenhouse gas footprint)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement2",
                    responseType: questionType.input,
                    questionText: "If yes, what type of assessment have you or are you going to conduct?(Water or Greenhouse)",
                    inputType: "text",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5
                },
                {
                    id: "improvement3",
                    responseType: questionType.input,
                    questionText: "If already completed, what was your footprint?",
                    inputType: "text",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5
                },
                {
                    id: "improvement4",
                    responseType: questionType.select,
                    questionText: "Do you have a health plan developed through a Veterinary-Client Patient Relationship (VCPR)?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement5",
                    responseType: questionType.select,
                    questionText: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement6",
                    responseType: questionType.select,
                    questionText: "Do you utilize, or facilitate the use of, RFID or alternative traceability technology?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement7",
                    responseType: questionType.select,
                    questionText: "Are all the proper facilities recommendations implemented at the auction to reduce animal stress and injury?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement8",
                    responseType: questionType.select,
                    questionText: "Does the auction emphasize the BQA transportation guidelines to its customers?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement9",
                    responseType: questionType.select,
                    questionText: "Have you or are you planning to install green infrastructure?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement10",
                    responseType: questionType.select,
                    questionText: "Have you are or you planning to develop on-site habitat restoration?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                }
            ]
        }
        this.createQuestionnaire(questionnaireData);
    }
}