import { Widget } from "../../widget.mjs";
import { sections, calculateSustainabilityQuestionnaireMaxScores } from "../../../core/sustainability_constants.mjs";
import { makeGaugeChart } from "../../../core/sustainability_utilities.mjs";

export class BaseSummaryV2Widget extends Widget {
    constructor(frame) {
        super(frame);
        this.dataCounter = {};
        this.getSustainabilityData();
    }
    createCharts() {}

    getSustainabilityData = () =>{
        const getAccountSustainabilityData = this.getData(
            "get_account_sustainability_data"
        ).then((data) => {
            this.accountAverages = data.account_sustainability_section_and_score_averages;
            this.accountSustainabilityResponses = data.account_sustainability_responses 
        });
        const getGlobalSustainabilityData = this.getData(
            "data_request",
            {
                request: {type: 'sustainability_response_averages', params: {} }
            }
        ).then((data) => {
            this.globalAverages = data.result;
        }); 
        const getSectorsByName = this.getData(
            "direct/sectors_name_to_id"
        ).then((data) => {
            this.sectorsNameToId = data.sectors_name_to_id
        })
        Promise.all([
            getAccountSustainabilityData, getGlobalSustainabilityData, getSectorsByName
        ]).then(()=> {
            this.createCharts();
        })
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

    makeAverageScoreGaugeCharts = (row, sectorID) =>{
        let globalSustainabilityScoreAverageForSector = 0;
        let sectorBasedSectionalTotals = calculateSustainabilityQuestionnaireMaxScores(this.sectorsNameToId);
        let sectionalTotals = sectorBasedSectionalTotals[sectorID];
        

        for(let section of Object.values(sections)){
            // Ensuring that the sustainability section exists for the particular sector
            if(section.name in sectionalTotals){
                globalSustainabilityScoreAverageForSector+= this.globalAverages[sectorID][section.name+"_average"];
            }
        }
        let currentSectorTotalScore = sectorBasedSectionalTotals[sectorID]["total"];
        let accountSustainabilityScoreAverage = this.accountAverages["score_average"];

        let chartWrapper = document.createElement("div");
        chartWrapper.className = "col-md-6";
        row.append(chartWrapper);

        let chartCard = document.createElement("div");
        chartCard.className = "card";
        let chartCardBody = document.createElement("div");
        chartCardBody.className = "card-body d-flex";
        chartWrapper.append(chartCard);

        let chartHeader = document.createElement("div");
        chartHeader.className = "card-header";
        let chartHeaderRow = document.createElement("div");
        chartHeaderRow.className = "row";
        chartHeader.append(chartHeaderRow);
        
        let chartHeaderLabelWrapper = document.createElement("div");
        chartHeaderLabelWrapper.className = "col-sm-4";
        chartHeaderRow.append(chartHeaderLabelWrapper);
        let chartHeaderLabel = document.createElement("h5");
        chartHeaderLabel.textContent = "Sustainability Score";
        chartHeaderLabelWrapper.append(chartHeaderLabel);
        
        let cardHeaderIconWrapper = document.createElement("div");
        cardHeaderIconWrapper.className = "col-sm-8";
        chartHeaderRow.append(cardHeaderIconWrapper);

        let cardHeaderIconText = document.createElement("h6");
        cardHeaderIconText.className = "d-inline text-c-green";
        cardHeaderIconText.textContent = "Your Score: "+parseFloat(accountSustainabilityScoreAverage).toFixed(2)+ " |Global Score: " + parseFloat(globalSustainabilityScoreAverageForSector).toFixed(2);
        let cardHeaderIcon = document.createElement("i");
        cardHeaderIcon.className = "fas fa-leaf text-c-green f-15 pr-2";
        cardHeaderIconWrapper.append(cardHeaderIcon);
        cardHeaderIconWrapper.append(cardHeaderIconText);
        
        chartCard.append(chartHeader);
        chartCard.append(chartCardBody);

        let accountChart = document.createElement("div");
        accountChart.className = "col-md-6";
        chartCardBody.append(accountChart);

        let globalChart = document.createElement("div");
        globalChart.className = "col-md-6";
        chartCardBody.append(globalChart);

        makeGaugeChart(accountChart, accountSustainabilityScoreAverage, "Your Average Total Score", 0 , currentSectorTotalScore);
        makeGaugeChart(globalChart, globalSustainabilityScoreAverageForSector, "Global Average Total Score", 0, currentSectorTotalScore);
    }

    makeSectionalGaugeCharts = (sectorID) =>{
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);
        let sectorBasedSectionalTotals = calculateSustainabilityQuestionnaireMaxScores(this.sectorsNameToId);
        let sectionalTotals = sectorBasedSectionalTotals[sectorID]

        // loop through all sections and create a graph for each section
        for(let section of Object.values(sections)) {
            // Ensuring that the sustainability section exists for the particular sector
            if(section.name in sectionalTotals){
                let chartWrapper = document.createElement("div");
                chartWrapper.className = "col-md-6";
                let chartCard = document.createElement("div");
                chartCard.className = "card";
                let chartCardBody = document.createElement("div");
                chartCardBody.className = "card-body d-flex";
                chartWrapper.append(chartCard);
                row.append(chartWrapper);

                let chartHeader = document.createElement("h5");
                chartHeader.className = "card-header";
                let chartHeaderRow = document.createElement("div");
                chartHeaderRow.className = "row";
                chartHeader.append(chartHeaderRow);
        
                let chartHeaderLabelWrapper = document.createElement("div");
                chartHeaderLabelWrapper.className = "col-sm-4";
                chartHeaderRow.append(chartHeaderLabelWrapper);
                let chartHeaderLabel = document.createElement("h5");
                chartHeaderLabel.textContent = section.header;
                chartHeaderLabelWrapper.append(chartHeaderLabel);
        
                let cardHeaderIconWrapper = document.createElement("div");
                cardHeaderIconWrapper.className = "col-sm-8";
                chartHeaderRow.append(cardHeaderIconWrapper);

                let cardHeaderIconText = document.createElement("h6");
                cardHeaderIconText.className = "d-inline text-c-green";
                cardHeaderIconText.textContent = "Your Score: "+parseFloat(this.accountAverages[section.name+"_average"]).toFixed(2)+ " |Global Score: " + parseFloat(this.globalAverages[sectorID][section.name+"_average"]).toFixed(2);
                let cardHeaderIcon = document.createElement("i");
                cardHeaderIcon.className = "fas fa-leaf text-c-green f-15 pr-2";
                cardHeaderIconWrapper.append(cardHeaderIcon);
                cardHeaderIconWrapper.append(cardHeaderIconText);

                chartCard.append(chartHeader);
                chartCard.append(chartCardBody);
            
                let accountChart = document.createElement("div");
                accountChart.className = "col-md-6";
                chartCardBody.append(accountChart);

                let globalChart = document.createElement("div");
                globalChart.className = "col-md-6";
                chartCardBody.append(globalChart);
                
                makeGaugeChart(accountChart, this.accountAverages[section.name+"_average"], "Your Average Score", 0 , sectionalTotals[section.name]);
                makeGaugeChart(globalChart, this.globalAverages[sectorID][section.name+"_average"], "Global Average Score", 0, sectionalTotals[section.name]);
            }
            
        }
    }

}