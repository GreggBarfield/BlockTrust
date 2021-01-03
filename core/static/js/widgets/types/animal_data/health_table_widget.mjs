import { Widget } from '../../widget.mjs';

export class HealthTableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.animal = parseInt(this.frame.getAttribute("data-widget-animal"));

        this.getData(
            "data_request",
            {
                request: {
                    type: 'matches_by_eids',
                    params: {
                        eids: [this.animal],
                        ljoin_account_links: true,
                        types: ["Medical"]
                    }
                }
            }
        ).then((data) => {
            this.match_rows = data.result.matches;
            this.frame.innerHTML = "";
            this.prepData();
            this.makeTable();
        });
    }

    formatDate(epoch) {
        if (epoch == null || epoch <= 0)
            return "--";
        let d = new Date(parseInt(epoch) * 1000);
        return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
    }

    prepData() {

        this.headers = ["date", "symptom", "diagnosis", "product"];
        this.rows = [];

        for (const match_row of this.match_rows) {
            let data_obj = match_row["data"];
            data_obj.date = this.formatDate(match_row.time);
            let row = [];
            for (const header in data_obj) {
                if (this.headers.indexOf(header) == -1) {
                    this.headers.push(header);
                }
            }
            for (const header of this.headers) {
                if (header in data_obj) {
                    row.push(data_obj[header]);
                }
                else {
                    row.push("");
                }
            }
            this.rows.push(row);
        }
    }

    makeTable() {

        this.divTableResponsive = document.createElement("div");
        this.divTableResponsive.className = "table-responsive";

        this.mainTable = document.createElement("table");
        this.mainTable.className = "table table-xs";
        this.divTableResponsive.appendChild(this.mainTable);

        // Header

        this.mainTableHead = document.createElement("thead");
        this.mainTableHead.className = "thead-light";
        this.mainTable.appendChild(this.mainTableHead);

        this.mainTableHeadRow0 = document.createElement("tr");
        this.mainTableHead.appendChild(this.mainTableHeadRow0);

        for (const header of this.headers) {
            let th = document.createElement("th");
            th.textContent = header;
            this.mainTableHeadRow0.appendChild(th);
        }

        // Body

        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        if (this.rows.length == 0) {
            let noData = document.createElement("div");
            noData.style = "text-align:center;padding:10px;width:100%;";
            noData.textContent = "No health data is available for this animal.";
            this.divTableResponsive.append(noData);
        }
        else {
            for (const row of this.rows) {
                let tr = document.createElement("tr");
                this.mainTableBody.append(tr);

                for (const cell of row) {
                    let td = document.createElement("td");
                    tr.append(td);
                    td.textContent = cell;
                }
            }
        }

        // Put HTML in frame

        this.frame.appendChild(this.divTableResponsive);
    }
}