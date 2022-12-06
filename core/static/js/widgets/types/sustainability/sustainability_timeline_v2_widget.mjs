import { Widget } from "../../widget.mjs";
import { icons } from "../../../core/icons.mjs";
import { makeGaugeChart } from "../../../core/sustainability_utilities.mjs";

export class SustainabilityTimelineV2Widget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () => {
        const getSectorsByID = this.getData(
            "direct/sectors_id_to_name",
            {}
        ).then((data) => {
            this.sectorsIdToName = data.sectors_id_to_name;
        });
        const getSustainabilityResponseTimelineData = this.getData(
            "get_sustainability_response_timeline_data",
            {}
            ).then((data) => {
                this.timelineData = data.timeline_data;
                this.frame.innerHTML = "";
        });

        Promise.all([
            getSectorsByID, getSustainabilityResponseTimelineData
        ]).then(()=> {
            this.makeTimeline();
            // Auto disposing chart related objects and event handlers in case chart container is destroyed/replaced
            am4core.options.autoDispose = true;
        })
    }

    makeTimeline = () =>{
        let codyhouseContainer = document.createElement("codyhouse");
        let timelineContainer = document.createElement("div");
        timelineContainer.className = "js position-relative z-index-1 overflow-hidden padding-y-xl bg-contrast-lower";
        codyhouseContainer.appendChild(timelineContainer);

        let cdContainer = document.createElement("div");
        cdContainer.className = "container max-width-adaptive-lg";
        timelineContainer.appendChild(cdContainer);

        let cdTimeline = document.createElement("div");
        cdTimeline.className = "v-timeline v-timeline--icons js-v-timeline";
        cdTimeline.setAttribute("data-animation", "on");
        cdContainer.appendChild(cdTimeline);

        for(const matchAccount of this.timelineData){

            let section = document.createElement("section");
            section.className = "v-timeline__section js-v-timeline__section";

            let sectionHeader = document.createElement("div");
            sectionHeader.className = "v-timeline__marker bg-contrast-high border border-3 border-contrast-lower";
            section.append(sectionHeader);

            section.innerHTML = icons.plus;

            let itemsGroup = document.createElement("div");
            itemsGroup.className = "v-timeline__items-group";

            // create gauge chart div
            let itemDiv = document.createElement("div");
            itemDiv.className = "v-timeline__item bg radius-md shadow-xs card";

            let timeDiv = document.createElement("div");
            timeDiv.className = "v-timeline__date margin-bottom-sm";
            itemDiv.append(timeDiv);
            let timeE = document.createElement("time");
            let dateOnlyStr = new Date(matchAccount.date).toDateString();
            timeE.textContent =  dateOnlyStr;
            timeE.className = "v-timeline__date-value"
            timeDiv.append(timeE);

            let textComponent = document.createElement("div");
            textComponent.className = "card-header d-flex justify-content-between";
            itemDiv.append(textComponent);

            let title = document.createElement("h5");
            title.textContent = matchAccount.account_name + " [" + this.sectorsIdToName[matchAccount.account_sector_id] + "]";
            title.className = "h5";

            let scoreText = document.createElement("h4");
            scoreText.className = "d-inline text-c-green";
            scoreText.textContent = parseFloat(matchAccount.account_score_average).toFixed(2);
            let scoreIcon = document.createElement("i");
            scoreIcon.className = "fas fa-leaf text-c-green f-15";
            scoreIcon.style = "padding-right:10px";

            
            textComponent.append(title);
            if(matchAccount.account_score_average != 0){
                textComponent.append(scoreIcon);
                textComponent.append(scoreText);
            }

            let cardGraph = document.createElement("div");
            cardGraph.className = "card-body";
            itemDiv.append(cardGraph);
            makeGaugeChart(cardGraph, matchAccount.account_score_average, "Average Score", 0 , 35);

            itemsGroup.append(itemDiv);
            section.append(itemsGroup);
            cdTimeline.append(section);
        }

        this.frame.appendChild(codyhouseContainer);
        window.VTimeline(cdTimeline);
    }

}