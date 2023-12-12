import { Widget } from '../../widget.mjs';
import { SalesGroupsCommonForm } from './sales_group_common_form.mjs';

export class CreateSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() =>{
        this.frame.innerHTML = "";
        this.postRoute = this.frame.getAttribute("data-widget-form-post-route");
        this.auctionMarkets = this.processAuctionMarketsData(JSON.parse(this.frame.getAttribute("data-widget-auction-markets")));
        this.preSelectAuctionMarket = this.frame.getAttribute("data-widget-pre-select-auction-market").toLowerCase();
        this.preSelectedAuctionMarketId = this.frame.getAttribute("data-widget-pre-selected-auction-market-id");
        this.fieldIdsToNames = JSON.parse(this.frame.getAttribute("data-widget-sales-group-field-ids-to-names"));
        this.salesGroupFieldsValues = this.processSalesGroupFieldsValues(JSON.parse(this.frame.getAttribute("data-widget-sales-group-fields-values")));
        this.makeForm();
    }

    processAuctionMarketsData(auctionMarkets){
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
            "pregnancy_status": []
        }
        for(const fieldData of salesGroupFieldsValues){
            let fieldId = fieldData.field_id;
            let fieldName = this.fieldIdsToNames[fieldId];
            processedSalesGroupFieldsValues[fieldName].push(fieldData.value);
        }
        return processedSalesGroupFieldsValues;
    }

    makeForm(){

    let that = this;
    let card = document.createElement("div");
    card.className = "card";

    let createGroupName = document.createElement("h5");
    createGroupName.className = "mt-2 font-weight-bold p-1 text-center";

    createGroupName.textContent = "Create New Sales Group ";

    let cardHeader = document.createElement("div");
    cardHeader.className = "card-header form-group d-flex justify-content-between p-1";
    cardHeader.append(createGroupName);
    card.append(cardHeader)

    let cardBody = document.createElement("div");
    cardBody.className = "card-body";
    card.append(cardBody);
    this.frame.append(card)
    // Widget containing common input fields used in sales group form
    let salesGroupForm = new SalesGroupsCommonForm(null, this.auctionMarkets, this.postRoute, this.salesGroupFieldsValues, this.preSelectAuctionMarket, this.preSelectedAuctionMarketId);
    cardBody.append(salesGroupForm);
    }
}