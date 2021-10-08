import { AbstractBaseSummaryWidget } from "./abstract_base_summary.mjs";

export class SustainabilitySummaryWidget extends AbstractBaseSummaryWidget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        
        this.getData(
            "get_sustainability",
            {}
            ).then((data) => {
            this.frame.innerHTML = "";
            this.responses = data.results;
            
            if (data.results.length == 0) {
                this.data = null;
            } else {
                this.data = JSON.parse(data.results[0].response);
                this.prepData();
            }

            let sections = {
                "air": "Air & Greenhouse Gas Emissions",
                "land": "Land Resources",
                "water": "Water Resources",
                "animal": "Animal Health & Well-Being",
                "safety": "Employee Safety & Well-Being",
                "efficiency": "Efficiency & Yield"
            };
            
            this.makeNewSurveyBtn();

            let row = document.createElement("div");
            row.className = "row";
            this.frame.appendChild(row);

            this.makeAverageScoreGraph(row);
            this.makeGraphOverTime(row);
            this.makeOtherPieGraphs(sections);
        });
    }

    prepData() {
        let dataCounter = {
            "air": {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            },
            "animal": {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            },
            "efficiency": {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            },
            "safety": {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            },
            "land": {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            },
            "water": {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            },
        };

        let totals = {
            "excellent": 0, 
            "acceptable": 0,
            "needsWork": 0
        };

        for(const item in this.data){
            for(const response of this.data[item]){
                if (response.includes('a')) {
                    dataCounter[item].excellent += 1;
                    totals.excellent += 1;
                } else if (response.includes('b')) {
                    dataCounter[item].acceptable += 1;
                    totals.acceptable += 1;
                } else if (response.includes('c')) {
                    dataCounter[item].needsWork += 1;
                    totals.needsWork += 1;
                }
            }
        }

        dataCounter["all"] = totals;
        // this.data["all"] = [totals.excellent, totals.acceptable, totals.needsWork];
        this.setDataSet(dataCounter);
    }

}