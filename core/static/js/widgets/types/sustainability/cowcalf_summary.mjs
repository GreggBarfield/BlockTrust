import { AbstractBaseSummaryWidget } from "./abstract_base_summary.mjs";

export class CowcalfSummaryWidget extends AbstractBaseSummaryWidget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";
    }

    // This is overriding the Base Class method
    createCharts() {
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        this.makeAverageScoreGaugeCharts(row, "Cow-Calf");
        // this.makeGraphOverTime(row);
        this.makeSectionalGaugeCharts("Cow-Calf");
    }
}