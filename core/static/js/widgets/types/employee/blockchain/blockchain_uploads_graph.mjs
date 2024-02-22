import { Widget } from '../../../widget.mjs';

export class BlockchainDailyUploadsGraphWidget extends Widget {
    constructor(frame) {
        super(frame);
    }
    
    initType = () => {
        this.frame.innerHTML = "";
        let dailyUploadCounts = JSON.parse(this.frame.getAttribute("data-widget-daily-upload-counts"));
        let dailyUploadGraph = this.makeDailyUploadGraph(dailyUploadCounts);
        this.frame.append(dailyUploadGraph);
    }
    
    makeDailyUploadGraph = (dailyUploadCounts) =>{
        let graphContainer = document.createElement("div");
        graphContainer.className = "card m-1 p-1";

        let graphContainerHeader = document.createElement("h5");
        graphContainerHeader.className = "card-header";
        graphContainerHeader.textContent = "Blockchain Daily Uploads";
        graphContainer.append(graphContainerHeader);

        let graphContainerBody = document.createElement("div");
        graphContainerBody.className = "card-body m-1 p-1";
        let lineGraphContainer = document.createElement("div");
        graphContainerBody.append(lineGraphContainer);
        graphContainer.append(graphContainerBody);
        let chartData = this.getLineDataForGraph(dailyUploadCounts);
        this.makeLineGraph(lineGraphContainer, chartData);
        return graphContainer;
    }

    getLineDataForGraph = (values) =>{
        let graphableData = [];
        for(const value of values) {
            graphableData.push({
                "date": new Date(value.date),
                "value": value.daily_upload_count
            });
        }
        return graphableData;
    }

    makeLineGraph = (container, chartData) => {
        if (chartData == null) {
            container.textContent = "Data is not available yet.";
        }
        else if (chartData.length < 2) {
            container.textContent = "There is not enough data yet.";
        }
        else {
            let self = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(container, am4charts.XYChart);
                chart.data = chartData;
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