import { Widget } from '../../widget.mjs';
import { ProgressBar } from '../../../core/progress_bar.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';

export class SustainabilityQuestionaireWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        
        this.frame.innerHTML = "";

        this.inputs = {};

        this.generate();


    }


    generate() {

        function createOption(input, value, text) {
            let option = document.createElement("option");
            option.value = value;
            option.textContent = text;
            input.append(option);
            return option;
        }
        function createQuestion(card, id, question, a, b, c) {
            let row = document.createElement("div")
            row.className = "form-row"
            card.append(row)

            let group = document.createElement("div");
            group.className = "form-group col-md-12";
            row.append(group);

            let label = document.createElement("label");
            label.textContent = question;
            group.append(label);

            let input = document.createElement("select");
            // input.type = "option";
            input.className = "form-control";
            input.id = id;
            group.append(input);

            createOption(input, "Any", "Please Choose")
            createOption(input, id + "A", a)
            createOption(input, id + "B", b)
            if (c != "") {
                createOption(input, id + "C", c)

            }



            return input;
        }

        //Air & Greenhouse Gas Emissions
        let that = this;
        let form = document.createElement("form");
        this.frame.append(form)
        // cardBody.append(form);

        let air = document.createElement("div");
        air.className = "card";

        let airHeader = document.createElement("div");
        airHeader.className = "card-header";
        air.append(airHeader);

        let airHeaderText = document.createElement("div");
        airHeaderText.className = "h4";
        airHeaderText.textContent = "Air & Greenhouse Gas Emissions";
        airHeader.append(airHeaderText);

        let airBody = document.createElement("div");
        airBody.className = "card-body";
        air.append(airBody);

        let q1 = createQuestion(airBody, "air1", "Are all employees trained through the LMA Guide to Animal Handling & Employee Training?", "The principles of the LMA Guide are followed and there is some training provided.",
            "No training is given and the topic is not addressed.", "Supervisors and employees are fully trained by recognized trainers and remain up-to-date.");
        let q2 = createQuestion(airBody, "air2", "Is there proper training and oversight in place to prohibit animal abuse?",
            "We have some training but there isn’t a process for reporting or even what to report.", "No training is provided.", "Yes, we have the training and we empower our employees at all levels to watch for issues.")
        let q3 = createQuestion(airBody, "air3", "Does the auction have protocols for non-ambulatory animals and euthanasia?", "No protocol and it is up to the supervisors to take care of these issues.",
            "Yes, only persons trained are allowed to euthanize animals.", "We don’t have a protocol but we do report down animals to our supervisor and they take care of it.")

        let q4 = createQuestion(airBody, "air4", "Are all the proper facilities recommendations implemented at the auction to reduce animal stress and injury?",
            "The facility was designed based on the guidelines at the time.",
            "The facility is in need of significant updates to come in line with current recommendations.", "All facilities are in line with the LMA guidelines for facilities and are monitored for potential injury-causing issues.")

        let q5 = createQuestion(airBody, "air5", "Does the auction emphasize the BQA Transportation Guidelines to its customers?",
            "Yes",
            "No", "")

        // this.frame.append(air);
        form.append(air);

        //Employee Safety & Well-Being

        let employee = document.createElement("div");
        employee.className = "card";

        let employeeHeader = document.createElement("div");
        employeeHeader.className = "card-header";
        employee.append(employeeHeader);

        let employeeHeaderText = document.createElement("div");
        employeeHeaderText.className = "h4";
        employeeHeaderText.textContent = "Employee Safety & Well-Being";
        employeeHeader.append(employeeHeaderText);

        let employeeBody = document.createElement("div");
        employeeBody.className = "card-body";
        employee.append(employeeBody);

        let q6 = createQuestion(employeeBody, "employee1", "Does the auction have a written safety plan and is it provided to the employees?",
            "Nothing written but accidents are strongly discouraged.",
            "Yes, we have a fully developed plan that is updated regularly along with mandatory training.",
            "We have a written safety plan that we got from a state or industry labor group.")

        let q7 = createQuestion(employeeBody, "employee2", "Are regular safety meetings held and is job-specific training provided?",
            "We have training and some specific training is done but it isn’t mandatory.",
            "A few times a year someone comes by and talks about safety.",
            "Regular mandatory meetings are held and additional area-specific training is provided.")
        let q8 = createQuestion(employeeBody, "employee3", "Are accidents and injuries documented and reported to OSHA if needed?",
            "We report our serious accidents if worker’s compensation is needed.",
            "We are fully compliant with OSHA reporting, have robust records, and review internally.",
            "We report our required OSHA accidents and have a compliant system for reporting.")

        // this.frame.append(employee);
        form.append(employee);


        //Water Resources


        let water = document.createElement("div");
        water.className = "card";

        let waterHeader = document.createElement("div");
        waterHeader.className = "card-header";
        water.append(waterHeader);

        let waterHeaderText = document.createElement("div");
        waterHeaderText.className = "h4";
        waterHeaderText.textContent = "Water Resources";
        waterHeader.append(waterHeaderText);

        let waterBody = document.createElement("div");
        waterBody.className = "card-body";
        water.append(waterBody);

        let q9 = createQuestion(waterBody, "water1", "Does the auction or parent organizations support community activities and encourage employee involvement?",
            "No formal process but we support our local community, and allow employees to take time to participate.",
            "We don’t have any sort of program to speak of.",
            "We have a structured support/donation policy and encourage our employees to participate.")

        let q10 = createQuestion(waterBody, "water2", "If required for the facility does the auction have a waste water permit and is it in compliance with the permit?",
            "I believe we have permits or are exempt from them but haven’t really checked.",
            "We have a permit or confirmed exemption and compliance is assured by our trained staff.",
            "We have a permit and with help we keep the permit in compliance.")
        let q11 = createQuestion(waterBody, "water3", "Does the auction have a nutrient management plan and is it being implemented?",
            "Yes",
            "No", "")
        let q12 = createQuestion(waterBody, "water4", "Does the auction have a written water management strategy including measures to prevent leaks and protect water quality?",

            "Yes, we have an extensive strategy and we adopt new technology whenever possible.",
            "We have a water strategy and we try to check it periodically.",
            "No real strategy.")
        let q13 = createQuestion(waterBody, "water5", "Are employees with environmental responsibilities regularly trained?",
            "Annually.",
            "Less than annually.", "Rarely or not at all.")

        // this.frame.append(water);
        form.append(water)


        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        form.append(submitFormGroup);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        // submitButton.style="right: align-right";
        submitButton.type = "button";
        submitFormGroup.append(submitButton);

        this.progressBar = new ProgressBar();
        this.progressBar.attach(form);
        this.progressBar.hide();

        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);
        this.internalErrorMessage = document.createElement("p");
        this.internalErrorMessage.style.display = "none";
        this.internalErrorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(this.internalErrorMessage);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/save_sustainability",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {

                return {
                    
                    response: {
                        1: $(q1).val(),
                        2: $(q2).val(),
                        3: $(q3).val(),
                        4: $(q4).val(),
                        5: $(q5).val(),
                        6: $(q6).val(),
                        7: $(q7).val(),
                        8: $(q8).val(),
                        9: $(q9).val(),
                        10: $(q10).val(),
                        11: $(q11).val(),
                        12: $(q12).val(),
                        13: $(q13).val()
                    }
                }
            }
        });

        submitButton.addEventListener("click", () => {
           
            
                
                        this.asyncForm.submit();
     
        });


    }



}