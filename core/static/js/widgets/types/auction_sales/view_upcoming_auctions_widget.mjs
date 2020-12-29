import { Widget } from '../../widget.mjs';
import { Table } from '../../../core/table.mjs';
import { formatDateTime } from '../../../core/time.mjs';

export class ViewUpcomingAuctionsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.getData(
            "get_auction_sales",
            {},
        ).then((data)=>{
            this._displayAuctionSales(data["auction_sales"]);
        });


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

        if (this.frame.hasAttribute("data-widget-manage-auction-sales-new")) {
            manageAuctionSale();
        }
    }

    /**
     * Displays the auction sales provided.
     * 
     * @param {Object[]} auctionSales The auction sales to display
     * @param {string} auctionSales[].name The name of the auction sale
     * @param {string} auctionSales[].at The epoch of when the sale occurs
     * @param {boolean|number} auctionSales[].published Whether the auction sale is published
     */
    _displayAuctionSales(auctionSales) {
        this.table = new Table();

        let currentTime = Date.now() / 1000;

        let filteredAuctionSales = auctionSales.filter(
            auctionSale => auctionSale.at >= currentTime
        );

        this.table.setHeader(["Name", "At", "Published"]);

        for (const auctionSale of filteredAuctionSales) {
            this.table.addRow([
                auctionSale.name,
                formatDateTime(auctionSale.at),
                auctionSale.published ? "Yes" : "No"
            ]);
        }

        this.table.attach(this.frame);

        if (filteredAuctionSales.length == 0) {
            let centerText = document.createElement("div");
            centerText.style.textAlign = "center";
            centerText.textContent = "No upcoming auction sales";
            this.frame.append(centerText);
        }
    }
}
