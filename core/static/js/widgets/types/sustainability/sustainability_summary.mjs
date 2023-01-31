import { BaseSummaryV2Widget } from "./base_summary_v2.mjs";
import { makeAverageScoreGaugeCharts, makeSectionalGaugeCharts } from "../../../core/sustainability_utilities.mjs";

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

        makeAverageScoreGaugeCharts(row, "Account Score: ", this.currentSectorID, this.sectorsNameToId, this.accountScores, this.globalAverages);
        this.makeGraphOverTime(row);
        makeSectionalGaugeCharts(this.frame, "Account Score: ", this.currentSectorID, this.sectorsNameToId, this.accountScores, this.globalAverages);
    }
}