import { Widget } from "../../widget.mjs";
import { icons } from "../../../core/icons.mjs";

export class SustainabilityTimelineV2Widget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () => {
        const getSectorsByID = this.getData(
            "direct/sectors_by_id",
            {}
        ).then((data) => {
            this.sectorsByID = data.sectors_by_id;
        });
        const getSustainabilityResponseTimelineData = this.getData(
            "get_sustainability_response_timeline_data",
            {}
            ).then((data) => {
                this.timelineData = data.timeline_data;
                this.timelineDataOrder = data.order;
                this.frame.innerHTML = "";
        });

        Promise.all([
            getSectorsByID, getSustainabilityResponseTimelineData
        ]).then(()=> {
            this.makeTimeline();
            // Auto disposing chart related object and event handlers in case chart container is destroyed/replaced
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

        for(const order of this.timelineDataOrder){
            let matchAccount = this.timelineData[order];

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
            title.textContent = matchAccount.account_name + " [" + this.sectorsByID[matchAccount.account_sector_id] + "]";
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
            this.makeGaugeChart(cardGraph, matchAccount.account_score_average, "Average Score", 0 , 35);

            itemsGroup.append(itemDiv);
            section.append(itemsGroup);
            cdTimeline.append(section);
        }

        this.frame.appendChild(codyhouseContainer);
        window.VTimeline(cdTimeline);
    }

    makeGaugeChart = (container, data, title, gaugeMin, gaugeMax) =>{
        if(data == 0){
            container.textContent = "( No data )"
        }
        else{
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
    
                setInterval(function() {
                    hand.showValue(data, 1000, am4core.ease.cubicOut);
                }, 2000);
            });
        }
        
    }

}