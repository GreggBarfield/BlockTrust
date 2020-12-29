import { Widget } from '../../widget.mjs';
import { Table } from '../../../core/table.mjs';
import { ShortControls } from '../../../ui/short_controls.mjs';
import { formatDateTime } from '../../../core/time.mjs';
import { SwitchFormGroup } from '../../../ui/switch.mjs';
import { InfoModal } from '../../../core/info_modal.mjs';
import { DateFormGroup } from '../../../ui/inputs.mjs';

/**
 * 
 * @param {Object} [auctionSale] Preconfiguration row object
 * @param {number} auctionSale.id Auction Sale ID to update
 * @param {string} auctionSale.name Name
 */
let manageAuctionSale = (auctionSale={}) => {

    let isNew = true;
    let title = "New Auction Sale";
    let submitName = "Create";
    let submitInProgress = "Creating";
    let submitted = "Created";

    if ('id' in auctionSale) {
        isNew = false;
        title = "Edit Auction Sale";
        submitName = "Update";
        submitInProgress = "Updating";
        submitted = "Updated";
    }

    let infoModal = new InfoModal(title);
    let modalBody = infoModal.getBody();

    let form = document.createElement("form");
    modalBody.append(form);

    let inputName;

    {
        let formGroup = document.createElement("div");
        formGroup.className = "form-group";
        form.append(formGroup);

        let label = document.createElement("label");
        label.textContent = "Name:";
        formGroup.append(label);

        inputName = document.createElement("input");
        inputName.className = "form-control";
        inputName.setAttribute("maxlength", 1000);
        inputName.type = "text";
        inputName.value = auctionSale.name || "";
        formGroup.append(inputName);
    }

    let commentsTA;

    {
        let formGroup = document.createElement("div");
        formGroup.className = "form-group";
        form.append(formGroup);

        let label = document.createElement("label");
        label.textContent = "Comments:";
        formGroup.append(label);

        commentsTA = document.createElement("textarea");
        commentsTA.className = "form-control";
        commentsTA.setAttribute("maxlength", 1000);
        commentsTA.value = auctionSale.comments || "";
        formGroup.append(commentsTA);
    }

    let at;

    {
        at = new DateFormGroup(form, "At:", auctionSale.at || null);
    }

    let publishSwitch = new SwitchFormGroup(form, "Publish", ((!isNew) ? auctionSale.published : false));

    let submitButton = document.createElement("button");
    submitButton.textContent = submitName;
    submitButton.className = "btn btn-primary";
    infoModal.getFooter().append(submitButton);

    submitButton.addEventListener("click", ()=>{
        submitButton.disabled = true;
        submitButton.textContent = submitInProgress;

        let params = {
            name: inputName.value,
            comments: commentsTA.value,
            published: publishSwitch.isChecked(),
            at: at.getTime()

        };
        if (!isNew) {
            params.id = auctionSale.id;
        }

        $.ajax({
            url: "/widgets/data",
            data: JSON.stringify({
                "action": (isNew?"new_auction_sale":"update_auction_sale"),
                "params": params
            }),
            contentType: 'application/json',
            method: "POST"
        })
        .fail((jqXHR, textStatus) => {
            let e = "HTTP error " + jqXHR.status + " " + textStatus + ": " + jqXHR.responseText;
            let alert = document.createElement("div");
            alert.className = "alert alert-danger";
            alert.textContent = "Error occurred: " + e;
            modalBody.append(alert);
            submitButton.disabled = false;
            submitButton.textContent = submitName;
        })
        .then(()=>{
            submitButton.textContent = submitted;
            setTimeout(()=>{location.replace("/dashboard/auction-sales/manage");},500);
        });
    });
}

export class ManageAuctionSalesWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.getData(
            "get_auction_sales",
            {},
        ).then((data)=>{
            this.displayAuctionSales(data["auction_sales"]);
        });


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

        if (this.frame.hasAttribute("data-widget-manage-auction-sales-new")) {
            manageAuctionSale();
        }
    }

    /**
     * 
     * @param {Object[]} auctionSales The auction sales to display
     * @param {integer} auctionSales[].id The ID of the auction sale
     * @param {string} auctionSales[].name The name of the auction sale
     * @param {string} auctionSales[].at The epoch of when the sale occurs
     * @param {boolean|number} auctionSales[].published Whether the auction sale is published
     */
    displayAuctionSales(auctionSales) {
        this.table = new Table();

        this.table.setHeader(["Name", "At", "Published", "Options"]);

        for (const auctionSale of auctionSales) {
            let optionsGroup = document.createElement("div");
            let controls = new ShortControls(optionsGroup);
            controls.addButton(
                "Edit",
                "btn btn-sm btn-info",
                ()=>{manageAuctionSale(auctionSale);}
            );
            this.table.addRow([
                auctionSale.name,
                formatDateTime(auctionSale.at),
                auctionSale.published ? "Yes" : "No",
                optionsGroup
            ]);
        }

        this.table.attach(this.frame);

        if (auctionSales.length == 0) {
            let centerText = document.createElement("div");
            centerText.style.textAlign = "center";
            centerText.textContent = "No auction sales owned by this account";
            this.frame.append(centerText);
        }
    }
}
