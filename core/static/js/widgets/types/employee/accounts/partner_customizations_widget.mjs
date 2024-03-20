import { Widget } from '../../../widget.mjs';
import { FileUploader } from '../../../../files/file_uploader.mjs';
import { AsyncForm } from '../../../../../global/async_form.mjs';

export class PartnerCustomizationsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () =>{
        this.frame.innerHTML = "";
        let partnerId = this.frame.getAttribute("data-widget-partner-id");
        let partnerCustomizationsForm = this.createPartnerCustomizationsForm(partnerId);
        this.frame.append(partnerCustomizationsForm);
    }

    createPartnerCustomizationsForm = (partnerId) =>{
        let card = document.createElement("div");
        card.className = "card";
        
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header p-1 d-flex";
        let cardHeaderText = document.createElement("h5");
        cardHeaderText.className = "mt-2 p-2 col-md-6";
        cardHeaderText.textContent = "Customization options for Partner " + partnerId;
        cardHeader.append(cardHeaderText);
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body row d-block";

        let form = document.createElement("form");
        let colorFormRow = document.createElement("div");
        colorFormRow.className = "col-md-3 d-inline-flex";
        let colorInputText = document.createElement("label");
        colorInputText.className = "form-label";
        colorInputText.textContent = "Select Color Scheme";
        colorFormRow.append(colorInputText);
        let colorInput = document.createElement("input");
        colorInput.type = "color";
        colorInput.className = "form-control form-control-color";
        colorInput.value = "#563d7c";
        colorInput.title = "Choose your color";
        colorFormRow.append(colorInput);
        form.append(colorFormRow);

        let logoInputRow = document.createElement("div");
        logoInputRow.className = "m-1 p-1";
        let logoUploader = new FileUploader(logoInputRow, []);
        form.append(logoInputRow);
        


 

        cardBody.append(form);
        card.append(cardBody);
        return card;
    }
}