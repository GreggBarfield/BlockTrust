import { BootstrapCarousel } from "../core/bootstrap_carousel.mjs";
import { fileNameIsImage } from "../files/file_types.mjs";

export class SalesGroupViewer {
    constructor(data, attachTo=null) {
        this.frame = null;

        this.box = document.createElement("div");

        if (!"id" in data || !"reported" in data) {
            throw "data incomplete";
        }

        this.data = data;
        this.createDisplay();

        if (attachTo !== null)
            this.attach(attachTo);
    }

    createDisplay() {
        // General layout

        let layout = {};
        this.layout = layout;

        layout.content = document.createElement("div");
        layout.content.className = "row";

        layout.header = document.createElement("div");
        layout.header.className = "col-12";
        layout.header.style.paddingBottom = "10px";
        layout.header.style.borderBottom = "solid 1px #0288d1";
        layout.content.append(layout.header);

        layout.data = document.createElement("div");
        layout.data.className = "col-12 col-md-8";
        layout.data.style.paddingTop = "10px";
        layout.content.append(layout.data);

        layout.side = document.createElement("div");
        layout.side.className = "col-12 col-md-4";
        layout.side.style.paddingTop = "10px";
        layout.content.append(layout.side);

        // Configure header

        {
            let row = document.createElement("div");
            row.className = "row";
            layout.header.append(row);

            let left = document.createElement("div");
            left.className = "col";
            row.append(left);

            let headCount = document.createElement("span");
            headCount.className = "text-dark h4";
            headCount.textContent = this.data.reported.count || "?";
            left.append(headCount);

            let headsOf = document.createElement("span");
            headsOf.className = "text-info";
            headsOf.style.marginLeft = "20px";
            headsOf.style.marginRight = "20px";
            headsOf.textContent = "HEAD OF";
            left.append(headsOf);

            let breeds = document.createElement("span");
            breeds.className = "text-dark h4";
            if (this.data.reported.breeds && this.data.reported.breeds.length > 0)
                breeds.textContent = this.data.reported.breeds.join(', ');
            else
                breeds.textContent = "?";
            left.append(breeds);

            let right = document.createElement("div");
            right.className = "col-auto";
            row.append(right);

            let rightText = document.createElement("span");
            rightText.className = "text-muted";
            rightText.textContent = "#" + this.data.id;
            right.append(rightText);
        }

        // Configure data

        {

            let layoutDataRow = document.createElement("div");
            layoutDataRow.className = "row";
            layout.data.append(layoutDataRow);
            function addKV(key, value) {
                let str = "";

                if (Array.isArray(value)) {
                    if (value.length > 0)
                        str = "" + value.join(', ');
                    else
                        str = "?";
                }
                else {
                    str = "" + value;
                }

                let kvp = document.createElement("div");
                kvp.className = "col col-md-6";

                let kvpKey = document.createElement("div");
                kvpKey.className = "text-info";
                kvpKey.textContent = key;
                kvp.append(kvpKey);

                let kvpValue = document.createElement("div");
                kvpValue.className = "h5 text-dark";
                kvpValue.textContent = str;
                kvp.append(kvpValue);

                layoutDataRow.append(kvp);
            }

            addKV("PRECONDITIONING", this.data.reported.preconditioning_program);
            addKV("FEEDING", this.data.reported.feeding_programs);
            addKV("PROCESS VERIFIED", this.data.reported.process_verified_program);
        }

        // Configure image & numbers

        {
            let numImgRow = document.createElement("div");
            numImgRow.className = "row";
            layout.side.append(numImgRow);

            let numCol = document.createElement("div");
            numCol.className = "col-12 col-md-auto d-flex d-md-block";
            numCol.style.justifyContent = "space-around";
            numCol.style.backgroundColor = "hsl(232,50%,45%)";
            numCol.style.color = "white";
            numImgRow.append(numCol);

            let numRow = numCol;

            function addNum(key, num) {
                let bin = document.createElement("div");
                bin.style.height = "80px";
                bin.style.width = "80px";
                bin.style.textAlign = "center";
                bin.style.display = "flex";
                bin.style.flexDirection = "column";
                bin.style.justifyContent = "center";
                numRow.append(bin);

                let numDiv = document.createElement("span");
                numDiv.textContent = num;
                numDiv.style.fontSize = "20px";
                bin.append(numDiv);

                let keyDiv = document.createElement("span");
                keyDiv.textContent = key;
                bin.append(keyDiv);
                keyDiv.style.wordSpacing = "100px";
            }

            addNum("AVERAGE WEIGHT", this.data.reported.weight || "?");
            
            let milesAway = "--";
            if ("context" in this.data && "milesAway" in this.data.context) {
                milesAway = Math.floor(this.data.context.milesAway);
            }
            addNum("MILES AWAY", milesAway);

            let daysRemaining = "--";

            if ("end" in this.data && this.data.end !== null) {
                let currentEpoch = Date.now()/1000;
                daysRemaining = Math.floor((this.data.end - currentEpoch) / (60 * 60 * 24));
            }
            addNum("DAYS REMAINING", daysRemaining);

            let img = document.createElement("div");
            img.className = "col-12 col-md";
            img.style.height = "240px";
            img.style.padding = "0px";
            numImgRow.append(img);

            let images = [];

            for (const image of this.data.reported.images) {
                if (image in this.data.file_auths) {
                    if (fileNameIsImage(this.data.file_auths[image]["name"])) {
                        images.push(this.data.file_auths[image]["get"]);
                    }   
                    else {
                        console.log(image + " is not an image?");
                    }                 
                }
                else {
                    console.log("Expected file auth for " + image);
                }
            }

            new BootstrapCarousel(images, img);
        }

        this.box.append(layout.content);

        function createAcc(attachTo, headerText, firstOpen=null) {
            let container = document.createElement("div");
            container.className = "acc-container";
            attachTo.append(container);

            let bar = document.createElement("div");
            bar.className = "acc-bar";
            container.append(bar);

            let tri = document.createElement("span");
            tri.style.marginRight = "10px";

            let triClosed = document.createElement("i");
            triClosed.className = "fa fa-caret-right";
            tri.append(triClosed);

            let triOpened = document.createElement("i");
            triOpened.style.display = "none";
            triOpened.className = "fa fa-caret-down";
            tri.append(triOpened);


            let header = document.createElement("div");
            header.className = "acc-header h5 text-dark";
            header.append(tri);
            header.append(document.createTextNode(headerText));
            container.append(header);

            let body = document.createElement("div");
            body.className = "acc-body";
            body.style.display = "none";
            container.append(body);

            let isClosed = true;
            let isFirstOpen = true;

            header.addEventListener("click", ()=>{
                if (isClosed) {
                    triOpened.style.display = "inline-block";
                    body.style.display = "block";
                    triClosed.style.display = "none";
                    isClosed = false;
                }
                else {
                    triOpened.style.display = "none";
                    body.style.display = "none";
                    triClosed.style.display = "inline-block";
                    isClosed = true;
                }

                if (isFirstOpen) {
                    isFirstOpen = false;
                    if (firstOpen !== null) {
                        firstOpen(body);
                    }
                }
            });

            return body;
        }

        let b_contactInfo = createAcc(this.box, "Contact Info");
        let b_additionalInformation = createAcc(this.box, "Additional Information");
        let b_tags = createAcc(this.box, "Tags (EIDs)", (body)=>{
            let divTableResponsive = document.createElement("div");
            divTableResponsive.className = "dt-responsive table-responsive";

            let mainTable = document.createElement("table");
            mainTable.className = "table table-striped table-bordered nowrap";
            divTableResponsive.appendChild(mainTable);

            // Header

            let mainTableHead = document.createElement("thead");
            mainTable.appendChild(mainTableHead);

            let mainTableHeadRow0 = document.createElement("tr");
            mainTableHead.appendChild(mainTableHeadRow0);
            const headers = ["EID", "Options"];
            for (const headerText of headers) {
                let th = document.createElement("th");
                th.textContent = headerText;
                mainTableHeadRow0.appendChild(th);
            }

            // Body

            let mainTableBody = document.createElement("tbody");
            mainTable.appendChild(mainTableBody);

            for (const eid of this.data.eids) {
                let rowTag = document.createElement("tr");
                mainTableBody.appendChild(rowTag);

                let row = [];

                row.push(eid);

                for (const value of row) {
                    let td = document.createElement("td");
                    td.textContent = value;
                    rowTag.appendChild(td);
                }

                let tdOptions = document.createElement("td");
                rowTag.appendChild(tdOptions);

                let button = document.createElement("a");
                button.className = "btn btn-outline-secondary btn-sm";
                button.setAttribute("href", "/dashboard/animals/" + eid);
                button.textContent = "View";
                tdOptions.appendChild(button);
            }

            // Put HTML in frame

            body.appendChild(divTableResponsive);
            $(mainTable).DataTable();
        });
    }

    attach(frame) {
        if (this.frame !== null) {
            this.detach();
        }
        this.frame = frame;
        this.frame.append(this.box);
    }

    detach() {
        if (this.frame !== null) {
            this.box.remove();
        }
        this.frame = null;
    }


}