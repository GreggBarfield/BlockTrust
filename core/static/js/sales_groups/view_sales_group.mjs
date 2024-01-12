import { BootstrapCarousel } from "../core/bootstrap_carousel.mjs";
import { fileNameIsImage } from "../files/file_types.mjs";
import { urlHighlighter } from "../core/url_highlighter.mjs";
import { promptNewMessage } from "../widgets/types/messages/new_message.mjs";

export class SalesGroupViewer {
    constructor(data, attachTo = null) {
        this.frame = null;

        this.box = document.createElement("div");
        this.box.id = "sales-group-viewer";
        if (!"id" in data || !"reported" in data) {
            throw "data incomplete";
        }
        this.data = data;
        this.createDisplay();

        if (attachTo !== null)
            this.attach(attachTo);
    }

    createDisplay = async() =>{
        // Get USDA Quality Grade distribution for sales group account
        let accountUSDAQualityGradeDistribution = null;
        const fetchAccountCarcassData = await fetch(
            '/widgets/data/get_count_distribution_for_account', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    account_id: this.data.account
                }),
        });
        const accountUSDAQualityGradeDistributionData = await fetchAccountCarcassData.json();
        if(accountUSDAQualityGradeDistributionData.result !== null){
            accountUSDAQualityGradeDistribution = accountUSDAQualityGradeDistributionData.result.count_distribution;
        }
        // General layout

        let layout = {};
        this.layout = layout;

        layout.formatRow = document.createElement("div");
        layout.formatRow.className = "row";

        layout.formatCol = document.createElement("div");
        layout.formatCol.className = "col-sm-12";
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
        layout.media.className = "col-12 col-sm-4";
        layout.media.style.paddingTop = "10px";
        layout.content.append(layout.media);

        layout.marketData = document.createElement("div");
        layout.marketData.className = "col-12 col-sm-4";
        layout.marketData.style.paddingTop = "10px";
        layout.content.append(layout.marketData);

        layout.characteristicsData = document.createElement("div");
        layout.characteristicsData.className = "col-12 col-sm-4";
        layout.characteristicsData.style.paddingTop = "10px";
        layout.content.append(layout.characteristicsData);

        layout.maintenanceData = document.createElement("div");
        layout.maintenanceData.className = "col-12 col-sm-4";
        layout.maintenanceData.style.paddingTop = "10px";
        layout.content.append(layout.maintenanceData);

        layout.geneticsData = document.createElement("div");
        layout.geneticsData.className = "col-12 col-sm-4";
        layout.geneticsData.style.paddingTop = "10px";
        layout.content.append(layout.geneticsData);

        layout.valueAddData = document.createElement("div");
        layout.valueAddData.className = "col-12 col-sm-4";
        layout.valueAddData.style.paddingTop = "10px";
        layout.content.append(layout.valueAddData);

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
            valueText.className = "text-right m-0 p-0";

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

        const createSectionContainer = (sectionHeaderText) =>{
            let sectionContainer = document.createElement("div");
            sectionContainer.className = "card";
            sectionContainer.style = "border-radius: 5%";

            let sectionHeader = document.createElement("div");
            sectionHeader.className = "card-header p-4";
            sectionHeader.style = "color:#8B4513;";
            sectionHeader.style.borderBottom = "solid 1px #c0c0c0";
            sectionHeader.textContent = sectionHeaderText;
            sectionContainer.append(sectionHeader);
            return sectionContainer;
        }

        const createCommentSection = (text) =>{
            let commentCard = document.createElement("div");
            commentCard.className = "card";

            let commentHeader = document.createElement("div");
            commentHeader.className = "card-header border-bottom-0 pb-0";
            commentHeader.style = "color:#8B4513";
            commentHeader.textContent = "Comments";
            commentCard.append(commentHeader);

            let commentBody = document.createElement("div");
            commentBody.className = "card-body pt-0";
            commentBody.textContent = text;
            commentCard.append(commentBody);
            return commentCard;
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
            salesGroupID.className = "mb-0 d-inline pr-2"
            salesGroupID.textContent = `Sales Group ${this.data.id}: ${this.data.group_name}`;
            left.append(salesGroupID);

            let scoreText = document.createElement("h4");
            scoreText.className = "d-inline text-c-green";
            scoreText.textContent = parseFloat(this.data.owner_account_sustainability_score_average).toFixed(2);
            let scoreIcon = document.createElement("i");
            scoreIcon.className = "fas fa-leaf text-c-green f-15 pr-2";

            if( this.data.owner_account_sustainability_score_average){
                left.append(scoreIcon);
                left.append(scoreText);
            }

            if(this.data["is_archived"]==0){
                let sendMessageButton = document.createElement("button");
                sendMessageButton.className = "btn btn-sm btn-primary";
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
            if(this.data["is_sold"] == 0 && this.data["is_account_payouts_enabled"] == 1 && this.data["price"] > 0){
                let purchaseButton = document.createElement("button");
                purchaseButton.className = "btn btn-sm btn-success";
                purchaseButton.style = "float:right"
                purchaseButton.textContent = "Purchase";
                purchaseButton.addEventListener("click", () => {
                    window.location.href = "/dashboard/sales-groups/purchase/"+this.data["id"];
                });
                left.append(purchaseButton);
                let priceLabel = document.createElement("label");
                priceLabel.innerHTML = `$${this.data["price"]}`;
                priceLabel.className = "h3 text-info mr-4";
                priceLabel.style = "float:right";
                left.append(priceLabel);
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

            let category = document.createElement("div");
            category.style = "color:black";
            category.textContent =`Category: ${this.data.category}`;
            left.append(category);
            
            if(this.data.show_account_carcass_data == 1 && accountUSDAQualityGradeDistribution.length > 0){
                let carcassData = document.createElement("div");
                carcassData.style = "color:black";
                let qualityGradeDistribution = "";
                if(accountUSDAQualityGradeDistribution != null){
                    let total = 0;
                    let qualityGradePercentages = {"Select or Lower": 0, "Choice": 0,"Prime": 0};
                    for(let qualityGradeData of accountUSDAQualityGradeDistribution){
                        total += qualityGradeData.count;
                    }
                    for(let qualityGradeData of accountUSDAQualityGradeDistribution){
                        qualityGradePercentages[qualityGradeData.data] = (100*qualityGradeData.count/total).toFixed(2) + "%";
                    }
                    qualityGradeDistribution = qualityGradePercentages["Choice"] + "/" + qualityGradePercentages["Prime"] + "/" + qualityGradePercentages["Select or Lower"];
                }
                let tooltip = document.createElement("a");
                tooltip.className = "feather icon-info text-primary pl-2";
                tooltip.style = "color:blue";
                tooltip.dataToggle = "tooltip";
                tooltip.dataPlacement = "right";
                tooltip.title = "Choice/Prime/Select";
                carcassData.textContent =`Ranch Carcass History: ${qualityGradeDistribution}`;
                carcassData.append(tooltip);
                left.append(carcassData);
            }

            let addedDate = document.createElement("div");
            addedDate.style = "color:black";
            addedDate.textContent =`Added: ${this.data.created_date}`;
            left.append(addedDate);
        }

        //Configure market data 
        {
            let marketDataContainer = createSectionContainer("Market Data");
            layout.marketData.append(marketDataContainer);

            let marketBody = document.createElement("div");
            marketBody.className = "card-body";
            marketDataContainer.append(marketBody);

            addInfo("Total Count", this.formatData(this.data.reported.count), marketBody);

            var date = new Date(this.data.sale_date * 1000);
            addInfo("Sales Date", date.toDateString(), marketBody);

            addInfo("Delivery Location Type", this.formatData(this.data.delivery_location_type), marketBody);
            if(this.data.delivery_location_type == "Video Auction"){
                addInfo("Slide", this.formatData(this.data.reported.marketing_slide), marketBody);
                addInfo("Weighing Conditions", this.formatData(this.data.reported.marketing_weighing_conditions), marketBody);
            }
            else{
                addInfo("Delivery Location", this.formatData(this.data.delivery_location), marketBody);
            }
            addInfo("Represented By", this.formatData(this.data.reported.marketing_represented_by), marketBody);

            let commentCard = createCommentSection(this.data.reported.marketing_comments);
            marketDataContainer.append(commentCard);
        }

        //Configure media data
        {
            let mediaDataContainer = createSectionContainer("Media");
            layout.media.append(mediaDataContainer);

            let mediaBody = document.createElement("div")
            mediaBody.className = "card-body";
            mediaDataContainer.append(mediaBody);

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
            img.className = "col-12 col-sm";
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

        // Characteristics
        {
            let characteristicsDataContainer = createSectionContainer("Characteristics");
            layout.characteristicsData.append(characteristicsDataContainer);

            let characteristicsBody = document.createElement("div");
            characteristicsBody.className = "card-body";
            characteristicsDataContainer.append(characteristicsBody);

            addInfo("Breed", this.formatData(this.data.reported.breeds), characteristicsBody);
            addInfo("Category", this.formatData(this.data.category), characteristicsBody);
            addInfo("Base Weight", this.formatData(this.data.reported.weight), characteristicsBody);
            addInfo("Wt. Variance", this.formatData(this.data.reported.weight_variance), characteristicsBody);
            addInfo("Frame", this.formatData(this.data.reported.usda_frame_size), characteristicsBody);
            addInfo("Horns", this.formatData(this.data.reported.horns), characteristicsBody);
            addInfo("Muscling", this.formatData(this.data.reported.muscling), characteristicsBody);
            addInfo("Pregnancy Status", this.formatData(this.data.reported.pregnancy_status), characteristicsBody);

            let commentCard = createCommentSection(this.data.reported.characteristics_comments);
            characteristicsDataContainer.append(commentCard);
        }

        // Maintenance
        {
            let maintenanceDataContainer = createSectionContainer("Management");
            layout.maintenanceData.append(maintenanceDataContainer);

            let maintenanceBody = document.createElement("div");
            maintenanceBody.className = "card-body";
            maintenanceDataContainer.append(maintenanceBody);

            addInfo("Vaccinations", this.formatData(this.data.reported.vaccinations), maintenanceBody);
            addInfo("Comingled Status", this.formatData(this.data.reported.comingled_status), maintenanceBody);
            addInfo("Creep Feed", this.formatData(this.data.reported.creep_feed), maintenanceBody);
            addInfo("Implants", this.formatData(this.data.reported.implants), maintenanceBody);
            addInfo("Castrated", this.formatData(this.data.reported.castrated), maintenanceBody);
            addInfo("Weaned", this.formatData(this.data.reported.weaned), maintenanceBody);

            let commentCard = createCommentSection(this.data.reported.maintenance_comments);
            maintenanceDataContainer.append(commentCard);
        }

        // Genetics
        {
            let geneticsDataContainer = createSectionContainer("Genetics");
            layout.geneticsData.append(geneticsDataContainer);

            let geneticsBody = document.createElement("div");
            geneticsBody.className = "card-body";
            geneticsDataContainer.append(geneticsBody);
            
            addInfo("Genetic or genomic testing performed?", this.formatData(this.data.reported.genomic_testing), geneticsBody);
            addInfo("Possess EPD's on the sires of the cattle planning to be sold", this.formatData(this.data.reported.epd), geneticsBody);
            addInfo("Genetics Merit Verification Co.", this.formatData(this.data.reported.verification), geneticsBody);
            addInfo("Breed Program Verification Co.", this.formatData(this.data.reported.breed_program_certification_co), geneticsBody);
            
            let commentCard = createCommentSection(this.data.reported.genetics_comments);
            geneticsDataContainer.append(commentCard);
        }

        // Value Add Programs
        {
            let valueAddDataContainer = createSectionContainer("Value Add Programs");
            layout.valueAddData.append(valueAddDataContainer);

            let valueAddBody = document.createElement("div");
            valueAddBody.className = "card-body";
            valueAddDataContainer.append(valueAddBody);
            
            addInfo("Program", this.formatData(this.data.reported.program), valueAddBody);
            addInfo("Precon Program", this.formatData(this.data.reported.preconditioning_program), valueAddBody);
            addInfo("Feeding Program", this.formatData(this.data.reported.feeding_programs), valueAddBody);

            let commentCard = createCommentSection(this.data.reported.program_comments);
            valueAddDataContainer.append(commentCard);
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
            return "N/A";
        else
            return data;
    }
}
