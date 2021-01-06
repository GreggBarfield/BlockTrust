import { Widget } from '../../widget.mjs';

export class TableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.account = parseInt(this.frame.getAttribute("data-widget-account"));
        this.accountName = this.frame.getAttribute("data-widget-account-name");

        // TODO: This is a bad data request, optimize later
        this.getData(
            "data_request",
            {
                request: {
                    type: 'matches_by_account',
                    params: {
                        account: this.account,
                        types: ["Weaned", "Sighting"]
                    }
                }
            }
        ).then((data) => {
            this.match_rows = data.result.matches;
            this.displayMatches();
            this.displayAccount();
        });

        this.getData(
            "direct/match_types_by_name",
            {}
        ).then((data) => {
            this.match_types_by_name = data.match_types_by_name;
            this.displayAccount();
        });
        
        this.getData(
            "data_request",
            {
                request: {
                    type: 'count_distribution_global',
                    params: {
                        match_type: 'USDA Yield Grade'
                    }
                }
            }
        ).then((data) => {
            this.global_usda_yield_grade_distribution = data.result.count_distribution;
            this.displayGlobal();
        });
            
        this.getData(
            "data_request",
            {
                request: {
                    type: 'count_distribution_global',
                    params: {
                        match_type: 'USDA Quality Grade'
                    }
                }
            }
        ).then((data) => {
            this.global_usda_quality_grade_distribution = data.result.count_distribution;
            this.displayGlobal();
        });
            
        this.getData(
            "data_request",
            {
                request: {
                    type: 'count_distribution',
                    params: {
                        match_type: 'USDA Yield Grade',
                        account: null
                    }
                }
            }
        ).then((data) => {
            this.account_usda_yield_grade_distribution = data.result.count_distribution;
            this.displayAccount();
        });
            
        this.getData(
            "data_request",
            {
                request: {
                    type: 'count_distribution',
                    params: {
                        match_type: 'USDA Quality Grade',
                        account: null
                    }
                }
            }
        ).then((data) => {
            this.account_usda_quality_grade_distribution = data.result.count_distribution;
            this.displayAccount();
        });
            
        this.getData(
            "data_request",
            {
                request: {
                    type: 'count_eid_distinct',
                    params: {}
                }
            },
        ).then((data) => {
            this.count_eid_distinct = data.result.count_eid_distinct;
            this.displayGlobal();
        });


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
            this.makeTable();
        });

    }

    displayMatches() {
        let research = {};

        for (const match of this.match_rows) {
            if (!(match["eid"] in research)) {
                research[match["eid"]] = 1;
            }
        }

        let totalCalves = 0;

        for (const animal_i in research) {
            totalCalves += 1;
        }

        this.account_total_distinct = totalCalves;
    }

    displayGlobal() {
        if ('count_eid_distinct' in this) {
            this.tableSectionSightingsRows[1].children[2].textContent = this.count_eid_distinct;
        }
        if ('global_usda_yield_grade_distribution' in this) {
            let total = 0;
            let yg = [0,0,0,0,0,0];
            for (const r of this.global_usda_yield_grade_distribution) {
                total += r.count;
                if (r.data >= 1 && r.data <= 5) {
                    yg[5-r.data]+=r.count;
                }
                else {
                    yg[5]+=r.count;
                }
            }
            for (const i in yg) {
                let v = "n/a";
                if (total > 0) {
                    v = Math.round(100 * yg[i] / total) + "%";
                }
                this.tableSectionYieldRows[1 + parseInt(i)].children[2].textContent = v;
            }
            this.global_total_available = total;
        }
        if ('global_usda_quality_grade_distribution' in this) {
            let total = 0;
            let yg = [0,0,0,0];
            for (const r of this.global_usda_quality_grade_distribution) {
                total += r.count;
                if (r.data == "Prime") {
                    yg[0]+=r.count;
                }
                else if (r.data == "Choice") {
                    yg[1]+=r.count;
                }
                else if (r.data == "Select or Lower") {
                    yg[2]+=r.count;
                }
                else {
                    yg[3]+=r.count;
                }
            }
            for (const i in yg) {
                let v = "n/a";
                if (total > 0) {
                    v = Math.round(100 * yg[i] / total) + "%";
                }
                this.tableSectionQualityRows[1 + parseInt(i)].children[2].textContent = v;
            }
            this.global_total_available = total;
        }
        if ('global_total_available' in this && 'count_eid_distinct' in this) {
            this.tableSectionSightingsRows[2].children[2].textContent = this.global_total_available;
            let v = "n/a";
            if (this.count_eid_distinct != 0) {
                v = Math.round(100 * this.global_total_available / this.count_eid_distinct) + "%";
            }
            this.tableSectionSightingsRows[3].children[2].textContent = v;
        }
    }

    displayAccount() {
        if ('account_usda_yield_grade_distribution' in this) {
            let total = 0;
            let yg = [0,0,0,0,0,0];
            for (const r of this.account_usda_yield_grade_distribution) {
                total += r.count;
                if (r.data >= 1 && r.data <= 5) {
                    yg[5-r.data]+=r.count;
                }
                else {
                    yg[5]+=r.count;
                }
            }
            for (const i in yg) {
                let v = "n/a";
                if (total > 0) {
                    v = Math.round(100 * yg[i] / total) + "%";
                }
                this.tableSectionYieldRows[1 + parseInt(i)].children[1].textContent = v;
            }
            this.account_total_available = total;
        }
        if ('account_usda_quality_grade_distribution' in this) {
            let total = 0;
            let yg = [0,0,0,0];
            for (const r of this.account_usda_quality_grade_distribution) {
                total += r.count;
                if (r.data == "Prime") {
                    yg[0]+=r.count;
                }
                else if (r.data == "Choice") {
                    yg[1]+=r.count;
                }
                else if (r.data == "Select or Lower") {
                    yg[2]+=r.count;
                }
                else {
                    yg[3]+=r.count;
                }
            }
            for (const i in yg) {
                let v = "n/a";
                if (total > 0) {
                    v = Math.round(100 * yg[i] / total) + "%";
                }
                this.tableSectionQualityRows[1 + parseInt(i)].children[1].textContent = v;
            }
            this.account_total_available = total;
        }

        if ('tableSectionSightingsRows' in this && 'account_total_distinct' in this) {
            this.tableSectionSightingsRows[1].children[1].textContent = this.account_total_distinct;
        }
        if ('account_total_available' in this) {
            this.tableSectionSightingsRows[2].children[1].textContent = this.account_total_available;
        }
        if ('account_total_available' in this && 'account_total_distinct' in this) {
            let v = "n/a";
            if (this.account_total_distinct != 0) {
                v = Math.round(100 * this.account_total_available / this.account_total_distinct) + "%";
            }
            this.tableSectionSightingsRows[3].children[1].textContent = v;
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
        this.mainTable.appendChild(this.mainTableHead);

        this.mainTableHeadRow0 = document.createElement("tr");
        this.mainTableHead.appendChild(this.mainTableHeadRow0);

        this.mainTableHeadRow0TH0 = document.createElement("th");
        this.mainTableHeadRow0TH0.textContent = "";
        this.mainTableHeadRow0.appendChild(this.mainTableHeadRow0TH0);

        this.mainTableHeadRow0TH1 = document.createElement("th");
        this.mainTableHeadRow0TH1.textContent = this.accountName;
        this.mainTableHeadRow0.appendChild(this.mainTableHeadRow0TH1);

        this.mainTableHeadRow0TH2 = document.createElement("th");
        this.mainTableHeadRow0TH2.textContent = "Global Benchmark";
        this.mainTableHeadRow0.appendChild(this.mainTableHeadRow0TH2);

        // Body

        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        function generateSection(title, rowTitles, to) {
            let allRows = [];
            let headRow = document.createElement("tr");
            allRows.push(headRow);

            let headRowTitle = document.createElement("td");
            headRowTitle.style = "font-weight:bold;";
            headRow.appendChild(headRowTitle);

            headRow.appendChild(document.createElement("td"));
            headRow.appendChild(document.createElement("td"));

            let headRowTitleDiv = document.createElement("div");
            headRowTitleDiv.style = "overflow-x:visible;width:0px;";
            headRowTitleDiv.textContent = title;
            headRowTitle.appendChild(headRowTitleDiv);

            for (const rowTitle of rowTitles) {
                let bodyRow = document.createElement("tr");
                allRows.push(bodyRow);

                for (let i = 0; i < 3; i++) {
                    let bodyTd = document.createElement("td");
                    bodyRow.appendChild(bodyTd);
                    if (i == 0) {
                        bodyTd.textContent = rowTitle;
                    }
                    else {
                        bodyTd.style = "text-align:center;";
                        /*bodyTd.innerHTML = '<div class="spinner-grow spinner-grow-sm" role="status">\
                        <span class="sr-only">Loading...</span>\
                    </div>';*/
                        bodyTd.innerHTML = '<div class="spinner-border spinner-border-sm" role="status">\
                        <span class="sr-only">Loading...</span>\
                    </div>';
                    }
                }
            }

            for (const row of allRows) {
                to.append(row);
            }

            return allRows;
        }

        this.tableSectionSightingsRows = generateSection("Sightings Summary", ["Total Calves", "Total Available", "% Available"], this.mainTableBody);
        this.tableSectionQualityRows = generateSection("Carcass Quality (% of available)", ["Prime", "Choice", "Select or Lower", "Other"], this.mainTableBody);
        this.tableSectionYieldRows = generateSection("Carcass Yield Grade (% of available)", ["YG 5", "YG 4", "YG 3", "YG 2", "YG 1", "Other"], this.mainTableBody);

        // Put HTML in frame

        this.frame.appendChild(this.divTableResponsive);
    }
}
