import { sections, calculateSustainabilityQuestionnaireMaxScores } from "./sustainability_constants.mjs";

const makeGaugeChart = (container, data, title, gaugeMin, gaugeMax) =>{
    am4core.ready(function() {
    am4core.useTheme(am4themes_animated);

    // create chart
    var chart = am4core.create(container, am4charts.GaugeChart);
    chart.innerRadius = -15;
    let label = chart.chartContainer.createChild(am4core.Label);
    label.text = title;
    label.align = "center";

    var axis = chart.xAxes.push(new am4charts.ValueAxis());
    axis.min = gaugeMin;
    axis.max = gaugeMax;
    axis.strictMinMax = true;

    var gradient = new am4core.LinearGradient();
    gradient.stops.push({color:am4core.color("red")});
    gradient.stops.push({color:am4core.color("#42f572")});

    axis.renderer.line.stroke = gradient;
    axis.renderer.line.strokeWidth = 15;
    axis.renderer.line.strokeLinecap = "round";
    axis.renderer.line.strokeOpacity = 0.90;

    var hand = chart.hands.push(new am4charts.ClockHand());
    hand.radius = am4core.percent(100);
    hand.startWidth = 16;
    hand.pin.radius = 8;
    hand.parent.zIndex = 100;

    // Setting an interval to display the gauge pointer transition animation instead of directly setting the gauge pointer
    setInterval(function() {
        hand.showValue(data, 1000, am4core.ease.cubicOut);
        }, 2000);
    });
}

const makeAverageScoreGaugeCharts = (row, scoreLabel, sectorID, sectorsNameToId, accountScores, globalAverages) => {
    let globalSustainabilityScoreAverageForSector = 0;
    let sectorBasedSectionalTotals = calculateSustainabilityQuestionnaireMaxScores(sectorsNameToId);
    let sectionalTotals = sectorBasedSectionalTotals[sectorID];
    

    for(let section of Object.values(sections)){
        // Ensuring that the sustainability section exists for the particular sector
        if(section.name in sectionalTotals){
            globalSustainabilityScoreAverageForSector+= globalAverages[sectorID][section.name+"_average"];
        }
    }
    let currentSectorTotalScore = sectorBasedSectionalTotals[sectorID]["total"];
    let accountSustainabilityScore = accountScores["total_score"];

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
    cardHeaderIconText.textContent = scoreLabel+parseFloat(accountSustainabilityScore).toFixed(2)+ " |Global Score: " + parseFloat(globalSustainabilityScoreAverageForSector).toFixed(2);
    let cardHeaderIcon = document.createElement("i");
    cardHeaderIcon.className = "fas fa-leaf text-c-green f-15";
    cardHeaderIcon.style = "padding-right:10px";
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

    makeGaugeChart(accountChart, accountSustainabilityScore, "Average Total Score", 0 , currentSectorTotalScore);
    makeGaugeChart(globalChart, globalSustainabilityScoreAverageForSector, "Global Average Total Score", 0, currentSectorTotalScore);
}

const makeSectionalGaugeCharts = (row, scoreLabel, sectorID, sectorsNameToId, accountScores, globalAverages) => {
    let sectionalScoresContainer = document.createElement("div");
    sectionalScoresContainer.className = "row";
    row.appendChild(sectionalScoresContainer);
    let sectorBasedSectionalTotals = calculateSustainabilityQuestionnaireMaxScores(sectorsNameToId);
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
            sectionalScoresContainer.append(chartWrapper);

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
            cardHeaderIconText.textContent = scoreLabel+parseFloat(accountScores[section.name+"_score"]).toFixed(2)+ " |Global Score: " + parseFloat(globalAverages[sectorID][section.name+"_average"]).toFixed(2);
            let cardHeaderIcon = document.createElement("i");
            cardHeaderIcon.className = "fas fa-leaf text-c-green f-15";
            cardHeaderIcon.style = "padding-right:10px";
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
            
            makeGaugeChart(accountChart, accountScores[section.name+"_score"], "Account Average Score", 0 , sectionalTotals[section.name]);
            makeGaugeChart(globalChart, globalAverages[sectorID][section.name+"_average"], "Global Average Score", 0, sectionalTotals[section.name]);
        }
        
    }
}


export {
    makeGaugeChart,
    makeAverageScoreGaugeCharts,
    makeSectionalGaugeCharts
}