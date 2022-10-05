import { Widget } from '../../widget.mjs';

const epdTableHeaderContent = [
    {text: "CED", title: "Calving Ease EPD (CED) is expressed as a difference in percentage of unassisted births, with a higher value indicating greater calving ease in first-calf heifers"},
    {text: "BW", title: "Birth Weight EPD (BW), expressed in pounds, is a predictor of a bull's ability to transmit birth weight to his progeny compared to that of other bulls. Birth Weight EPDs are a component trait for calculating Calving Ease EPDs."},
    {text: "WW", title: "Weaning Weight EPD (WW), expressed in pounds, is a predictor of a bull's ability to transmit weaning growth to his progeny compared to that of other sires."},
    {text: "YW", title: "Yearling Weight EPD (YW), expressed in pounds, is a predictor of a bull's ability to transmit yearling growth to his progeny compared to that of other sires."},
    {text: "MILK", title: "Milk EPD (Milk), expressed in pounds, is an estimate of the portion of a calf's weaning weight attributed to milk and mothering ability. Optimal Milk EPDs can vary between environments."},
    {text: "CW", title: "Carcass Weight EPD (CW), expressed in pounds, is a predictor of the differences in hot carcass weight of a sire's progeny compared to progeny of other sires."},
    {text: "MARB", title: "Marbling EPD (Marb), expressed as a fraction of the difference in USDA marbling score of a sire's progeny compared to progeny of other sires."},
    {text: "REA", title: "Ribeye Area (REA), expressed in square inches, is a predictor of the difference in ribeye area of a sire's progeny compared to progeny of other sires. "},
    {text: "API", title: ""},
    {text: "TI", title: ""},
    {text: "REA", title: "The Adjusted weight is on the left and the ratio is on the right"},
    {text: "IMF", title: "The Adjusted weight is on the left and the ratio is on the right"},
    {text: "ADJ. YW", title: "The Adjusted weight is on the left and the ratio is on the right"},
    {text: "ADJ. WW", title: "The Adjusted weight is on the left and the ratio is on the right"},
    {text: "BW/BWR", title: "The Adjusted weight is on the left and the ratio is on the right"}
];

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

        let tHead = document.createElement("thead");
        tHead.className = "thead-light";

        let tHeadRow = document.createElement("tr");

        for (const header of epdTableHeaderContent) {
            let th = document.createElement("th");
            let link = this.createLinkWithTitle(header.text, "");
            th.append(link);
            tHeadRow.appendChild(th);
        }
        tHead.appendChild(tHeadRow);
        table.append(tHead);
        
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