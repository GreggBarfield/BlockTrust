import { Widget } from '../../widget.mjs';

export class MarketDataTableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.slug_id = this.frame.getAttribute('slug_id');

        this.getData(
            "get_market_data/" + this.slug_id,
            {}
        ).then((data) => {
            this.match_rows = data.market_data;
            console.log(this.match_rows);
            this.frame.innerHTML = "";
            this.makeTable();
        });
    }

    // Sections
    addTooltip(dataToggle,title,position){
        let toolTip = document.createElement("a");
        toolTip.className="feather icon-info";
        toolTip.style = "color:#2962FF;padding-left:6px;width:100%; vertical-align:-1px";
        toolTip.setAttribute("data-toggle" ,dataToggle);
        toolTip.setAttribute("data-placement" ,"right");
        toolTip.setAttribute("title" ,title);
        position.append(toolTip);           
        $(document).ready(function(){
            $('[data-toggle='+dataToggle+']').tooltip(); 
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
        const headers = Object.keys(this.match_rows[0]);
        for (const headerText of headers) {
            if (headerText != "report_narrative") {
                let th = document.createElement("th");
                th.textContent = headerText;
                this.mainTableHeadRow0.appendChild(th);
            }
        }

        let th = document.createElement("th");
        th.textContent = "Notes";
        this.mainTableHeadRow0.appendChild(th);

        // Body

        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        for (const row in this.match_rows) {
            let rowTag = document.createElement("tr");
            this.mainTableBody.appendChild(rowTag);

            for (const item in this.match_rows[row]) {
                if (item != "report_narrative") {
                    let td = document.createElement("td");
                    rowTag.append(td);
                    if (item.includes('price') && this.match_rows[row][item] != null){
                        td.textContent = '$' + this.match_rows[row][item];
                    } else {
                        td.textContent = this.match_rows[row][item];
                    }
                }
            }
            
            let notesTD = document.createElement("td");
            rowTag.append(notesTD);
            let toolTipText = this.match_rows[row]["report_narrative"];
            console.log(toolTipText);
            this.addTooltip("Notes", toolTipText, notesTD);            
        }

        // Put HTML in frame
        this.frame.appendChild(this.divTableResponsive);
        $(this.mainTable).DataTable();
    }
}