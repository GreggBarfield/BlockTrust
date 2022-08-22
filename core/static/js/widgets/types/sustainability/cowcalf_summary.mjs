import { AbstractBaseSummaryWidget } from "./abstract_base_summary.mjs";

export class CowcalfSummaryWidget extends AbstractBaseSummaryWidget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";
        this.currentSector = this.frame.getAttribute("data-widget-sector-name");
    }

    // This is overriding the Base Class method
    createCharts() {
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        this.makeAverageScoreGaugeCharts(row, this.currentSector);
        // this.makeGraphOverTime(row);
        this.makeSectionalGaugeCharts(this.currentSector);
    }
}