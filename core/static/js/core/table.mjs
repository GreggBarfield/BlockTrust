export class Table {
    constructor() {
        this.frame = null;

        this.tableResponsive = document.createElement("div");
        this.tableResponsive.className = "table-responsive";
        
        this.table = document.createElement("table");
        this.table.className = "table table-xs";
        this.tableResponsive.append(this.table);

        this.thead = document.createElement("thead");
        this.table.append(this.thead);

        this.tbody = document.createElement("tbody");
        this.table.append(this.tbody);
    }

    setHeader(values) {
        if (this.thead.firstChild !== null) {
            this.thead.firstChild.remove();
        }

        let tr = document.createElement("tr");

        for (const value of values) {
            let th = document.createElement("th");
            th.textContent = value;
            tr.append(th);
        }

        this.thead.append(tr);
    }

    addRow(values) {
        let tr = document.createElement("tr");

        for (const value of values) {
            let td = document.createElement("td");
            if (typeof value == "object") {
                td.appendChild(value);
            }
            else {
                td.textContent = value;
            }
            tr.append(td);
        }

        this.tbody.append(tr);
        return tr;
    }

    setValue(row, colItr, value) {
        row.children[colItr].textContent = value;
    }

    attach(frame) {
        if (this.frame !== null) {
            this.detach();
        }
        this.frame = frame;
        this.frame.append(this.tableResponsive);
    }

    detach() {
        this.frame.removeChild(this.tableResponsive);
        this.frame = null;
    }


}