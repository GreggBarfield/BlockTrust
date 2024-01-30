import { Widget } from '../../widget.mjs';
import { SalesGroupsCommonForm } from './sales_group_common_form.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';
import { printContainer } from '../../utilities/general_utilities.mjs';

export class EditSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.qrSource = this.frame.getAttribute("data-widget-qr-src");
        this.shareableLink = this.frame.getAttribute("data-widget-shareable-link");
        this.formElements = {};
        this.postRoute = this.frame.getAttribute("data-widget-form-post-route");
        this.fieldIdsToNames = JSON.parse(this.frame.getAttribute("data-widget-sales-group-field-ids-to-names"));
        this.salesGroupFieldsValues = this.processSalesGroupFieldsValues(JSON.parse(this.frame.getAttribute("data-widget-sales-group-fields-values")));
        this.accountId = this.frame.getAttribute("data-widget-account-id");
        this.carcassDataAvailable = true;

        const getSalesGroupData = this.getData(
            "sales_group",
            {
                sales_group: this.salesGroupID
            }
        ).then((data) => {
            this.data = data;  
        });
        const getAuctionMarketsData = this.getData(
            "auction_markets"
        ).then((data) => {
            this.auctionMarketsData = this.processAuctionMarketsData(data.auction_markets);
        });
        const getAccountUSDAQualityGradeDistribution = this.getData(
            "get_count_distribution_for_account", {account_id: parseInt(this.accountId)}
        ).then((data) => {
            if("result" in data && "count_distribution" in data.result){
                let accountUSDAQualityGradeDistribution = data.result.count_distribution;
                if(accountUSDAQualityGradeDistribution.length == 0){
                    this.carcassDataAvailable = false;
                }
            }
            else{
                this.carcassDataAvailable = false;
            }
        });
        Promise.all([
            getSalesGroupData, getAuctionMarketsData, getAccountUSDAQualityGradeDistribution
        ]).then(()=> {
            this.makeForm();
        })
        
        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });
    }

    createPrintFlyerButton = () =>{
        let printFlyerButton = document.createElement("button");
        printFlyerButton.className = "btn btn-outline-primary btn-sm";
        printFlyerButton.innerHTML = "Print Flyer";
        let salesGroupViewerContainer = document.createElement("div");
        new SalesGroupViewer(this.data, salesGroupViewerContainer);
        printFlyerButton.onclick =  () => {
            printContainer(salesGroupViewerContainer);
        };
        return printFlyerButton;
    }

    processAuctionMarketsData = (auctionMarkets) =>{
        let selectData={};
        selectData[0] = "None";
        for(const auctionMarket of auctionMarkets){
            let optionText = auctionMarket.name+", "+auctionMarket.city+", "+auctionMarket.state;
            selectData[auctionMarket.id] = optionText;
        }
        return selectData;
    }

    processSalesGroupFieldsValues = (salesGroupFieldsValues) =>{
        let processedSalesGroupFieldsValues = {
            "vaccination": [],
            "genetics_verification": [],
            "comingled_status": [],
            "creep_feed": [],
            "weaned": [],
            "breed": [],
            "pvp_program": [],
            "preconditioning_program": [],
            "frame": [],
            "muscling": [],
            "horn": [],
            "delivery_location_type": [],
            "castrated": [],
            "feeding_program": [],
            "implant": [],
            "category": [],
            "pregnancy_status": [],
            "breed_program_certification_co": [],
            "certified_through": []
        }
        for(const fieldData of salesGroupFieldsValues){
            let fieldId = fieldData.field_id;
            let fieldName = this.fieldIdsToNames[fieldId];
            processedSalesGroupFieldsValues[fieldName].push(fieldData.value);
        }
        return processedSalesGroupFieldsValues;
    }
    
    makeForm() {

        // Sections
        // Card header needs to be custom based on function
        let that = this;
        let card = document.createElement("div");
        card.className = "card";

        let editGroupName = document.createElement("h5");
        editGroupName.className = "mt-2 font-weight-bold p-1 text-center";
        editGroupName.textContent = `Edit Sales Group ${this.data.id}: ${this.data.group_name}`;

        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between p-1";
        cardHeader.append(editGroupName);

        let btnQrDiv = document.createElement("div");
        btnQrDiv.className = "d-flex align-items-end flex-row";

        this.printFlyerButton = this.createPrintFlyerButton();
        btnQrDiv.appendChild(this.printFlyerButton);

        let copyLinkButton = document.createElement("button");
        copyLinkButton.className = "btn btn-outline-primary btn-sm";
        copyLinkButton.innerHTML = "Copy Link";
        copyLinkButton.onclick = function () {
            navigator.clipboard.writeText(that.shareableLink);
        };
        btnQrDiv.append(copyLinkButton);

        let qrImg = document.createElement("img");
        qrImg.src = this.qrSource;
        qrImg.id = "sales_group_qrcode"
        btnQrDiv.append(qrImg);

        cardHeader.append(btnQrDiv);
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);
        // Setup
        this.frame.append(card);
        // Widget containing common input fields used in sales group form
        let salesGroupForm = new SalesGroupsCommonForm(this.data, this.auctionMarketsData, this.postRoute, this.salesGroupFieldsValues, this.carcassDataAvailable);
        cardBody.append(salesGroupForm);
    }

    showError(error) {
        this.internalErrorMessage.style.display = "block";
        this.internalErrorMessage.textContent = error;
    }
}

/**
 * TODO: Below code used to add auction sale dropdown which is retained in case needed in future.
 * Presents a selector for auction sale.
 */


// class SelectAuctionSaleFormGroup extends FormGroup {

//     /**
//      * Constructs SelectAuctionSale.
//      * 
//      * @param {Node} attachTo Where to place DOM elements
//      * @param {number|null} auctionSaleID The ID for the auction sale or null
//      * @param {string|null} auctionSaleName The auction sale name or null
//      */
//     constructor(attachTo, auctionSaleID, auctionSaleName) {
//         super(attachTo, "Select auction sale (i/a):");
        
//         this._select = document.createElement("select");
//         this._select.id = this._input_id;
//         this._select.className = "select2-hidden-accessible";
//         this._form_group.append(this._select);

//         if (auctionSaleID !== null) {
//             let option = document.createElement("option");
//             option.value = auctionSaleID;
//             option.textContent = auctionSaleName;
//             this._select.append(option);
//         }

//         $(this._select).select2({
//             ajax: {
//                 url: "/widgets/data/search_auction_sales",
//                 data: (params) => {
//                     return JSON.stringify({
//                         "term": params.term
//                     })
//                 },
//                 contentType: 'application/json',
//                 method: "POST",
//                 delay: 250,
//                 processResults: function (data) {
//                     let results = [];
//                     for (const auction_sale of data.auction_sales) {
//                         results.push({
//                             id: auction_sale.id,
//                             text: (
//                                 auction_sale.name + " (" +
//                                 auction_sale.account_name + ")"
//                             )
//                         });
//                     }
//                     return { results };
//                 },
//             },
//             placeholder: 'Type here to search...',
//             minimumInputLength: 3,
//             allowClear: true
//         });
//     }

//     /**
//      * Gets the ID of the auction sale selected.
//      */
//     getID() {
//         if (this._select.value === null || this._select.value === "") {
//             return null;
//         }
//         return parseInt(this._select.value);
//     }
// }
