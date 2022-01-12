import { Widget } from '../../widget.mjs';

export class SourceSummaryWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {

        this.display = this.frame.getAttribute("data-widget-display");
        if(this.display == "animals-with-data") {
            this.request = {
                type: "matches_by_account",
                params: {
                    animals_with_data: true
                }
            }
        }
        else {
            this.request = {
                type: "matches_by_account",
                params: {
                    all_matches: true,
                    params: {
                        types: ["Sighting"]
                    }

                }
            }
        }

        this.getData(
            "data_request",
            {
                request: this.request
            }
        ).then((data) => {
            this.match_rows = data.result.matches;
        }).then(() => {
            this.frame.innerHTML = "";
            this.makeAnimals();
            this.makeTable();
        });
    }

    makeAnimals() {
        this.animals = {};

        for (const match_row of this.match_rows) {
            if (!(match_row.eid in this.animals)) {
                this.animals[match_row.eid] = {
                    "visual_id": "(no data)"
                };
            }
            if(match_row.visual_id != null)
                this.animals[match_row.eid]["visual_id"] = match_row.visual_id;
        }

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
        const headers = ["EID", "Visual ID", "Options"]
        for (const headerText of headers) {
            let th = document.createElement("th");
            th.textContent = headerText;
            this.mainTableHeadRow0.appendChild(th);
        }

        // Body
        //
        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        for (const eid in this.animals) {
            let rowTag = document.createElement("tr");
            this.mainTableBody.appendChild(rowTag);

            let rowPreformat = this.animals[eid];

            let row = [];

            row.push(eid);
            row.push(rowPreformat["visual_id"]);

            for (const value of row) {
                let td = document.createElement("td");
                td.textContent = value;
                rowTag.appendChild(td);
            }

            let tdOptions = document.createElement("td");
            rowTag.appendChild(tdOptions);

            let button = document.createElement("a");
            button.className = "btn btn-outline-secondary btn-sm";
            button.setAttribute("href", "/dashboard/animals/" + eid);
            button.textContent = "View";
            tdOptions.appendChild(button);
        }

        // Put HTML in frame

        this.frame.appendChild(this.divTableResponsive);
        $(this.mainTable).DataTable();
    }
}
