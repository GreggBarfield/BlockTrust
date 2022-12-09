import { Widget } from '../../widget.mjs';

export class TableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.account = parseInt(this.frame.getAttribute("data-widget-account"));
        this.companyName = this.frame.getAttribute("data-widget-company-name");
        this.downloadButtonId = this.frame.getAttribute("data-widget-button-id");

        this.frame.innerHTML = "";
        this.makeTable();

        Promise.all([
            this.getData(
                "data_request",
                {
                    request: {
                        type: 'count_eid_distinct_by_account',
                        params: {

                        }
                    }
                }
            ).then((data) => {
                if (data.result === null) {
                    this.account_total_distinct = null
                }
                else {
                    this.account_total_distinct = data.result.count_eid_distinct;
                }
                this.displayAccount();
            }),
            
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
                if (data.result === null) {
                    this.global_usda_yield_grade_distribution = null;
                }
                else {
                    this.global_usda_yield_grade_distribution = data.result.count_distribution;
                }
                this.displayGlobal();
            }),
                
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
                if (data.result === null) {
                    this.global_usda_quality_grade_distribution = null;
                }
                else {
                    this.global_usda_quality_grade_distribution = data.result.count_distribution;
                }
                this.displayGlobal();
            }),
                
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
                if (data.result === null) {
                    this.account_usda_yield_grade_distribution = null;
                }
                else {
                    this.account_usda_yield_grade_distribution = data.result.count_distribution;
                }
                this.displayAccount();
            }),
                
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
                if (data.result === null) {
                    this.account_usda_quality_grade_distribution = null;
                }
                else {
                    this.account_usda_quality_grade_distribution = data.result.count_distribution;
                }
                this.displayAccount();
            }),
                
            this.getData(
                "data_request",
                {
                    request: {
                        type: 'count_eid_distinct',
                        params: {}
                    }
                },
            ).then((data) => {
                if (data.result === null) {
                    this.count_eid_distinct = null;
                }
                else {
                    this.count_eid_distinct = data.result.count_eid_distinct;
                }
                this.displayGlobal();
            })
        ]).then(() => {
            if (this.downloadButtonId && this.account_usda_quality_grade_distribution) {
                this.createSummaryTableExport()
            }
        })

    }

    createSummaryTableExport() {
        let qualityGrades = ["Prime", "Choice", "Select or Lower"];
        let columnHeaders = ["", this.companyName, "GLOBAL BENCHMARK"];

        //First table
        let tableExport = [["Sightings Summary"], columnHeaders];
        tableExport.push(["Total Calves", this.account_total_distinct, this.count_eid_distinct]);

        let accountDataAvailableTotal = 0, globalDataAvailableTotal = 0;

        let qualityGradeToCountAccount = {"Prime":0, "Choice":0, "Select or Lower":0,"Others":0};
        let qualityGradeToCountGlobal = {"Prime":0, "Choice":0, "Select or Lower":0,"Others":0};
        for(let dataItem of this.account_usda_quality_grade_distribution)
        {
            accountDataAvailableTotal += dataItem.count;
            if(qualityGrades.includes(dataItem.data))
                qualityGradeToCountAccount[dataItem.data] += dataItem.count;
            else
                qualityGradeToCountAccount["Others"] += dataItem.count;
        }
        for(let dataItem of this.global_usda_quality_grade_distribution)
        {          
            globalDataAvailableTotal += dataItem.count;
            if(qualityGrades.includes(dataItem.data))
                qualityGradeToCountGlobal[dataItem.data] += dataItem.count;
            else
                qualityGradeToCountGlobal["Others"] += dataItem.count
        }
        tableExport.push(["Total Available", accountDataAvailableTotal,globalDataAvailableTotal ]);

        if (this.account_total_distinct) {
            tableExport.push(["% Available", (100 * accountDataAvailableTotal / this.account_total_distinct).toFixed(2) + "%", 
                (100 * globalDataAvailableTotal / this.count_eid_distinct).toFixed(2) + "%"]);
        }
        else
            tableExport.push(["% Available", "n/a", (100 * globalDataAvailableTotal / this.count_eid_distinct).toFixed(2) + "%"]);            

        //Second table
        tableExport.push([""], ["Carcass Quality Grade(% of available)"], columnHeaders)
        for(let grade of Object.keys(qualityGradeToCountAccount)) {
            let row = [grade]
   
            if (accountDataAvailableTotal) 
                row.push((100*qualityGradeToCountAccount[grade]/accountDataAvailableTotal).toFixed(2) + "%")
            else
                row.push("n/a")

            row.push((100*qualityGradeToCountGlobal[grade]/globalDataAvailableTotal).toFixed(2) + "%")
            tableExport.push(row)
        }

        //Third table
        let yieldGrades = [5, 4, 3, 2, 1];
        let yieldGradeToCountAccount = {5:0, 4:0, 3:0, 2:0, 1:0, 0:0}, yieldGradeToCountGlobal = {5:0, 4:0, 3:0, 2:0, 1:0, 0:0};
        for(let dataItem of this.account_usda_yield_grade_distribution)
        {
            if(yieldGrades.includes(dataItem.data))
                yieldGradeToCountAccount[dataItem.data] += dataItem.count;
            else 
                 yieldGradeToCountAccount[0] += dataItem.count ;
        }
        for(let dataItem of this.global_usda_yield_grade_distribution)
        {
            if(yieldGrades.includes(dataItem.data))
                yieldGradeToCountGlobal[dataItem.data] += dataItem.count;
            else
                yieldGradeToCountGlobal[0] += dataItem.count ;
        }
        tableExport.push([""], ["Carcass Yield Grade(% of available)"], columnHeaders)
        for(let grade of Object.keys(yieldGradeToCountAccount).sort().reverse()) {         
            let row = grade==0? ["Others"]:  [`YG ${grade}`] 
            if (accountDataAvailableTotal) 
                row.push((100*yieldGradeToCountAccount[grade]/accountDataAvailableTotal).toFixed(2) + "%")
            else 
                row.push( "n/a")
            row.push((100*yieldGradeToCountGlobal[grade]/globalDataAvailableTotal).toFixed(2) + "%")
            tableExport.push(row)         
        }

        let csvContent = "data:text/csv;charset=utf-8," + tableExport.map(e => e.join(",")).join("\n");
        var encodedUri = encodeURI(csvContent);
        let downloadButton = document.getElementById(this.downloadButtonId)
        downloadButton.setAttribute("href", encodedUri);
        downloadButton.setAttribute("download", "Calf-Crop Summary.csv");
        downloadButton.classList.remove("d-none")
    }

    unavailableSection(rows, indx) {
        for (let row of rows.slice(1)) {
            let interest = row.children[indx];
            interest.innerHTML = "";
            interest.append(this.createNotAvailableYet());
        }
    };

    displayGlobal() {
        if ('count_eid_distinct' in this) {
            let interest = this.tableSectionSightingsRows[1].children[2];
            if (this.count_eid_distinct === null) {
                interest.innerHTML = "";
                interest.append(this.createNotAvailableYet());
            }
            else {
                interest.textContent = this.count_eid_distinct;
            }
        }
        if ('global_usda_yield_grade_distribution' in this) {
            if (this.global_usda_yield_grade_distribution === null) {
                this.unavailableSection(this.tableSectionYieldRows, 2);
            }
            else {
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
                        v = (100 * yg[i] / total).toFixed(2) + "%";
                    }
                    this.tableSectionYieldRows[1 + parseInt(i)].children[2].textContent = v;
                }
                this.global_total_available = total;
            }
        }
        if ('global_usda_quality_grade_distribution' in this) {
            if (this.global_usda_quality_grade_distribution === null) {
                this.unavailableSection(this.tableSectionQualityRows, 2);
            }
            else {
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
                        v = (100 * yg[i] / total).toFixed(2) + "%";
                    }
                    this.tableSectionQualityRows[1 + parseInt(i)].children[2].textContent = v;
                }
                this.global_total_available = total;
            }
        }
        if ('global_total_available' in this || 'count_eid_distinct' in this) {
            let interest1 = this.tableSectionSightingsRows[2].children[2];
            let interest2 = this.tableSectionSightingsRows[3].children[2];

            if (
                'global_total_available' in this && this.global_total_available === null ||
                'count_eid_distinct' in this && this.count_eid_distinct === null
            ) {
                interest1.innerHTML = "";
                interest1.append(this.createNotAvailableYet());
                interest2.innerHTML = "";
                interest2.append(this.createNotAvailableYet());
            }
            else if ('global_total_available' in this && 'count_eid_distinct' in this) {
                interest1.textContent = this.global_total_available;
                let v = "n/a";
                if (this.count_eid_distinct != 0) {
                    v = (100 * this.global_total_available / this.count_eid_distinct).toFixed(2) + "%";
                }
                interest2.textContent = v;
            }
        }
    }

    displayAccount() {
        if ('account_usda_yield_grade_distribution' in this) {
            if (this.account_usda_yield_grade_distribution === null) {
                this.unavailableSection(this.tableSectionYieldRows, 1);
                if (!('account_total_available' in this)) {
                    this.account_total_available = null;
                }
            }
            else {
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
                        v = (100 * yg[i] / total).toFixed(2) + "%";
                    }
                    this.tableSectionYieldRows[1 + parseInt(i)].children[1].textContent = v;
                }
                this.account_total_available = total;
            }
        }
        if ('account_usda_quality_grade_distribution' in this) {
            if (this.account_usda_quality_grade_distribution === null) {
                this.unavailableSection(this.tableSectionQualityRows, 1);
                if (!('account_total_available' in this)) {
                    this.account_total_available = null;
                }
            }
            else {
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
                        v = (100 * yg[i] / total).toFixed(2) + "%";
                    }
                    this.tableSectionQualityRows[1 + parseInt(i)].children[1].textContent = v;
                }
                this.account_total_available = total;
            }
        }

        if ('account_total_distinct' in this) {
            let interest = this.tableSectionSightingsRows[1].children[1];
            if (this.account_total_distinct === null) {
                interest.innerHTML = "";
                interest.append(this.createNotAvailableYet());
            }
            else {
                interest.textContent = this.account_total_distinct;
            }
        }
        if ('account_total_available' in this) {
            let interest = this.tableSectionSightingsRows[2].children[1];
            if (this.account_total_available === null) {
                interest.innerHTML = "";
                interest.append(this.createNotAvailableYet());
            }
            else {
                interest.textContent = this.account_total_available;
            }
        }
        if ('account_total_available' in this || 'account_total_distinct' in this) {
            let interest = this.tableSectionSightingsRows[3].children[1];
            if (
                'account_total_available' in this && this.account_total_available === null ||
                'account_total_distinct' in this && this.account_total_distinct === null) {
                interest.innerHTML = "";
                interest.append(this.createNotAvailableYet());
            }
            else if ('account_total_available' in this && 'account_total_distinct' in this) {
                let v = "n/a";
                if (this.account_total_distinct != 0) {
                    v = (100 * this.account_total_available / this.account_total_distinct).toFixed(2) + "%";
                }
                interest.textContent = v;
            }
        }
    }

    createNotAvailableYet() {
        let span = document.createElement("span");
        span.textContent = "?";
        span.className = "badge badge-pill badge-info";
        span.setAttribute("toggle", "tooltip");
        span.setAttribute("data-placement", "top");
        span.setAttribute("data-original-title", "Data is still being processed.");
        $(span).tooltip({
            offset: -50
        });
        return span;
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
        this.mainTableHeadRow0TH1.textContent = this.companyName;
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
                        //This is what each column gets set to and then overwritten by displayAccount and displayGlobal
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
