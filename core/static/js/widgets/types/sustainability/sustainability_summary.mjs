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
            console.log(data['results']);
            this.data = JSON.parse(data['results']);
            this.generate();
        });
    }

    generate() {
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        // Air Card
        let airGraphWrapper = document.createElement("div");
        airGraphWrapper.className = "col-sm-4";
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
        this.makeGraph(airGraph, this.data.air);

        // Animal Card
        let animalGraphWrapper = document.createElement("div");
        animalGraphWrapper.className = "col-sm-4";
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
        this.makeGraph(animalGraph, this.data.animal);

        // Efficiency Card
        let efficiencyGraphWrapper = document.createElement("div");
        efficiencyGraphWrapper.className = "col-sm-4";
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
        this.makeGraph(efficiencyGraph, this.data.efficiency);

        // Safety Card
        let safetyGraphWrapper = document.createElement("div");
        safetyGraphWrapper.className = "col-sm-4";
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
        this.makeGraph(safetyGraph, this.data.safety);

        // Land Card
        let landGraphWrapper = document.createElement("div");
        landGraphWrapper.className = "col-sm-4";
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
        this.makeGraph(landGraph, this.data.land);

        // Water Card
        let waterGraphWrapper = document.createElement("div");
        waterGraphWrapper.className = "col-sm-4";
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
        this.makeGraph(waterGraph, this.data.water);
    }

    prepData(data) {
        let dataCounter = {
            "excellent": 0, 
            "acceptable": 0,
            "needsWork": 0
        };
        
        for(const item of data){
            if (item.includes('a')) {
                dataCounter.excellent += 1;
            } else if (item.includes('b')) {
                dataCounter.acceptable += 1;
            } else if (item.includes('c')) {
                dataCounter.needsWork += 1;
            }
        }

        let graphableData = [{
            "sector": "Excellent",
            "size": dataCounter.excellent,
        },
        {
            "sector": "Acceptable",
            "size": dataCounter.acceptable,
        },
        {
            "sector": "Needs Work",
            "size": dataCounter.needsWork,
        }];

        return graphableData;
    }

    makeGraph(container, data) {
        if (data === null) {
            container.textContent = "Data is not available yet.";
        }
        else if (data.length == 0) {
            container.textContent = "(no data)";
        }
        else {
            let that = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                // var chart = am4core.create(that.container, am4charts.PieChart);
                var chart = am4core.create(container, am4charts.PieChart);

                chart.data = that.prepData(data);
                
                chart.innerRadius = am4core.percent(30);
                
                var pieSeries = chart.series.push(new am4charts.PieSeries());
                pieSeries.dataFields.value = "size";
                pieSeries.dataFields.category = "sector";
                pieSeries.slices.template.stroke = am4core.color("#fff");
                // pieSeries.slices.template.strokeWidth = 2;
                // pieSeries.slices.template.strokeOpacity = 1;

                pieSeries.colors.step = 2;
                // pieSeries.slices.template.propertyFields.fill = "color";

                pieSeries.labels.template.disabled = true;
                pieSeries.ticks.template.disabled = true;
                
                // pieSeries.hiddenState.properties.opacity = 1;
                // pieSeries.hiddenState.properties.endAngle = -90;
                // pieSeries.hiddenState.properties.startAngle = -90;

                chart.legend = new am4charts.Legend();
                chart.legend.position = "left";
                chart.legend.markers.template.width = 10;
                chart.legend.markers.template.height = 10;
                chart.legend.markers.template.children.getIndex(0).cornerRadius(20, 20, 20, 20);
                // chart.legend.maxHeight = 150;
                // chart.legend.maxWidth = 150;

            });
        }
    }
}