import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { sections, scoringCriteria, questionType } from "../../../core/sustainability_constants.mjs";

export class FeedlotQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
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
                    questionText: "Are animals sorted into contemporary groups to improve efficiency at the pen level?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "air2",
                    responseType: questionType.select,
                    questionText: "Are you or are you planning to implement early diagnostic tools to identify and treat sick animals earlier?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "air3",
                    responseType: questionType.select,
                    questionText: "Are you using feed additives to optimize growth in an effort to reduce emissions?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "air4",
                    responseType: questionType.input,
                    questionText: "If so, which feed additives?",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "text",
                    score: 0.5
                },
                {
                    id: "air5",
                    responseType: questionType.select,
                    questionText: "Are energy uses reviewed periodically to identify opportunities to gain efficiencies or reduce usage?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "air6",
                    responseType: questionType.input,
                    questionText: "What opportunities have you identified?",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "text",
                    score: 1
                }
            ],
            [sections.land.name] : [
                {
                    id: "land1",
                    responseType: questionType.select,
                    questionText: "Do you implement nutrient management BMPs? (ie. manure management, tillage strategies, fertilizer and pesticide applications etc.)",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "land2",
                    responseType: questionType.select,
                    questionText: "Does the feedyard have applicable state and or federal water and or environmental permits?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "land3",
                    responseType: questionType.select,
                    questionText: "If yes, are all records required for the permits being properly maintained and reported?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "land4",
                    responseType: questionType.select,
                    questionText: "Do you have a written nutrient management plan?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "land5",
                    responseType: questionType.select,
                    questionText: "If yes, do you have SOPs for measuring the required items in the nutrient management plan?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "land6",
                    responseType: questionType.upload,
                    questionText: "If you have a plan, are you willing to share it?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                }
            ],
            [sections.water.name] : [
                {
                    id: "water1",
                    responseType: questionType.select,
                    questionText: "Do you currently implement water conservation management practices?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water2",
                    responseType: questionType.input,
                    questionText: "If so, which practices?",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "text",
                    score: 0.5
                },
                {
                    id: "water3",
                    responseType: questionType.select,
                    questionText: "Is water use reviewed regularly to improve water use optimization?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water4",
                    responseType: questionType.input,
                    questionText: "If so, what practices have you identified?",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "text",
                    score: 0.5
                },
                {
                    id: "water5",
                    responseType: questionType.select,
                    questionText: "Is water infrastructure properly maintained and upgraded to improve water use efficiency?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water6",
                    responseType: questionType.select,
                    questionText: "Do you have a written water management strategy?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water7",
                    responseType: questionType.upload,
                    questionText: "If yes, are you willing to share it?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
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
                    scoringCriteria: scoringCriteria.roundOff,
                    inputType: "number",
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
                    responseType: questionType.upload,
                    questionText: "If yes, what was your score? Please upload",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "animal6",
                    responseType: questionType.select,
                    questionText: "What percentage of your livestock handling employees are BQA certified?",
                    scoringCriteria: scoringCriteria.roundOff,
                    score: 1
                },
            ],
            [sections.safety.name] : [
                {
                    id: "safety1",
                    responseType: questionType.select,
                    questionText: "Do you have an employee safety program?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety2",
                    responseType: questionType.input,
                    questionText: "If yes, are you willing to share it?",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType : "text",
                    score: 1
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
                    questionText: "Do 100% of your employees undergo safety training annually?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety5",
                    responseType: questionType.input,
                    questionText: "What percentage of your employees have undergone safety training?",
                    scoringCriteria: scoringCriteria.roundOff
                }
            ],
            [sections.efficiency.name] : [
                {
                    id: "efficiency1",
                    responseType: questionType.select,
                    questionText: "Are closeout metrics and performance tracked and compared over time?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "efficiency2",
                    responseType: questionType.select,
                    questionText: "Are feed rations formulated to optimize resources and performance?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "efficiency3",
                    responseType: questionType.select,
                    questionText: "Are feed ingredients stored to prevent or minimize spoilage and is loss prevention practiced?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "efficiency4",
                    responseType: questionType.select,
                    questionText: "Is feed delivery monitored for efficiency and reviewed for improvements?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "efficiency5",
                    responseType: questionType.select,
                    questionText: "Is energy consumption measured and is there a process to look for more efficient utilization?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                }
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
                    inputType: "number",
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
                    inputType: "number",
                    scoringCriteria: scoringCriteria.responsePresent,
                    score: 0.5
                },
                {
                    id: "improvement5",
                    responseType: questionType.select,
                    questionText: "Have you or are you planning to install green infrastructure?",
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