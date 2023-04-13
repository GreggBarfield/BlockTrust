import { Widget } from '../../widget.mjs';

export class PartnerCountDistributionWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
            this.getData(
                "data_request",
                {
                    request: { 
                        type: "count_distribution",
                        params: {}
                    }
                }
            ).then((data) => {
                let accountSummaryData = data.result.count_distribution !== null ? data.result.count_distribution: {};
                this.frame.innerHTML = "";
                let table = this.makeTable(accountSummaryData);
                this.frame.appendChild(table);
            })
        

    }

    makeTable = (distributionData) => {
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
        const headers = ["Ranch", "Sightings", "Sustainability Score", "Prime", "Choice", "Select", "YG1", "YG2", "YG3", "YG4", "YG5"]
        for (const headerText of headers) {
            let th = document.createElement("th");
            th.textContent = headerText;
            this.mainTableHeadRow0.appendChild(th);
        }

        // Body
        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        for (const [accountName,data] of Object.entries(distributionData)) {
            let rowTag = document.createElement("tr");
            this.mainTableBody.appendChild(rowTag);

            let row = [];
            let accountNameButton = document.createElement("button");
            accountNameButton.innerText = accountName;
            accountNameButton.classList.add("btn", "btn-link");
            accountNameButton.onclick = () => {
                let widgets = document.querySelectorAll("[data-widget-type='source summary']");
                for(let widget of widgets) {
                    widget.setAttribute("data-widget-account-id",data["account_id"]);
                    widget.setAttribute("data-widget-account-name",accountName);
                    document.getElementById(widget.getAttribute("data-widget-refresh-id")).click();
                }
                let tagDetailId = this.frame.getAttribute("data-widget-tag-detail");
                let tagDetailContainer = document.getElementById(tagDetailId);
                tagDetailContainer.getElementsByTagName("span")[0].innerText = `All Tags for ${accountName}`
                tagDetailContainer.classList.remove('d-none');
                document.getElementById(tagDetailId).focus();
            };
            row.push(accountNameButton);
            row.push(data["sightings"]);
            let dataCount = 0;
            let qualityDistribution = data.quality_distribution;
            Object.values(qualityDistribution).forEach(total => dataCount+=total);
            let sustainabilityScoreLink = document.createElement('a');
            sustainabilityScoreLink.href = "/dashboard/view-account-sustainability-scores/" + data.account_id.toString();
            sustainabilityScoreLink.text = "View Score";
            sustainabilityScoreLink.target = "_blank";
            sustainabilityScoreLink.classList.add("btn", "btn-link");
            row.push(sustainabilityScoreLink)
            if (dataCount){
                row.push(("Prime" in qualityDistribution? 100*qualityDistribution.Prime/dataCount : 0).toFixed(2)+"%");
                row.push(("Choice" in qualityDistribution? 100*qualityDistribution.Choice/dataCount : 0).toFixed(2)+"%");
                if("Select" in qualityDistribution)
                    row.push((100*qualityDistribution.Select/dataCount).toFixed(2)+"%");
                else if("Select or Lower" in qualityDistribution)
                    row.push((100*qualityDistribution["Select or Lower"]/dataCount).toFixed(2)+"%");
                else 
                    row.push((0).toFixed(2)+"%")

                let yieldDistribution = data.yield_distribution;
                row.push(("1" in yieldDistribution? 100*yieldDistribution["1"]/dataCount : 0).toFixed(2)+"%");
                row.push(("2" in yieldDistribution? 100*yieldDistribution["2"]/dataCount : 0).toFixed(2)+"%");
                row.push(("3" in yieldDistribution? 100*yieldDistribution["3"]/dataCount : 0).toFixed(2)+"%");
                row.push(("4" in yieldDistribution? 100*yieldDistribution["4"]/dataCount : 0).toFixed(2)+"%");
                row.push(("5" in yieldDistribution? 100*yieldDistribution["5"]/dataCount : 0).toFixed(2)+"%");
            }
            else {
                for(let i=0; i<8; i++)
                    row.push("n/a");
            }

            for (const value of row) {
                let td = document.createElement("td");
                td.classList.add("align-middle");
                if(value instanceof HTMLElement){
                    td.append(value);
                }
                else{
                    td.textContent = value;
                }
                rowTag.appendChild(td);
            }
        }

        $(this.mainTable).DataTable();
        return this.mainTable;
    }
}
