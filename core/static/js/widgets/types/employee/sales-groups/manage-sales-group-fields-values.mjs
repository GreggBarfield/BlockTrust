import { AsyncForm } from '../../../../../global/async_form.mjs';
import { Widget } from "../../../widget.mjs";

export class ManageSalesGroupFieldsValuesWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {

        let salesGroupFieldsValues = JSON.parse(this.frame.getAttribute("data-widget-sales-group-fields-values"));
        let salesGroupFieldsIdsToNames = JSON.parse(this.frame.getAttribute("data-widegt-sales-group-field-ids-to-names"));

        let salesGroupFieldsValuesContainer  = this.createSalesGroupFieldsValuesContainer();
        this.frame.append(salesGroupFieldsValuesContainer);
    }

    createSalesGroupFieldsValuesContainer = () =>{

    }
}