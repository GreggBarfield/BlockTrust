import { BaseSummaryV2Widget } from "./base_summary_v2.mjs";

export class SustainabilitySummaryWidget extends BaseSummaryV2Widget {
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
        this.makeGraphOverTime(row);
        this.makeSectionalGaugeCharts(this.currentSectorID);
    }
}