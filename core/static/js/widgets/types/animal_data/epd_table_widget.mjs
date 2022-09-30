import { Widget } from '../../widget.mjs';

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
        table.className = "table table-xs";

        let thead = document.createElement("thead");
        thead.className = "thead-light";

        let theadRow0 = document.createElement("tr");
        let headers = ["A", "B", "C", "D"];
        for (const header of headers) {
            let th = document.createElement("th");
            th.textContent = header;
            theadRow0.appendChild(th);
        }
        thead.appendChild(theadRow0);
        table.append(thead);

        this.frame.appendChild(table);
    }
}