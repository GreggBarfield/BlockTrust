import { AbstractBaseSummaryWidget } from "./abstract_base_summary.mjs";

export class FeedyardSummaryWidget extends AbstractBaseSummaryWidget {
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

        let sections = {
            "air": "Air & Greenhouse Gas Emissions",
            "land": "Land Resources",
            "water": "Water Resources",
            "animal": "Animal Health & Well-Being",
            "safety": "Employee Safety & Well-Being",
            "efficiency": "Efficiency & Yield"
        };

        this.makeAverageScoreGraph(row);
        this.makeGraphOverTime(row);
        this.makeOtherPieGraphs(sections);
    }

}