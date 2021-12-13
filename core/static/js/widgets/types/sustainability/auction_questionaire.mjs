import { AbstractBaseQuestionaireWidget } from "./abstract_base_questionaire.mjs";

export class AuctionQuestionaireWidget extends AbstractBaseQuestionaireWidget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";

        let formInfo = {
            questions: {
                animal: {
                    1: "Are all employees trained through the LMA Guide to Animal Handling & Employee Training?",
                    2: "Is there proper training and oversight in place to prohibit animal abuse?",
                    3: "Does the auction have protocols for non-ambulatory animals and euthanasia?",
                    4: "Are all the proper facilities recommendations implemented at the auction to reduce animal stress and injury?",
                    5: "Does the auction emphasize the BQA Transportation Guidelines to its customers?"
                },
                safety: {
                    1: "Does the auction have a written safety plan and is it provided to the employees?",
                    2: "Are regular safety meetings held and is job-specific training provided?",
                    3: "Are accidents and injuries documented and reported to OSHA if needed?"
                },
                water: {
                    1: "Does the auction or parent organizations support community activities and encourage employee involvement?",
                    2: "If required for the facility does the auction have a waste water permit and is it in compliance with the permit?",
                    3: "Does the auction have a nutrient management plan and is it being implemented?",
                    4: "Does the auction have a written water management strategy including measures to prevent leaks and protect water quality?",
                    5: "Are employees with environmental responsibilities regularly trained?"
                },
            },
            answers: {
                animal: {
                    "1a": "The principles of the LMA Guide are followed and there is some training provided.",
                    "1b": "No training is given and the topic is not addressed.",
                    "1c": "Supervisors and employees are fully trained by recognized trainers and remain up-to-date.",
                    "2a": "We have some training but there isn’t a process for reporting or even what to report.",
                    "2b": "No training is provided.",
                    "2c": "Yes, we have the training and we empower our employees at all levels to watch for issues.",
                    "3a": "No protocol and it is up to the supervisors to take care of these issues.",
                    "3b": "Yes, only persons trained are allowed to euthanize animals.",
                    "3c": "We don’t have a protocol but we do report down animals to our supervisor and they take care of it.",
                    "4a": "The facility was designed based on the guidelines at the time.",
                    "4b": "The facility is in need of significant updates to come in line with current recommendations.",
                    "4c": "All facilities are in line with the LMA guidelines for facilities and are monitored for potential injury-causing issues.",
                    "5a": "Yes",
                    "5b": "No",
                    "5c": ""
                },
                safety: {
                    "1a": "Nothing written but accidents are strongly discouraged.",
                    "1b": "Yes, we have a fully developed plan that is updated regularly along with mandatory training.",
                    "1c": "We have a written safety plan that we got from a state or industry labor group.",
                    "2a": "We have training and some specific training is done but it isn’t mandatory.",
                    "2b": "A few times a year someone comes by and talks about safety.",
                    "2c": "Regular mandatory meetings are held and additional area-specific training is provided.",
                    "3a": "We report our serious accidents if worker’s compensation is needed.",
                    "3b": "We are fully compliant with OSHA reporting, have robust records, and review internally.",
                    "3c": "We report our required OSHA accidents and have a compliant system for reporting."
                },
                water: {
                    "1a": "No formal process but we support our local community, and allow employees to take time to participate.",
                    "1b": "We don’t have any sort of program to speak of.",
                    "1c": "We have a structured support/donation policy and encourage our employees to participate.",
                    "2a": "I believe we have permits or are exempt from them but haven’t really checked.",
                    "2b": "We have a permit or confirmed exemption and compliance is assured by our trained staff.",
                    "2c": "We have a permit and with help we keep the permit in compliance.",
                    "3a": "Yes",
                    "3b": "No",
                    "3c": "",
                    "4a": "Yes, we have an extensive strategy and we adopt new technology whenever possible.",
                    "4b": "We have a water strategy and we try to check it periodically.",
                    "4c": "No real strategy.",
                    "5a": "Annually.",
                    "5b": "Less than annually.",
                    "5c": "Rarely or not at all."
                },
            },
        };

        let sections = {
            "water": "Water Resources",
            "animal": "Animal Health & Well-Being",
            "safety": "Employee Safety & Well-Being"
        };

        this.generate(formInfo, sections);
    }

}
