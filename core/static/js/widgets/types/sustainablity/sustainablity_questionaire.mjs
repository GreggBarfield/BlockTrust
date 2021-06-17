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

            this.frame.append(air);

        }

    }



}