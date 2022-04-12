import { Widget } from '../../widget.mjs';
import { SalesGroupsCommonForm } from './sales_group_common_form.mjs';

export class CreateNewSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.postRoute = "/widgets/data/create_sales_group";
    this.getData(
        "auction_markets"
    ).then((data) => {
        this.auctionMarketsData = this.processAuctionMarketsData(data.auction_markets);
        this.makeForm();
    });

    this.onSomeDataLoaded(function () {
        this.frame.innerHTML = "";
    });
    }

    processAuctionMarketsData(auctionMarkets){
        let selectData=[];
        selectData.push("None");
        for(const auctionMarket of auctionMarkets){
            let optionText = auctionMarket.name+", "+auctionMarket.city+", "+auctionMarket.state;
            selectData.push(optionText);
        }
        return selectData;
    }

    makeForm(){

    let that = this;
    let card = document.createElement("div");
    card.className = "card";

    let createGroupName = document.createElement("h5");
    createGroupName.className = "mt-2";
    createGroupName.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;"

    createGroupName.textContent = "Create New Sales Group ";

    let cardHeader = document.createElement("div");
    cardHeader.className = "card-header form-group d-flex justify-content-between";
    cardHeader.style = "padding:5px;padding-left: 15px;"
    cardHeader.append(createGroupName);
    card.append(cardHeader)

    let cardBody = document.createElement("div");
    cardBody.className = "card-body";
    card.append(cardBody);
    this.frame.append(card)
    // Widget containing common input fields used in sales group form
    let salesGroupForm = new SalesGroupsCommonForm(null, this.auctionMarketsData, this.postRoute);
    cardBody.append(salesGroupForm);
    }
}