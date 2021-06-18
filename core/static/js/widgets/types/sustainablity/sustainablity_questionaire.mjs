import { Widget } from '../../widget.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';

export class SustainablityQuestionaireWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";

        this.inputs = {};

        this.generate();

    }


    generate() {

        function createOption(input,value,text) {
            let option = document.createElement("option");
            option.value = value;
            option.textContent= text;
            input.append(option);
            return option;
        }
        function createQuestion(card,id,question,a,b,c){
            let row = document.createElement("div")
            row.className = "form-row"
            card.append(row)

            let group = document.createElement("div");
            group.className = "form-group col-md-12";
            row.append(group);

            let label = document.createElement("label");
            label.textContent=question;
            group.append(label);

            let input = document.createElement("select");
            // input.type = "option";
            input.className = "form-control";
            input.id = id;
            group.append(input);

            createOption(input,"Any","Please Choose")
            createOption(input,id+"A",a)
            createOption(input,id+"B",b)
            createOption(input,id+"C",c)


            
            return input;
        }
        //Air & Greenhouse Gas Emissions
        {
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

            createQuestion(airBody,"air1","Are all employees trained through the LMA Guide to Animal Handling & Employee Training?","The principles of the LMA Guide are followed and there is some training provided.",
            "No training is given and the topic is not addressed.","Supervisors and employees are fully trained by recognized trainers and remain up-to-date.");
            createQuestion(airBody,"air2","Is there proper training and oversight in place to prohibit animal abuse?",
            "We have some training but there isn’t a process for reporting or even what to report.","No training is provided.","Yes, we have the training and we empower our employees at all levels to watch for issues.")
            createQuestion(airBody,"air3","Does the auction have protocols for non-ambulatory animals and euthanasia?","No protocol and it is up to the supervisors to take care of these issues.",
            "Yes, only persons trained are allowed to euthanize animals.","We don’t have a protocol but we do report down animals to our supervisor and they take care of it.")

            createQuestion(airBody,"air4","Are all the proper facilities recommendations implemented at the auction to reduce animal stress and injury?",
            "The facility was designed based on the guidelines at the time.",
            "The facility is in need of significant updates to come in line with current recommendations.","All facilities are in line with the LMA guidelines for facilities and are monitored for potential injury-causing issues.")

            createQuestion(airBody,"air5","Does the auction emphasize the BQA Transportation Guidelines to its customers?",
            "Yes",
            "No","----")
            
            this.frame.append(air);

        }

    }



}