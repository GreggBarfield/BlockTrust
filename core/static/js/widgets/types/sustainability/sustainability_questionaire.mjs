import { AbstractBaseQuestionaireWidget } from "./abstract_base_questionaire.mjs";

export class SustainabilityQuestionaireWidget extends AbstractBaseQuestionaireWidget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";

        let formInfo = {
            questions: {
                air: {
                    1: "Do you have a grazing management plan (GMP)?",
                    2: "Do you, or does your grazing management plan (GMP), consider livestock distribution and/or stocking rate for optimal forage health?",
                    3: "Do you identify high use areas and/or strive to reduce soil erosion?",
                },
                animal: {
                    1: "Do you utilize the Beef Quality Assurance (BQA) Program principles?",
                    2: "Do you have a herd health plan developed through a Veterinary-Client Patient Relationship (VCPR)?",
                    3: "Do you implement a disease prevention plan that includes vaccination, biosecurity and nutrition protocols, which improves cattle health and reduces the need for antibiotics?",
                },
                efficiency: {
                    1: "Have you measured pounds weaned per cow or a similar production efficiency measurement and compared it from year to year?",
                    2: "When determining mating decisions are you selecting bulls based on a breeding plan that includes marketing goals and considers your cowherd's strengths and weaknesses?",
                    3: "Does your operation record revenues and expenses throughout the year in an accounting format?",
                },
                safety: {
                    1: "Have employees been trained on stockmanship techniques and their importance?",
                    2: "Do you conduct safety trainings for all employees?",
                    3: "Does your operation actively try to mitigate or remove safety hazards in facilities and equipment?",
                },
                land: {
                    1: "Is the operation setup in an estate plan or other type of succession plan that keeps it in working lands?",
                    2: "Do you have a grazing management plan (GMP) that includes contingency plans for natural disasters (whatever is applicable in your region: drought, flood, fire, hurricane, blizzard)?",
                    3: "Do you have a grazing management plan (GMP) that considers protection of local endangered species and reduction of invasive plants?",
                    4: "Is wildlife conservation taken into account in your GMP?",
                },
                water: {
                    1: "Have you leveraged outside resources to help you protect existing, or develop new water resources? (examples may include: private technical service providers, Cooperative)",
                    2: "Do you or does your grazing management plan (GMP) identify wetland areas or navigable waterways on your operation and manage grazing to protect and/or improve them?",
                    3: "Do you have a plan to improve water resources, distribution and access for your cattle? (examples may be: spring development, solar wells, rotational grazing, alternative water)",
                },
            },
            answers: {
                air: {
                    "1a": "Yes, we manage our grazing with a plan, but it is not a written plan.",
                    "1b": "I don't have a formal grazing management plan.",
                    "1c": "Yes, we have a written grazing management plan.",
                    "2a": "Both are analyzed annually, but no written records are kept.",
                    "2b": "We stock our grazing land at generally the same level each year.",
                    "2c": "Both are analyzed annually, and records are kept to evaluate long term.",
                    "3a": "No, we are not working to reduce erosion at this time.",
                    "3b": "Yes, we identify erosion prone areas and work to limit erosion.",
                    "3c": "Yes, we are making plans to manage erosion-prone areas.",
                },
                animal: {
                    "1a": "We are not certified but follow BQA principles.",
                    "1b": "We don't follow BQA principles.",
                    "1c": "All animal handlers are BQA certified.",
                    "2a": "The veterinarian visits routinely and is familiar with our operation and animals.",
                    "2b": "We call the veterinarian for emergencies, but not for routine procedures.",
                    "2c": "We handle most issues on-site without vet consultation.",
                    "3a": "We don't have a formal plan that addresses these areas.",
                    "3b": "Our plan includes all these components.",
                    "3c": "Our plan includes some of these protocols, but not all.",
                },
                efficiency: {
                    "1a": "Yes",
                    "1b": "No",
                    "1c": "",
                    "2a": "I usually get a bull based on visual appraisal, but I don't use EPDs or performance information.",
                    "2b": "Yes, I select sires to use in an AI program based on EPDs and/or performance of my cowherd as well as the bull.",
                    "2c": "I trust my breeder to select a bull for me that fits my needs.",
                    "3a": "We keep track of expenses and evaluate periodically.",
                    "3b": "We reconcile our accounts when it becomes important.",
                    "3c": "We use an accounting program to accurately track revenues and expenses in real time.",
                },
                safety: {
                    "1a": "We have not gone through any trainings, and do not intend to.",
                    "1b": "Everyone who handles livestock has been trained or certified and implements these techniques consistently.",
                    "1c": "Some, but not all, who handle livestock have been through trainings on stockmanship.",
                    "2a": "New employees are provided with safety training in the tasks they perform.",
                    "2b": "We have no official training or safety protocol.",
                    "2c": "We conduct or attend safety trainings for all employees at least annually.",
                    "3a": "Yes, where possible we conduct an analysis of hazards and try to eliminate or reduce risk.",
                    "3b": "No, it is up to each person to operate machinery, handle livestock, or do other hazardous jobs in a safe manner.",
                    "3c": "",
                },
                land: {
                    "1a": "Yes, we have a legal arrangement for the operation to remain a working landscape through ownership transfer.",
                    "1b": "We have a will and the heirs will decide what to do with the property.",
                    "1c": "We intend to get a succession plan put together at some point.",
                    "2a": "We do not have a written grazing management plan.",
                    "2b": "Contingency plans are incorporated into our grazing management plan for natural disasters that occur in our area.",
                    "2c": "Our grazing management plan does not currently address disasters/contingency plans.",
                    "3a": "Yes, our GMP does specifically address these and we implement measures for both endangered species and invasive plants.",
                    "3b": "Our GMP addresses one of these considerations.",
                    "3c": "Our GMP does not currently address either of these topics or we don't have a GMP.",
                    "4a": "Wildlife is not a concern on our operation.",
                    "4b": "Wildlife management is a priority in my grazing management plan.these topics or we don't have a GMP.",
                    "4c": "I leave food and cover for wildlife when possible.",
                },
                water: {
                    "1a": "Yes",
                    "1b": "No",
                    "1c": "",
                    "2a": "We do not have wetland areas on our operation.",
                    "2b": "We do not have a GMP and we don't manage water features on our operation.",
                    "2c": "Yes, we have done an inventory of wetlands on our property and manage cattle grazing to protect or improve them.",
                    "3a": "Yes",
                    "3b": "No, we do not have a GMP or it doesn't involve water source improvements.",
                    "3c": "",
                },
            },
        };

        let sections = {
            "air": "Air & Greenhouse Gas Emissions",
            "land": "Land Resources",
            "water": "Water Resources",
            "animal": "Animal Health & Well-Being",
            "safety": "Employee Safety & Well-Being",
            "efficiency": "Efficiency & Yield"
        };

        let saveCall = "save_sustainability";

        this.generate(formInfo, sections, saveCall);
    }

}
