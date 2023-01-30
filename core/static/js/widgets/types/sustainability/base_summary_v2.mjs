import { Widget } from "../../widget.mjs";

export class BaseSummaryV2Widget extends Widget {
    constructor(frame) {
        super(frame);
        this.dataCounter = {};
        this.getSustainabilityData();
    }
    createCharts() {}

    getSustainabilityData = async() =>{
        let accountSustainabilityData = await this.getData("get_account_sustainability_data");
        this.accountScores = accountSustainabilityData.account_sustainability_section_and_scores;
        this.accountSustainabilityResponses = accountSustainabilityData.account_sustainability_responses;
        
        let globalSustainabilityData = await this.getData("data_request", {request: {type: 'sustainability_response_averages', params: {}}});
        this.globalAverages = globalSustainabilityData.result;
         
        let sectorsByName = await this.getData("direct/sectors_name_to_id");
        this.sectorsNameToId = sectorsByName.sectors_name_to_id;
        this.createCharts();
    }

    makeGraphOverTime = (row) =>{
        let cardWrapper = document.createElement("div");
        cardWrapper.className = "col-md-6";
        row.appendChild(cardWrapper);

        let card = document.createElement("div");
        card.className = "card";
        cardWrapper.append(card);

        let cardHeader = document.createElement("h5");
        cardHeader.className = "card-header";
        cardHeader.textContent = "Sustainability Over Time";
        card.append(cardHeader);
        
        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);

        let lineGraph = document.createElement("div");
        lineGraph.style = "height: 18em;";
        cardBody.append(lineGraph);
        this.makeLineGraph(lineGraph);
    }

    getGraphableLineData = () =>{
        let graphableData = [];
        for(const sustainabilityResponse of this.accountSustainabilityResponses){
            graphableData.push({
                "date": new Date(sustainabilityResponse.created_timestamp),
                "value": sustainabilityResponse.score
            });
        }
        return graphableData;
    }

    makeLineGraph = (container) =>{
        if (this.accountSustainabilityResponses == null) {
            container.textContent = "Data is not available yet.";
        }
        else if (this.accountSustainabilityResponses.length < 1) {
            container.textContent = "There is not enough data yet.";
        }
        else {
            let self = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(container, am4charts.XYChart);

                chart.data = self.getGraphableLineData();

                var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                dateAxis.renderer.minGridDistance = 40;

                var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis.renderer.minGridDistance = 20;

                var series = chart.series.push(new am4charts.LineSeries());
                series.dataFields.valueY = "value";
                series.dataFields.dateX = "date";
                series.fillOpacity = 0.1;
                series.tooltipText = "{valueY.value}";
                series.fill = am4core.color("#e52d27");
                series.stroke = am4core.color("#008000");
                series.strokeWidth = 3;

                chart.cursor = new am4charts.XYCursor();
                chart.cursor.fullWidthLineX = true;
                chart.cursor.lineX.strokeWidth = 0;
                chart.cursor.lineX.fill = am4core.color("#fff");
                chart.cursor.lineX.fillOpacity = 0;
            });
        }
    }
}