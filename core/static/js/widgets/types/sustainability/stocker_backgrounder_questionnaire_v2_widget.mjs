import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { sections, scoringCriteria, questionType } from "../../../core/sustainability_constants.mjs";

export class StockerBackgrounderQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        this.frame.innerHTML = "";
        let questionnaireData = {
            [sections.air.name] : [
                {
                    id: "air1",
                    responseType: questionType.select,
                    questionText: "Do you have a Grazing Management Plan (GMP)?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "air2",
                    responseType: questionType.select,
                    questionText: "Is your grazing management plan written?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1   
                },
                {
                    id: "air3",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5   
                },
                {
                    id: "air4",
                    responseType: questionType.select,
                    questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1   
                },
                {
                    id: "air5",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5   
                },
                {
                    id: "air6",
                    responseType: questionType.input,
                    questionText: "How many acres are under your grazing management plan?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5   
                },
                {
                    id: "air7",
                    responseType: questionType.input,
                    questionText: "What percent of your grazing land does this cover?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5  
                }
            ],
            [sections.land.name] : [
                {
                    id: "land1",
                    responseType: questionType.select,
                    questionText: "Do you have a Grazing Management Plan (GMP)?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "land2",
                    responseType: questionType.select,
                    questionText: "Is your grazing management plan written?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1   
                },
                {
                    id: "land3",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5   
                },
                {
                    id: "land4",
                    responseType: questionType.select,
                    questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1   
                },
                {
                    id: "land5",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5   
                },
                {
                    id: "land6",
                    responseType: questionType.input,
                    questionText: "How many acres are under your grazing management plan?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5   
                },
                {
                    id: "land7",
                    responseType: questionType.input,
                    questionText: "What percent of your grazing land does this cover?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5  
                }
            ],
            [sections.water.name] : [
                {
                    id: "water1",
                    responseType: questionType.select,
                    questionText: "Do you have a Grazing Management Plan (GMP)?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water2",
                    responseType: questionType.select,
                    questionText: "Is your grazing management plan written?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1   
                },
                {
                    id: "water3",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share the plan? If so, please upload (PDF only)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5   
                },
                {
                    id: "water4",
                    responseType: questionType.select,
                    questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1   
                },
                {
                    id: "water5",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share data or information related to that active management? If so, please upload (PDF only)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5   
                },
                {
                    id: "water6",
                    responseType: questionType.input,
                    questionText: "How many acres are under your grazing management plan?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5   
                },
                {
                    id: "water7",
                    responseType: questionType.input,
                    questionText: "What percent of your grazing land does this cover?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5  
                }
            ],
            [sections.safety.name] : [
                {
                    id: "safety1",
                    responseType: questionType.select,
                    questionText: "Do you conduct stockmanship and/or safety training?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety2",
                    responseType: questionType.upload,
                    questionText: "If yes, what training? Please upload training (PDF only)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "safety3",
                    responseType: questionType.select,
                    questionText: "Did you conduct employee safety training in the last 12 months?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety4",
                    responseType: questionType.select,
                    questionText: "Are 100% of your employees stockmanship & safety training annually?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety5",
                    responseType: questionType.input,
                    questionText: "What percentage of your employees have undergone stockmanship &/or safety training?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.roundOff
                }
            ],
            [sections.animal.name] : [
                {
                    id: "animal1",
                    responseType: questionType.select,
                    questionText: "Does you operation participate in BQA or equivalent programs?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "animal2",
                    responseType: questionType.select,
                    questionText: "Is your operation BQA Certified or an equivalent program? Or are you certified?",
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
                    questionText: "Have you conducted a BQA audit?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "animal5",
                    responseType: questionType.input,
                    questionText: "If yes, what was your score? Please enter",
                    inputType: "text",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 1
                },
                {
                    id: "animal6",
                    responseType: questionType.input,
                    questionText: "What percentage of your employees are BQA Certified?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.roundOff
                }
            ],
            [sections.efficiency.name] : [
                {
                    id: "efficiency1",
                    responseType: questionType.select,
                    questionText: "Do you measure weaning weight either by individual cow or by unit of land? Neither?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "efficiency2",
                    responseType: questionType.select,
                    questionText: "Do you track calf weaning percentage per cow exposed?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "efficiency3",
                    responseType: questionType.input,
                    questionText: "What is your calf weaning percentage per cow exposed?",
                    inputType: "number",
                    scoringCriteria: scoringCriteria.roundOff
                },
                {
                    id: "efficiency4",
                    responseType: questionType.select,
                    questionText: "Are you/will you making culling decisions based on calf weaning weight or cow reproductive success?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "efficiency5",
                    responseType: questionType.select,
                    questionText: "When determing mating decisions are you selecting bulls in considerations of your own cowherds strengths and weaknesses?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "efficiency6",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share your breeding plan? If so, please upload (PDF only)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
            ],
            [sections.improvement.name] : [
                {
                    id: "improvement1",
                    responseType: questionType.select,
                    questionText: "Have you or are you planning to examine the environmental impact of your operation? (Water footprint)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "improvement2",
                    responseType: questionType.input,
                    questionText: "If already completed, what was your footprint?",
                    inputType: "text",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5
                },
                {
                    id: "improvement3",
                    responseType: questionType.select,
                    questionText: "Have you or are you planning to examine the environmental impact of your operation? (Greenhouse Gas footprint)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "improvement4",
                    responseType: questionType.input,
                    questionText: "If already completed, what was your footprint?",
                    inputType: "text",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5
                },
                {
                    id: "improvement5",
                    responseType: questionType.select,
                    questionText: "Is your operation actively participating in ecosystem service markets or convservation programs?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement6",
                    responseType: questionType.select,
                    questionText: "Do you have a herd health plan developed through a Veterinary-Client Patient Relationship (VCPR)?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement7",
                    responseType: questionType.select,
                    questionText: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "improvement8",
                    responseType: questionType.select,
                    questionText: "Do you utilize RFID or alternative traceability technology?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                }
            ]
        }
        this.createQuestionnaire(questionnaireData);
    }
}