import { BaseQuestionnaireV2Widget } from "./base_questionnaire_v2.mjs";
import { sections, scoringCriteria, questionType } from "../../../core/sustainability_constants.mjs";

export class PackerQuestionnaireV2Widget extends BaseQuestionnaireV2Widget {
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
                    questionText: "Are strategies in place to optimize energy efficiency and reduce greenhouse gas emissions at company facilities?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "air2",
                    responseType: questionType.input,
                    questionText: "Report Scope 1 emissions.",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "number",
                    score: 1
                },
                {
                    id: "air3",
                    responseType: questionType.input,
                    questionText: "Report Scope 2 emissions.",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "number",
                    score: 1
                },
                {
                    id: "air4",
                    responseType: questionType.select,
                    questionText: "Does your company calculate carbon dioxide equivalents per head or per mass of finished product?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "air5",
                    responseType: questionType.input,
                    questionText: "What is the company's carbon dioxide equivalents per head or per mass of finished product (please specify unit)?",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "text",
                    score: 1
                },
                {
                    id: "air6",
                    responseType: questionType.select,
                    questionText: "Does your company make carbon dioxide equivalents or GHG emissions publicly available?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "air7",
                    responseType: questionType.select,
                    questionText: "Does your company track air and GHG emissions overtime and set goals for continued improvement? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "air8",
                    responseType: questionType.input,
                    questionText: "What is your GHG reduction goal?",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "text",
                    score: 1
                },
                {
                    id: "air9",
                    responseType: questionType.select,
                    questionText: "Does your company participate in partnerships, initiatives or programs to further GHG reduction and improve air quality? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "air10",
                    responseType: questionType.select,
                    questionText: "Is your Company taking tangible action to achieve an approved science-based target to reduce emissions in line with limiting global temperature increases to well below 2 or, ideally, 1.5 degrees Celsius relative to pre-industrial levels?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                }
            ],
            [sections.land.name] : [
                {
                    id: "land1",
                    responseType: questionType.select,
                    questionText: "Have opportunities relating to mitigating land and biodiversity impacts from company facilities been evaluated by your company? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "land2",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share the opportunities identified by your company? If so, please upload.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "land3",
                    responseType: questionType.select,
                    questionText: "Is you company currently involved or exploring involvement in initiatives and programs to mitigate land and biodiversity impacts from company facilities? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "land4",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share current involvement or plans for involvement for your company? If so, please upload.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "land5",
                    responseType: questionType.select,
                    questionText: "Do your company's facility construction, renovation or expansion projects will include a plan to mitigate impacts on natural resources by 2025.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "land6",
                    responseType: questionType.upload,
                    questionText: "Please share these plans.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                }
            ],
            [sections.water.name] : [
                {
                    id: "water1",
                    responseType: questionType.select,
                    questionText: "Do all company facilities have a water management plan?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water2",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share the plan? If so, please upload.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water3",
                    responseType: questionType.select,
                    questionText: "Is waste water permit non-compliances monitored for all company facilities? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water4",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share how many wastewater permit non-compliances for all company facilities in the previous calendar year? If so, please upload.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water5",
                    responseType: questionType.input,
                    questionText: "What is the water use in gallons/head/day or gallons/pound of beef processed for your company (please specify unit)?",
                    scoringCriteria: scoringCriteria.responsePresent,
                    inputType: "text",
                    score: 0.5
                },
                {
                    id: "water6",
                    responseType: questionType.select,
                    questionText: "Does the company make water performance efforts public?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water7",
                    responseType: questionType.select,
                    questionText: "Does your company track water use year-over-year?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water8",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share changes in water use for this year compared to the previous year? If so, please upload.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water9",
                    responseType: questionType.select,
                    questionText: "Does the company have goals for continued improvement in water use?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water10",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share these goals and company progress on these goals? Is so, please upload.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water11",
                    responseType: questionType.select,
                    questionText: "Does the company participate in partnerships, initiatives or programs to further advance water resource management?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water12",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share details on company involvement in partnerships, initiatives or programs to further advance water resource management? Is so, please upload.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "water13",
                    responseType: questionType.select,
                    questionText: "Have you assessed and implemented plans according to a water risk assessment at your facilities ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "water14",
                    responseType: questionType.upload,
                    questionText: "Do you work with your beef value chain to encourage adoption of the Beef Industry Sustainability Framework? If so, please share this relevant details of this strategy.",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                }
            ],
            [sections.safety.name] : [
                {
                    id: "safety1",
                    responseType: questionType.select,
                    questionText: "Does your company have a documented employee safety program?",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "safety2",
                    responseType: questionType.upload,
                    questionText: "If yes, please provide specifics on the program. Please upload. ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety3",
                    responseType: questionType.select,
                    questionText: "Does this program take into consideration employee well-being? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "safety4",
                    responseType: questionType.select,
                    questionText: "Does your company's employee safety program engage front-line employees and leadership? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "safety5",
                    responseType: questionType.select,
                    questionText: "Does the company track Total Recordable Incident Rates (TRIR)? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "safety6",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share your company's TRIR from this year and the previous year?  ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety7",
                    responseType: questionType.select,
                    questionText: "Does your company track trends for TRIR and reference rates against the NAICS industry standard rate to set goals for the upcoming year? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "safety8",
                    responseType: questionType.upload,
                    questionText: "Did you meet your goal?  ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                },
                {
                    id: "safety9",
                    responseType: questionType.select,
                    questionText: "Does the company participate in partnerships, initiatives or programs to further advance employee safety and well-being? ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 0.5
                },
                {
                    id: "safety10",
                    responseType: questionType.upload,
                    questionText: "Are you willing to share company involvement in partnerships, initiatives or programs to further advance employee safety and well-being? Is so, please upload. ",
                    scoringCriteria: scoringCriteria.confirmation,
                    score: 1
                }
            ],
            [sections.animal.name] : [],
            [sections.efficiency.name] : [],
            [sections.improvement.name] : [],
        }
        this.createQuestionnaire(questionnaireData);
    }
}


/*

SELECT
{
    id: "",
    responseType: questionType.select,
    questionText: "",
    scoringCriteria: scoringCriteria.confirmation,
    score: 
},


INPUT
{
    id: "",
    responseType: questionType.input,
    questionText: "",
    scoringCriteria: scoringCriteria.responsePresent,
    inputType: "",
    score: 
},
*/