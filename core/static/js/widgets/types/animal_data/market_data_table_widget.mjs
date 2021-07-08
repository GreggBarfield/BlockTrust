import { Widget } from '../../widget.mjs';

export class MarketDataTableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.count = 0;
        this.getData(
            "get_market_data",
            {}
        ).then((data) => {
            this.match_rows = data.market_data;
            console.log(this.match_rows);
            this.frame.innerHTML = "";
            this.makeTable();
        });
    }

    makeTable() {
        this.divTableResponsive = document.createElement("div");
        this.divTableResponsive.className = "dt-responsive table-responsive";

        this.mainTable = document.createElement("table");
        this.mainTable.className = "table table-striped table-bordered nowrap";
        this.divTableResponsive.appendChild(this.mainTable);

        // Header

        this.mainTableHead = document.createElement("thead");
        this.mainTable.appendChild(this.mainTableHead);

        this.mainTableHeadRow0 = document.createElement("tr");
        this.mainTableHead.appendChild(this.mainTableHeadRow0);
        const headers = Object.keys(this.match_rows[0]);
        for (const headerText of headers) {
            let th = document.createElement("th");
            th.textContent = headerText;
            this.mainTableHeadRow0.appendChild(th);
        }

        // Body

        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        for (const row in this.match_rows) {
            let rowTag = document.createElement("tr");
            this.mainTableBody.appendChild(rowTag);

            for (const item in this.match_rows[row]) {
                let td = document.createElement("td");
                rowTag.append(td);
                td.textContent = this.match_rows[row][item];
            }
        }

        // Put HTML in frame
        this.frame.appendChild(this.divTableResponsive);
        $(this.mainTable).DataTable();
    }
}