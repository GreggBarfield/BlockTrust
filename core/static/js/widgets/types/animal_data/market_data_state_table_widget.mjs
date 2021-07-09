import { Widget } from '../../widget.mjs';

export class MarketDataStateTableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.getData(
            "get_market_state_data",
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
        const headers = ["Market State", "Options"];
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

            let tdOptions = document.createElement("td");
            rowTag.appendChild(tdOptions);

            let button = document.createElement("a");
            button.className = "btn btn-outline-secondary btn-sm";
            let state = this.match_rows[row]['market_location_state'];
            button.setAttribute("href", "/dashboard/data/market/" + state);
            button.textContent = "View";
            tdOptions.appendChild(button);
        }

        // Put HTML in frame
        this.frame.appendChild(this.divTableResponsive);
        $(this.mainTable).DataTable();
    }
}