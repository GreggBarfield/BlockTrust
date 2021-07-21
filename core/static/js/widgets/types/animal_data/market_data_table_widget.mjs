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
        const headerAlias = {
            "report_date": "date",
            "commodity": "commodity",
            "class": "class",
            "frame": "frame",
            "muscle_grade": "musc_grad",
            "quality_grade_name": "qual_grad",
            "lot_desc": "lot_desc",
            "price_unit": "price",
            "age": "age",
            "pregnancy_stage": "preg_st",
            "weight_collect": "wgt_coll",
            "offspring_weight_est": "offspr_wgt",
            "dressing": "dressing",
            "yield_grade": "yld_grad",
            "head_count": "hd_cnt",
            "avg_weight": "avg_wgt",
            "avg_price": "avg_price"
        }
        for (const headerText of headers) {
            if (headerText != "report_narrative") {
                let th = document.createElement("th");
                th.textContent = headerAlias[headerText];
                th.setAttribute("data-toggle" ,headerText);
                th.setAttribute("data-placement" ,"top");
                th.setAttribute("title" ,headerText);
                $(document).ready(function(){
                    $('[data-toggle='+headerText+']').tooltip(); 
                });
                this.mainTableHeadRow0.appendChild(th);
            }
        }

        let th = document.createElement("th");
        th.textContent = "Info";
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
                    if (item == "avg_price" && this.match_rows[row][item] != null){
                        td.textContent = '$' + this.match_rows[row][item];
                    } else {
                        td.textContent = this.match_rows[row][item];
                    }
                }
            }
            
            let notesTD = document.createElement("td");
            rowTag.append(notesTD);
            let toolTipText = this.match_rows[row]["report_narrative"];
            this.addTooltip("Info", toolTipText, notesTD);            
        }

        // Put HTML in frame
        this.frame.appendChild(this.divTableResponsive);
        $(this.mainTable).DataTable();
    }
}