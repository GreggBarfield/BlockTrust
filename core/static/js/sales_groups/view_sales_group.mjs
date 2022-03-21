import { BootstrapCarousel } from "../core/bootstrap_carousel.mjs";
import { fileNameIsImage } from "../files/file_types.mjs";
import { urlHighlighter } from "../core/url_highlighter.mjs";
import { promptNewMessage } from "../widgets/types/messages/new_message.mjs";

export class SalesGroupViewer {
    constructor(data, attachTo = null) {
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

        layout.formatRow = document.createElement("div");
        layout.formatRow.className = "row";

        layout.formatCol = document.createElement("div");
        layout.formatCol.className = "col-md-12 col-sm-12";
        layout.formatRow.append(layout.formatCol);

        layout.format = document.createElement("div");
        layout.format.className = "container-fluid";
        layout.format.style = "margin-bottom:5px;border-radius: 25px";
        layout.formatCol.append(layout.format);

        layout.content = document.createElement("div");
        layout.content.className = "row";

        layout.content.style = "border:1px solid #c0c0c0;padding:15px;border-radius:25px";
        layout.format.append(layout.content);

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

        layout.tabs = document.createElement("div");
        layout.tabs.className = "row";
        layout.tabs.style = "width:100%;margin:auto";
        layout.content.append(layout.tabs);

        layout.contact = document.createElement("div");
        layout.contact.className = "col-12";
        layout.tabs.append(layout.contact);

        layout.tags = document.createElement("div");
        layout.tags.className = "col-12";
        layout.tabs.append(layout.tags);

        function addInfo(key, value, position, wide = false, highlighting = false) {
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
            kvp.className = "row";
            let kvpKey = document.createElement("dt");
            kvpKey.className = "col-sm-6";
            kvpKey.textContent = key;

            kvp.append(kvpKey);

            let kvpValue = document.createElement("dd");
            kvpValue.className = "col-sm-6";
            kvpValue.style.whiteSpace = "pre-wrap";
            kvpValue.style.maxHeight = "200px";// To prevent trolls from making it completely usable

            let valueText = document.createElement("p");
            valueText.className = "text-right";

            if (highlighting) {
                urlHighlighter(str, valueText);
            }
            else {
                valueText.textContent = str;
            }
            kvpValue.append(valueText);

            kvp.append(kvpValue);
            position.append(kvp);
        }

        // Configure header
        {
            let row = document.createElement("div");
            row.className = "card";
            row.style = "margin-bottom:5px;border-radius: 25px"
            layout.header.append(row);

            let left = document.createElement("div");
            left.className = "card-body";
            row.append(left);

            let salesGroupID = document.createElement("h5");
            salesGroupID.className = "mb-0";
            salesGroupID.style = "display: inline;";
            salesGroupID .textContent = "Sales Group "+this.data.id+": "+this.data.group_name; 
            left.append(salesGroupID);
            if(this.data["is_archived"]==0){
                let sendMessageButton = document.createElement("button");
                sendMessageButton.className = "btn btn-sm btn-outline-primary";
                sendMessageButton.style = "float:right"
                sendMessageButton.textContent = "Contact Seller";
                sendMessageButton.addEventListener("click", () => {
                    promptNewMessage(this.data.account, this.data.account_name);
                });
                left.append(sendMessageButton);
            }
            else{
                let unarchiveButton = document.createElement("button");

                unarchiveButton.className = "btn btn-sm btn-primary";
                unarchiveButton.style = "float:right"
                unarchiveButton.textContent = "Unarchive";
                unarchiveButton.addEventListener("click", () => {
                    $.ajax({
                        url: "/widgets/data/unarchive_sales_group",
                        data: JSON.stringify({
                            "action": "unarchive_sales_group",
                            "params": {
                                id:this.data.id
                            }
                        }),
                        contentType: 'application/json',
                        method: "POST"
                    }).then(()=>{
                        let alert = document.createElement("div");
                        alert.className = "alert alert-success";
                        alert.textContent = "Unarchived success!";
                        left.append(alert);   
                        window.location.reload();
                    })               
                });
                left.append(unarchiveButton);
            }
            
            let location = document.createElement("div");

            let milesAway = "--";

            if ("context" in this.data && "milesAway" in this.data.context) {
                milesAway = Math.floor(this.data.context.milesAway);
            }
            let milesAwayInt = "--"
            if (milesAway != "--") {
                milesAwayInt = parseInt(milesAway);
            }

            location.style = "color:black";
            location.textContent = "  Location: " + this.formatData(this.data.market_location) + " ( " + milesAwayInt + " Miles)";
            left.append(location);
        }

        // Configure Animal data
        {

            let animalDataCol = document.createElement("div");
            animalDataCol.className = "card";
            animalDataCol.style = "border-radius: 5%";
            layout.animalData.append(animalDataCol);

            let animalHeader = document.createElement("div");
            animalHeader.className = "card-header";
            animalHeader.style = "color:#8B4513; height:75px";
            animalHeader.style.borderBottom = "solid 1px #c0c0c0";
            animalHeader.textContent = "Animal Data";
            animalDataCol.append(animalHeader);

            let animalBody = document.createElement("div");
            animalBody.className = "card-body";
            animalDataCol.append(animalBody);

            addInfo("Breed", this.formatData(this.data.reported.breeds), animalBody);
            addInfo("Base Weight", this.formatData(this.data.reported.weight), animalBody);
            addInfo("Wt. Variance", this.formatData(this.data.reported.weight_variance), animalBody);
            addInfo("Frame", this.formatData(this.data.reported.usda_frame_size), animalBody);
            addInfo("Horns", this.formatData(this.data.reported.horns), animalBody);
            addInfo("Precon Program", this.formatData(this.data.reported.preconditioning_program), animalBody);
            addInfo("Implants", this.formatData(this.data.reported.implants), animalBody);
            addInfo("Castrated", this.formatData(this.data.reported.castrated), animalBody);
            addInfo("Vaccinations", this.formatData(this.data.reported.vaccinations), animalBody);
            addInfo("Feeding Program", this.formatData(this.data.reported.feeding_programs), animalBody);
            addInfo("PVP Program", this.formatData(this.data.reported.process_verified_program), animalBody);
        }

        //Configure market data 
        {
            let marketDataCol = document.createElement("div");
            marketDataCol.className = "card";
            marketDataCol.style = "border-radius: 5%";
            layout.marketData.append(marketDataCol);

            let marketHeader = document.createElement("div");
            marketHeader.className = "card-header";
            marketHeader.style = "color:#8B4513; height:75px";
            marketHeader.style.borderBottom = "solid 1px #c0c0c0";
            marketHeader.textContent = "Market Data";
            marketDataCol.append(marketHeader);

            let marketBody = document.createElement("div");
            marketBody.className = "card-body";
            marketDataCol.append(marketBody);

            let marketInfo = document.createElement("div");
            marketInfo.className = "col-sm-12";
            marketBody.append(marketInfo);

            let marketInfoText = document.createElement("dl");
            marketInfoText.className = "dl-horizontal row";

            addInfo("Total Count", this.formatData(this.data.reported.count), marketBody);
            addInfo("Delivery Location", this.formatData(this.data.delivery_location), marketBody);

            let daysRemaining = "--";

            if ("end" in this.data && this.data.end !== null) {
                let currentEpoch = Date.now() / 1000;
                daysRemaining = Math.floor((this.data.end - currentEpoch) / (60 * 60 * 24));
            }
            var date = new Date(this.data.start * 1000);
            addInfo("Sales Date", date.toDateString(), marketBody);
            addInfo("Days Remaining", daysRemaining, marketBody);

            marketInfo.append(marketInfoText);
            let commentCol = document.createElement("div");
            commentCol.className = "card";
            marketDataCol.append(commentCol);

            let commentHeader = document.createElement("div");
            commentHeader.className = "card-header";
            commentHeader.style = "color:#8B4513";
            commentHeader.textContent = "Comments";
            commentCol.append(commentHeader);

            let commentBody = document.createElement("div");
            commentBody.className = "card-body";
            commentBody.textContent = this.data.reported.comments;
            commentCol.append(commentBody);
        }

        //Configure media data
        {
            let mediaDataCol = document.createElement("div");
            mediaDataCol.className = "card";
            mediaDataCol.style = "border-radius: 5%";
            layout.media.append(mediaDataCol);

            let mediaHeader = document.createElement("div");
            mediaHeader.className = "card-header";
            mediaHeader.style = "color:#8B4513; height:75px";
            mediaHeader.style.borderBottom = "solid 1px #c0c0c0";
            mediaHeader.textContent = "Media";
            mediaDataCol.append(mediaHeader);

            let mediaBody = document.createElement("div")
            mediaBody.className = "card-body";
            mediaDataCol.append(mediaBody);

            let mediaNav = document.createElement("ul");
            mediaNav.className = "nav nav-tabs";
            mediaNav.id = "myTab";
            mediaNav.setAttribute("role", "tablist");

            mediaBody.append(mediaNav);

            let photoNav = document.createElement("li");
            photoNav.className = "nav-item";
            mediaNav.append(photoNav);

            let photoNavLink = document.createElement("a");
            photoNavLink.className = "nav-link text-uppercase active";
            photoNavLink.textContent = "Photos";
            photoNavLink.id = "photo-tab";
            photoNavLink.href = "#photo";
            photoNavLink.setAttribute("role", "tab");
            photoNavLink.setAttribute("data-toggle", "tab");
            photoNavLink.setAttribute("aria-controls", "home");
            photoNavLink.setAttribute("aria-selected", "true");
            photoNav.append(photoNavLink);

            let videoNav = document.createElement("li");
            videoNav.className = "nav-item";
            mediaNav.append(videoNav);

            let videoNavLink = document.createElement("a");
            videoNavLink.className = "nav-link text-uppercase";
            videoNavLink.textContent = "Video";
            videoNavLink.id = "video-tab";
            videoNavLink.href = "#video";
            videoNavLink.setAttribute("role", "tab");
            videoNavLink.setAttribute("data-toggle", "tab");
            videoNavLink.setAttribute("aria-controls", "home");
            videoNavLink.setAttribute("aria-selected", "true");
            videoNav.append(videoNavLink);

            let mediaContent = document.createElement("div");
            mediaContent.className = "tab-content";
            mediaContent.id = "myTabContent";
            mediaBody.append(mediaContent);

            let photo = document.createElement("div");
            photo.className = "tab-pane fade active show";
            photo.id = "photo";
            photo.setAttribute("role", "tabpanel");
            photo.setAttribute("aria-labelledby", "photo");
            mediaContent.append(photo);

            let img = document.createElement("div");
            img.className = "col-12 col-md";
            img.style.height = "240px";
            img.style.padding = "0px";
            photo.append(img);

            let images = [];

            if (this.data.reported.images != undefined) {
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
            }
            new BootstrapCarousel(images, img, "img");

            //Video tab
            let video = document.createElement("div");
            video.className = "tab-pane fade";
            video.id = "video";
            video.setAttribute("role", "tabpanel");
            video.setAttribute("aria-labelledby", "video");
            mediaContent.append(video);

            let thumb = document.createElement("div");
            thumb.className = "thumb";
            video.append(thumb);

            
            let embed = document.createElement("div");
            embed.className ="embed-responsive embed-responsive-16by9";
            thumb.append(embed);

            let videos = this.data.reported.videos;
            var videoUrls = [];
            if (videos != undefined) {
                for (let video of videos) {
                    if (video[0] == "youtube") {
                        videoUrls.push("https://www.youtube.com/embed/" + video[1]);
                    }
                    if (video[0] == "vimeo") {
                        videoUrls.push("https://player.vimeo.com/video/" + video[1]);
                    }
                }
            }
            new BootstrapCarousel(videoUrls, video, "video");

            videoNavLink.onclick = videoOnClick();
            photoNavLink.onclick = photoOnClick();
            function photoOnClick() {

                photoNavLink.className = "nav-link text-uppercase active";
                photo.className = "tab-pane fade active show";
                photoNavLink.setAttribute("aria-selected", "true");

                videoNavLink.className = "nav-link text-uppercase";
                videoNavLink.setAttribute("aria-selected", "false");
                video.className = "tab-pane fade";

            }

            function videoOnClick() {

                videoNavLink.className = "nav-link text-uppercase active";
                video.className = "tab-pane fade active show";
                videoNavLink.setAttribute("aria-selected", "true");

                photoNavLink.className = "nav-link text-uppercase";
                photoNavLink.setAttribute("aria-selected", "false");
                photo.className = "tab-pane fade";
            }

        }

        this.box.append(layout.content);

        function createAcc(attachTo, headerText, firstOpen = null) {
            let container = document.createElement("div");
            container.className = "acc-container";
            attachTo.append(container);

            let tri = document.createElement("span");
            tri.style.marginRight = "10px";

            let triClosed = document.createElement("i");
            triClosed.className = "fa fa-caret-right";
            tri.append(triClosed);

            let triOpened = document.createElement("i");
            triOpened.style = "margin-bottom:5px;border-radius: 25px";
            triOpened.style.display = "none";
            triOpened.className = "fa fa-caret-down";
            tri.append(triOpened);

            let header = document.createElement("div");
            header.className = "btn btn-outline-secondary btn-sm";
            header.style = "float:left";
            header.append(tri);
            header.append(document.createTextNode(headerText));
            container.append(header);

            let body = document.createElement("div");
            body.className = "acc-body";
            body.style.display = "none";
            container.append(body);

            let isClosed = true;
            let isFirstOpen = true;

            header.addEventListener("click", () => {
                if (isClosed) {
                    triOpened.style = "margin-bottom:5px;border-radius: 25px";
                    triOpened.style.display = "inline-block";
                    body.style = "border:1px solid #c0c0c0;padding:15px;width:100%";
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
            let b_tags = createAcc(layout.tags, "Tags (EIDs)", (body) => {
                let divTableResponsive = document.createElement("div");
                divTableResponsive.className = "dt-responsive table-responsive";
                divTableResponsive.style = "width:100%;padding:15px";

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
    
    formatData(data) {
        if (data === null || data === undefined)
            return "";
        else
            return data;
    }
}
