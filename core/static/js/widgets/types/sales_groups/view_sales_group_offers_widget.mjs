import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { InfoModal } from '../../../core/info_modal.mjs';

export class ViewSalesGroupOffersWidget extends Widget{
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.getData(
            "get_sales_groups_offers",
            {
                sales_group_id: this.salesGroupID
            }
        ).then((data) => {
            this.data = data;
            console.log(this.data);
            this.makeOffersTable();
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });
    
    }

    createConfirmationAlert(buttonText, buttonClassName, postRoute, offer){
        let alertModal = new InfoModal("Confirm Action");
        let alertModalBody = alertModal.getBody();
        let alertMessage = document.createElement("label");
        alertMessage.textContent = `${buttonText} the offer from Account ${offer.offering_account_id} for ${offer.offer_amount}?`;
        alertMessage.className = "font-weight-bold h5";
        alertModalBody.append(alertMessage);

        let warningMessage = document.createElement("label");
        warningMessage.textContent = "*Accepting an offer will automatically decline all existing offers"
        warningMessage.className = "font-weight-light font-italic";
        alertModalBody.append(warningMessage);

        let postActionButton = document.createElement("button");
        postActionButton.className = buttonClassName;
        postActionButton.textContent = buttonText;
        postActionButton.addEventListener("click", (e)=>{
            let offer_string = JSON.stringify(offer);
            fetch(
                postRoute,{
                method: "POST",
                body: offer_string,
                headers: {"Content-type": "application/json; charset=UTF-8"}
                })
                .then(function(response){
                if(response.status == 200){
                    location.reload();
                }
                });
        });
        alertModal.getFooter().prepend(postActionButton);
        return alertModal;
    }

    createButton(buttonText, offer, postRoute, buttonClassName){
        let button = document.createElement("button");
        button.className = buttonClassName;
        button.textContent = buttonText;
        button.onclick = () => {
            let confirmationAlert = this.createConfirmationAlert(buttonText, buttonClassName, postRoute, offer);
        }
        return button;
    }

    createTable(offersList){
        // Creating checklist table
        let table = document.createElement('table');
        table.className = "table table-striped table-bordered nowrap";
        let tableHead = document.createElement("thead");
        table.appendChild(tableHead);
        //Table header row
        let tableHeadRow0 = document.createElement("tr");
        tableHead.appendChild(tableHeadRow0);
        const tableHeaders = ["Offering Account", "Offer Amount", "Options"];
        for (const tableHeaderText of tableHeaders) {
            let th = document.createElement("th");
            th.textContent = tableHeaderText;
            tableHeadRow0.appendChild(th);
        }
        let tableBody = document.createElement("tbody");
        table.appendChild(tableBody);
        //Creating checklist table body
        for (const offer of offersList) {
            let rowTag = document.createElement("tr");
            tableBody.appendChild(rowTag);
            let tdOfferingAccount = document.createElement("td");
            tdOfferingAccount.textContent = offer.offering_account_id;
            rowTag.appendChild(tdOfferingAccount);
            let tdOfferAmount = document.createElement("td")
            tdOfferAmount.textContent = offer.offer_amount;
            rowTag.appendChild(tdOfferAmount);
            let tdOptions = document.createElement("td");
            let acceptButton = this.createButton("Accept", offer, "/widgets/data/sales-group/accept-offer", "btn btn-primary");
            let declineButton = this.createButton("Decline", offer, "/widgets/data/sales-group/decline-offer", "btn btn-danger");
            tdOptions.appendChild(acceptButton);
            tdOptions.appendChild(declineButton);
            rowTag.appendChild(tdOptions);
        }
        return table;
    }

    makeOffersTable(){
        let card = document.createElement("div");
        card.className = "card";

        let salesGroupOffersName = document.createElement("h5");
        salesGroupOffersName.className = "mt-2";
        salesGroupOffersName.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;";
        salesGroupOffersName.textContent = `View Offers for Sales Group ${this.salesGroupID}`;

        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between";
        cardHeader.style = "padding:5px;padding-left: 15px;";
        
        cardHeader.append(salesGroupOffersName);
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);

        let offersTable = this.createTable(this.data.sales_group_offers);
        cardBody.append(offersTable);

        this.frame.append(card);
    }
}