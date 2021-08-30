import { Widget } from "../../widget.mjs";

export class SustainabilitySummaryWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        
        this.getData(
            "get_sustainability",
            {}
            ).then((data) => {
            this.frame.innerHTML = "";
            console.log(data);
            this.responses = data;
            this.data = JSON.parse(data.results[0].response);
            this.prepData();

            let row = document.createElement("div");
            row.className = "row";
            this.frame.appendChild(row);
    
            this.makeAverageScoreGraph(row);
            this.makeGraphOverTime(row);
            this.makeOtherPieGraphs();
        });
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

        let timeLineGraph = document.createElement("div");
        cardBody.append(timeLineGraph);
        this.makeTimeLineGraph(timeLineGraph);
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
        let susCardHeaderLabel = document.createElement("h5");
        susCardHeaderLabel.textContent = "Sustainability Score";
        susCardHeader.append(susCardHeaderLabel);
        susCard.append(susCardHeader);
        
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
        this.makeGraph(susGraph, "all");

        let supplyChainGraph = document.createElement("div");
        supplyChainGraph.id = "supply-chain";
        supplyChainGraph.className = "tab-pane fade";
        susTabContent.append(supplyChainGraph);
        this.makeGraph(supplyChainGraph, "all");
    }

    makeOtherPieGraphs() {
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        // Air Card
        let airGraphWrapper = document.createElement("div");
        airGraphWrapper.className = "col-md-4";
        let airGraphCard = document.createElement("div");
        airGraphCard.className = "card";
        airGraphWrapper.append(airGraphCard);
        row.append(airGraphWrapper);

        let airGraphHeader = document.createElement("h5");
        airGraphHeader.className = "card-header";
        airGraphHeader.textContent = "Air & Greenhouse Gas Emissions";
        airGraphCard.append(airGraphHeader);
        
        let airGraph = document.createElement("div");
        airGraph.className = "card-body";
        airGraphCard.append(airGraph);
        this.makeGraph(airGraph, "air");

        // Animal Card
        let animalGraphWrapper = document.createElement("div");
        animalGraphWrapper.className = "col-md-4";
        let animalGraphCard = document.createElement("div");
        animalGraphCard.className = "card";
        animalGraphWrapper.append(animalGraphCard);
        row.append(animalGraphWrapper);

        let animalGraphHeader = document.createElement("h5");
        animalGraphHeader.className = "card-header";
        animalGraphHeader.textContent = "Animal Health & Well-Being";
        animalGraphCard.append(animalGraphHeader);
        
        let animalGraph = document.createElement("div");
        animalGraph.className = "card-body";
        animalGraphCard.append(animalGraph);
        this.makeGraph(animalGraph, "animal");

        // Efficiency Card
        let efficiencyGraphWrapper = document.createElement("div");
        efficiencyGraphWrapper.className = "col-md-4";
        let efficiencyGraphCard = document.createElement("div");
        efficiencyGraphCard.className = "card";
        efficiencyGraphWrapper.append(efficiencyGraphCard);
        row.append(efficiencyGraphWrapper);

        let efficiencyGraphHeader = document.createElement("h5");
        efficiencyGraphHeader.className = "card-header";
        efficiencyGraphHeader.textContent = "Efficiency & Yield";
        efficiencyGraphCard.append(efficiencyGraphHeader);
        
        let efficiencyGraph = document.createElement("div");
        efficiencyGraph.className = "card-body";
        efficiencyGraphCard.append(efficiencyGraph);
        this.makeGraph(efficiencyGraph, "efficiency");

        // Safety Card
        let safetyGraphWrapper = document.createElement("div");
        safetyGraphWrapper.className = "col-md-4";
        let safetyGraphCard = document.createElement("div");
        safetyGraphCard.className = "card";
        safetyGraphWrapper.append(safetyGraphCard);
        row.append(safetyGraphWrapper);

        let safetyGraphHeader = document.createElement("h5");
        safetyGraphHeader.className = "card-header";
        safetyGraphHeader.textContent = "Employee Safety";
        safetyGraphCard.append(safetyGraphHeader);
        
        let safetyGraph = document.createElement("div");
        safetyGraph.className = "card-body";
        safetyGraphCard.append(safetyGraph);
        this.makeGraph(safetyGraph, "safety");

        // Land Card
        let landGraphWrapper = document.createElement("div");
        landGraphWrapper.className = "col-md-4";
        let landGraphCard = document.createElement("div");
        landGraphCard.className = "card";
        landGraphWrapper.append(landGraphCard);
        row.append(landGraphWrapper);

        let landGraphHeader = document.createElement("h5");
        landGraphHeader.className = "card-header";
        landGraphHeader.textContent = "Employee land";
        landGraphCard.append(landGraphHeader);
        
        let landGraph = document.createElement("div");
        landGraph.className = "card-body";
        landGraphCard.append(landGraph);
        this.makeGraph(landGraph, "land");

        // Water Card
        let waterGraphWrapper = document.createElement("div");
        waterGraphWrapper.className = "col-md-4";
        let waterGraphCard = document.createElement("div");
        waterGraphCard.className = "card";
        waterGraphWrapper.append(waterGraphCard);
        row.append(waterGraphWrapper);

        let waterGraphHeader = document.createElement("h5");
        waterGraphHeader.className = "card-header";
        waterGraphHeader.textContent = "Employee water";
        waterGraphCard.append(waterGraphHeader);
        
        let waterGraph = document.createElement("div");
        waterGraph.className = "card-body";
        waterGraphCard.append(waterGraph);
        this.makeGraph(waterGraph, "water");
    }

    prepData() {
        this.dataCounter = {
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
                    this.dataCounter[item].excellent += 1;
                    totals.excellent += 1;
                } else if (response.includes('b')) {
                    this.dataCounter[item].acceptable += 1;
                    totals.acceptable += 1;
                } else if (response.includes('c')) {
                    this.dataCounter[item].needsWork += 1;
                    totals.needsWork += 1;
                }
            }
        }

        this.dataCounter["all"] = totals;
        this.data["all"] = [totals.excellent, totals.acceptable, totals.needsWork];

        console.log(this.dataCounter);
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

    getGraphableTimeLineData() {
        // for(const response in this.responses)

        // let graphableData = [{
        //     "date": ,
        //     "price": 
        // },
        // {

        // },
        // ]

    }

    makeTimeLineGraph(container) {
        if (this.responses == null) {
            container.textContent = "Data is not available yet.";
        }
        else if (this.responses.length < 2) {
            container.textContent = "(not data)";
        }
        else {
            let that = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(container, am4charts.XYChart);

                chart.data = that.getGraphableTimeLineData();
                
                // Create axes
                var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                dateAxis.renderer.grid.template.location = 1;
                dateAxis.renderer.grid.template.disabled = false;
                dateAxis.startLocation = 1.6;
                dateAxis.endLocation = 0.4;
                dateAxis.renderer.labels.template.disabled = false;
                dateAxis.renderer.inside = true;

                var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis.logarithmic = false;
                valueAxis.renderer.minGridDistance = 20;
                valueAxis.renderer.grid.template.disabled = false;
                valueAxis.renderer.inside = true;
                valueAxis.renderer.labels.template.disabled = false;

                // Create series
                var series = chart.series.push(new am4charts.LineSeries());
                series.dataFields.valueY = "price";
                series.dataFields.dateX = "date";
                series.strokeWidth = 3;
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
                chart.padding(0, 0, 0, 0);
            });
        }
    }

    makeGraph(container, dataType) {
        if (this.data[dataType] == null) {
            container.textContent = "Data is not available yet.";
        }
        else if (this.data[dataType].length == 0) {
            container.textContent = "(no data)";
        }
        else {
            let that = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(container, am4charts.PieChart);

                chart.data = that.getGraphablePieData(dataType);
                
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