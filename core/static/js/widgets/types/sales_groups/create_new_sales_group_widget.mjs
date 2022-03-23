import { ProgressBar } from '../../../core/progress_bar.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';
import { SwitchFormGroup } from '../../../ui/switch.mjs';
import { DateFormGroup, DateRangeFormGroup} from '../../../ui/inputs.mjs';
import { VideoSession } from '../../../files/video_links.mjs';

export class CreateNewSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
    this.getData(
        "auction_markets"
    ).then((data) => {
        this.auctionMarketsData = this.processAuctionMarketsData(data.auction_markets);
        this.makeForm();
    });

    this.onSomeDataLoaded(function () {
        this.frame.innerHTML = "";
    });
    }

    processAuctionMarketsData(auctionMarkets){
        let selectData=[];
        selectData.push("None");
        for(const auctionMarket of auctionMarkets){
            let optionText = auctionMarket.name+", "+auctionMarket.city+", "+auctionMarket.state;
            selectData.push(optionText);
        }
        return selectData;
    }

    makeForm(){
    
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

    function createGroup(row, name, htmlFor,hasTooltip,dataToggle,tooltipText) {
        let group = document.createElement("div");
        group.className = "form-group col-md-4";
        row.append(group);


        let groupLabel = document.createElement("label");
        groupLabel.className = "form-label";
        groupLabel.textContent = name;
        if (hasTooltip)
            addTooltip(dataToggle,tooltipText,groupLabel);
        if (htmlFor !== null) {
            groupLabel.htmlFor = htmlFor;
        }
        group.append(groupLabel);
        return group;
    }

    function createNumber(row, name, value,hasTooltip=false,dataToggle="",tooltipText="") {
        let id = "domuid" + window.DOMUIDNext++;
        let group = createGroup(row, name, id,hasTooltip,dataToggle,tooltipText);
        let input = document.createElement("input");
        input.type = "number";
        input.value = value;
        input.className = "form-control";
        input.id = id;
        input.required = true
        group.append(input);
        return input;
    }

    function createText(row, name, value,hasTooltip=false,dataToggle="",tooltipText="") {
        let id = "domuid" + window.DOMUIDNext++;
        let group = createGroup(row, name, id,hasTooltip,dataToggle,tooltipText);
        let input = document.createElement("input");
        input.type = "text";
        input.value = value;
        input.className = "form-control";
        input.id = id;
        input.required = true
        group.append(input);
        return input;
    }

    function createDate(row, name, epoch,hasTooltip=false,dataToggle="",tooltipText="") {
        let dateFormGroup = new DateFormGroup(row, name, epoch);
        dateFormGroup.getFormGroup().classList.add("col-md-4");
        if (hasTooltip)
            addTooltip(dataToggle,tooltipText,dateFormGroup.getFormLabel());
        return dateFormGroup;
    }

    function createDateRangePicker(row,name,startEpoch,endEpoch,hasTooltip=false,dataToggle="",tooltipText="") {
        let startDate = new DateRangeFormGroup(row, name, startEpoch, endEpoch);
        startDate.getFormGroup().classList.add("col-md-4");
        if (hasTooltip)
            addTooltip(dataToggle,tooltipText,startDate.getFormLabel());
        return startDate;
    }

    function createSelect({row, name, options, values, multiple, tags, placeholder},hasTooltip=false,dataToggle="",tooltipText="") {
        let id = "domuid" + window.DOMUIDNext++;
        if (!Array.isArray(values)) {
            values = [values];
        }
        let group = createGroup(row, name, id,hasTooltip,dataToggle,tooltipText);
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
    let card = document.createElement("div");
    card.className = "card";

    let createGroupName = document.createElement("h5");
    createGroupName.className = "mt-2";
    createGroupName.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;"

    createGroupName.textContent = "Create New Sales Group ";

    let cardHeader = document.createElement("div");
    cardHeader.className = "card-header form-group d-flex justify-content-between";
    cardHeader.style = "padding:5px;padding-left: 15px;"
    cardHeader.append(createGroupName);
    card.append(cardHeader)

    let cardBody = document.createElement("div");
    cardBody.className = "card-body";
    card.append(cardBody);

    let form = document.createElement("form");
    cardBody.append(form);

    // Marketing

    let marketingRow = createSection(form, "Marketing");

    let salesGroupName = createText(marketingRow,"Sales Group Nickname",null,true,"salesGroupNickname","This is the name for this sales group");
    let marketingCount = createNumber(marketingRow, "Total Animals", null);
    let marketingZIP = createNumber(marketingRow, "Market ZIP Code", null,true,"marketingZIP","This is the zip code of location where the cattle will be picked up.");
    let marketingDates = createDateRangePicker(marketingRow, "Market Dates", null, null, true, "marketingRange","This is the date range for the sale.");
    let marketingDeliveryLocationType = createSelect({
        row: marketingRow,
        name: "Delivery Location Type",
        options: ["Off Ranch", "Auction"],
        values: "Off Ranch",
        multiple: false,
        tags: false,
        placeholder: "Select Sale Location Type"
    });
    
    let marketingOffRanchLocation = createText(marketingRow,"Delivery Location",null,true,"marketingOffRanchLocation","This is the place where the cattle will be picked up (example “ABC Auction Market” or “Off Ranch”)");
    let marketingAuctionMarketLocation = createSelect({
        row: marketingRow,
        name: "Auction Market",
        options: this.auctionMarketsData,
        values: [],
        multiple: false,
        tags: false,
        placeholder: "Select Auction Market"
    })

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
    marketingDeliveryLocationType.onchange()

    let characteristicsRow = createSection(form, "Characteristics");

    let characteristicBreeds = createSelect({
        row: characteristicsRow,
        name: "Breed",
        options: SalesGroupFields.commonBreedNames,
        values: [],
        multiple: true,
        tags: true,
        placeholder: "Select Applicable Breeds"
    },true,"characteristicBreeds","Please choose all the breeds of cattle in the group.");
    let characteristicsWeight = createNumber(characteristicsRow, "Base Weight", null,true,"characteristicsWeight",
    "Please enter the average weight of the cattle in the group");
    let characteristicsWeightVariance = createText(characteristicsRow, "Weight Variance", null,
    true,"characteristicsWeightVariance","Please enter the variance of the weight average since it is not exact. (example: “20 lbs”)");
    let characteristicsFrame = createSelect({
        row: characteristicsRow,
        name: "Frame",
        options: ["Small", "Medium", "Large"],
        values: "Small",
        multiple: false,
        tags: false,
        placeholder: "Select Frame"
    });
    let characteristicsMuscling = createSelect({
        row: characteristicsRow,
        name: "Muscling",
        options: ["Light", "Heavy"],
        values: "Light",
        multiple: false,
        tags: false,
        placeholder: "Select Muscling"
    });
    let characteristicsHorns = createSelect({
        row: characteristicsRow,
        name: "Horns",
        options: ["Horns", "No Horns"],
        values: "Horns",
        multiple: false,
        tags: false,
        placeholder: "Select Horns"
    });

    // Maintenance

    let maintenanceRow = createSection(form, "Maintenance");

    let maintenancePreconditioningProgram = createSelect({
        row: maintenanceRow,
        name: "Precon Program",
        options: SalesGroupFields.commonPreconditioningProgramNames,
        values: "None",
        multiple: false,
        tags: true,
        placeholder: "Select Precon Program"
    },true,"maintenancePreconditioningProgram","Please enter the pre-conditioning program this group of cattle is on or “not listed”.");
    let maintenanceVaccinations = createSelect({
        row: maintenanceRow,
        name: "Vaccinations",
        options: ["Not Applicable", "Covexin 8", "One Shot BVD", "Infor"],
        values: [],
        multiple: true,
        tags: true,
        placeholder: "Select Vaccinations"
    },true,"maintenanceVaccinations","Please enter vaccinations given to the cattle in this group or “not listed”.");
    let maintenanceFeedingProgram = createSelect({
        row: maintenanceRow,
        name: "Feeding Program",
        options: ["Not Applicable", "Native Range", "Improved Pasture"],
        values: [],
        multiple: true,
        tags: true,
        placeholder: "Select Feeding Program"
    },true,"maintenanceFeedingProgram","Please enter the feeding program this group of cattle is on or “not listed”.");
    let maintenanceImplants = createSelect({
        row: maintenanceRow,
        name: "Implants",
        options: ["Not Applicable", "Raigro"],
        values: [],
        multiple: true,
        tags: true,
        placeholder: "Select Implants"
    },false,"","");
    let maintenanceCastrated = createSelect({
        row: maintenanceRow,
        name: "Castrated",
        options: ["Not Applicable", "Not Castrated", "Banded", "Blade", "Chemicals", "Other"],
        values: "Not Castrated",
        multiple: false,
        tags: false,
        placeholder: "Select Castration Method"
    });
    let maintenanceProcessVerifiedProgram = createSelect({
        row: maintenanceRow,
        name: "PVP Program",
        options: SalesGroupFields.commonPVPProgramNames,
        values: "None",
        multiple: false,
        tags: false,
        placeholder: "Select Process Verified Program"
    },true,"maintenanceProcessVerifiedProgram","Please enter the Processed Verified  program this group of cattle is on or “not listed”.");
    // Media

    let mediaRow = createSection(form, "Image");

    let mediaGroup = document.createElement("div");
    mediaGroup.className = "form-group col-12";
    mediaRow.append(mediaGroup);

    let mediaLabel = document.createElement("label")
    mediaLabel.textContent = "Add images here to make the post look more attractive!";
    mediaGroup.append(mediaLabel);

    let fileEditorFrame = document.createElement("div");
    this.fileEditor = new BasicFileEditor({filetype:["image"]}, fileEditorFrame, [], null);
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
    this.VideoEditor = new VideoSession({}, videoText, [], null);
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
    commentsTA.value = "";
    commentsGroup.append(commentsTA);

    form.append(document.createElement("br"));

    // Publish

    let publishSwitch = new SwitchFormGroup(form, "Publish", false);

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

    // Setup

    this.frame.append(card);

    this.asyncForm = new AsyncForm({
        action: "/widgets/data/create_new_sales_group",
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