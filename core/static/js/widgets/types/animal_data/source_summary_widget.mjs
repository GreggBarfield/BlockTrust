import { Widget } from '../../widget.mjs';
import { spinner } from '../../../ui/spinner.mjs';

export class SourceSummaryWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType(accountId=undefined) {
        this.display = this.frame.getAttribute("data-widget-display");
        if(this.display == "animals-with-data") {
            this.request = {
                type: "matches_by_account",
                params: {
                    sighted_animals: true,
                    account_id: accountId
                }
            }
            this.sightedAnimals = true;
        }
        else {
            this.request = {
                type: "matches_by_account",
                params: {
                    all_matches: true,
                    types: ["Sighting"],
                    account_id: accountId   
                }
            }
        }

        this.getData(
            "data_request",
            {
                request: this.request
            }
        ).then((data) => {
            let matchRows = data.result.matches;
            this.frame.innerHTML = "";
            if(this.frame.getAttribute("data-widget-refresh-id")) {
                this.refreshButton = document.createElement("button");
                this.refreshButton.className = "btn btn-outline-primary btn-sm d-none";
                this.refreshButton.id = this.frame.getAttribute("data-widget-refresh-id");
                this.refreshButton.innerHTML = "Refresh";
                this.refreshButton.onclick = () => {
                    this.frame.innerHTML = spinner;
                    this.initType(this.frame.getAttribute("data-widget-account-id"));
                }
                this.frame.appendChild(this.refreshButton);
            }

            if (this.sightedAnimals && matchRows.length){
                this.downloadButton = document.createElement("button");
                this.downloadButton.className = "btn btn-outline-primary btn-sm float-right";
                this.downloadButton.innerHTML = "<i class='fa fa-download'></i> Download";
                
                let exportTable = this.makeExportTable(matchRows);
                this.downloadButton.onclick = () => {
                    let csvContent = "data:text/csv;charset=utf-8," + exportTable.map(e => e.join(",")).join("\n");
                    let encodedUri = encodeURI(csvContent);
                    //Having text color issues on mouse hover when making this.downloadButton a hyperlink tag. So below workaround is used
                    let temporaryLink = document.createElement("a");
                    temporaryLink.setAttribute("href", encodedUri);
                    let fileName = "Sighted Calves";
                    let accountName = this.frame.getAttribute("data-widget-account-name");
                    fileName = accountName? `${fileName} for ${accountName}.csv` : `${fileName}.csv`
                    temporaryLink.setAttribute("download", fileName);
                    temporaryLink.click();
                } 
                this.frame.appendChild(this.downloadButton)
            }
            this.makeDisplayTable(matchRows);
        });
    }

    makeExportTable = (matchRows) => {
        let exportTable = [["EID", "VISUAL ID", "QUALITY GRADE", "YIELD GRADE", "CREEP FEED", "FIRST 14 DAY FEED METHOD", 
            "SECOND 31 DAY FEED METHOD", "HOT WEIGHT", "MARKETING DATE", "MARKETING METHOD NAME", "NUMBER OF CALVES", "SALE LOCATION", "WEAN DATE", 
            "WEAN WEIGHT", "WEANING STRATEGY"]];

        for(const match_row of matchRows){
            let row = [match_row["eid"], match_row["visual_id"], match_row["quality_grade"], match_row["yield_grade"]]

            let saleLocation = match_row["sale_location"] ? '\"' + match_row["sale_location"] + '\"' : ""
            row.push([match_row["creep_feed"] ?? "", match_row["first_14_day_feed_method"] ?? "", match_row["second_31_day_feed_method"] ?? "", 
                match_row["hot_weight"] ?? "", match_row["marketing_date"] ?? "", match_row["marketing_method_name"] ?? "", 
                match_row["number_of_calves"] ?? "", saleLocation, match_row["wean_date"] ?? "", match_row["wean_weight"] ?? "", 
                match_row["weaning_strategy"]  ?? ""])

            exportTable.push(row)
        }
        return exportTable;
    }

    makeAnimals(matchRows, isNameAvailable) {
        let animals = {};

        for (const match_row of matchRows) {
            animals[match_row.eid] = {}
            animals[match_row.eid]["visual_id"] = match_row.visual_id? match_row.visual_id : "(no data)";
            if (isNameAvailable) {
                animals[match_row.eid]["name"] = match_row.name? match_row.name : "(no data)";
            }
        }
        return animals;
    }

    makeDisplayTable(matchRows) {

        this.divTableResponsive = document.createElement("div");
        this.divTableResponsive.className = "dt-responsive table-responsive";

        this.mainTable = document.createElement("table");
        this.mainTable.className = "table table-striped table-bordered nowrap";
        this.divTableResponsive.appendChild(this.mainTable);

        if (matchRows.length){
            // Header
            this.mainTableHead = document.createElement("thead");
            this.mainTable.appendChild(this.mainTableHead);

            this.mainTableHeadRow0 = document.createElement("tr");
            this.mainTableHead.appendChild(this.mainTableHeadRow0);

            const isNameAvailable = matchRows.length? "name" in matchRows[0]: false;
            const headers = isNameAvailable? ["EID", "Ranch", "Visual ID", "Options"] : ["EID", "Visual ID", "Options"]
            for (const headerText of headers) {
                let th = document.createElement("th");
                th.textContent = headerText;
                this.mainTableHeadRow0.appendChild(th);
            }

            // Body
            this.mainTableBody = document.createElement("tbody");
            this.mainTable.appendChild(this.mainTableBody);
            let animals = this.makeAnimals(matchRows, isNameAvailable);
            for (const eid in animals) {
                let rowTag = document.createElement("tr");
                this.mainTableBody.appendChild(rowTag);

                let rowPreformat = animals[eid];

                let row = [];

                row.push(eid);
                if(isNameAvailable) {
                    row.push(rowPreformat["name"]);
                }
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
                button.setAttribute("href", this.frame.getAttribute("data-widget-animal-URL") + eid);
                button.textContent = "View";
                tdOptions.appendChild(button);
            }
            $(this.mainTable).DataTable();
        }
        else {
            this.mainTableBody = document.createElement("tbody");
            let rowTag = document.createElement("tr");
            this.mainTableBody.appendChild(rowTag);
            let td = document.createElement("td");
            td.textContent = "Nothing to show here";
            td.classList.add("text-center")
            rowTag.appendChild(td);
            this.mainTableBody.appendChild(rowTag);
            this.mainTable.appendChild(this.mainTableBody);
        }

        // Put HTML in frame    
        this.frame.appendChild(this.divTableResponsive);
    }
}
