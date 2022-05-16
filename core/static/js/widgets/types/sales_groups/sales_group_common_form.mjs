import { ProgressBar } from '../../../core/progress_bar.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';
import { SwitchFormGroup } from '../../../ui/switch.mjs';
import { DateFormGroup, DateRangeFormGroup} from '../../../ui/inputs.mjs';
import { VideoSession } from '../../../files/video_links.mjs';
import { CreateAuctionMarketWidget } from './create_auction_market_widget.mjs'

export class SalesGroupsCommonForm{
    constructor(data, auctionMarketsData, postRoute) {
        this.box = document.createElement("div");
        this.data = data;
        // Initialize variables which hold field values
        if(data != null){
            this.salesGroupID = data.id;
            this.salesGroupNameValue = this.data.group_name;
            this.marketingCountValue = this.data.reported.count;
            this.marketingZIPValue = this.data.zip;
            this.marketingStartDateValue = this.data.start;
            this.marketingEndDateValue = this.data.end;
            this.marketingDeliveryLocationTypeValue = this.data.delivery_location_type;
            this.marketingDeliveryLocationValue = this.data.delivery_location;
            this.marketingPriceValue = this.data.price;
            this.characteristicBreedsValue = this.data.reported.breeds;
            this.characteristicsWeightValue = this.data.reported.weight;
            this.characteristicsWeightVarianceValue = this.data.reported.weight_variance;
            this.characteristicsFrameValue = this.data.reported.usda_frame_size;
            this.characteristicsMusclingValue = this.data.reported.muscling;
            this.characteristicsHornsValue = this.data.reported.horns;
            this.maintenancePreconditioningProgramValue = this.data.reported.preconditioning_program;
            this.maintenanceVaccinationsValue = this.data.reported.vaccinations;
            this.maintenanceFeedingProgramValue = this.data.reported.feeding_programs;
            this.maintenanceImplantsValue = this.data.reported.implants;
            this.maintenanceCastratedValue = this.data.reported.castrated;
            this.maintenanceProcessVerifiedProgramValue = this.data.reported.process_verified_program;
            this.reportedImages = this.data.reported.images;
            this.reportedVideos = this.data.reported.videos;
            this.fileAuths = this.data.file_auths
            this.comments = this.data.reported.comments;
            this.published = this.data.published;

        }
        else{
            this.salesGroupID = null;
            this.salesGroupNameValue = null;
            this.marketingCountValue = null;
            this.marketingZIPValue = null;
            this.marketingStartDateValue = null;
            this.marketingEndDateValue = null;
            this.marketingDeliveryLocationTypeValue = "Off Ranch";
            this.marketingAuctionMarketLocationValue = "None";
            this.marketingOffRanchLocationValue = null;
            this.marketingPriceValue = 0;
            this.characteristicBreedsValue = [];
            this.characteristicsWeightValue = null;
            this.characteristicsWeightVarianceValue = null;
            this.characteristicsFrameValue = "Small";
            this.characteristicsMusclingValue = "Light";
            this.characteristicsHornsValue = "Horns";
            this.maintenancePreconditioningProgramValue = "None";
            this.maintenanceVaccinationsValue = [];
            this.maintenanceFeedingProgramValue = [];
            this.maintenanceImplantsValue = [];
            this.maintenanceCastratedValue = "Not Castrated";
            this.maintenanceProcessVerifiedProgramValue = "None";
            this.reportedImages = [];
            this.reportedVideos = [];
            this.fileAuths = null;
            this.comments = "";
            this.published = true;
        }
        this.auctionMarketsData = auctionMarketsData;
        this.postRoute = postRoute;
        this.makeForm();
        return this.box;
    }
    
    makeForm() {
        // Sections
        function addTooltip(dataToggle,title,position){
            let toolTip = document.createElement("a");
            toolTip.className="feather icon-info";
            toolTip.style = "color:#2962FF;padding-left:6px;width:100%; vertical-align:-1px";
            toolTip.setAttribute("data-toggle" ,dataToggle);
            toolTip.setAttribute("data-placement" ,"right");
            toolTip.setAttribute("title" ,title);
            position.append(toolTip);           
            $(document).ready(function(){
                $('[data-toggle='+dataToggle+']').tooltip();
            });
        }
       

        function createSection(form, name) {
            let header = document.createElement("h6");
            header.textContent = name;
            form.append(header);
            let row = document.createElement("div");
            row.className = "form-row";
            form.append(row);
            form.append(document.createElement("br"));
            return row;
        }

        function createGroup(row, name, htmlFor, hasTooltip, dataToggle, tooltipText, groupColumnSize=4, addAuctionMarketLink=false) {
            let group = document.createElement("div");
            group.className = `form-group col-md-${groupColumnSize}`;
            row.append(group);
            let groupLabel = document.createElement("label");
            groupLabel.className = "form-label";
            groupLabel.textContent = name;
            if (hasTooltip)
                addTooltip(dataToggle,tooltipText,groupLabel);
            if (htmlFor !== null) {
                groupLabel.htmlFor = htmlFor;
            }
            if(addAuctionMarketLink){
                let newLink = document.createElement("a");
                newLink.className = "form-label text-primary";
                newLink.textContent = "Not Listed?";
                newLink.onclick = () => {
                    let widget = new CreateAuctionMarketWidget();
                    widget.init();
                }
                groupLabel.append(newLink);
            }
            group.append(groupLabel);
            return group;
        }

        function createNumber(row, name, value, hasTooltip=false, dataToggle="", tooltipText="", groupColumnSize=4, isDecimal=false) {
            let id = "domuid" + window.DOMUIDNext++;
            let group = createGroup(row, name, id, hasTooltip, dataToggle, tooltipText, groupColumnSize);
            let input = document.createElement("input");
            input.type = "number";
            if (isDecimal) {
                input.step = "0.01";
            }
            input.value = value;
            input.className = "form-control";
            input.id = id;
            input.required = true
            group.append(input);
            return input;
        }

        function createText(row, name, value, hasTooltip=false, dataToggle="", tooltipText="", groupColumnSize=4) {
            let id = "domuid" + window.DOMUIDNext++;
            let group = createGroup(row, name, id, hasTooltip, dataToggle, tooltipText, groupColumnSize);
            let input = document.createElement("input");
            input.type = "text";
            input.value = value;
            input.className = "form-control";
            input.id = id;
            input.required = true
            group.append(input);
            return input;
        }

        function createDate(row, name, epoch, hasTooltip=false, dataToggle="", tooltipText="") {
            let dateFormGroup = new DateFormGroup(row, name, epoch);
            dateFormGroup.getFormGroup().classList.add("col-md-4");
            if (hasTooltip)
                addTooltip(dataToggle,tooltipText,dateFormGroup.getFormLabel());
            return dateFormGroup;
        }

        function createDateRangePicker(row, name, startEpoch, endEpoch, hasTooltip=false, dataToggle="", tooltipText="") {
            let startDate = new DateRangeFormGroup(row, name, startEpoch, endEpoch);
            startDate.getFormGroup().classList.add("col-md-4");
            if (hasTooltip)
                addTooltip(dataToggle,tooltipText,startDate.getFormLabel());
            return startDate;
        }

        function createSelect({row, name, options, values, multiple, tags, placeholder}, hasTooltip=false, dataToggle="", tooltipText="", groupColumnSize=4, addAuctionMarketLink=false) {
            let id = "domuid" + window.DOMUIDNext++;
            if (!Array.isArray(values)) {
                values = [values];
            }
            let group = createGroup(row, name, id, hasTooltip, dataToggle, tooltipText, groupColumnSize, addAuctionMarketLink);
            let select = document.createElement("select");
            select.className = "select2-hidden-accessible";
            select.id = id;
            select.required = true
            group.append(select);
            let optionsStacked = [];
            for (const option of options) {
                optionsStacked.push({
                    id: option,
                    text: option
                })
            }

            for (const value of values) {
                let good = false;
                for (const option of optionsStacked) {
                    if (option.id == value) {
                        option.selected = true;
                        good = true;
                        break;
                    }
                }
                if (!good) {
                    optionsStacked.push({
                        id: value,
                        text: value,
                        selected: true
                    });
                }
            }

            $(select).select2({
                data: optionsStacked,
                multiple: multiple,
                tags: tags,
                placeholder: placeholder
            });

            if (values.length == 0) {
                // Patch
                $(select).val([options[0]]);
                $(select).trigger('change');
                setTimeout(function () {
                    $(select).val([]);
                    $(select).trigger('change');
                }, 1);
            }
            return select;
        }

        let that = this;
        let form = document.createElement("form");
        this.box.append(form);

        // Marketing

        let marketingRow = createSection(form, "Marketing");

        let salesGroupName = createText(marketingRow,"Sales Group Nickname", this.salesGroupNameValue,true,"salesGroupNickname","This is the name for this sales group", 4);
        let marketingCount = createNumber(marketingRow, "Total Animals", this.marketingCountValue, false, "", "", 2);
        let marketingZIP = createNumber(marketingRow, "Market ZIP Code", this.marketingZIPValue,true,"marketingZIP","This is the zip code of location where the cattle will be picked up.", 2);
        let marketingPrice = createNumber(marketingRow, "Sales Group Price", this.marketingPriceValue || null,true,"marketingPrice", "Please enter the approximate price for the Sales Group", 4, true);
        let marketingDates = createDateRangePicker(marketingRow, "Market Dates", this.marketingStartDateValue, this.marketingEndDateValue, true, "marketingRange","This is the date range for the sale.");
        let marketingDeliveryLocationType = createSelect({
            row: marketingRow,
            name: "Delivery Location Type",
            options: SalesGroupFields.commonDeliveryLocationTypes,
            values: this.marketingDeliveryLocationTypeValue,
            multiple: false,
            tags: false,
            placeholder: "Select Sale Location Type"
        }, false, "", "", 4);
        
        let deliveryLocation = "";
        let auctionMarket = "";
        if(this.marketingDeliveryLocationTypeValue === "Off Ranch"){
            deliveryLocation = this.marketingDeliveryLocationValue;
        }
        else{
            auctionMarket = this.marketingDeliveryLocationValue;
        }
        
        let marketingAuctionMarketLocation = createSelect({
            row: marketingRow,
            name: "Auction Market: ",
            options: this.auctionMarketsData,
            values: auctionMarket || "None",
            multiple: false,
            tags: false,
            placeholder: "Select Auction Market"
        }, false, "", "", 4, true);
        let marketingOffRanchLocation = createText(marketingRow,"Delivery Location",deliveryLocation || null,true,"marketingOffRanchLocation","This is the place where the cattle will be picked up (example “ABC Auction Market” or “Off Ranch”)", 4);

        marketingDeliveryLocationType.onchange = () => {
            if(marketingDeliveryLocationType.value === "Off Ranch"){
                marketingOffRanchLocation.disabled=false;

                marketingAuctionMarketLocation.value="None";
                marketingAuctionMarketLocation.disabled=true;
            }
            else{
                marketingAuctionMarketLocation.disabled=false;

                marketingOffRanchLocation.value="";
                marketingOffRanchLocation.disabled=true;
            }
        }
        marketingDeliveryLocationType.onchange();

        //TODO: below code adds a dropdown to select auction sale which is retained in case needed in future.
        // let marketingAuctionSale = new SelectAuctionSaleFormGroup(
        //     marketingRow,
        //     this.data.auction_sale || null,
        //     this.data.auction_sale_name || null
        // );
        // marketingAuctionSale.getFormGroup().classList.add("col-md-4");
        
        // Characteristics

        let characteristicsRow = createSection(form, "Characteristics");

        let characteristicBreeds = createSelect({
            row: characteristicsRow,
            name: "Breed",
            options: SalesGroupFields.commonBreedNames,
            values: this.characteristicBreedsValue,
            multiple: true,
            tags: true,
            placeholder: "Select Applicable Breeds"
        },true,"characteristicBreeds","Please choose all the breeds of cattle in the group.", 4);
        let characteristicsWeight = createNumber(characteristicsRow, "Base Weight", this.characteristicsWeightValue,true,"characteristicsWeight",
        "Please enter the average weight of the cattle in the group", 4);
        let characteristicsWeightVariance = createText(characteristicsRow, "Weight Variance", this.characteristicsWeightVarianceValue,
        true,"characteristicsWeightVariance","Please enter the variance of the weight average since it is not exact. (example: “20 lbs”)", 4);
        let characteristicsFrame = createSelect({
            row: characteristicsRow,
            name: "Frame",
            options: SalesGroupFields.commonFrames,
            values: this.characteristicsFrameValue,
            multiple: false,
            tags: false,
            placeholder: "Select Frame"
        }, false, "", "", 4);
        let characteristicsMuscling = createSelect({
            row: characteristicsRow,
            name: "Muscling",
            options: ["Light", "Heavy"],
            values: this.characteristicsMusclingValue,
            multiple: false,
            tags: false,
            placeholder: "Select Muscling"
        }, false, "", "", 4);
        let characteristicsHorns = createSelect({
            row: characteristicsRow,
            name: "Horns",
            options: ["Horns", "No Horns"],
            values: this.characteristicsHornsValue,
            multiple: false,
            tags: false,
            placeholder: "Select Horns"
        }, false, "", "", 4);

        // Maintenance

        let maintenanceRow = createSection(form, "Maintenance");

        let maintenancePreconditioningProgram = createSelect({
            row: maintenanceRow,
            name: "Precon Program",
            options: SalesGroupFields.commonPreconditioningProgramNames,
            values: this.maintenancePreconditioningProgramValue,
            multiple: false,
            tags: true,
            placeholder: "Select Precon Program"
        }, true, "maintenancePreconditioningProgram", "Please enter the pre-conditioning program this group of cattle is on or “not listed”.", 4);
        let maintenanceVaccinations = createSelect({
            row: maintenanceRow,
            name: "Vaccinations",
            options: SalesGroupFields.commonVaccinations,
            values: this.maintenanceVaccinationsValue,
            multiple: true,
            tags: true,
            placeholder: "Select Vaccinations"
        }, true, "maintenanceVaccinations", "Please enter vaccinations given to the cattle in this group or “not listed”.", 4);
        let maintenanceFeedingProgram = createSelect({
            row: maintenanceRow,
            name: "Feeding Program",
            options: SalesGroupFields.commonFeedingPrograms,
            values: this.maintenanceFeedingProgramValue,
            multiple: true,
            tags: true,
            placeholder: "Select Feeding Program"
        }, true, "maintenanceFeedingProgram", "Please enter the feeding program this group of cattle is on or “not listed”.", 4);
        let maintenanceImplants = createSelect({
            row: maintenanceRow,
            name: "Implants",
            options: SalesGroupFields.commonImplants,
            values: this.maintenanceImplantsValue,
            multiple: true,
            tags: true,
            placeholder: "Select Implants"
        }, false, "" , "", 4);
        let maintenanceCastrated = createSelect({
            row: maintenanceRow,
            name: "Castrated",
            options: SalesGroupFields.commonCastrated,
            values: this.maintenanceCastratedValue,
            multiple: false,
            tags: false,
            placeholder: "Select Castration Method"
        }, false, "", "", 4);
        let maintenanceProcessVerifiedProgram = createSelect({
            row: maintenanceRow,
            name: "PVP Program",
            options: SalesGroupFields.commonPVPProgramNames,
            values: this.maintenanceProcessVerifiedProgramValue,
            multiple: false,
            tags: false,
            placeholder: "Select Process Verified Program"
        }, true, "maintenanceProcessVerifiedProgram", "Please enter the Processed Verified  program this group of cattle is on or “not listed”.", 4);
        // Media

        let mediaRow = createSection(form, "Image");

        let mediaGroup = document.createElement("div");
        mediaGroup.className = "form-group col-12";
        mediaRow.append(mediaGroup);

        let mediaLabel = document.createElement("label")
        mediaLabel.textContent = "Add images here to make the post look more attractive!";
        mediaGroup.append(mediaLabel);

        let fileEditorFrame = document.createElement("div");
        this.fileEditor = new BasicFileEditor({filetype:["image"]}, fileEditorFrame, this.reportedImages, this.fileAuths);
        mediaGroup.append(fileEditorFrame);


        //Video

        let videoRow = createSection(form, "Video");

        let videoGroup = document.createElement("div");
        videoGroup.className = "form-group col-12";
        videoRow.append(videoGroup);

        let videoLabel = document.createElement("label");
        videoLabel.textContent = "Add Youtube/Vimeo links here to make the post look more attractive!";
        videoGroup.append(videoLabel);

        let videoText = document.createElement("div");
        this.VideoEditor = new VideoSession({}, videoText, this.reportedVideos, this.fileAuths);
        videoGroup.append(videoText);

        // Comments

        let commentsHeader = document.createElement("h6");
        commentsHeader.textContent = "Comments";
        form.append(commentsHeader);
        addTooltip("commentsHeader","Please enter anything you want the buyers to know about this group of cattle that may not be listed in the above sections.",commentsHeader);

        let commentsRow = document.createElement("div");
        commentsRow.className = "form-row";
        form.append(commentsRow);

        let commentsGroup = document.createElement("div")
        commentsGroup.className = "form-group col";
        commentsRow.append(commentsGroup);

        let commentsTA = document.createElement("textarea");
        commentsTA.maxLength = 1000;
        commentsTA.className = "form-control max-textarea";
        commentsTA.rows = 4;
        commentsTA.value = this.comments;
        commentsGroup.append(commentsTA);

        form.append(document.createElement("br"));

        // EIDs
        
        // Leaving this here just in case we will need it for new in house UI
        // let eidsHeader = document.createElement("h6");
        // eidsHeader.textContent = "EIDs";
        // form.append(eidsHeader);

        // let eidButton = document.createElement("button");
        // eidButton.className = "btn btn-primary";
        // eidButton.textContent = "Add EID's";
        // eidButton.type = "button";
        // form.append(eidButton);

        // Publish

        let publishSwitch = new SwitchFormGroup(form, "Publish", this.published);

        // Save

        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        form.append(submitFormGroup);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.type = "button";
        submitFormGroup.append(submitButton);

        this.progressBar = new ProgressBar();
        this.progressBar.attach(form);
        this.progressBar.hide();

        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);
        this.internalErrorMessage = document.createElement("p");
        this.internalErrorMessage.style.display = "none";
        this.internalErrorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(this.internalErrorMessage);

        this.asyncForm = new AsyncForm({
            action: this.postRoute,
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                function safeInt(v) {
                    if (v === "") {
                        return null;
                    }
                    return Math.floor(parseFloat(v));
                }

                return {
                    id: that.salesGroupID,
                    published: publishSwitch.isChecked(),
                    eids: [],
                    reported: {
                        comments: commentsTA.value,
                        count: safeInt(marketingCount.value),
                        weight: safeInt(characteristicsWeight.value),
                        weight_variance: characteristicsWeightVariance.value,
                        breeds: $(characteristicBreeds).val(),
                        horns: characteristicsHorns.value,
                        muscling: characteristicsMuscling.value,
                        usda_frame_size: characteristicsFrame.value,
                        preconditioning_program: maintenancePreconditioningProgram.value,
                        vaccinations: $(maintenanceVaccinations).val(),
                        feeding_programs: $(maintenanceFeedingProgram).val(),
                        implants: $(maintenanceImplants).val(),
                        castrated: maintenanceCastrated.value,
                        process_verified_program: maintenanceProcessVerifiedProgram.value,
                        images: that.fileEditor.getFileIDs(),
                        videos: that.VideoEditor.getVideoLinks(),
                    },
                    "delivery_location_type": marketingDeliveryLocationType.value,
                    "delivery_location": marketingOffRanchLocation.value,
                    "zip": parseInt(marketingZIP.value),
                    "start": marketingDates.getStartTime(),
                    "end": marketingDates.getEndTime(),
                    "group_name": salesGroupName.value,
                    "price": marketingPrice.value,
                    "auction_market_location": marketingAuctionMarketLocation.value,
                    //TODO: Removed auction_sale for now. Retained incase needed in future.
                    //auction_sale: marketingAuctionSale.getID()
                    auction_sale: null                   
                }
            }
        });

        submitButton.addEventListener("click", () => {
            this.internalErrorMessage.style.display = "none";
            function progress(perc) {
                that.progressBar.setProgress(perc);
            }
            that.progressBar.show();
            this.fileEditor.upload(progress)
                .then(() => {
                    this.asyncForm.submit();
                });
        });
    }
}