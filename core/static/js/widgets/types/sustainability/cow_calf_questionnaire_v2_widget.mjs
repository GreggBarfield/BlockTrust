import { AbstractBaseQuestionnaireV2Widget } from "./abstract_base_questionnaire_v2.mjs";
import { getSustainabilitySections } from "../../../core/sustainability_sections.mjs";

export class CowCalfQuestionnaireV2Widget extends AbstractBaseQuestionnaireV2Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";
        let sectionalFormData = {
            "air": [
                {
                    id: "air1",
                    responseType: "select",
                    questionText: "Do you have a Grazing Management Plan (GMP)?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "air2",
                    responseType: "select",
                    questionText: "Is your grazing management plan written?",
                    scoringCriteria: "confirmation",
                    score: 1   
                },
                {
                    id: "air3",
                    responseType: "upload",
                    questionText: "Are you willing to share the plan? If so, please upload",
                    scoringCriteria: "confirmation",
                    score: 0.5   
                },
                {
                    id: "air4",
                    responseType: "select",
                    questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
                    scoringCriteria: "confirmation",
                    score: 1   
                },
                {
                    id: "air5",
                    responseType: "upload",
                    questionText: "Are you willing to share data or information related to that active management? If so, please upload",
                    scoringCriteria: "confirmation",
                    score: 0.5   
                },
                {
                    id: "air6",
                    responseType: "input",
                    questionText: "How many acres are under your grazing management plan?",
                    inputType: "number",
                    scoringCriteria: "responsePresent",
                    score: 0.5   
                },
                {
                    id: "air7",
                    responseType: "input",
                    questionText: "What percent of your grazing land does this cover?",
                    inputType: "number",
                    scoringCriteria: "responsePresent",
                    score: 0.5  
                }
            ],
            "land": [
                {
                    id: "land1",
                    responseType: "select",
                    questionText: "Do you have a Grazing Management Plan (GMP)?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "land2",
                    responseType: "select",
                    questionText: "Is your grazing management plan written?",
                    scoringCriteria: "confirmation",
                    score: 1   
                },
                {
                    id: "land3",
                    responseType: "upload",
                    questionText: "Are you willing to share the plan? If so, please upload",
                    scoringCriteria: "confirmation",
                    score: 0.5   
                },
                {
                    id: "land4",
                    responseType: "select",
                    questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
                    scoringCriteria: "confirmation",
                    score: 1   
                },
                {
                    id: "land5",
                    responseType: "upload",
                    questionText: "Are you willing to share data or information related to that active management? If so, please upload",
                    scoringCriteria: "confirmation",
                    score: 0.5   
                },
                {
                    id: "land6",
                    responseType: "input",
                    questionText: "How many acres are under your grazing management plan?",
                    inputType: "number",
                    scoringCriteria: "responsePresent",
                    score: 0.5   
                },
                {
                    id: "land7",
                    responseType: "input",
                    questionText: "What percent of your grazing land does this cover?",
                    inputType: "number",
                    scoringCriteria: "responsePresent",
                    score: 0.5  
                }
            ],
            "water": [
                {
                    id: "water1",
                    responseType: "select",
                    questionText: "Do you have a Grazing Management Plan (GMP)?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "water2",
                    responseType: "select",
                    questionText: "Is your grazing management plan written?",
                    scoringCriteria: "confirmation",
                    score: 1   
                },
                {
                    id: "water3",
                    responseType: "upload",
                    questionText: "Are you willing to share the plan? If so, please upload",
                    scoringCriteria: "confirmation",
                    score: 0.5   
                },
                {
                    id: "water4",
                    responseType: "select",
                    questionText: "Are you actively monitoring and adapting your GMP to ensure continuous progress towards management goals?",
                    scoringCriteria: "confirmation",
                    score: 1   
                },
                {
                    id: "water5",
                    responseType: "upload",
                    questionText: "Are you willing to share data or information related to that active management? If so, please upload",
                    scoringCriteria: "confirmation",
                    score: 0.5   
                },
                {
                    id: "water6",
                    responseType: "input",
                    questionText: "How many acres are under your grazing management plan?",
                    inputType: "number",
                    scoringCriteria: "responsePresent",
                    score: 0.5   
                },
                {
                    id: "water7",
                    responseType: "input",
                    questionText: "What percent of your grazing land does this cover?",
                    inputType: "number",
                    scoringCriteria: "responsePresent",
                    score: 0.5  
                }
            ],
            "safety": [
                {
                    id: "safety1",
                    responseType: "select",
                    questionText: "Do you conduct stockmanship and/or safety training?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "safety2",
                    responseType: "upload",
                    questionText: "If yes, what training? Please upload training",
                    scoringCriteria: "confirmation",
                    score: 0.5
                },
                {
                    id: "safety3",
                    responseType: "select",
                    questionText: "Did you conduct employee safety training in the last 12 months?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "safety4",
                    responseType: "select",
                    questionText: "Are 100% of your employees stockmanship & safety training annually?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "safety5",
                    responseType: "input",
                    questionText: "What percentage of your employees have undergone stockmanship &/or safety training?",
                    inputType: "number",
                    scoringCriteria: "roundOff"
                }
            ],
            "animal": [
                {
                    id: "animal1",
                    responseType: "select",
                    questionText: "Does you operation participate in BQA or equivalent programs?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "animal2",
                    responseType: "select",
                    questionText: "Is your operation BQA Certified or an equivalent program? Or are you certified?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "animal3",
                    responseType: "input",
                    questionText: "If yes, what is your BQA certification number? Please upload",
                    inputType: "text",
                    scoringCriteria: "responsePresent",
                    score: 0.5
                },
                {
                    id: "animal4",
                    responseType: "select",
                    questionText: "Have you conducted a BQA audit?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "animal5",
                    responseType: "input",
                    questionText: "If yes, what was your score? Please enter",
                    inputType: "text",
                    scoringCriteria: "responsePresent",
                    score: 1
                },
                {
                    id: "animal6",
                    responseType: "input",
                    questionText: "What percentage of your employees are BQA Certified?",
                    inputType: "number",
                    scoringCriteria: "roundOff"
                }
            ],
            "efficiency": [
                {
                    id: "efficiency1",
                    responseType: "select",
                    questionText: "Do you measure weaning weight either by individual cow or by unit of land? Neither?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "efficiency2",
                    responseType: "select",
                    questionText: "Do you track calf weaning percentage per cow exposed?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "efficiency3",
                    responseType: "input",
                    questionText: "What is your calf weaning percentage per cow exposed?",
                    inputType: "number",
                    scoringCriteria: "roundOff"
                },
                {
                    id: "efficiency4",
                    responseType: "select",
                    questionText: "Are you/will you making culling decisions based on calf weaning weight or cow reproductive success?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "efficiency5",
                    responseType: "select",
                    questionText: "When determing mating decisions are you selecting bulls in considerations of your own cowherds strengths and weaknesses?",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "efficiency6",
                    responseType: "upload",
                    questionText: "Are you willing to share your breeding plan? If so, please upload",
                    scoringCriteria: "confirmation",
                    score: 0.5
                },
            ],
            "improvement": [
                {
                    id: "improvement1",
                    responseType: "select",
                    questionText: "Have you or are you planning to examine the environmental impact of your operation? (Water footprint)",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "improvement2",
                    responseType: "input",
                    questionText: "If already completed, what was your footprint?",
                    inputType: "number",
                    scoringCriteria: "responsePresent",
                    score: 0.5
                },
                {
                    id: "improvement3",
                    responseType: "select",
                    questionText: "Have you or are you planning to examine the environmental impact of your operation? (Greenhouse Gas footprint)",
                    scoringCriteria: "confirmation",
                    score: 1
                },
                {
                    id: "improvement4",
                    responseType: "input",
                    questionText: "If already completed, what was your footprint?",
                    inputType: "number",
                    scoringCriteria: "responsePresent",
                    score: 0.5
                },
                {
                    id: "improvement5",
                    responseType: "select",
                    questionText: "Is your operation actively participating in ecosystem service markets or convservation programs?",
                    scoringCriteria: "confirmation",
                    score: 0.5
                },
                {
                    id: "improvement6",
                    responseType: "select",
                    questionText: "Do you have a herd health plan developed through a Veterinary-Client Patient Relationship (VCPR)?",
                    scoringCriteria: "confirmation",
                    score: 0.5
                },
                {
                    id: "improvement7",
                    responseType: "select",
                    questionText: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
                    scoringCriteria: "confirmation",
                    score: 0.5
                },
                {
                    id: "improvement8",
                    responseType: "select",
                    questionText: "Do you utilize RFID or alternative traceability technology?",
                    scoringCriteria: "confirmation",
                    score: 0.5
                }
            ]
        }
        this.createQuestionnaire(sectionalFormData, getSustainabilitySections());
    }
}