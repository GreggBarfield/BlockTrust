import { Widget } from '../../widget.mjs';
import { InfoModal } from '../../../core/info_modal.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class NewAuctionMarketForm extends Widget {
    constructor(requestRedirectTo) {
        let infoModal = new InfoModal("Create Auction Market");
        super(infoModal.getBody());
        this.searchFrame = infoModal.getFooter();
        this.requestRedirectTo = requestRedirectTo;
    }

    initType() {
        this.frame.innerHTML = "";
        this.inputs = {};
        this.generate();

    }

    generate(){
        let form = document.createElement("form");

        let firstFormRow = document.createElement("div");
        firstFormRow.className = "form-row";
        form.append(firstFormRow);

        let required = document.createElement("span");
        required.textContent = "*Required"
        required.style = "color: red;";
        firstFormRow.append(required);

        let auctionMarketFormGroup = document.createElement("div");
        auctionMarketFormGroup.className = "form-group col-md-12";
        form.append(auctionMarketFormGroup);
        
        let requiredIconName = document.createElement("span");
        requiredIconName.textContent = "*"
        requiredIconName.style = "color:red";
        let auctionMarketName = document.createElement("label");
        auctionMarketName.textContent = "Auction Market Name";
        auctionMarketFormGroup.append(auctionMarketName);
        auctionMarketFormGroup.append(requiredIconName);
        this.inputs.auctionMarketName = document.createElement("input");
        this.inputs.auctionMarketName.className = "form-control";
        this.inputs.auctionMarketName.type = "text";
        this.inputs.auctionMarketName.placeholder = "12345"
        auctionMarketFormGroup.append(this.inputs.auctionMarketName);

        let auctionMarketAddress = document.createElement("label");
        auctionMarketAddress.textContent = "Address";
        auctionMarketFormGroup.append(auctionMarketAddress);
        this.inputs.auctionMarketAddress = document.createElement("input");
        this.inputs.auctionMarketAddress.className = "form-control";
        this.inputs.auctionMarketAddress.type = "text";
        auctionMarketFormGroup.append(this.inputs.auctionMarketAddress);

        let requiredIconCity = document.createElement("span");
        requiredIconCity.textContent = "*"
        requiredIconCity.style = "color:red";
        let auctionMarketCity = document.createElement("label");
        auctionMarketCity.textContent = "City";
        auctionMarketFormGroup.append(auctionMarketCity);
        auctionMarketFormGroup.append(requiredIconCity);
        this.inputs.auctionMarketCity = document.createElement("input");
        this.inputs.auctionMarketCity.className = "form-control";
        this.inputs.auctionMarketCity.type = "text";
        auctionMarketFormGroup.append(this.inputs.auctionMarketCity);

        let requiredIconState = document.createElement("span");
        requiredIconState.textContent = "*"
        requiredIconState.style = "color:red";
        let auctionMarketState = document.createElement("label");
        auctionMarketState.textContent = "State";
        auctionMarketFormGroup.append(auctionMarketState);
        auctionMarketFormGroup.append(requiredIconState);
        this.inputs.auctionMarketState = document.createElement("input");
        this.inputs.auctionMarketState.className = "form-control";
        this.inputs.auctionMarketState.type = "text";
        auctionMarketFormGroup.append(this.inputs.auctionMarketState);

        let auctionMarketZip = document.createElement("label");
        auctionMarketZip.textContent = "Zip";
        auctionMarketFormGroup.append(auctionMarketZip);
        this.inputs.auctionMarketZip = document.createElement("input");
        this.inputs.auctionMarketZip.className = "form-control";
        this.inputs.auctionMarketZip.type = "text";
        auctionMarketFormGroup.append(this.inputs.auctionMarketZip);

        let auctionMarketPhone = document.createElement("label");
        auctionMarketPhone.textContent = "Phone";
        auctionMarketFormGroup.append(auctionMarketPhone);
        this.inputs.auctionMarketPhone = document.createElement("input");
        this.inputs.auctionMarketPhone.className = "form-control";
        this.inputs.auctionMarketPhone.type = "text";
        auctionMarketFormGroup.append(this.inputs.auctionMarketPhone);

        let auctionMarketEmail = document.createElement("label");
        auctionMarketEmail.textContent = "Email";
        auctionMarketFormGroup.append(auctionMarketEmail);
        this.inputs.auctionMarketEmail = document.createElement("input");
        this.inputs.auctionMarketEmail.className = "form-control";
        this.inputs.auctionMarketEmail.type = "text";
        auctionMarketFormGroup.append(this.inputs.auctionMarketEmail);

        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.addEventListener("click", (e)=>{
            this.asyncForm.submit();
        });
        this.searchFrame.prepend(submitButton);

        this.frame.append(form);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/create-new-auction-market",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            getData: () => {
                return {
                    name: this.inputs.auctionMarketName.value,
                    address: this.inputs.auctionMarketAddress.value,
                    city: this.inputs.auctionMarketCity.value,
                    state: this.inputs.auctionMarketState.value,
                    zip: this.inputs.auctionMarketZip.value,
                    phone: this.inputs.auctionMarketPhone.value,
                    email: this.inputs.auctionMarketEmail.value             
                }
            },
            requestRedirectTo: this.requestRedirectTo
        });

    }

    submit(){

    }
}