import { ProgressBar } from '../../../core/progress_bar.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { SwitchFormGroup } from '../../../ui/switch.mjs';
import { DateFormGroup, DateRangeFormGroup} from '../../../ui/inputs.mjs';
import { VideoSession } from '../../../files/video_links.mjs';
import { CreateAuctionMarketWidget } from './create_auction_market_widget.mjs';
import { CreateVaccinationWidget } from './create_vaccination_widget.mjs';
import { salesGroupFormInputIds } from '../../utilities/sales_group_constants.mjs';
import { InfoModal } from "../../../core/info_modal.mjs";
import { spinner } from '../../../ui/spinner.mjs';
import { UploadEIDsForSalesGroupWidget } from './upload_eids_for_sales_group_widget.mjs';

export class SalesGroupsCommonForm{
    constructor(data, auctionMarketsData, postRoute, salesGroupFieldsValues, preSelectAuctionMarket="false", preSelectedAuctionMarketId=null, carcassDataAvailable=false, viewSalesGroupURL=null, paymentURL=null) {
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
            this.marketingExpectedShipDateValue = this.data.reported.expected_ship_date;
            this.markertingCommentsValue = this.data.reported.marketing_comments;
            this.characteristicsCategoryValue = this.data.category;
            this.characteristicBreedsValue = this.data.reported.breeds;
            this.characteristicsBreedCommentsValue = this.data.breed_comments;
            this.characteristicsWeightValue = this.data.reported.weight;
            this.characteristicsWeightVarianceValue = this.data.reported.weight_variance;
            this.characteristicsWeighingConditionsValue = this.data.weighing_conditions;
            this.characteristicsFrameValue = this.data.reported.usda_frame_size;
            this.characteristicsMusclingValue = this.data.reported.muscling;
            this.characteristicsHornsValue = this.data.reported.horns;
            this.characteristicsPregnancyStatusValue = this.data.reported.pregnancy_status;
            this.characteristicsFirstBirthDateValue = this.data.reported.first_birth_date;
            this.characteristicsCommentsValue = this.data.reported.characteristics_comments;
            this.geneticsGenomicTestingValue = this.data.reported.genomic_testing;
            this.geneticsEPDValue = this.data.reported.epd;
            this.geneticsCommentsValue = this.data.reported.genetics_comments;
            this.geneticsVerificationValue = this.data.reported.verification;
            this.maintenanceVaccinationsValue = this.data.reported.vaccinations;
            this.characteristicsImplantsValue = this.data.reported.implants;
            this.maintenanceCastratedValue = this.data.reported.castrated;
            this.maintenanceProgramValue = this.data.reported.program;
            this.maintenanceComingledStatusValue = this.data.reported.comingled_status;
            this.maintenanceCreepFeedValue = this.data.reported.creep_feed;
            this.maintenanceWeanedValue = this.data.reported.weaned;
            this.maintenanceWeanedDateValue = this.data.reported.weaned_date;
            this.maintenanceCommentsValue = this.data.reported.maintenance_comments;
            this.valueAddProgramsProgramValue = this.data.reported.program;
            this.valueAddProgramsPreconditioningProgramsValue = this.data.reported.preconditioning_program;
            this.valueAddedProgramsFeedingProgramsValue = this.data.reported.feeding_programs;
            this.valueAddProgramsBreedProgramCertificationCoValue = this.data.reported.breed_program_certification_co;
            this.valueAddProgramsCertifiedThroughValue = this.data.reported.certified_through;
            this.valueAddedProgramsCommentsValue = this.data.reported.program_comments;
            this.reportedImages = this.data.reported.images;
            this.reportedVideos = this.data.reported.videos;
            this.fileAuths = this.data.file_auths
            this.comments = this.data.reported.comments;
            this.published = this.data.published;
            this.showAccountCarcassData = this.data.show_account_carcass_data;
            this.isPaid = this.data.is_paid;
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
            this.marketingExpectedShipDateValue = null;
            this.markertingCommentsValue = "";
            this.characteristicsCategoryValue = [];
            this.characteristicBreedsValue = [];
            this.characteristicsBreedCommentsValue = null;
            this.characteristicsWeightValue = null;
            this.characteristicsWeightVarianceValue = null;
            this.characteristicsWeighingConditionsValue = null;
            this.characteristicsFrameValue = [];
            this.characteristicsMusclingValue = [];
            this.characteristicsHornsValue = [];
            this.characteristicsPregnancyStatusValue = [];
            this.characteristicsFirstBirthDateValue = null;
            this.characteristicsCommentsValue = "";
            this.geneticsGenomicTestingValue = [];
            this.geneticsEPDValue = [];
            this.geneticsCommentsValue = "";
            this.geneticsVerificationValue = [];
            this.maintenancePreconditioningProgramValue = [];
            this.maintenanceVaccinationsValue = [];
            this.maintenanceFeedingProgramValue = [];
            this.characteristicsImplantsValue = [];
            this.maintenanceCastratedValue = [];
            this.maintenanceProgramValue = [];
            this.maintenanceComingledStatusValue = [];
            this.maintenanceCreepFeedValue = [];
            this.maintenanceWeanedValue = [];
            this.maintenanceCommentsValue = "";
            this.maintenanceWeanedDateValue = null;
            this.valueAddProgramsProgramValue = [];
            this.valueAddProgramsPreconditioningProgramsValue = [];
            this.valueAddedProgramsFeedingProgramsValue = [];
            this.valueAddProgramsBreedProgramCertificationCoValue = [];
            this.valueAddProgramsCertifiedThroughValue = [];
            this.valueAddedProgramsCommentsValue = "";
            this.reportedImages = [];
            this.reportedVideos = [];
            this.fileAuths = null;
            this.comments = "";
            this.published = true;
            this.isPaid = false;
            this.showAccountCarcassData = true;
        }
        this.auctionMarketsData = auctionMarketsData;
        this.postRoute = postRoute;
        this.salesGroupFieldsValues = salesGroupFieldsValues;
        this.preSelectAuctionMarket = preSelectAuctionMarket;
        this.preSelectedAuctionMarketId = preSelectedAuctionMarketId;
        this.carcassDataAvailable = carcassDataAvailable;
        this.viewSalesGroupURL = viewSalesGroupURL;
        this.paymentURL = paymentURL;
        console.log("this.paymentURL", this.paymentURL, typeof this.paymentURL);
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

        function createGroup(row, name, htmlFor, hasTooltip, dataToggle, tooltipText, groupColumnSize=4, attachWidget=false, attachedWidget=null, widgetLinkText="") {
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
            if(attachWidget){
                let newLink = document.createElement("a");
                newLink.className = "form-label text-primary";
                newLink.textContent = widgetLinkText;
                newLink.onclick = () => {
                    let widget = new attachedWidget();
                    widget.init();
                }
                groupLabel.append(newLink);
            }
            group.append(groupLabel);
            return group;
        }

        function createEmptyRowElement(row, groupColumnSize=4){
            let group = document.createElement("div");
            group.className = `col-md-${groupColumnSize} d-flex justify-content-center align-items-center`;
            row.append(group);
            return group;
        }

        function createNumber(row, name, id, value, hasTooltip=false, dataToggle="", tooltipText="", groupColumnSize=4, isDecimal=false) {
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

        function createText(row, name, id, value, hasTooltip=false, dataToggle="", tooltipText="", groupColumnSize=4, maxLength=null) {
            let group = createGroup(row, name, id, hasTooltip, dataToggle, tooltipText, groupColumnSize);
            let input = document.createElement("input");
            input.type = "text";
            input.value = value;
            input.className = "form-control";
            input.id = id;
            input.required = true
            if (maxLength!==null){
                input.maxLength = maxLength;
            }
            group.append(input);
            return input;
        }

        function createDate(row, name, id, epoch, hasTooltip=false, dataToggle="", tooltipText="") {
            let dateFormGroup = new DateFormGroup(row, name, id, epoch);
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

        function createSelect({row, name, id, options, values, multiple, tags, placeholder}, hasTooltip=false, dataToggle="", tooltipText="", groupColumnSize=4, attachWidget=false, optionsObject=null, attachedWidget=null, widgetLinkText="") {
            if (!Array.isArray(values)) {
                values = [values];
            }
            let group = createGroup(row, name, id, hasTooltip, dataToggle, tooltipText, groupColumnSize, attachWidget, attachedWidget, widgetLinkText);
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

        function safeInt(v) {
            if (v === "") {
                return null;
            }
            return Math.floor(parseFloat(v));
        }

        let form = document.createElement("form");
        this.box.append(form);

        // Marketing

        let marketingRow = createSection(form, "Marketing");

        let salesGroupName = createText(marketingRow,"Visible Name of Group", salesGroupFormInputIds.marketingGroupName, this.salesGroupNameValue,true,"salesGroupNickname","This is the name for this sales group", 4);
        let marketingZIP = createNumber(marketingRow, "Market ZIP Code", salesGroupFormInputIds.marketingZIP, this.marketingZIPValue,true,"marketingZIP","This is the zip code of location where the cattle will be picked up.", 4);
        //let marketingPrice = createNumber(marketingRow, "Sales Group Price", this.marketingPriceValue || null,true,"marketingPrice", "Please enter the approximate price for the Sales Group", 4, true);
        let marketingDate = createDate(marketingRow, "Market Date", salesGroupFormInputIds.marketingDate, this.marketingSaleDateValue, true, "marketingDate","This is the date for the sale.");
        
        let marketingDeliveryLocationType = createSelect({
            row: marketingRow,
            name: "Market Type",
            id: salesGroupFormInputIds.marketingDeliveryLocationType,
            options: this.salesGroupFieldsValues.delivery_location_type,
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
            id: salesGroupFormInputIds.marketingAuctionMarketLocation,
            values: auctionMarket || "None",
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4, true, this.auctionMarketsData, CreateAuctionMarketWidget, "Not Listed?");


        let marketingOffRanchLocation = createText(marketingRow,"Delivery Location", salesGroupFormInputIds.marketingOffRanchLocation, deliveryLocation || null,true,"marketingOffRanchLocation","This is the place where the cattle will be picked up (example “ABC Auction Market” or “Direct/Off Ranch”)", 4);
        let marketingSlide = createText(marketingRow, "Slide", salesGroupFormInputIds.marketingSlide, this.marketingSlideValue || "",true,"marketingSlide","", 4);
        let marketingWeighingConditions = createText(marketingRow,"Weighing Conditions", salesGroupFormInputIds.marketingWeighingConditions, this.marketingWeighingConditionsValue || "",true,"marketingWeighingConditions","", 4);
        let marketingRepresentedBy = createText(marketingRow,"Represented By", salesGroupFormInputIds.marketingRepresentedBy, this.marketingRepresentedByValue || "",true,"marketingRepresentedBy","", 4);  
        let marketingExpectedShipDate = createDate(marketingRow, "Expected Ship Date", salesGroupFormInputIds.marketingExpectedShipDate, this.marketingExpectedShipDateValue, false, "marketingExpectedShipDate","");
        
        let uploadEIDsWidget = new UploadEIDsForSalesGroupWidget();
        let widgetContainer = createEmptyRowElement(marketingRow, 4);
        widgetContainer.append(uploadEIDsWidget.createModalLink());

        let marketingComments = createText(marketingRow,"Marketing Comments", salesGroupFormInputIds.marketingComments, this.markertingCommentsValue || "",true,"marketingComments","", 12, 150);

        marketingDeliveryLocationType.onchange = () => {
            marketingSlide.disabled = true;
            marketingWeighingConditions.disabled = true;
            marketingAuctionMarketLocation.disabled=true;
            marketingOffRanchLocation.disabled=true;
            marketingExpectedShipDate.setInputDisabledStatus(true);

            marketingSlide.value = "";
            marketingWeighingConditions.value = "";
            marketingOffRanchLocation.value= "";
            marketingAuctionMarketLocation.value="None";

            if(marketingDeliveryLocationType.value === "Direct/Off Ranch"){
                marketingOffRanchLocation.disabled=false;
                marketingOffRanchLocation.value = deliveryLocation;
                marketingExpectedShipDate.setInputDisabledStatus(false);
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
        
        let characteristicsCount = createNumber(characteristicsRow, "Total Head Count", salesGroupFormInputIds.characteristicsCount, this.marketingCountValue, false, "", "", 4);
        let characteristicBreeds = createSelect({
            row: characteristicsRow,
            name: "Breed",
            id: salesGroupFormInputIds.characteristicBreeds,
            options: this.salesGroupFieldsValues.breed,
            values: this.characteristicBreedsValue,
            multiple: true,
            tags: true,
            placeholder: "Please Select"
        },true,"characteristicBreeds","Please choose all the breeds of cattle in the group.", 4);
        let characteristicsCategory = createSelect({
            row: characteristicsRow,
            name: "Category/Sex",
            id: salesGroupFormInputIds.characteristicsCategory,
            options: this.salesGroupFieldsValues.category,
            values: this.characteristicsCategoryValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        },false,"","", 4);
        let characteristicsWeight = createNumber(characteristicsRow,"Base Weight", salesGroupFormInputIds.characteristicsWeight,this.characteristicsWeightValue,true,"characteristicsWeight",
        "Please enter the average weight of the cattle in the group", 4);
        let characteristicsWeightVariance = createText(characteristicsRow, "Weight Variance", salesGroupFormInputIds.characteristicsWeightVariance, this.characteristicsWeightVarianceValue,
        true,"characteristicsWeightVariance","Please enter the variance of the weight average since it is not exact. (example: “20 lbs”)", 4);
        let characteristicsFrame = createSelect({
            row: characteristicsRow,
            name: "Frame",
            id: salesGroupFormInputIds.characteristicsFrame,
            options: this.salesGroupFieldsValues.frame,
            values: this.characteristicsFrameValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let characteristicsHorns = createSelect({
            row: characteristicsRow,
            name: "Horns",
            id: salesGroupFormInputIds.characteristicsHorns,
            options: this.salesGroupFieldsValues.horn,
            values: this.characteristicsHornsValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let characteristicsMuscling = createSelect({
            row: characteristicsRow,
            name: "Muscling",
            id: salesGroupFormInputIds.characteristicsMuscling,
            options: this.salesGroupFieldsValues.muscling,
            values: this.characteristicsMusclingValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let characteristicsPregnancyStatus = createSelect({
            row: characteristicsRow,
            name: "Pregnancy Status (Heifers)",
            id: salesGroupFormInputIds.characteristicsPregnancyStatus,
            options: this.salesGroupFieldsValues.pregnancy_status,
            values: this.characteristicsPregnancyStatusValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let characteristicsImplants = createSelect({
            row: characteristicsRow,
            name: "Implants",
            id: salesGroupFormInputIds.characteristicsImplants,
            options: this.salesGroupFieldsValues.implant,
            values: this.characteristicsImplantsValue,
            multiple: true,
            tags: true,
            placeholder: "Please Select"
        }, false, "" , "", 4);
        let characteristicFirstBirthDate = createDate(characteristicsRow, "1st Birth Date", salesGroupFormInputIds.characteristicsFirstBirthDate, this.characteristicsFirstBirthDateValue, true, "characteristicFirstBirthDate","");
        let characteristicsComments = createText(characteristicsRow,"Characteristics Comments",salesGroupFormInputIds.characteristicsComments, this.characteristicsCommentsValue || "",true,"characteristicsComments","", 12, 150);

        // Maintenance

        let maintenanceRow = createSection(form, "Management");

        let maintenanceVaccinations = createSelect({
            row: maintenanceRow,
            name: "Vaccinations",
            id: salesGroupFormInputIds.maintenanceVaccinations,
            options: this.salesGroupFieldsValues.vaccination,
            values: this.maintenanceVaccinationsValue,
            multiple: true,
            tags: true,
            placeholder: "Please Select"
        }, true, "maintenanceVaccinations", "Please enter vaccinations given to the cattle in this group or “not listed”.", 4, true, null, CreateVaccinationWidget, "Add New");
        let maintenanceComingledStatus = createSelect({
            row: maintenanceRow,
            name: "Comingled Status",
            id: salesGroupFormInputIds.maintenanceComingledStatus,
            options: this.salesGroupFieldsValues.comingled_status,
            values: this.maintenanceComingledStatusValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let maintenanceCreepFeed = createSelect({
            row: maintenanceRow,
            name: "Creep Feed",
            id: salesGroupFormInputIds.maintenanceCreepFeed,
            options: this.salesGroupFieldsValues.creep_feed,
            values: this.maintenanceCreepFeedValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let maintenanceCastrated = createSelect({
            row: maintenanceRow,
            name: "Castrated",
            id: salesGroupFormInputIds.maintenanceCastrated,
            options: this.salesGroupFieldsValues.castrated,
            values: this.maintenanceCastratedValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let maintenanceWeaned = createSelect({
            row: maintenanceRow,
            name: "Weaned",
            id: salesGroupFormInputIds.maintenanceWeaned,
            options: this.salesGroupFieldsValues.weaned,
            values: this.maintenanceWeanedValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let mantainanceWeanedDate = createDate(maintenanceRow, "Weaned Date", salesGroupFormInputIds.maintenanceWeanedDate, this.mantainanceWeanedDateValue, true, "mantainanceWeanedDate","");
        let maintenanceComments = createText(maintenanceRow,"Maintenance Comments", salesGroupFormInputIds.maintenanceComments,this.maintenanceCommentsValue || "",false,"maintenanceComments","", 12, 150);

        // Genetics

        let geneticsRow = createSection(form, "Genetics");

        let geneticsGenomicTesting = createSelect({
            row: geneticsRow,
            name: "Do you do genetic or genomic testing?",
            id: salesGroupFormInputIds.geneticsGenomicTesting,
            options: ["Yes", "No"],
            values: this.geneticsGenomicTestingValue || "",
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let geneticsEPD = createSelect({
            row: geneticsRow,
            name: "Do you have the EPD's on the sires of the cattle you're planning to sell?",
            id: salesGroupFormInputIds.geneticsEPD,
            options: ["Yes", "No"],
            values: this.geneticsEPDValue || "",
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let geneticsVerification = createSelect({
            row: geneticsRow,
            name: "Genetics Merit Verification Co.",
            id: salesGroupFormInputIds.geneticsVerification,
            options: this.salesGroupFieldsValues.genetics_verification,
            values: this.geneticsVerificationValue || [],
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let geneticsComments = createText(geneticsRow,"Enter any comment related to genetics.", salesGroupFormInputIds.geneticsComments,this.geneticsCommentsValue || "",false,"geneticsComments","", 12, 150);

        // Value-Add Programs

        let valueAddProgramsRow = createSection(form, "Value-Add Programs");
        let valueAddProgramsProgram = createSelect({
            row: valueAddProgramsRow,
            name: "Program",
            id: salesGroupFormInputIds.valueAddProgramProgramType,
            options: this.salesGroupFieldsValues.pvp_program,
            values: this.valueAddProgramsProgramValue,
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, true, "maintenanceProgram", "Please enter the Processed Verified  program this group of cattle is on or “not listed”.", 4);
        let valueAddProgramsPreconditioningProgram = createSelect({
            row: valueAddProgramsRow,
            name: "Preconditioning Program",
            id: salesGroupFormInputIds.valueAddProgramPreconditioningProgram,
            options: this.salesGroupFieldsValues.preconditioning_program,
            values: this.valueAddProgramsPreconditioningProgramsValue,
            multiple: false,
            tags: true,
            placeholder: "Please Select"
        }, true, "maintenancePreconditioningProgram", "Please enter the pre-conditioning program this group of cattle is on or “not listed”.", 4);
        let valueAddProgramsFeedingProgram = createSelect({
            row: valueAddProgramsRow,
            name: "Feeding Program",
            id: salesGroupFormInputIds.valueAddProgramFeedingProgram,
            options: this.salesGroupFieldsValues.feeding_program,
            values: this.valueAddedProgramsFeedingProgramsValue,
            multiple: true,
            tags: true,
            placeholder: "Please Select"
        }, true, "maintenanceFeedingProgram", "Please enter the feeding program this group of cattle is on or “not listed”.", 4);
        let valueAddProgramsBreedProgramCertificationCo = createSelect({
            row: valueAddProgramsRow,
            name: "Breed Program Certification Co.",
            id: salesGroupFormInputIds.valueAddProgramBreedProgramCertificationCo,
            options: this.salesGroupFieldsValues.breed_program_certification_co,
            values: this.valueAddProgramsBreedProgramCertificationCoValue || [],
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let valueAddProgramsCertifiedThrough = createSelect({
            row: valueAddProgramsRow,
            name: "Certified Through",
            id: salesGroupFormInputIds.valueAddProgramCertifiedThrough,
            options: this.salesGroupFieldsValues.certified_through,
            values: this.valueAddProgramsCertifiedThroughValue || [],
            multiple: false,
            tags: false,
            placeholder: "Please Select"
        }, false, "", "", 4);
        let valueAddProgramsComments = createText(valueAddProgramsRow,"Program Comments", salesGroupFormInputIds.valueAddProgramProgramComments,this.valueAddedProgramsCommentsValue || "",false,"geneticsComments","", 12, 150);

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
        commentsTA.maxLength = 150;
        commentsTA.className = "form-control max-textarea";
        commentsTA.rows = 4;
        commentsTA.value = this.comments;
        commentsGroup.append(commentsTA);

        form.append(document.createElement("br"));

        // Publish

        let publishSwitch = new SwitchFormGroup(form, "Publish", this.published);


        let showAccountCarcassDataSwitch = new SwitchFormGroup(form, "Show Carcass History", this.showAccountCarcassData);
        if(!this.carcassDataAvailable){
            showAccountCarcassDataSwitch.hideSwitch();
        }
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
                return {
                    id: this.salesGroupID,
                    published: publishSwitch.isChecked(),
                    show_account_carcass_data: showAccountCarcassDataSwitch.isChecked(),
                    eids: [],
                    reported: {
                        comments: commentsTA.value,
                        count: safeInt(characteristicsCount.value),
                        weight: safeInt(characteristicsWeight.value),
                        weight_variance: characteristicsWeightVariance.value,
                        breeds: $(characteristicBreeds).val(),
                        horns: characteristicsHorns.value,
                        muscling: characteristicsMuscling.value,
                        usda_frame_size: characteristicsFrame.value,
                        preconditioning_program: valueAddProgramsPreconditioningProgram.value,
                        vaccinations: $(maintenanceVaccinations).val(),
                        feeding_programs: $(valueAddProgramsFeedingProgram).val(),
                        implants: $(characteristicsImplants).val(),
                        castrated: maintenanceCastrated.value,
                        program: valueAddProgramsProgram.value,
                        images: fileEditor.getFileIDs(),
                        videos: videoEditor.getVideoLinks(),
                        marketing_slide: marketingSlide.value,
                        marketing_weighing_conditions: marketingWeighingConditions.value,
                        marketing_represented_by: marketingRepresentedBy.value,
                        genomic_testing: geneticsGenomicTesting.value,
                        epd: geneticsEPD.value,
                        marketing_comments: marketingComments.value,
                        genetics_comments: geneticsComments.value,
                        pregnancy_status: characteristicsPregnancyStatus.value,
                        characteristics_comments: characteristicsComments.value,
                        comingled_status: maintenanceComingledStatus.value,
                        creep_feed: maintenanceCreepFeed.value,
                        verification: geneticsVerification.value,
                        program_comments: valueAddProgramsComments.value,
                        weaned: maintenanceWeaned.value,
                        maintenance_comments: maintenanceComments.value,
                        breed_program_certification_co: valueAddProgramsBreedProgramCertificationCo.value,
                        certified_through: valueAddProgramsCertifiedThrough.value,
                        expected_ship_date: marketingExpectedShipDate.getTime(),
                        first_birth_date: characteristicFirstBirthDate.getTime(),
                        weaned_date: maintenanceWeanedDate.getTime()
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
                    "breed_comments": characteristicsComments.value,
                    "weighing_conditions": marketingWeighingConditions.value,
                    "is_paid": this.isPaid,
                    "uploaded_eids": uploadEIDsWidget.getUploadedEids()
                }
            },
            onFinished: (data, status) => {
                if (200 <= status && status < 300) {
                    if (!this.salesGroupID) {
                        this.salesGroupID = data.id;
                    }
                    if (this.paymentURL) {
                        if (publishSwitch.isChecked() && !this.isPaid) {
                            let infoModal = new InfoModal(`Since you are publishing this sales group, you will be charged <span class="text-danger">$${safeInt(characteristicsCount.value).toFixed(2)}</span> on your saved card. 
                                                           If no card has been added to your account or if payment on your saved card fails, you will be redirected to enter new payment details. Click <span class="text-danger">OK</span> to proceed.
                                                           <br/><br/>In case, you are not ready to pay, click <span class="text-danger">Cancel</span>. In this case, the sales group will be saved and not published.`,
                                null, false, "d-none", () => window.location.href = this.viewSalesGroupURL + this.salesGroupID);
                            infoModal.getHeader().classList.add("text-center", "p-4");
                            let proceedButton = document.createElement("button");
                            proceedButton.textContent = "OK";
                            proceedButton.className = "btn btn-primary";
                            let processPayment = (id) => {
                                infoModal.getHeader().innerHTML = spinner;
                                infoModal.getHeader().classList.add("justify-content-center");
                                infoModal.getFooter().className = "d-none";
                                fetch(this.paymentURL, {
                                    method: "POST",
                                    body: JSON.stringify({ id: id })
                                }).then(response => {
                                    if (response.redirected) {
                                        window.location.href = response.url;
                                    }
                                    else {
                                        new InfoModal("An error occured. Please try again later.", null, false, "d-none", () => window.location.reload(), "OK");
                                    }
                                })
                            }
                            proceedButton.onclick = () => processPayment(this.salesGroupID);
                            infoModal.getActionButtonDiv().append(proceedButton);
                        }
                        else {
                            window.location.href = this.viewSalesGroupURL + this.salesGroupID;
                        }
                    }
                    else {
                        window.location.href = this.viewSalesGroupURL + this.salesGroupID;
                    }
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