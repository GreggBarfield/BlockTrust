import { Widget } from '../../widget.mjs';
import { InfoModal } from '../../../core/info_modal.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class NewAuctionMarketForm extends Widget {
    constructor(requestRedirectTo) {
        let infoModal = new InfoModal("Create Auction Market");
        super(infoModal.getBody());
        this.auctionSaleFrame = infoModal.getFooter();
        this.requestRedirectTo = requestRedirectTo;
    }

    initType() {
        this.frame.innerHTML = "";
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
        let auctionMarketNameInput = document.createElement("input");
        auctionMarketNameInput.className = "form-control";
        auctionMarketNameInput.type = "text";
        auctionMarketFormGroup.append(auctionMarketNameInput);

        let auctionMarketAddress = document.createElement("label");
        auctionMarketAddress.textContent = "Address";
        auctionMarketFormGroup.append(auctionMarketAddress);
        let auctionMarketAddressInput = document.createElement("input");
        auctionMarketAddressInput.className = "form-control";
        auctionMarketAddressInput.type = "text";
        auctionMarketFormGroup.append(auctionMarketAddressInput);

        let requiredIconCity = document.createElement("span");
        requiredIconCity.textContent = "*"
        requiredIconCity.style = "color:red";
        let auctionMarketCity = document.createElement("label");
        auctionMarketCity.textContent = "City";
        auctionMarketFormGroup.append(auctionMarketCity);
        auctionMarketFormGroup.append(requiredIconCity);
        let auctionMarketCityInput = document.createElement("input");
        auctionMarketCityInput.className = "form-control";
        auctionMarketCityInput.type = "text";
        auctionMarketFormGroup.append(auctionMarketCityInput);

        let requiredIconState = document.createElement("span");
        requiredIconState.textContent = "*"
        requiredIconState.style = "color:red";
        let auctionMarketState = document.createElement("label");
        auctionMarketState.textContent = "State";
        auctionMarketFormGroup.append(auctionMarketState);
        auctionMarketFormGroup.append(requiredIconState);
        let auctionMarketStateInput = document.createElement("input");
        auctionMarketStateInput.className = "form-control";
        auctionMarketStateInput.type = "text";
        auctionMarketFormGroup.append(auctionMarketStateInput);

        let auctionMarketZip = document.createElement("label");
        auctionMarketZip.textContent = "Zip";
        auctionMarketFormGroup.append(auctionMarketZip);
        let auctionMarketZipInput = document.createElement("input");
        auctionMarketZipInput.className = "form-control";
        auctionMarketZipInput.type = "text";
        auctionMarketFormGroup.append(auctionMarketZipInput);

        let auctionMarketPhone = document.createElement("label");
        auctionMarketPhone.textContent = "Phone";
        auctionMarketFormGroup.append(auctionMarketPhone);
        let auctionMarketPhoneInput = document.createElement("input");
        auctionMarketPhoneInput.className = "form-control";
        auctionMarketPhoneInput.type = "number";
        auctionMarketFormGroup.append(auctionMarketPhoneInput);

        let auctionMarketEmail = document.createElement("label");
        auctionMarketEmail.textContent = "Email";
        auctionMarketFormGroup.append(auctionMarketEmail);
        let auctionMarketEmailInput = document.createElement("input");
        auctionMarketEmailInput.className = "form-control";
        auctionMarketEmailInput.type = "text";
        auctionMarketFormGroup.append(auctionMarketEmailInput);

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
        this.auctionSaleFrame.prepend(submitButton);
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
                    name: auctionMarketNameInput.value,
                    address: auctionMarketAddressInput.value,
                    city: auctionMarketCityInput.value,
                    state: auctionMarketStateInput.value,
                    zip: auctionMarketZipInput.value,
                    phone: auctionMarketPhoneInput.value,
                    email: auctionMarketEmailInput.value             
                }
            },
            requestRedirectTo: this.requestRedirectTo
        });
    }
}