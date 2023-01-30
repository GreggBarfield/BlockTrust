import { Widget } from '../../widget.mjs';

export class TagDistributionSectorAtAccountWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {

        let companyName = this.frame.getAttribute("data-widget-account-company");

        this.getData(
            "direct/sectors_name_to_id",
            {}
        ).then((data) => {
            this.request = {
                type: "count_distribution_for_sector_at_account",
                params: {
                    sector_id: data.sectors_name_to_id["Cow-Calf"]      
                }
            }

            this.getData(
                "data_request",
                {
                    request: this.request
                }
            ).then((data) => {
                this.feedyardData = data.result !== null ? data.result.matched_data : {};
                this.accountData = data.result !== null ? data.result.all_data: {};
            }).then(() => {
                this.frame.innerHTML = "";
                this.frame.appendChild(this.createTabs(companyName));
                let tabDataContainer = this.createContainer();
                tabDataContainer.appendChild(this.makeMatchedTabContents(this.feedyardData));
                tabDataContainer.appendChild(this.makeAllDataTabContents(this.accountData));
                this.frame.appendChild(tabDataContainer);
            });
        })

    }

    createTabs = (companyName) => {
        let ulTabs = document.createElement("ul");
        ulTabs.className = "nav nav-tabs";
        ulTabs.setAttribute("role", "tablist")    

        let liTab = this.createTab("matched-data", companyName, true)
        ulTabs.appendChild(liTab);

        liTab = this.createTab("all-data", "All", false);
        ulTabs.appendChild(liTab);

        return ulTabs;
    }

    createTab = (tabIdentifier, label, isSelected) => {
        let liTab = document.createElement("li");
        liTab.className = "nav-item";
        let aTab = document.createElement("a");
        aTab.className = `nav-link text-uppercase ${isSelected?"active":""}` ;
        aTab.href = `#${tabIdentifier}`;
        aTab.id = `${tabIdentifier}-tab`;
        aTab.setAttribute("data-toggle", "tab");
        aTab.setAttribute("role", "tab");
        aTab.setAttribute("aria-controls", tabIdentifier);
        aTab.setAttribute("aria-selected", isSelected);
        aTab.text = label
        liTab.appendChild(aTab);
        return liTab
    }

    createContainer = () => {
        let divTabContent = document.createElement("div");
        divTabContent.className = "tab-content";
        divTabContent.id = "myTabContent";
        return divTabContent;
    }

    makeMatchedTabContents = (distributionData) => {
        let divTab = document.createElement("div");
        divTab.className = "tab-pane fade show active"
        divTab.id = "matched-data"
        divTab.setAttribute("role", "tabpanel");
        divTab.setAttribute("aria-labelledby", "matched-data-tab")
        let table = this.makeTable(distributionData);
        divTab.appendChild(table);
        return divTab;
    }

    makeAllDataTabContents = (distributionData) => {
        let divTab = document.createElement("div");
        divTab.className = "tab-pane fade"
        divTab.id = "all-data"
        divTab.setAttribute("role", "tabpanel");
        divTab.setAttribute("aria-labelledby", "all-data-tab")       
        let table = this.makeTable(distributionData);
        divTab.appendChild(table);
        return divTab;
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
        const headers = ["Ranch", "Count", "Sustainability Score", "Prime", "Choice", "Select", "YG1", "YG2", "YG3", "YG4", "YG5"]
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
            row.push(accountName);
            let qualityDistribution = data.quality_distribution;
            let count = 0;
            Object.values(qualityDistribution).forEach(total => count+=total);
            row.push(count);

            let sustainabilityScoreLink = document.createElement('a');
            sustainabilityScoreLink.href = "/dashboard/view-account-sustainability-scores/" + data.account_id.toString();
            sustainabilityScoreLink.text = "View Score";
            sustainabilityScoreLink.target = "_blank";
            row.push(sustainabilityScoreLink)

            row.push(("Prime" in qualityDistribution? 100*qualityDistribution.Prime/count : 0).toFixed(2)+"%");
            row.push(("Choice" in qualityDistribution? 100*qualityDistribution.Choice/count : 0).toFixed(2)+"%");
            if("Select" in qualityDistribution)
                row.push((100*qualityDistribution.Select/count).toFixed(2)+"%");
            else if("Select or Lower" in qualityDistribution)
                row.push((100*qualityDistribution["Select or Lower"]/count).toFixed(2)+"%");
            else 
                row.push((0).toFixed(2)+"%")

            let yieldDistribution = data.yield_distribution;
            row.push(("1" in yieldDistribution? 100*yieldDistribution["1"]/count : 0).toFixed(2)+"%");
            row.push(("2" in yieldDistribution? 100*yieldDistribution["2"]/count : 0).toFixed(2)+"%");
            row.push(("3" in yieldDistribution? 100*yieldDistribution["3"]/count : 0).toFixed(2)+"%");
            row.push(("4" in yieldDistribution? 100*yieldDistribution["4"]/count : 0).toFixed(2)+"%");
            row.push(("5" in yieldDistribution? 100*yieldDistribution["5"]/count : 0).toFixed(2)+"%");

            for (const value of row) {
                let td = document.createElement("td");
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
