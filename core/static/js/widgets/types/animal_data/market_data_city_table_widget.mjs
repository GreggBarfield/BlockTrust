import { Widget } from '../../widget.mjs';

export class MarketDataCityTableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.state = this.frame.getAttribute('state');

        this.getData(
            "get_market_city_data/" + this.state,
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
        const headers = ["Market City", "ID", "Options"];
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
            let citySlug = this.match_rows[row]['slug_id'];
            button.setAttribute("href", "/dashboard/data/market/" + 
                this.state + "/" + citySlug.toString());
            button.textContent = "View";
            tdOptions.appendChild(button);
        }

        // Put HTML in frame
        this.frame.appendChild(this.divTableResponsive);
        $(this.mainTable).DataTable();
    }
}