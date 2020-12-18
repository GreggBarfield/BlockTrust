import { Widget } from '../widget.mjs';

export class TimelineWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.animal = parseInt(this.frame.getAttribute("data-widget-animal"));

        // TODO: This is a bad data request, optimize later
        this.getData(
            "matches",
            {
                animal: this.animal,
                ljoin_data_str: true,
                ljoin_account_links: true
            },
            (data) => {
                this.match_rows = data.match_rows;
            }
        );
        this.getData(
            "match_types_by_name",
            {},
            (data) => {
                this.match_types_by_name = data.match_types_by_name;
            }
        );
        this.getData(
            "match_types_by_id",
            {},
            (data) => {
                this.match_types_by_id = data.match_types_by_id;
            }
        );

        this.onAllDataLoaded(function () {
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
        this.codyhouseContainer = document.createElement("div");
        this.codyhouseContainer.className = "codyhouse";
        this.timelineContainer = document.createElement("div");
        this.timelineContainer.className = "position-relative z-index-1 overflow-hidden padding-y-xl bg-contrast-lower";
        let cd_container = document.createElement("div");
        cd_container.className = "container max-width-adaptive-lg";
        this.timelineContainer.appendChild(cd_container);
        let cd_timeline = document.createElement("div");
        cd_timeline.className = "v-timeline js-v-timeline";
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

        function createEventObject(title, description, time, company=null) {
            let eventObj = {
                "title": title,
                "description": description,
                "time": time
            };

            if (company !== null) {
                eventObj["company"] = company;
            }
            return eventObj;
        }

        // Provide handlers for each type of event group
        let handlers = {
            "Born": function(rows) {
                return [
                    createEventObject("Calf Born", "", rows[0].time, rows[0]["account_links.company"])
                ];
            },
            "Weaned": function(rows) {
                return [
                    createEventObject("Calf Weaned", "", rows[0].time, rows[0]["account_links.company"])
                ];
            },
            "Died": function(rows) {
                return [
                    createEventObject("Died", "", rows[0].time, rows[0]["account_links.company"])
                ];
            },
            "Sighting": function(rows) {
                return [
                    createEventObject("Sighting", "", rows[0].time, rows[0]["account_links.company"])
                ];
            },
            "Medical": function(rows) {
                let description = "";
                for (const row of rows) {
                    let jObj = null;
                    try {
                        jObj = JSON.parse(row.data_str);
                    }
                    catch {}
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
                    createEventObject("Health Event", description, rows[0].time, rows[0]["account_links.company"])
                ];
            }
        }

        // 
        let events = [];
        let windowSizeSecs = 100;

        for (let startItr = 0; startItr < availableRows.length; startItr++) {
            let endItr = startItr + 1;

            for (; endItr < availableRows.length && Math.abs(availableRows[endItr].time-availableRows[startItr].time) < windowSizeSecs; endItr++) {}

            let eventGroup = [];

            let typeName = this.match_types_by_id[availableRows[startItr].type];
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
                timeDiv.append(timeE);

                let textComponent = document.createElement("div");
                textComponent.className = "text-component";
                itemDiv.append(textComponent);

                let tcTitle = document.createElement("h2");
                tcTitle.textContent = event["title"];
                textComponent.append(tcTitle);

                if (event.hasOwnProperty("company")) {
                    let tcCompany = document.createElement("h4");
                    tcCompany.textContent = event["company"];
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
    }
}