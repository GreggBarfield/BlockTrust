import { Widget } from '../../widget.mjs';
export class SummaryGraphWidget extends Widget {
    constructor(frame) {
        super(frame);
    }
    
    initType = () => {
        this.getData(
            "get_employee_summary_graphs_data",
            {}
        ).then((data) => {
            this.data = data;
            this.makeSummaryGraphs();
        });
        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });
    }
    
    makeSummaryGraphs = () => {
        let cardBody = document.getElementById("card");
        let ranchesGraph = this.makeLineGraphContainer("Ranches", this.data.ranches, false);
        let feedyardsGraph = this.makeLineGraphContainer("Feedyards", this.data.feedyards, false);
        let tagsCountGraph = this.makeLineGraphContainer("Tags", this.data.tags_count_list, true);
        cardBody.append(ranchesGraph);
        cardBody.append(feedyardsGraph);
        cardBody.append(tagsCountGraph);
    }

    makeLineGraphContainer = (title, values, tagsCountData) => {
        let lineGraphOutline = document.createElement("div");
        let lineGraphContainer = document.createElement("div");
        lineGraphContainer.style = "height: 18em;";
        let graphLabel = document.createElement("span");
        graphLabel.className = "label label-info d-flex";
        graphLabel.textContent = title;
        lineGraphOutline.append(graphLabel);
        lineGraphOutline.append(lineGraphContainer);
        this.makeLineGraph(lineGraphContainer, values, tagsCountData);
        return lineGraphOutline;
    }

    getGraphableLineData = (values) => {
        let graphableData = [];
        let valueCounter = 0;
        for(const value of values) {
            valueCounter += 1;
            graphableData.push({
                "date": new Date(value.created_timestamp),
                "value": valueCounter
            });
        }
        return graphableData;
    }

    getGraphableLineDataForTagsCount = (values) => {
        let graphableData = [];
        for(const value of values) {
            if(value.result !== null){
                let count_eid_distinct_object = JSON.parse(value.result)
                graphableData.push({
                    "date": new Date(value.created_timestamp),
                    "value": count_eid_distinct_object.count_eid_distinct
                });
            }     
        }
        return graphableData;
    }

    makeLineGraph = (container, values, tagsCountData) => {
        if (this.data == null) {
            container.textContent = "Data is not available yet.";
        }
        else if (this.data.length < 2) {
            container.textContent = "There is not enough data yet.";
        }
        else {
            let self = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(container, am4charts.XYChart);
                if(tagsCountData){
                    chart.data = self.getGraphableLineDataForTagsCount(values);
                }
                else{
                    chart.data = self.getGraphableLineData(values);
                }
                // Create axes
                var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                dateAxis.renderer.minGridDistance = 40;

                var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis.renderer.minGridDistance = 20;

                // Create series
                var series = chart.series.push(new am4charts.LineSeries());
                series.dataFields.valueY = "value";
                series.dataFields.dateX = "date";
                series.fillOpacity = 0.1;
                series.tooltipText = "{valueY.value}";
                series.fill = am4core.color("#e52d27");
                series.stroke = am4core.color("#008000");
                series.strokeWidth = 3;

                // Add cursor
                chart.cursor = new am4charts.XYCursor();
                chart.cursor.fullWidthLineX = true;
                chart.cursor.lineX.strokeWidth = 0;
                chart.cursor.lineX.fill = am4core.color("#fff");
                chart.cursor.lineX.fillOpacity = 0;
            });
        }
    }

}