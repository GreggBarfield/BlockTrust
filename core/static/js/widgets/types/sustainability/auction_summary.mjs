import { AbstractBaseSummaryWidget } from "./abstract_base_summary.mjs";

export class AuctionSummaryWidget extends AbstractBaseSummaryWidget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";
        this.makeNewSurveyBtn();
    }

    // This is overriding the Base Class method
    createCharts() {
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        let sections = {
            "water": "Water Resources",
            "animal": "Animal Health & Well-Being",
            "safety": "Employee Safety & Well-Being"
        };

        this.makeAverageScoreGraph(row);
        this.makeGraphOverTime(row);
        this.makeOtherPieGraphs(sections);
    }
}