import { InfoModal } from '../../../core/info_modal.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { Widget } from '../../widget.mjs';

export class SalesGroupOfferWidget extends Widget{
    constructor(salesGroupID, salesGroupName=null) {
        let salesGroupNameStr = salesGroupName;
        if (salesGroupNameStr === null || salesGroupNameStr == undefined) {
            if (typeof salesGroupID === "number") {
                salesGroupNameStr = "Sales Group " + salesGroupID;
            }
            else {
                throw "Needs to know the Sales Group";
            }
        }
        let infoModal = new InfoModal("Make an Offer for: <span class='text-primary'>" + salesGroupNameStr + "</span>");
        super(infoModal.getBody());
        this.saleGroupOfferFrame = infoModal.getFooter();
        this.salesGroupID = salesGroupID;
    }

    initType() {
        this.frame.innerHTML = "";
        this.getData(
            "get_existing_offers_for_sales_group",
            {
                sales_group_id: this.salesGroupID
            }
        ).then((data) => {
            this.data = data;
            this.generate();
        });
    }

    generate(){
        let form = document.createElement("form");

        let formGroup = document.createElement("div");
        formGroup.className = "form-group";
        form.append(formGroup);

        if(this.data.existing_offers_by_account.length > 0){
            let existing_offer_data = this.data.existing_offers_by_account[0];
            let existingOfferLabel = document.createElement("label");
            existingOfferLabel.className = "col-md-12 mt-1 mb-1 alert alert-primary";
            existingOfferLabel.textContent = "You have an existing offer for : $"+ existing_offer_data.offer_amount;
            formGroup.append(existingOfferLabel);
        }

        let offerAmountlabel = document.createElement("label");
        offerAmountlabel.textContent = "Offer Amount:";
        formGroup.append(offerAmountlabel);

        let offerAmountInput = document.createElement("input");
        offerAmountInput.type = "number";
        offerAmountInput.step = "0.01";
        offerAmountInput.className = "form-control";
        formGroup.append(offerAmountInput);

        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        formGroup.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        formGroup.append(errorMessage);

        let submitButton = document.createElement("button");
        submitButton.textContent = "Send";
        submitButton.className = "btn btn-primary";
        this.saleGroupOfferFrame.prepend(submitButton);
        this.frame.append(form);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/add_or_update_offer_for_sales_group",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            getData: () => {
                return {
                    sales_group_id: this.salesGroupID,
                    offer_amount: offerAmountInput.value            
                }
            },
            requestRedirectTo: window.location.href
        });
    
        submitButton.addEventListener("click", (e)=>{
            this.asyncForm.submit();
        });
    }

}
