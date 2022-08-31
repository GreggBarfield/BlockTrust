import { Widget } from "../../widget.mjs";

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
                this.data = data;
                this.timelineData = data.timeline_data;
                this.timelineDataOrder = data.order;
                this.frame.innerHTML = "";
        });

        Promise.all([
            getSectorsByID, getSustainabilityResponseTimelineData
        ]).then(()=> {
            this.makeTimeline(); 
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

        let fasStyle = "font-size: 24px;text-align: center;position: absolute;left: 0px;top: 0px;height: 100%;width: 100%;line-height: 40px;vertical-align: middle;";
        var icons = {
            warning: '<div class="v-timeline__marker bg-primary border border-3 border-bg shadow-xs" aria-hidden="true"><svg class="icon icon--sm color-white" viewBox="0 0 24 24"><title>o-warning</title><g><path d="M23.707,6.736,17.263.293A1,1,0,0,0,16.556,0H7.444a1,1,0,0,0-.707.293L.293,6.736A1,1,0,0,0,0,7.443v9.114a1,1,0,0,0,.293.707l6.444,6.443A1,1,0,0,0,7.444,24h9.112a1,1,0,0,0,.707-.293l6.444-6.443A1,1,0,0,0,24,16.557V7.443A1,1,0,0,0,23.707,6.736ZM13.645,5,13,14H11l-.608-9ZM12,20a2,2,0,1,1,2-2A2,2,0,0,1,12,20Z"></path></g></svg></div>',
            image: '<div class="v-timeline__marker bg-primary border border-3 border-bg shadow-xs" aria-hidden="true"><svg class="icon icon--sm color-white" viewBox="0 0 24 24"><g><path d="M22,1H2A1,1,0,0,0,1,2V22a1,1,0,0,0,1,1H22a1,1,0,0,0,1-1V2A1,1,0,0,0,22,1ZM21,21H3V3H21Z"></path><path d="M6,19H18a1,1,0,0,0,.895-1.447l-4-8a1,1,0,0,0-.735-.54.984.984,0,0,0-.867.28l-8,8A1,1,0,0,0,6,19Z"></path><circle cx="8" cy="8" r="2"></circle></g></svg></div>',
            bug: '<div class="v-timeline__marker bg-accent border border-3 border-bg shadow-xs" aria-hidden="true"><svg class="icon icon--sm color-white" viewBox="0 0 24 24"><g><path d="M12,3A8.964,8.964,0,0,1,16,3.951a4,4,0,0,0-7.99,0A8.964,8.964,0,0,1,12,3Z"></path><path d="M24,7V6H22V7a2,2,0,0,1-2,2h-.589A7.992,7.992,0,0,0,4.589,9H4A2,2,0,0,1,2,7V6H0V7a4,4,0,0,0,4,4h.069A8.047,8.047,0,0,0,4,12v1H0v2H4v1a8.047,8.047,0,0,0,.069,1H4a4,4,0,0,0-4,4v1H2V21a2,2,0,0,1,2-2h.589a7.992,7.992,0,0,0,14.822,0H20a2,2,0,0,1,2,2v1h2V21a4,4,0,0,0-4-4h-.069A8.047,8.047,0,0,0,20,16V15h4V13H20V12a8.047,8.047,0,0,0-.069-1H20A4,4,0,0,0,24,7Z"></path></g></svg></div>',
            flag: '<div class="v-timeline__marker bg-contrast-high border border-3 border-bg shadow-xs" aria-hidden="true"><svg class="icon icon--sm color-white" viewBox="0 0 24 24"><g><path d="M2,0C1.448,0,1,0.448,1,1v22c0,0.552,0.448,1,1,1s1-0.448,1-1V1C3,0.448,2.552,0,2,0z"></path> <path d="M23,2H6C5.448,2,5,2.448,5,3v12c0,0.552,0.448,1,1,1h17l-3-7L23,2z"></path></g></svg></div>',
            activity: '<div class="v-timeline__marker bg-accent border border-3 border-bg shadow-xs" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg></div>',
            healthIcon: '<div class="v-timeline__marker bg-accent border border-3 border-bg shadow-xs" aria-hidden="true">\
                <i class="icon icon--sm color-white fas fa-notes-medical" icon="" style="' + fasStyle + '"></i>\
                </div>',
            archive: '<div class="v-timeline__marker bg-accent border border-3 border-bg shadow-xs" aria-hidden="true">\
                <i class="icon icon--sm color-white fas fa-archive" icon="" style="' + fasStyle + '"></i>\
                </div>',
            sighting: '<div class="v-timeline__marker bg-primary border border-3 border-bg shadow-xs" aria-hidden="true">\
                <i class="icon icon--sm color-white fas fa-eye" icon="" style="' + fasStyle + '"></i>\
                </div>',
            plus: '<div class="v-timeline__marker bg-accent border border-3 border-bg shadow-xs" aria-hidden="true">\
                <i class="icon icon--sm color-white fas fa-plus" icon="" style="' + fasStyle + '"></i>\
                </div>',
            carrot: '<div class="v-timeline__marker bg-contrast-high border border-3 border-bg shadow-xs" aria-hidden="true">\
                <i class="icon icon--sm color-white fas fa-carrot" icon="" style="' + fasStyle + '"></i>\
                </div>',
            
        };

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