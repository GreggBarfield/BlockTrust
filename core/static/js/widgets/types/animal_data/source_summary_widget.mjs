import { Widget } from '../../widget.mjs';

export class SourceSummaryWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {

        // TODO: This is a bad data request, optimize later
        Promise.all([
            this.getData(
                "data_request",
                {
                    request: {
                        type: "matches_by_account",
                        params: {
                            types: ["Weaned", "Sighting"]
                        }
                    }
                }
            ).then((data) => {
                console.log("Match row sourcing: ", data.result.matches);
                this.match_rows = data.result.matches;
            }),

            this.getData(
                "direct/match_types_by_name",
                {}
            ).then((data) => {
                this.match_types_by_name = data.match_types_by_name;
            }),

        ]).then(() => {
            this.frame.innerHTML = "";
            this.makeAnimals();
            this.makeTable();
        });
    }

    formatDate(epoch) {
        if (epoch == null || epoch <= 0)
            return "--";
        let d = new Date(parseInt(epoch) * 1000);
        return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
    }

    makeAnimals() {
        this.animals = {};

        for (const match_row of this.match_rows) {
            if (!(match_row.eid in this.animals)) {
                this.animals[match_row.eid] = {
                    "weaned": "(no data)",
                    "sightings": "(no data)"
                };
            }
            let animal = this.animals[match_row.eid];
            if (match_row.type == this.match_types_by_name["Weaned"]) {
                animal["weaned"] = this.formatDate(match_row.time);
            }
            else if (match_row.type == this.match_types_by_name["Sighting"]) {
                if (animal["sightings"] == "(no data)") {
                    animal["sightings"] = [];
                }
                animal["sightings"].push(this.formatDate(match_row.time));
            }
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
        const headers = ["EID", "Weaned", "Sightings", "Options"];
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
            row.push(rowPreformat["weaned"]);

            {
                let temp = "";
                let sightings = rowPreformat["sightings"];
                if (typeof(sightings) == typeof("")) {
                    temp = sightings;
                }
                else {
                    temp = sightings.join(", ");
                }
                row.push(temp);
            }

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
