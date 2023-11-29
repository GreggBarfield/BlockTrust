import { CreateAuctionMarketWidget } from "../../../js/widgets/types/sales_groups/create_auction_market_widget.mjs";

document.addEventListener('DOMContentLoaded', function () {
    $('#auction-markets-table').DataTable({pageLength:50});
    let createNewAuctionMarketButton = document.getElementById("create-new-auction-market");
    createNewAuctionMarketButton.onclick = () =>{
        console.log("Clicked");
        let widget = new CreateAuctionMarketWidget();
        widget.init();
    }
});