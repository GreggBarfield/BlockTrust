import { Widget } from '../../widget.mjs';

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
                "direct/match_types_by_name",
                {}
            ).then((data) => {
                this.match_types_by_name = data.match_types_by_name;
            }),
            
            this.getData(
                "direct/match_types_by_id",
                {}
            ).then((data) => {
                this.match_types_by_id = data.match_types_by_id;
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
                    createEventObject("Health Event", description, rows[0].time, rows[0]["account_links.company"])
                ];
            }
        }

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

        window.VTimeline(cd_timeline);
    }
}