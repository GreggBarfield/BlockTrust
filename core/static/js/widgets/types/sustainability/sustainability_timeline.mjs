import { Widget } from "../../widget.mjs";
import { InfoModal } from "../../../core/info_modal.mjs";

export class SustainabilityTimelineWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.getData(
            "get_sustainability_timeline_data",
            {}
            ).then((data) => {
            this.frame.innerHTML = "";
            this.matches = data.timeline_data;
            this.match_ordering = data.order;
        
            this.prepData();
            this.makeTimeLineChart();
            am4core.options.autoDispose = true;
        });

    }

    makeTimeLineChart(){
        let codyhouseContainer = document.createElement("codyhouse");
        let timelineContainer = document.createElement("div");
        timelineContainer.className = "js position-relative z-index-1 overflow-hidden padding-y-xl bg-contrast-lower";
        codyhouseContainer.appendChild(timelineContainer);

        let cd_container = document.createElement("div");
        cd_container.className = "container max-width-adaptive-lg";
        timelineContainer.appendChild(cd_container);

        let cd_timeline = document.createElement("div");
        cd_timeline.className = "v-timeline v-timeline--icons js-v-timeline";
        cd_timeline.setAttribute("data-animation", "on");
        cd_container.appendChild(cd_timeline);

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

        // Render
        for (const id of this.match_ordering) {
            let match = this.matches[id];

            let section = document.createElement("section");
            section.className = "v-timeline__section js-v-timeline__section";

            let sectionHeader = document.createElement("div");
            sectionHeader.className = "v-timeline__marker bg-contrast-high border border-3 border-contrast-lower";
            section.append(sectionHeader);

            section.innerHTML = icons.plus;

            let itemsGroup = document.createElement("div");
            itemsGroup.className = "v-timeline__items-group";

            // make card
            let itemDiv = document.createElement("div");
            itemDiv.className = "v-timeline__item bg radius-md shadow-xs card";

            let timeDiv = document.createElement("div");
            timeDiv.className = "v-timeline__date margin-bottom-sm";
            itemDiv.append(timeDiv);
            let timeE = document.createElement("time");
            let dateOnlyStr = new Date(match.date).toDateString();
            timeE.textContent = dateOnlyStr;
            timeE.className = "v-timeline__date-value"
            timeDiv.append(timeE);

            let textComponent = document.createElement("div");
            textComponent.className = "card-header d-flex justify-content-between";
            itemDiv.append(textComponent);

            let title = document.createElement("h5");
            title.textContent = match.name + " " + this.getSectorNameById(match.sector);
            title.className = "h5";
            textComponent.append(title);

            let titleLink = document.createElement("button");
            titleLink.className = "btn btn-sm btn-link shadow-none color-primary";
            titleLink.textContent = "See detail";
            titleLink.addEventListener("click", () => {
                this.openModal(match);
            });
            textComponent.append(titleLink);

            let cardGraph = document.createElement("div");
            cardGraph.className = "card-body";
            itemDiv.append(cardGraph);
            this.makeGraph(cardGraph, match.id, "all");

            itemsGroup.append(itemDiv);
            section.append(itemsGroup);
            cd_timeline.append(section);
        }

        this.frame.appendChild(codyhouseContainer);
        window.VTimeline(cd_timeline);
    }

    prepData() {
        this.response_data = {};
        
        for(const match in this.matches){
            this.response_data[match] = {};
            let totals = {
                "excellent": 0, 
                "acceptable": 0,
                "needsWork": 0
            };

            let responses = JSON.parse(this.matches[match].response);
            
            for(const type in responses){
                this.response_data[match][type] = {
                    "excellent": 0, 
                    "acceptable": 0,
                    "needsWork": 0
                };

                for(const item of responses[type]) {

                    if (item.includes('a')) {
                        this.response_data[match][type].excellent += 1;
                        totals.excellent += 1;
                    } else if (item.includes('b')) {
                        this.response_data[match][type].acceptable += 1;
                        totals.acceptable += 1;
                    } else if (item.includes('c')) {
                        this.response_data[match][type].needsWork += 1;
                        totals.needsWork += 1;
                    }
                }
            }

            this.response_data[match]['all'] = totals;
        }
    }

    getGraphablePieData(id, type) {
        let itemResults = this.response_data[id][type];

        let graphableData = [{
                "sector": "Excellent",
                "size": itemResults.excellent,
                "color": am4core.color("#008000")
            },
            {
                "sector": "Acceptable",
                "size": itemResults.acceptable,
                "color": am4core.color("#0000FF")
            },
            {
                "sector": "Needs Work",
                "size": itemResults.needsWork,
                "color": am4core.color("#C00000")
        }];

        return graphableData;
    }

    makeGraph(container, id, type) {
        if (this.response_data[id] == null == null) {
            container.textContent = "Data is not available yet.";
        }
        else if (this.response_data[id][type].excellent == 0
                && this.response_data[id][type].acceptable == 0
                && this.response_data[id][type].needsWork == 0) {
            container.textContent = "(no data)";
        }
        else {
            let self = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(container, am4charts.PieChart);

                chart.data = self.getGraphablePieData(id, type);
                
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

    getSectorNameById(id) {
        let name = "";
        switch(id) {
            case 4: 
                name = "[Cow-Calf]";
                break;
            case 6:
                name = "[Feeder]";
                break;
            case 7:
                name = "[Packer]";
                break;
            default:
                name = "";
        }
        return name;
    }

    openModal(match) {
        let title = match.name + " " + this.getSectorNameById(match.sector)
        let infoModal = new InfoModal("Details for " + title);
        let modalBody = infoModal.getBody();

        // TODO: fix when combine new stuff
        let sections = {
            "air": "Air & Greenhouse Gas Emissions",
            "land": "Land Resources",
            "water": "Water Resources",
            "animal": "Animal Health & Well-Being",
            "safety": "Employee Safety & Well-Being",
            "efficiency": "Efficiency & Yield"
        };

        for (const type in this.response_data[match.id]) {
            if (type != "all") {
                let card = document.createElement("div");
                let cardHeader = document.createElement("div");
                cardHeader.className = "card-header";
                cardHeader.textContent = sections[type];
                let cardBody = document.createElement("div");
                cardBody.className = "card-body";
                card.append(cardHeader);
                card.append(cardBody);
                modalBody.append(card);
                this.makeGraph(cardBody, match.id, type);
            }
        }
    }
}