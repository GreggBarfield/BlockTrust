import { Widget } from "../../widget.mjs";
import { makeAverageScoreGaugeCharts, makeSectionalGaugeCharts } from "../../utilities/sustainability_utilities.mjs";

export class AccountSustainabilityScores extends Widget{
     constructor(frame){
        super(frame);
    }

    initType = () => {
        this.frame.innerHTML = "";
        this.accountID = this.frame.getAttribute("data-widget-account-id");
        this.getSustainabilityScoresForAccount();
    }

    getSustainabilityScoresForAccount = async() => {
        let accountSustainabilityScores = await this.getData("get_account_sustainability_data",{account_id: this.accountID, scores_only: true});
        this.accountScores = accountSustainabilityScores.account_sustainability_section_and_scores;
        this.accountSectorID = accountSustainabilityScores.account_sector_id;
        
        let globalSustainabilityScores = await this.getData("data_request",{request: {type: 'sustainability_response_averages', params: {} }});
        this.globalAverages = globalSustainabilityScores.result;
        
        let sectorsByName = await this.getData("direct/sectors_name_to_id");
        this.sectorsNameToId = sectorsByName.sectors_name_to_id;
        this.createScoreCharts();
    }

    createScoreCharts = () => {
        let row = document.createElement("div");
        row.className = "row";
        this.frame.appendChild(row);

        makeAverageScoreGaugeCharts(row, "Account Score: ", this.accountSectorID, this.sectorsNameToId, this.accountScores, this.globalAverages);
        makeSectionalGaugeCharts(this.frame, "Account Score: ", this.accountSectorID, this.sectorsNameToId, this.accountScores, this.globalAverages);
    }
}