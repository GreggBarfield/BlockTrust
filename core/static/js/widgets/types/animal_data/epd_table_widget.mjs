import { Widget } from '../../widget.mjs';
import { epdTableHeaderContent } from '../../../core/epd_table_constants.mjs';

export class EPDTableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () => {
        this.frame.innerHTML = "";
        this.createTable();
    }
    
    createTable = () => {
        let table = document.createElement("table");
        table.className = "table table-responsive table-bordered table-xs";

        let thead = document.createElement("thead");
        thead.className = "thead-light";

        let theadRow0 = document.createElement("tr");

        for (const header of epdTableHeaderContent) {
            let th = document.createElement("th");
            let link = this.createLinkWithTitle(header.text, header.title);
            th.append(link);
            theadRow0.appendChild(th);
        }
        thead.appendChild(theadRow0);
        table.append(thead);
        
        // Placeholder values until the actual data comes in
        let valuesRow = document.createElement("tr");
        for (const header of epdTableHeaderContent){
            let td = document.createElement("td");
            td.textContent = "N/A";
            valuesRow.appendChild(td);
        }
        table.append(valuesRow)

        this.frame.appendChild(table);
    }

    createLinkWithTitle = (linkText, titleText) => {
        let link = document.createElement("a");
        link.textContent = linkText;
        link.title = titleText;
        link.href = "#";
        return link;
    }
}