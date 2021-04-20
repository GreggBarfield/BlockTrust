import { BootstrapCarousel } from "../core/bootstrap_carousel.mjs";
import { fileNameIsImage } from "../files/file_types.mjs";
import { urlHighlighter } from "../core/url_highlighter.mjs";
import { DL } from "../core/dl.mjs";
import { formatDate } from "../core/time.mjs";
import { promptNewMessage } from "./messages.mjs";

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
        layout.content.style="border:1px solid #c0c0c0;padding:15px;border-radius:25px";

        // layout.format =document.createElement("div");
        // layout.format.className = "container-fluid";
        // layout.format.style="border:1px solid #c0c0c0;padding:15px;border-radius:25px";


        layout.header = document.createElement("div");
        layout.header.className = "col-12";
        layout.header.style.paddingBottom = "10px";
        layout.header.style.borderBottom = "solid 1px #c0c0c0";
        layout.content.append(layout.header);

        layout.media = document.createElement("div");
        layout.media.className = "col-12 col-md-4";
        layout.media.style.paddingTop = "10px";
        layout.content.append(layout.media);

        layout.animalData = document.createElement("div");
        layout.animalData.className = "col-12 col-md-4";
        layout.animalData.style.paddingTop = "10px";
        layout.content.append(layout.animalData);

        layout.marketData = document.createElement("div");
        layout.marketData.className = "col-12 col-md-4";
        layout.marketData.style.paddingTop = "10px";
        layout.content.append(layout.marketData);

        function addKV(key, value, position, wide=false, highlighting=false) {
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
            kvp.className="row";
            

            let kvpKey = document.createElement("dt");
            kvpKey.className = "col-sm-6";
            // kvpKey.style.paddingTop = "10px";
            kvpKey.textContent = key;
            
            kvp.append(kvpKey);
            // animalDataCol.append(kvpKey);

            let kvpValue = document.createElement("dd");
            kvpValue.className = "col-sm-6";
            // kvpValue.style.paddingTop = "10px";
            kvpValue.style.whiteSpace = "pre-wrap";
            kvpValue.style.maxHeight = "200px";// To prevent trolls from making it completely usable
            
            let valueText= document.createElement("p");
            valueText.className ="text-right";

            if (highlighting) {
                urlHighlighter(str, valueText);
            }
            else {
                valueText.textContent = str;
            }
            kvpValue.append(valueText);

            // animalDataCol.append(kvpValue);
            kvp.append(kvpValue);
            // let breakCol= document.createElement("div");
            // breakCol.className = "w-100";
            // animalDataCol.append(breakCol);
            position.append(kvp);
        }
        // Configure header

        {
            let row = document.createElement("div");
            row.className = "card";
            row.style ="margin-bottom:5px;border-radius: 25px"
            layout.header.append(row);

            let left = document.createElement("div");
            left.className = "card-body";
            row.append(left);

            let salesGroupID =document.createElement("h5");
            salesGroupID.className="mb-0";
            salesGroupID.style ="display: inline;";
            salesGroupID .textContent = "Sales Group "+this.data.id; 
            left.append(salesGroupID);

            // let right = document.createElement("div");
            // right.className = "col-auto";
            // row.append(right);

            let location = document.createElement("div");
            // location.className = "text-muted";
            
            let milesAway = "--";
            if ("context" in this.data && "milesAway" in this.data.context) {
                milesAway = Math.floor(this.data.context.milesAway);
            }
            let milesAwayInt = parseInt(milesAway);
            location.style="float:right;display: inline;color:black";
            location.textContent = "Location: " +"("+milesAwayInt+" Miles)";
            left.append(location);
            // right.append(location);


        }

        // Configure Animal data

        {

            let animalDataCol = document.createElement("div");
            animalDataCol.className = "card";
            animalDataCol.style ="border-radius: 5%";
            layout.animalData.append(animalDataCol);

            let animalHeader = document.createElement("div");
            animalHeader.className ="card-header";
            animalHeader.style ="color:#8B4513; height:75px";
            // animalHeader.style.paddingBottom = "10px";
            animalHeader.style.borderBottom = "solid 1px #c0c0c0";
            animalHeader.textContent ="Animal Data";
            animalDataCol.append(animalHeader);

            let animalBody = document.createElement("div");
            animalBody.className ="card-body";
            animalDataCol.append(animalBody);

            
            
            addKV("Breed", this.data.reported.breeds,animalBody);
            addKV("Base Weight", this.data.reported.weight,animalBody);
            addKV("Wt. Variance", this.data.reported.weight_variance,animalBody);
            addKV("Frame", this.data.reported.usda_frame_size,animalBody);
            addKV("Horns", this.data.reported.horns,animalBody);
            addKV("Precon Program", this.data.reported.preconditioning_program,animalBody);
            addKV("Implants", this.data.reported.implants,animalBody);
            addKV("Castrated", this.data.reported.castrated,animalBody);
            addKV("Vaccinations", this.data.reported.vaccinations,animalBody);
            addKV("Feeding Program", this.data.reported.feeding_programs,animalBody);
            addKV("PVP Program", this.data.reported.process_verified_program,animalBody);

        }
        //Configure market data 

        {
            let marketDataCol = document.createElement("div");
            marketDataCol.className = "card";
            marketDataCol.style ="border-radius: 5%";
            layout.marketData.append(marketDataCol);

            let marketHeader = document.createElement("div");
            marketHeader.className ="card-header";
            marketHeader.style ="color:#8B4513; height:75px";
            marketHeader.style.borderBottom = "solid 1px #c0c0c0";
            marketHeader.textContent ="Market Data";
            marketDataCol.append(marketHeader);

            //TODO: Logo img

            let marketBody = document.createElement("div");
            marketBody.className ="card-body";
            marketDataCol.append(marketBody);

            let marketInfo = document.createElement("div");
            marketInfo.className = "col-sm-12";
            marketBody.append(marketInfo);

            let marketInfoText = document.createElement("dl");
            marketInfoText.className = "dl-horizontal row";
            
            addKV("Total Count",this.data.reported.count, marketBody);
            let daysRemaining = "--";

            if ("end" in this.data && this.data.end !== null) {
                let currentEpoch = Date.now()/1000;
                daysRemaining = Math.floor((this.data.end - currentEpoch) / (60 * 60 * 24));
            }
            addKV("Days Remaining",daysRemaining,marketBody);
            //TODO: Count w Data, Delivery Location,Market
            // addKV("Count w Data",this.data.reported.count, marketInfoText);
            marketInfo.append(marketInfoText);
            let commentCol = document.createElement("div");
            commentCol.className = "card";
            marketDataCol.append(commentCol);

            let commentHeader = document.createElement("div");
            commentHeader.className ="card-header";
            commentHeader.style ="color:#8B4513";
            commentHeader.textContent ="Comments";
            commentCol.append(commentHeader);

            let commentBody = document.createElement("div");
            commentBody.className ="card-body";
            commentBody.textContent = this.data.reported.comments;
            commentCol.append(commentBody);


        


        }

        //Configure media data
        {
            let mediaDataCol = document.createElement("div");
            mediaDataCol.className = "card";
            mediaDataCol.style ="border-radius: 5%";
            layout.media.append(mediaDataCol);

            let mediaHeader = document.createElement("div");
            mediaHeader.className ="card-header";
            mediaHeader.style ="color:#8B4513; height:75px";
            mediaHeader.style.borderBottom = "solid 1px #c0c0c0";
            mediaHeader.textContent ="Media";
            mediaDataCol.append(mediaHeader);

            let mediaBody = document.createElement("div")
            mediaBody.className="card-body";
            mediaDataCol.append(mediaBody);

            let mediaNav = document.createElement("ul");
            mediaNav.className = "nav nav-tabs";
            mediaNav.id ="myTab";
            mediaBody.append(mediaNav);

            let photoNav = document.createElement("li");
            photoNav.className="nav-item";
            mediaBody.append(photoNav);

            let photoNavLink =document.createElement("a");
            photoNavLink.className="nav-link text-uppercase";
            photoNavLink.textContent="Photos";
            photoNavLink.id="photo-tab";
            photoNavLink.href="#photo";
            photoNav.append(photoNavLink);

            let videoNav = document.createElement("li");
            videoNav.className="nav-item";
            mediaBody.append(videoNav);

            let videoNavLink =document.createElement("a");
            videoNavLink.className="nav-link text-uppercase";
            videoNavLink.textContent="Video";
            videoNavLink.id="video-tab";
            videoNavLink.href="#video";
            videoNav.append(videoNavLink);

            let mediaContent = document.createElement("div");
            mediaContent.className = "tab-content";
            mediaContent.id ="myTabContent";
            mediaBody.append(mediaContent);

            let photo = document.createElement("div");
            photo.className = "tab-pane fade active show";
            photo.id = "photo";

            let img = document.createElement("div");
            img.className = "col-12 col-md";
            img.style.height = "240px";
            img.style.padding = "0px";
            photo.append(img);

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

        // Configure image & numbers

        // {
        //     let numImgRow = document.createElement("div");
        //     numImgRow.className = "col-md-4";
        //     layout.side.append(numImgRow);

        //     let numCol = document.createElement("div");
        //     numCol.className = "col-12 col-md-auto d-flex d-md-block";
        //     numCol.style.justifyContent = "space-around";
        //     numCol.style.backgroundColor = "hsl(232,50%,45%)";
        //     numCol.style.color = "white";
        //     numImgRow.append(numCol);

        //     let numRow = numCol;

        //     function addNum(key, num) {
        //         let bin = document.createElement("div");
        //         bin.style.height = "80px";
        //         bin.style.width = "80px";
        //         bin.style.textAlign = "center";
        //         bin.style.display = "flex";
        //         bin.style.flexDirection = "column";
        //         bin.style.justifyContent = "center";
        //         numRow.append(bin);

        //         let numDiv = document.createElement("span");
        //         numDiv.textContent = num;
        //         numDiv.style.fontSize = "20px";
        //         bin.append(numDiv);

        //         let keyDiv = document.createElement("span");
        //         keyDiv.textContent = key;
        //         bin.append(keyDiv);
        //         keyDiv.style.wordSpacing = "100px";
        //     }

        //     addNum("AVERAGE WEIGHT", this.data.reported.weight || "?");


        //     let daysRemaining = "--";

        //     if ("end" in this.data && this.data.end !== null) {
        //         let currentEpoch = Date.now()/1000;
        //         daysRemaining = Math.floor((this.data.end - currentEpoch) / (60 * 60 * 24));
        //     }
        //     addNum("DAYS REMAINING", daysRemaining);

        //     
        // }

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

        {
            let b_contactInfo = createAcc(this.box, "Contact Info");

            let p = document.createElement("p");
            p.textContent = this.data.account_name;
            b_contactInfo.append(p);

            let sendMessageButton = document.createElement("button");
            sendMessageButton.className = "btn btn-sm btn-primary";
            sendMessageButton.textContent = "Send Message";
            sendMessageButton.addEventListener("click", ()=>{
                promptNewMessage(this.data.account, this.data.account_name);
            });
            b_contactInfo.append(sendMessageButton);
        }

        {
            let b_additionalInformation = createAcc(this.box, "Additional Information");

            let row = document.createElement("div");
            row.className = "row";
            b_additionalInformation.append(row);

            function atos(value) {
                let result = value;
                if (value === null || value === undefined) {
                    result = "";
                }
                else {
                    if (typeof value === "number") {
                        if (value > 1000000) {
                            result = formatDate(value);
                        }
                        else {
                            result = value;
                        }
                    }
                    else if (Array.isArray(value)) {
                        let temp = [];
                        for (const value_in of value) {
                            temp.push(atos(value_in));
                        }
                        result = temp.join(", ");
                    }
                }
                return "" + result;
            }


            let createSection = (name, reportedKeys) => {
                let box = document.createElement("div");
                box.className = "col-12 col-md-4";
                row.append(box);
                let h6 = document.createElement('h6');
                h6.textContent = name;
                box.append(h6);

                let dl = new DL(true, box);

                for (const up of reportedKeys) {
                    let name = up[0];
                    if (up.length == 3) {
                        dl.add(name, atos(up[2]));
                    }
                    else if (up[1] in this.data.reported) {
                        dl.add(name, atos(this.data.reported[up[1]]));
                    }
                    else {
                        dl.add(name, "");
                    }
                }
            }
            createSection("Market", [
                ["Count", "count"], 
                ["Market Start", null, this.data.start], 
                ["Market End", null, this.data.end], 
                ["Market ZIP", null, this.data.zip], 
            ]);
            createSection("Characteristics", [
                ["Breed", "breeds"],
                ["Base Weight", "weight"],
                ["Wt. Variance", "weight_variance"],
                ["Frame", "usda_frame_size"],
                ["Muscling", "muscling"],
                ["Horns", "horns"],
            ]);
            createSection("Maintenance", [
                ["Implants", "implants"],
                ["Castrated", "castrated"],
                ["Vaccinations", "vaccinations"],
                ["Feeding Program", "feeding_programs"],
                ["Preconditioning Program", "preconditioning_program"],
                ["Process Verified Program", "process_verified_program"],
            ]);
        }
        
        {
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