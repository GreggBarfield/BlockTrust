import { Widget } from "../../widget.mjs";
import { getSustainabilitySections } from "../../../core/sustainability_sections.mjs";

export class AbstractBaseSummaryWidget extends Widget {
    constructor(frame) {
        super(frame);
        this.getResponseData();
        this.getSectorData();
    }

    /* Note: this will be called at the end of getSectorData()'s Promise
       
       This is left blank because the subclasses will need to override this method.
       If this is not done, then the other make charts methods will run before
       getResponseData() and getSectorData() have finished their Promises.
    */ 
    createCharts() {}

    getResponseData() {
        this.getData(
            "get_sustainability",
            {}
            ).then((data) => {
            this.responses = data.results;
            this.dataCounter = {};
            
            if (data.results.length > 0) {
                this.responseData = data.results[0];
                let sections = getSustainabilitySections();
                sections["total"] = "Total";

                for(const key in sections) {
                    this.dataCounter[key] = {
                        "excellent": 0,
                        "acceptable": 0,
                        "needsWork": 0
                    }

                    this.dataCounter[key].excellent = JSON.parse(this.responseData[key + "_excellent_score"]);
                    this.dataCounter[key].acceptable = JSON.parse(this.responseData[key + "_acceptable_score"]);
                    this.dataCounter[key].needsWork = JSON.parse(this.responseData[key + "_needsWork_score"]);
                }
            }
        });
    }

    getSectorData() {
        //This grabs the sector number for the current user pass in from dashboard.py.
        let sector = this.frame.getAttribute('data-widget-sector');

        this.getData(
            "data_request",
            {
                request: {
                    type: 'sustainability_averages',
                    params: {}
                }
            }
        ).then((data) => {
            let sectorData = data.result;
            this.dataCounter['this_sector'] = sectorData[sector]; 
            this.dataCounter['all_sectors'] = sectorData['allSectors'];

            this.createCharts();
        });
    }

    makeNewSurveyBtn() {
        let row = document.createElement("div");
        row.className = "row mb-2 flex-row-reverse";
        this.frame.appendChild(row);

        let btn = document.createElement("a");
        btn.className = "btn btn-outline-secondary btn-sm";
        btn.setAttribute("href", "/dashboard/sustainability/survey");
        btn.textContent = "New Survey";

        row.append(btn);
    }

    makeGraphOverTime(row) {
        let cardWrapper = document.createElement("div");
        cardWrapper.className = "col-md-6";
        let card = document.createElement("div");
        card.className = "card";
        cardWrapper.append(card);
        row.append(cardWrapper);

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

    makeAverageScoreGraph(row) {
        let susWrapper = document.createElement("div");
        susWrapper.className = "col-md-6";
        let susCard = document.createElement("div");
        susCard.className = "card";
        susWrapper.append(susCard);
        row.append(susWrapper);

        let susCardHeader = document.createElement("div");
        susCardHeader.className = "card-header";
        let cardHeaderRow = document.createElement("div");
        cardHeaderRow.className = "row";
        susCardHeader.append(cardHeaderRow);
        susCard.append(susCardHeader);
        
        let cardHeaderLabelWrapper = document.createElement("div");
        cardHeaderLabelWrapper.className = "col-sm-9";
        cardHeaderRow.append(cardHeaderLabelWrapper);
        let susCardHeaderLabel = document.createElement("h5");
        susCardHeaderLabel.textContent = "Sustainability Score";
        cardHeaderLabelWrapper.append(susCardHeaderLabel);
        
        let cardHeaderIconWrapper = document.createElement("div");
        cardHeaderIconWrapper.className = "col-sm-3";
        cardHeaderRow.append(cardHeaderIconWrapper);

        let cardHeaderIconText = document.createElement("h4");
        cardHeaderIconText.className = "d-inline text-c-green";
        cardHeaderIconText.textContent = "86";
        let cardHeaderIcon = document.createElement("i");
        cardHeaderIcon.className = "fas fa-leaf text-c-green f-15";
        cardHeaderIcon.style = "padding-right:10px";
        cardHeaderIconWrapper.append(cardHeaderIcon);
        cardHeaderIconWrapper.append(cardHeaderIconText);
        
        let susCardBody = document.createElement("div");
        susCardBody.className = "card-body";
        susCard.append(susCardBody);

        let susCardTabs = document.createElement("ul");
        susCardTabs.className = "nav nav-tabs";
        susCardTabs.id = "susTabs";
        susCardTabs.innerHTML = `
            <ul class="nav nav-tabs" id="susTab" role="tablist">
                <li class="nav-item">
                    <a class="nav-link active text-uppercase" href="#sector" id="sector-tab" data-toggle="tab"
                        role="tab" aria-controls="sector" aria-selected="true">This Sector</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-uppercase" href="#supply-chain" id="supply-chain-tab"
                        data-toggle="tab" role="tab" aria-controls="supply-chain" aria-selected="false">
                        Supply Chain</a>
                </li>
            </ul>
        `;

        susCardBody.append(susCardTabs);

        let susTabContent = document.createElement("div");
        susTabContent.className = "tab-content";
        susCardBody.append(susTabContent);

        let susGraph = document.createElement("div");
        susGraph.id = "sector";
        susGraph.className = "tab-pane fade show active";
        susTabContent.append(susGraph);
        this.makeGraph(susGraph, "this_sector");

        let supplyChainGraph = document.createElement("div");
        supplyChainGraph.id = "supply-chain";
        supplyChainGraph.className = "tab-pane fade";
        susTabContent.append(supplyChainGraph);
        this.makeGraph(supplyChainGraph, "all_sectors");
    }

    makeOtherPieGraphs(sections) {

        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        // loop through all sections and create a graph for each section
        for(const key in sections) {
            let graphWrapper = document.createElement("div");
            graphWrapper.className = "col-md-4";
            let graphCard = document.createElement("div");
            graphCard.className = "card";
            graphWrapper.append(graphCard);
            row.append(graphWrapper);

            let graphHeader = document.createElement("h5");
            graphHeader.className = "card-header";
            graphHeader.textContent = sections[key];
            graphCard.append(graphHeader);
            
            let graph = document.createElement("div");
            graph.className = "card-body px-3";
            graphCard.append(graph);
            this.makeGraph(graph, key);
        }
    }

    getGraphablePieData(dataType) {
        let graphableData = [{
                "sector": "Excellent",
                "size": this.dataCounter[dataType].excellent,
                "color": am4core.color("#008000")
            },
            {
                "sector": "Acceptable",
                "size": this.dataCounter[dataType].acceptable,
                "color": am4core.color("#0000FF")
            },
            {
                "sector": "Needs Work",
                "size": this.dataCounter[dataType].needsWork,
                "color": am4core.color("#C00000")
        }];

        return graphableData;
    }

    getGraphableLineData() {
        let graphableData = [];

        // Right now just takes the sum of the excellent scores
        // TODO: will change in the future this is a placeholder for now.
        for(const response of this.responses) {
            let valueCounter = 0;
            let jsonResponse = JSON.parse(response.response);

            for(const index in jsonResponse){
                for(const item of jsonResponse[index]){
                    if (item.includes('a')) {
                        valueCounter += 1;
                    }
                }
            }

            graphableData.push({
                "date": new Date(response.created_timestamp),
                "value": valueCounter
            });
        }

        return graphableData;
    }

    makeLineGraph(container) {
        if (this.responses == null) {
            container.textContent = "Data is not available yet.";
        }
        else if (this.responses.length < 2) {
            container.textContent = "There is not enough data yet.";
        }
        else {
            let self = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(container, am4charts.XYChart);

                chart.data = self.getGraphableLineData();

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

    makeGraph(container, dataType) {
        if (this.dataCounter == null 
            || this.dataCounter == {} 
            || this.dataCounter[dataType] == null) {
            container.textContent = "Data is not available yet.";
        }
        else if (this.dataCounter[dataType].length == 0) {
            container.textContent = "(no data)";
        }
        else {
            let self = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(container, am4charts.PieChart);

                chart.data = self.getGraphablePieData(dataType);
                
                chart.innerRadius = am4core.percent(30);
                
                var pieSeries = chart.series.push(new am4charts.PieSeries());
                pieSeries.dataFields.value = "size";
                pieSeries.dataFields.category = "sector";
                pieSeries.slices.template.propertyFields.fill = "color";
                pieSeries.slices.template.stroke = am4core.color("#fff");

                pieSeries.colors.step = 2;

                pieSeries.labels.template.disabled = true;
                pieSeries.ticks.template.disabled = true;

                chart.legend = new am4charts.Legend();
                chart.legend.position = "left";
                chart.legend.markers.template.width = 10;
                chart.legend.markers.template.height = 10;
                chart.legend.markers.template.children.getIndex(0).cornerRadius(20, 20, 20, 20);
            });
        }
    }

}