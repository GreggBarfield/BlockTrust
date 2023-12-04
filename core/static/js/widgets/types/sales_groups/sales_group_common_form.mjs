import { ProgressBar } from '../../../core/progress_bar.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';
import { SwitchFormGroup } from '../../../ui/switch.mjs';
import { DateFormGroup, DateRangeFormGroup} from '../../../ui/inputs.mjs';
import { VideoSession } from '../../../files/video_links.mjs';
import { CreateAuctionMarketWidget } from './create_auction_market_widget.mjs'

export class SalesGroupsCommonForm{
    constructor(data, auctionMarketsData, postRoute, preSelectAuctionMarket="false", preSelectedAuctionMarketId=null) {
        this.box = document.createElement("div");
        this.data = data;
        // Initialize variables which hold field values
        if(data != null){
            this.salesGroupID = data.id;
            this.salesGroupNameValue = this.data.group_name;
            this.marketingCountValue = this.data.reported.count;
            this.marketingZIPValue = this.data.zip;
            this.marketingSaleDateValue = this.data.sale_date;
            this.marketingDeliveryLocationTypeValue = this.data.delivery_location_type;
            this.marketingDeliveryLocationValue = this.data.delivery_location;
            this.auctionMarketID = this.data.auction_market_id;
            this.marketingPriceValue = this.data.price;
            this.marketingSlideValue = this.data.reported.marketing_slide;
            this.marketingWeighingConditionsValue = this.data.reported.marketing_weighing_conditions;
            this.marketingRepresentedByValue = this.data.reported.marketing_represented_by;
            this.characteristicsCategoryValue = this.data.category;
            this.characteristicBreedsValue = this.data.reported.breeds;
            this.characteristicsBreedCommentsValue = this.data.breed_comments;
            this.characteristicsWeightValue = this.data.reported.weight;
            this.characteristicsWeightVarianceValue = this.data.reported.weight_variance;
            this.characteristicsWeighingConditionsValue = this.data.weighing_conditions;
            this.characteristicsFrameValue = this.data.reported.usda_frame_size;
            this.characteristicsMusclingValue = this.data.reported.muscling;
            this.characteristicsHornsValue = this.data.reported.horns;
            this.geneticsGenomicTestingValue = this.data.reported.genomic_testing;
            this.geneticsEPDValue = this.data.reported.epd;
            this.geneticsCommentsValue = this.data.reported.genetics_comments;
            this.maintenancePreconditioningProgramValue = this.data.reported.preconditioning_program;
            this.maintenanceVaccinationsValue = this.data.reported.vaccinations;
            this.maintenanceAnnualCattleHerdVaccinationsValue = Boolean(this.data.are_annual_cattle_herd_vaccinations_given)?"Yes":"No";
            this.maintenanceFeedingProgramValue = this.data.reported.feeding_programs;
            this.maintenanceImplantsValue = this.data.reported.implants;
            this.maintenanceCastratedValue = this.data.reported.castrated;
            this.maintenanceProgramValue = this.data.reported.program;
            this.reportedImages = this.data.reported.images;
            this.reportedVideos = this.data.reported.videos;
            this.fileAuths = this.data.file_auths
            this.comments = this.data.reported.comments;
            this.published = this.data.published;
            this.showAccountCarcassData = this.data.show_account_carcass_data;
        }
        else{
            this.salesGroupID = null;
            this.salesGroupNameValue = null;
            this.marketingCountValue = null;
            this.marketingZIPValue = null;
            this.marketingSaleDateValue = null;
            this.marketingDeliveryLocationTypeValue = "";
            this.marketingDeliveryLocationValue = "";
            this.marketingAuctionMarketLocationValue = "";
            this.marketingOffRanchLocationValue = null;
            this.marketingPriceValue = 0;
            this.marketingSlideValue = "";
            this.marketingWeighingConditionsValue = "";
            this.marketingRepresentedByValue = "";
            this.characteristicsCategoryValue = "";
            this.characteristicBreedsValue = [];
            this.characteristicsBreedCommentsValue = null;
            this.characteristicsWeightValue = null;
            this.characteristicsWeightVarianceValue = null;
            this.characteristicsWeighingConditionsValue = null;
            this.characteristicsFrameValue = "";
            this.characteristicsMusclingValue = "";
            this.characteristicsHornsValue = "";
            this.geneticsGenomicTestingValue = "";
            this.geneticsEPDValue = "";
            this.geneticsCommentsValue = "";
            this.maintenancePreconditioningProgramValue = "";
            this.maintenanceVaccinationsValue = [];
            this.maintenanceAnnualCattleHerdVaccinationsValue = ""
            this.maintenanceFeedingProgramValue = [];
            this.maintenanceImplantsValue = [];
            this.maintenanceCastratedValue = "";
            this.maintenanceProgramValue = [];
            this.reportedImages = [];
            this.reportedVideos = [];
            this.fileAuths = null;
            this.comments = "";
            this.published = true;
            this.showAccountCarcassData = true;
        }
        this.auctionMarketsData = auctionMarketsData;
        this.postRoute = postRoute;
        this.preSelectAuctionMarket = preSelectAuctionMarket;
        this.preSelectedAuctionMarketId = preSelectedAuctionMarketId;
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

        function createSelect({row, name, options, values, multiple, tags, placeholder}, hasTooltip=false, dataToggle="", tooltipText="", groupColumnSize=4, addAuctionMarketLink=false, optionsObject=null) {
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

            if(optionsObject){
                for (const [key,value] of Object.entries(optionsObject)) {
                    optionsStacked.push({
                        id: key,
                        text: value
                    })
                }               
            }
            else{
                for (const option of options) {
                    optionsStacked.push({
                        id: option,
                        text: option
                    })
                }
            }
            for (const value of values) {
                for (const option of optionsStacked) {
                    if (option.id == value) {
                        option.selected = true;
                        break;
                    }
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
            $(select).trigger('change');
            return select;
        }

        let form = document.createElement("form");
        this.box.append(form);

        // Marketing

        let marketingRow = createSection(form, "Marketing");

        let salesGroupName = createText(marketingRow,"Sales Group Nickname", this.salesGroupNameValue,true,"salesGroupNickname","This is the name for this sales group", 4);
        let marketingCount = createNumber(marketingRow, "Total Animals", this.marketingCountValue, false, "", "", 2);
        let marketingZIP = createNumber(marketingRow, "Market ZIP Code", this.marketingZIPValue,true,"marketingZIP","This is the zip code of location where the cattle will be picked up.", 2);
        //let marketingPrice = createNumber(marketingRow, "Sales Group Price", this.marketingPriceValue || null,true,"marketingPrice", "Please enter the approximate price for the Sales Group", 4, true);
        let marketingDate = createDate(marketingRow, "Market Date", this.marketingSaleDateValue, true, "marketingDate","This is the date for the sale.");
        
        let marketingDeliveryLocationType = createSelect({
            row: marketingRow,
            name: "Market Type",
            options: SalesGroupFields.commonDeliveryLocationTypes,
            values: this.marketingDeliveryLocationTypeValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        
        let deliveryLocation = "";
        let auctionMarket = "";
        if(this.marketingDeliveryLocationTypeValue === "Direct/Off Ranch"){
            deliveryLocation = this.marketingDeliveryLocationValue;
        }
        else if(this.marketingDeliveryLocationTypeValue === "Auction"){
            auctionMarket = this.auctionMarketID;
        }
        let marketingAuctionMarketLocation = createSelect({
            row: marketingRow,
            name: "Auction Market: ",
            values: auctionMarket || "None",
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4, true, this.auctionMarketsData);


        let marketingOffRanchLocation = createText(marketingRow,"Delivery Location",deliveryLocation || null,true,"marketingOffRanchLocation","This is the place where the cattle will be picked up (example “ABC Auction Market” or “Direct/Off Ranch”)", 4);
        let marketingSlide = createText(marketingRow,"Slide",this.marketingSlideValue || "",true,"marketingSlide","", 4);
        let marketingWeighingConditions = createText(marketingRow,"Weighing Conditions",this.marketingWeighingConditionsValue || "",true,"marketingWeighingConditions","", 4);
        let marketingRepresentedBy = createText(marketingRow,"Represented By",this.marketingRepresentedByValue || "",true,"marketingRepresentedBy","", 4);

        marketingDeliveryLocationType.onchange = () => {
            marketingSlide.disabled = true;
            marketingWeighingConditions.disabled = true;
            marketingAuctionMarketLocation.disabled=true;
            marketingOffRanchLocation.disabled=true;

            marketingSlide.value = "";
            marketingWeighingConditions.value = "";
            marketingOffRanchLocation.value= "";
            marketingAuctionMarketLocation.value="None";

            if(marketingDeliveryLocationType.value === "Direct/Off Ranch"){
                marketingOffRanchLocation.disabled=false;
                marketingOffRanchLocation.value = deliveryLocation;
                // Remove comments when marketingPrice is enabled again
                //marketingPrice.disabled = false;
                //marketingPrice.value = this.marketingPriceValue
            }
            else if(marketingDeliveryLocationType.value === "Auction"){
                marketingAuctionMarketLocation.disabled=false;
                marketingAuctionMarketLocation.value = auctionMarket;
                // Remove comments when marketingPrice is enabled again
                //marketingPrice.disabled = true;
                //marketingPrice.value = 0;
            }
            else if(marketingDeliveryLocationType.value === "Video Auction"){
                marketingSlide.disabled = false;
                marketingWeighingConditions.disabled = false;
                marketingSlide.value = this.marketingSlideValue;
                marketingWeighingConditions.value = this.marketingWeighingConditionsValue;
            }
        }
        marketingDeliveryLocationType.onchange();

        if(this.preSelectAuctionMarket === "true"){
            $(marketingDeliveryLocationType).val("Auction");
            $(marketingDeliveryLocationType).trigger('change');
            marketingDeliveryLocationType.disabled=true;
            $(marketingAuctionMarketLocation).val(this.preSelectedAuctionMarketId);
            $(marketingAuctionMarketLocation).trigger('change');
            marketingAuctionMarketLocation.disabled=true;
            marketingOffRanchLocation.disabled=true;
            marketingSlide.disabled=true;
            marketingWeighingConditions.disabled=true;
        }

        // Characteristics

        let characteristicsRow = createSection(form, "Characteristics");
        
        let characteristicsCategory = createSelect({
            row: characteristicsRow,
            name: "Category/Sex",
            options: SalesGroupFields.commonCategoryNames,
            values: this.characteristicsCategoryValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        },false,"","", 4);
        let characteristicBreeds = createSelect({
            row: characteristicsRow,
            name: "Breed",
            options: SalesGroupFields.commonBreedNames,
            values: this.characteristicBreedsValue,
            multiple: true,
            tags: true,
            placeholder: "Please Select"
        },true,"characteristicBreeds","Please choose all the breeds of cattle in the group.", 4);
        let characteristicsBreedComments = createText(characteristicsRow,"Breed Comments",this.characteristicsBreedCommentsValue,false,"characteristicsBreedComments","",4);
        let characteristicsWeight = createNumber(characteristicsRow,"Base Weight",this.characteristicsWeightValue,true,"characteristicsWeight",
        "Please enter the average weight of the cattle in the group", 4);
        let characteristicsWeightVariance = createText(characteristicsRow, "Weight Variance", this.characteristicsWeightVarianceValue,
        true,"characteristicsWeightVariance","Please enter the variance of the weight average since it is not exact. (example: “20 lbs”)", 4);
        let characteristicsWeighingConditions = createText(characteristicsRow,"Other Comments",this.characteristicsWeighingConditionsValue,false,"characteristicsWeighingConditions","",4);
        let characteristicsFrame = createSelect({
            row: characteristicsRow,
            name: "Frame",
            options: SalesGroupFields.commonFrames,
            values: this.characteristicsFrameValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let characteristicsMuscling = createSelect({
            row: characteristicsRow,
            name: "Muscling",
            options: SalesGroupFields.commonMusclings,
            values: this.characteristicsMusclingValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let characteristicsHorns = createSelect({
            row: characteristicsRow,
            name: "Horns",
            options: SalesGroupFields.commonHorns,
            values: this.characteristicsHornsValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);

        // Maintenance

        let geneticsRow = createSection(form, "Genetics");

        let geneticsGenomicTesting = createSelect({
            row: geneticsRow,
            name: "Do you do genetic or genomic testing?",
            options: ["Yes", "No"],
            values: this.geneticsGenomicTestingValue || "",
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let geneticsEPD = createSelect({
            row: geneticsRow,
            name: "Do you have the EPD's on the sires of the cattle you're planning to sell?",
            options: ["Yes", "No"],
            values: this.geneticsEPDValue || "",
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let geneticsComments = createText(geneticsRow,"Enter any comment related to genetics.",this.geneticsCommentsValue || "",false,"geneticsComments","", 4);

        let maintenanceRow = createSection(form, "Maintenance");

        let maintenancePreconditioningProgram = createSelect({
            row: maintenanceRow,
            name: "Precon Program",
            options: SalesGroupFields.commonPreconditioningProgramNames,
            values: this.maintenancePreconditioningProgramValue,
            multiple: false,
            tags: true,
            placeholder: "Please Select"
        }, true, "maintenancePreconditioningProgram", "Please enter the pre-conditioning program this group of cattle is on or “not listed”.", 4);
        let maintenanceVaccinations = createSelect({
            row: maintenanceRow,
            name: "Vaccinations",
            options: SalesGroupFields.commonVaccinations,
            values: this.maintenanceVaccinationsValue,
            multiple: true,
            tags: true,
            placeholder: "Please Select"
        }, true, "maintenanceVaccinations", "Please enter vaccinations given to the cattle in this group or “not listed”.", 2);

        let maintenanceAnnualCattleHerdVaccinations = createSelect({
            row: maintenanceRow,
            name: "Annual Cattle Herd Vaccinations",
            options: ["Yes", "No"],
            values: this.maintenanceAnnualCattleHerdVaccinationsValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 2);
        let maintenanceFeedingProgram = createSelect({
            row: maintenanceRow,
            name: "Feeding Program",
            options: SalesGroupFields.commonFeedingPrograms,
            values: this.maintenanceFeedingProgramValue,
            multiple: true,
            tags: true,
            placeholder: "Please Select"
        }, true, "maintenanceFeedingProgram", "Please enter the feeding program this group of cattle is on or “not listed”.", 4);
        let maintenanceImplants = createSelect({
            row: maintenanceRow,
            name: "Implants",
            options: SalesGroupFields.commonImplants,
            values: this.maintenanceImplantsValue,
            multiple: true,
            tags: true,
            placeholder: "Please Select"
        }, false, "" , "", 4);
        let maintenanceCastrated = createSelect({
            row: maintenanceRow,
            name: "Castrated",
            options: SalesGroupFields.commonCastrated,
            values: this.maintenanceCastratedValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let maintenanceProgram = createSelect({
            row: maintenanceRow,
            name: "Program",
            options: SalesGroupFields.commonProgramNames,
            values: this.maintenanceProgramValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, true, "maintenanceProgram", "Please enter the Processed Verified  program this group of cattle is on or “not listed”.", 4);
        // Media

        let mediaRow = createSection(form, "Image");

        let mediaGroup = document.createElement("div");
        mediaGroup.className = "form-group col-12";
        mediaRow.append(mediaGroup);

        let mediaLabel = document.createElement("label")
        mediaLabel.textContent = "Add images here to make the post look more attractive!";
        mediaGroup.append(mediaLabel);

        let fileEditorFrame = document.createElement("div");
        let fileEditor = new BasicFileEditor({filetype:["image"]}, fileEditorFrame, this.reportedImages, this.fileAuths);
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
        let videoEditor = new VideoSession({}, videoText, this.reportedVideos, this.fileAuths);
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

        // Publish

        let publishSwitch = new SwitchFormGroup(form, "Publish", this.published);

        let showAccountCarcassDataSwitch = new SwitchFormGroup(form, "Show Carcass History", this.showAccountCarcassData);

        // Save

        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        form.append(submitFormGroup);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.type = "button";
        submitFormGroup.append(submitButton);
      
        //progress bar needs to be accessible from parent
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
        let internalErrorMessage = document.createElement("p");
        internalErrorMessage.style.display = "none";
        internalErrorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(internalErrorMessage);

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
                    id: this.salesGroupID,
                    published: publishSwitch.isChecked(),
                    show_account_carcass_data: showAccountCarcassDataSwitch.isChecked(),
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
                        program: maintenanceProgram.value,
                        images: fileEditor.getFileIDs(),
                        videos: videoEditor.getVideoLinks(),
                        marketing_slide: marketingSlide.value,
                        marketing_weighing_conditions: marketingWeighingConditions.value,
                        marketing_represented_by: marketingRepresentedBy.value,
                        genomic_testing: geneticsGenomicTesting.value,
                        epd: geneticsEPD.value,
                        genetics_comments: geneticsComments.value
                    },
                    "delivery_location_type": marketingDeliveryLocationType.value,
                    "delivery_location": marketingOffRanchLocation.value,
                    "auction_market_id": marketingAuctionMarketLocation.value,
                    "zip": parseInt(marketingZIP.value),
                    "sale_date": marketingDate.getTime(),
                    "group_name": salesGroupName.value,
                    "price": 0, //marketingPrice.value,
                    "auction_market_location": $(marketingAuctionMarketLocation).find(':selected').text(),
                    "category": characteristicsCategory.value,
                    "breed_comments": characteristicsBreedComments.value,
                    "weighing_conditions": characteristicsWeighingConditions.value,
                    "are_annual_cattle_herd_vaccinations_given": maintenanceAnnualCattleHerdVaccinations.value=="Yes"?1:0,              
                }
            }
        });

        submitButton.addEventListener("click", () => {
            internalErrorMessage.style.display = "none";
            let parent = this;
            function setProgress(perc) {
                parent.progressBar.setProgress(perc);
            }
            this.progressBar.show();
            fileEditor.upload(setProgress)
                .then(() => {
                    this.asyncForm.submit();
                });
        });
    }
}