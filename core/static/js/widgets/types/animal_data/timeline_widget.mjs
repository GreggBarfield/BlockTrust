import { Widget } from '../../widget.mjs';
import { icons } from '../../../core/icons.mjs';

export class TimelineWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.animal = parseInt(this.frame.getAttribute("data-widget-animal"));

        // TODO: This is a bad data request, optimize later
        Promise.all([

            this.getData(
                "data_request",
                {
                    request: {
                        type: 'matches_by_eids',
                        params: {
                            eids: [this.animal],
                            ljoin_account_links: true
                        }
                    }
                }
            ).then((data) => {
                this.match_rows = data.result.matches;
            }),


            
            this.getData(
                "direct/match_types_id_to_name",
                {}
            ).then((data) => {
                this.match_types_id_to_name = data.match_types_id_to_name;
            })

        ]).then(() => {
            this.frame.innerHTML = "";
            this.makeTimeline();
        });
    }

    formatDate(epoch) {
        if (epoch == null || epoch <= 0)
            return "--";
        let d = new Date(parseInt(epoch) * 1000);
        return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
    }

    makeTimeline() {
        this.codyhouseContainer = document.createElement("codyhouse");
        this.timelineContainer = document.createElement("div");
        this.timelineContainer.className = "js position-relative z-index-1 overflow-hidden padding-y-xl bg-contrast-lower";
        let cd_container = document.createElement("div");
        cd_container.className = "container max-width-adaptive-lg";
        this.timelineContainer.appendChild(cd_container);
        let cd_timeline = document.createElement("div");
        cd_timeline.className = "v-timeline v-timeline--icons js-v-timeline";
        cd_timeline.setAttribute("data-animation", "on");
        cd_container.appendChild(cd_timeline);

        // Create events

        // Only pull out timestamped events
        let availableRows = [];

        for (let match_row of this.match_rows) {
            if (match_row.time !== null && match_row.time > 10) {
                availableRows.push(match_row);
            }
        }

        // Sort ascending
        availableRows.sort(function(a,b){return a.time-b.time;});

        function createEventObject(title, description, time, name=null) {
            let eventObj = {
                "title": title,
                "description": description,
                "time": time
            };

            if (name !== null) {
                eventObj["name"] = name;
            }
            return eventObj;
        }

        // Provide handlers for each type of event group
        let handlers = {
            "Born": function(rows) {
                return [
                    createEventObject("Calf Born", "", rows[0].time, rows[0]["account_links.name"])
                ];
            },
            "Weaned": function(rows) {
                return [
                    createEventObject("Calf Weaned", "", rows[0].time, rows[0]["account_links.name"])
                ];
            },
            "Died": function(rows) {
                return [
                    createEventObject("Died", "", rows[0].time, rows[0]["account_links.name"])
                ];
            },
            "Sighting": function(rows) {
                return [
                    createEventObject("Sighting", "", rows[0].time, rows[0]["account_links.name"])
                ];
            },
            "Medical": function(rows) {
                let description = "";
                for (const row of rows) {
                    let jObj = row.data;
                    if (jObj !== null) {
                        if (jObj.hasOwnProperty("product")) {
                            description += jObj.product + "<br>";
                        }
                        else {
                            description += "No product info<br>";
                        }
                    }
                    else {
                        description += "No medical info<br>";
                    }
                }
                return [
                    createEventObject("Health Event", description, rows[0].time, rows[0]["account_links.name"])
                ];
            }
        }

        let events = [];
        let windowSizeSecs = 100;

        for (let startItr = 0; startItr < availableRows.length; startItr++) {
            let endItr = startItr + 1;

            for (;
                endItr < availableRows.length &&
                Math.abs(availableRows[endItr].time-availableRows[startItr].time) < windowSizeSecs &&
                availableRows[endItr].type==availableRows[startItr].type
            ; endItr++) {}

            let eventGroup = [];

            let typeName = this.match_types_id_to_name[availableRows[startItr].type];
            if (handlers.hasOwnProperty(typeName)) {
                eventGroup = handlers[typeName](availableRows.slice(startItr, endItr));
            }

            if (eventGroup === null || eventGroup.length == 0) {

            }
            else {
                events.push(eventGroup);
            }

            startItr = endItr - 1;
        }

        // Render

        for (const event_group of events) {
            let section = document.createElement("section");
            section.className = "v-timeline__section js-v-timeline__section";

            let sectionHeader = document.createElement("div");
            sectionHeader.className = "v-timeline__marker bg-contrast-high border border-3 border-contrast-lower";
            section.append(sectionHeader);

            if(event_group[0].title == "Calf Born")
                section.innerHTML = icons.plus;
            else if(event_group[0].title == "Calf Weaned")
                section.innerHTML = icons.carrot;
            else if(event_group[0].title == "Died")
                section.innerHTML = icons.archive;
            else if(event_group[0].title == "Sighting")
                section.innerHTML = icons.sighting;
            else if(event_group[0].title == "Health Event")
                section.innerHTML = icons.healthIcon;

            let itemsGroup = document.createElement("div");
            itemsGroup.className = "v-timeline__items-group";

            for (const event of event_group) {
                let itemDiv = document.createElement("div");
                itemDiv.className = "v-timeline__item bg padding-md radius-md shadow-xs";

                let timeDiv = document.createElement("div");
                timeDiv.className = "v-timeline__date margin-bottom-sm";
                itemDiv.append(timeDiv);
                let timeE = document.createElement("time");
                timeE.textContent = this.formatDate(event.time);
                timeE.className = "v-timeline__date-value"
                timeDiv.append(timeE);

                let textComponent = document.createElement("div");
                textComponent.className = "text-component";
                itemDiv.append(textComponent);

                let tcTitle = document.createElement("h2");
                tcTitle.textContent = event["title"];
                textComponent.append(tcTitle);

                if (event.hasOwnProperty("name")) {
                    let tcCompany = document.createElement("h4");
                    tcCompany.textContent = event["name"];
                    textComponent.append(tcCompany);
                }

                let tcBody = document.createElement("p");
                for (const d of event["description"].split("<br>")) {
                    if (d != "") {
                        tcBody.append(document.createTextNode(d));
                        tcBody.append(document.createElement("br"));
                    }
                }
                textComponent.append(tcBody);



                itemsGroup.append(itemDiv);
            }

            section.append(itemsGroup);
            cd_timeline.append(section);
        }

        this.codyhouseContainer.appendChild(this.timelineContainer);
        this.frame.appendChild(this.codyhouseContainer);

        window.VTimeline(cd_timeline);
    }
}