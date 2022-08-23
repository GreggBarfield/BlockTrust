import { AbstractBaseSummaryWidget } from "./abstract_base_summary.mjs";

export class CowcalfSummaryWidget extends AbstractBaseSummaryWidget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";
        this.currentSectorID = this.frame.getAttribute("data-widget-sector-id");
    }

    // This is overriding the Base Class method
    createCharts() {
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        this.makeAverageScoreGaugeCharts(row, this.currentSectorID);
        // this.makeGraphOverTime(row);
        this.makeSectionalGaugeCharts(this.currentSectorID);
    }
}