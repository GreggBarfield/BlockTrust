import { Widget } from "../../widget.mjs";
import { sections, calculateSustainabilityQuestionnaireMaxScores } from "../../../core/sustainability_constants.mjs";
import { makeGaugeChart } from "../../../core/sustainability_utilities.mjs";

export class AccountSustainabilityScores extends Widget{
     constructor(frame){
        super(frame);
    }

    initType = () => {
        this.frame.innerHTML = "";
        this.accountID = this.frame.getAttribute("data-widget-account-id");
        this.getSustainabilityScoresForAccount();
    }

    getSustainabilityScoresForAccount = () => {
        const getAccountSustainabilityScores = this.getData(
            "get_account_sustainability_scores",
            {
                account_id: this.accountID
            }
        ).then((data) => {
            this.accountAverages = data.account_sustainability_section_and_score_averages;
            this.accountSectorID = data.account_sector_id;
        });
        const getGlobalSustainabilityScores = this.getData(
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
            getAccountSustainabilityScores, getGlobalSustainabilityScores, getSectorsByName
        ]).then(()=> {
            this.createScoreCharts();
        })
    }

    createScoreCharts = () => {
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        this.makeAverageScoreGaugeCharts(row, this.accountSectorID);
        this.makeSectionalGaugeCharts(this.accountSectorID);
    }

    makeAverageScoreGaugeCharts = (row, sectorID) => {
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
        cardHeaderIconText.textContent = "Account Score: "+parseFloat(accountSustainabilityScoreAverage).toFixed(2)+ " |Global Score: " + parseFloat(globalSustainabilityScoreAverageForSector).toFixed(2);
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

        makeGaugeChart(accountChart, accountSustainabilityScoreAverage, "Average Total Score", 0 , currentSectorTotalScore);
        makeGaugeChart(globalChart, globalSustainabilityScoreAverageForSector, "Global Average Total Score", 0, currentSectorTotalScore);
    }

    makeSectionalGaugeCharts = (sectorID) => {
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
                cardHeaderIconText.textContent = "Account Score: "+parseFloat(this.accountAverages[section.name+"_average"]).toFixed(2)+ " |Global Score: " + parseFloat(this.globalAverages[sectorID][section.name+"_average"]).toFixed(2);
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
                
                makeGaugeChart(accountChart, this.accountAverages[section.name+"_average"], "Account Average Score", 0 , sectionalTotals[section.name]);
                makeGaugeChart(globalChart, this.globalAverages[sectorID][section.name+"_average"], "Global Average Score", 0, sectionalTotals[section.name]);
            }
            
        }
    }
}