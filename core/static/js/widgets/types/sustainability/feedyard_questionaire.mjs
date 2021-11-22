import { AbstractBaseQuestionaireWidget } from "./abstract_base_questionaire.mjs";

export class FeedyardQuestionaireWidget extends AbstractBaseQuestionaireWidget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        let formInfo = {
            questions: {
                air: {
                    1: "Are pen surfaces managed for both wet and dry conditions?",
                    2: "Are road and alley management strategies in place?",
                    3: "Are feed processing dust management strategies in place?",
                    4: "Are growth-promoting technologies utilized during the finishing phase to optimize growth?",
                    5: "Are energy uses reviewed periodically looking for opportunities to gain efficiencies or reduce usage?"
                },
                animal: {
                    1: "Are all employees that work with animals BQA certified?",
                    2: "Does the facility utilize professionals to create training and provide oversight for medical treatment and rations?",
                    3: "Is there proper training and oversight in place to prohibit animal abuse?",
                    4: "Is there a plan for antibiotic use and effective review and oversight to ensure proper use?",
                    5: "Does the feedyard have a SOP for non-ambulatory animals and euthanasia protocols?",
                    6: "Are the proper records of animal treatment and all associated medicines being maintained?"
                },
                efficiency: {
                    1: "Are closeout metrics and performance tracked and compared over time?",
                    2: "Are feed rations formulated to optimize resources and performance?",
                    3: "Are feed ingredients stored to prevent or minimize spoilage and is loss prevention practiced?",
                    4: "Is energy consumption measured and is there a process to look for more efficient utilization?",
                    5: "Is feed delivery monitored for efficiency and reviewed for improvements?"
                },
                safety: {
                    1: "Does the feedyard have a written safety plan and is it provided to the employees?",
                    2: "Are regular safety meetings held and is job specific training provided?",
                    3: "Are accidents and injuries documented and reported to OSHA if needed?",
                    4: "Are benefits provided to full-time employees? (Medical, retirement, etc.)",
                    5: "Does the feedyard or parent organizations support community activities and encourage employee involvement?"
                },
                land: {
                    1: "Does the feedyard have applicable state and/or federal water and/or environmental permits?",
                    2: "Are all records required for the permit(s) being properly maintained and reported?",
                    3: "Is there a documented Nutrient Management Plan?",
                    4: "Do you have SOPs for measuring the required items in the Nutrient Management Plan?",
                    5: "Is there an employee or employees assigned the responsibility for assuring compliance?"
                },
                water: {
                    1: "Does the feedyard have a waste water permit and is it in compliance with the permit?",
                    2: "Does the feedyard have a nutrient management plan and is it being followed?",
                    3: "Is there a documented water management strategy that is updated regularly?",
                    4: "Are employees with environmental responsibilities regularly trained?",
                },
            },
            answers: {
                air: {
                    "1a": "There are limited management practices or for only one condition.",
                    "1b": "There are no specific management practices in use.",
                    "1c": "Yes, there are full management practices for both wet and dry conditions.",
                    "2a": "We implement minimal management.",
                    "2b": "There are no specific management practices in use.",
                    "2c": "Yes, there is full management to reduce or eliminate dust and emissions.",
                    "3a": "There are no specific management practices in use.",
                    "3b": "Yes, there is management of the feed mill and loading area and unloading area.",
                    "3c": "There are minimal management or processes used.",
                    "4a": "We utilize some technologies.",
                    "4b": "We do not utilize this type of technology.",
                    "4c": "We utilize technologies extensively to reduce resource usage.",
                    "5a": "We actively seek out opportunities for reducing energy use.",
                    "5b": "As items wear out some attention is given to picking more efficient replacements.",
                    "5c": "No, we just pick based on price and availability."
                },
                animal: {
                    "1a": "No training is given and the topic is not addressed.",
                    "1b": "Supervisors and employees are fully trained by certified trainers and remain up-to-date.",
                    "1c": "The principles of BQA are followed and there is some training provided.",
                    "2a": "We sometimes use a vet or a nutritionist but don’t have one regularly providing oversight or advice.",
                    "2b": "No, we only use specialists in rare circumstances.",
                    "2c": "Yes, we contract or employ a licensed veterinarian or nutritionist.",
                    "3a": "No training is provided.",
                    "3b": "Yes, we have the training and we empower our employees at all levels to watch for issues.",
                    "3c": "We have some training but there isn’t any process for reporting or even what to report.",
                    "4a": "We have a veterinarian create our protocols, but there is no follow up or training.",
                    "4b": "No review is made and no training is given.",
                    "4c": "Yes, we have a vet prepare our protocols, provide training and provide oversight.",
                    "5a": "No SOP and it is up to the supervisors to take care of these issues.",
                    "5b": "Yes, only persons trained are allowed to euthanize animals.",
                    "5c": "We don’t have a SOP, but we do report down animals to our supervisor and they take care of it.",
                    "6a": "We have a medical system but it isn’t always used or isn’t very robust.",
                    "6b": "No system is maintained, we try to write down what we have done at the end of the day.",
                    "6c": "Yes, we have a robust medical system keeping records of all treatments given."
                },
                efficiency: {
                    "1a": "Yes, we are continually looking through the data and attempting to get more efficient.",
                    "1b": "We look through the data looking for problems and attempting to correct big problems.",
                    "1c": "No attempt to review the data is made and only minimal effort is made to improve.",
                    "2a": "Yes, rations are optimized to improve nutrition and/or performance, while minimizing cost and resources.",
                    "2b": "Yes, we attempt to provide basic nutrition at the cheapest cost for the performance.",
                    "2c": "No, we meet basic needs and rarely review our formulas.",
                    "3a": "Other than keeping the feed from going bad, no effort is made to protect the ingredients.",
                    "3b": "Yes, we use multiple methods of protecting our feed ingredients depending on ingredient.",
                    "3c": "Yes, we use some protection for our ingredients.",
                    "4a": "Yes, we review energy use in all areas and look for ways to reduce usage and be more efficient.",
                    "4b": "Yes, when we replace equipment we look to upgrade to more efficient equipment.",
                    "4c": "No real effort is made to review/reduce energy use other than price.",
                    "5a": "We deliver the feed as best we can, but do not have the resources for updates or trainings.",
                    "5b": "Feed delivery is reviewed multiple times and we are always looking for ways to improve through advanced technology, training and practices.",
                    "5c": "We train the drivers when they start and update equipment only when old equipment needs replacing."
                },
                safety: {
                    "1a": "Yes, we have a fully developed plan that is updated regularly along with mandatory training.",
                    "1b": "We have a written safety plan that we got from a state or industry labor group.",
                    "1c": "Nothing written but accidents are strongly discouraged.",
                    "2a": "We have training and some specific training is done but it isn’t mandatory.",
                    "2b": "A few times a year someone comes by and talks about safety.",
                    "2c": "Regular mandatory meetings are held and additional area-specific training is provided.",
                    "3a": "We report our serious accidents if worker’s compensation is needed.",
                    "3b": "We are fully compliant with OSHA reporting, have robust records, and review internally.",
                    "3c": "We report our required OSHA accidents and have a compliant system for reporting.",
                    "4a": "We have worker's compensation but nothing else.",
                    "4b": "Yes, full and comprehensive benefits are provided.",
                    "4c": "Yes, we have some benefits like medical and retirement.",
                    "5a": "No formal process but we support our local community, and allow employees to take time to participate.",
                    "5b": "We don’t have any sort of program to speak of.",
                    "5c": "We have a structured support/donation policy and encourage our employees to participate."
                },
                land: {
                    "1a": "We currently are exempt or do not have a permit.",
                    "1b": "Yes, we have all applicable licenses and are fully compliant.",
                    "1c": "We have the EPA water permit or state equivalent as required.",
                    "2a": "Yes, we have the minimum required records and have passed our annual reviews.",
                    "2b": "Records are on my notepad on my dash or no permit required.",
                    "2c": "Yes, we have a robust records system and trained personnel managing them.",
                    "3a": "No formal plan has been documented.",
                    "3b": "Yes, we have a professionally developed plan that we adhere to strictly.",
                    "3c": "We have a plan that is generic or minimal but meets the requirements.",
                    "4a": "We have SOPs for the items that are required for our plan and permit.",
                    "4b": "I try to be consistent when and where I can but no one knows the plan but me.",
                    "4c": "Our plan has SOPs and we follow it to the letter.",
                    "5a": "No particular person is assigned this duty but parts are assigned to people as needed from time to time.",
                    "5b": "We have trained and dedicated staff or we utilize outside experts who assure compliance.",
                    "5c": "I believe we have permits or are exempt from them but haven’t really checked."
                },                
                water: {
                    "1a": "We have a permit and with help we keep the permit in compliance.",
                    "1b": "I believe we have permits or are exempt from them but haven't really checked.",
                    "1c": "We have a permit and compliance is assured by our trained staff.",
                    "2a": "Yes",
                    "2b": "No",
                    "2c": "",
                    "3a": "No real strategy.",
                    "3b": "Yes, we have an extensive strategy and we adopt new technology whenever possible.",
                    "3c": "We have a water strategy and we try to check it periodically.",
                    "4a": "Rarely or not at all",
                    "4b": "Annually",
                    "4c": "Less than annually"
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

        this.frame.innerHTML = "";
        this.generate(formInfo, sections);
    }
}
