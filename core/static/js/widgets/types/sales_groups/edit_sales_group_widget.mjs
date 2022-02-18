import { ProgressBar } from '../../../core/progress_bar.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';
import { CreatePrintFlyerButton } from '../../../sales_groups/create_sales_group_flyer.mjs';
import { SwitchFormGroup } from '../../../ui/switch.mjs';
import { FormGroup, DateFormGroup } from '../../../ui/inputs.mjs';
import { VideoSession } from '../../../files/video_links.mjs';

export class EditSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.qrSource = this.frame.getAttribute("data-widget-qr-src");
        this.shareableLink = this.frame.getAttribute("data-widget-shareable-link");
        this.formElements = {};
        this.getData(
            "sales_group",
            {
                sales_group: this.salesGroupID
            }
        ).then((data) => {
            this.data = data;
            this.makeForm();
        });
        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });
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

        let cardHeader = document.createElement("h5");
        cardHeader.className = "mt-2";
        cardHeader.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;"

        let saleGroupNickname = "MarketTrust Sale";
        if (this.data.hasOwnProperty('group_name') && this.data.group_name != ""){
            saleGroupNickname = this.data.group_name;
        }
        cardHeader.textContent = "Edit Sales Group " + this.data.id + ": " + saleGroupNickname;

        let editGroupName = document.createElement("div");
        editGroupName.className = "card-header form-group d-flex justify-content-between";
        editGroupName.style = "padding:5px;padding-left: 15px;"
        editGroupName.append(cardHeader);

        let btnQrDiv = document.createElement("div");
        btnQrDiv.className = "d-flex align-items-end flex-row";
        editGroupName.append(btnQrDiv);

        this.printFlyerButton = CreatePrintFlyerButton(this.data);
        btnQrDiv.appendChild(this.printFlyerButton);

        let copyLinkButton = document.createElement("button");
        copyLinkButton.className = "btn btn-outline-primary btn-sm";
        copyLinkButton.innerHTML = "Copy Link";
        copyLinkButton.onclick = function () {
            navigator.clipboard.writeText(that.shareableLink);
        };
        btnQrDiv.append(copyLinkButton);

        let qrImg = document.createElement("img");
        qrImg.src = this.qrSource;
        qrImg.id = "sales_group_qrcode"
        btnQrDiv.append(qrImg);

        card.append(editGroupName);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);

        let form = document.createElement("form");
        cardBody.append(form);

        // Marketing

        let marketingRow = createSection(form, "Marketing");

        let salesGroupName = createText(marketingRow,"Sales Group Nickname",this.data.group_name || null,true,"salesGroupNickname","This is the name for this sales group");
        let marketingCount = createNumber(marketingRow, "Total Animals", this.data.reported.count || null);
        let marketingZIP = createNumber(marketingRow, "Market ZIP Code", this.data.zip || null,true,"marketingZIP","This is the zip code of location where the cattle will be picked up.");
        let marketingStart = createDate(marketingRow, "Market Start Date", this.data.start || null, true, "marketingStart","This is the first date the cattle will be available for sale.");
        let marketingEnd = createDate(marketingRow, "Market End Date", this.data.end || null,true,"marketingEnd","This is the last date the cattle will be for sale. This ad will expire.");
        let marketingLocation = createText(marketingRow,"Delivery Location",this.data.delivery_location || null,true,"marketingLocation","This is the place where the cattle will be picked up (example “ABC Auction Market” or “Off Ranch”)");
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
            values: this.data.reported.breeds || [],
            multiple: true,
            tags: true,
            placeholder: "Select Applicable Breeds"
        },true,"characteristicBreeds","Please choose all the breeds of cattle in the group.");
        let characteristicsWeight = createNumber(characteristicsRow, "Base Weight", this.data.reported.weight || null,true,"characteristicsWeight",
        "Please enter the average weight of the cattle in the group");
        let characteristicsWeightVariance = createText(characteristicsRow, "Weight Variance", this.data.reported.weight_variance || null,
        true,"characteristicsWeightVariance","Please enter the variance of the weight average since it is not exact. (example: “20 lbs”)");
        let characteristicsFrame = createSelect({
            row: characteristicsRow,
            name: "Frame",
            options: ["Small", "Medium", "Large"],
            values: this.data.reported.usda_frame_size || "Small",
            multiple: false,
            tags: false,
            placeholder: "Select Frame"
        });
        let characteristicsMuscling = createSelect({
            row: characteristicsRow,
            name: "Muscling",
            options: ["Light", "Heavy"],
            values: this.data.reported.muscling || "Light",
            multiple: false,
            tags: false,
            placeholder: "Select Muscling"
        });
        let characteristicsHorns = createSelect({
            row: characteristicsRow,
            name: "Horns",
            options: ["Horns", "No Horns"],
            values: this.data.reported.horns || "Horns",
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
            values: this.data.reported.preconditioning_program || "None",
            multiple: false,
            tags: true,
            placeholder: "Select Precon Program"
        },true,"maintenancePreconditioningProgram","Please enter the pre-conditioning program this group of cattle is on or “not listed”.");
        let maintenanceVaccinations = createSelect({
            row: maintenanceRow,
            name: "Vaccinations",
            options: ["Not Applicable", "Covexin 8", "One Shot BVD", "Infor"],
            values: this.data.reported.vaccinations || [],
            multiple: true,
            tags: true,
            placeholder: "Select Vaccinations"
        },true,"maintenanceVaccinations","Please enter vaccinations given to the cattle in this group or “not listed”.");
        let maintenanceFeedingProgram = createSelect({
            row: maintenanceRow,
            name: "Feeding Program",
            options: ["Not Applicable", "Native Range", "Improved Pasture"],
            values: this.data.reported.feeding_programs || [],
            multiple: true,
            tags: true,
            placeholder: "Select Feeding Program"
        },true,"maintenanceFeedingProgram","Please enter the feeding program this group of cattle is on or “not listed”.");
        let maintenanceImplants = createSelect({
            row: maintenanceRow,
            name: "Implants",
            options: ["Not Applicable", "Raigro"],
            values: this.data.reported.implants || [],
            multiple: true,
            tags: true,
            placeholder: "Select Implants"
        },false,"","");
        let maintenanceCastrated = createSelect({
            row: maintenanceRow,
            name: "Castrated",
            options: ["Not Applicable", "Not Castrated", "Banded", "Blade", "Chemicals", "Other"],
            values: this.data.reported.castrated || "Not Castrated",
            multiple: false,
            tags: false,
            placeholder: "Select Castration Method"
        });
        let maintenanceProcessVerifiedProgram = createSelect({
            row: maintenanceRow,
            name: "PVP Program",
            options: SalesGroupFields.commonPVPProgramNames,
            values: this.data.reported.process_verified_program || "None",
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
        this.fileEditor = new BasicFileEditor({filetype:["image"]}, fileEditorFrame, this.data.reported.images || [], this.data.file_auths);
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
        this.VideoEditor = new VideoSession({}, videoText, this.data.reported.videos || [], this.data.file_auths);
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
        commentsTA.value = this.data.reported.comments || "";
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

        let publishSwitch = new SwitchFormGroup(form, "Publish", this.data.published);

        let archiveSwitch = new SwitchFormGroup(form, "Archive", this.data.is_archived);
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
            action: "/widgets/data/save_sales_group",
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
                    "delivery_location": marketingLocation.value,
                    "zip": parseInt(marketingZIP.value),
                    "start": marketingStart.getTime(),
                    "end": marketingEnd.getTime(),
                    "group_name": salesGroupName.value,
                    "is_archived": archiveSwitch.isChecked(),
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

    showError(error) {
        this.internalErrorMessage.style.display = "block";
        this.internalErrorMessage.textContent = error;
    }
}

/**
 * TODO: Below code used to add auction sale dropdown which is retained in case needed in future.
 * Presents a selector for auction sale.
 */


// class SelectAuctionSaleFormGroup extends FormGroup {

//     /**
//      * Constructs SelectAuctionSale.
//      * 
//      * @param {Node} attachTo Where to place DOM elements
//      * @param {number|null} auctionSaleID The ID for the auction sale or null
//      * @param {string|null} auctionSaleName The auction sale name or null
//      */
//     constructor(attachTo, auctionSaleID, auctionSaleName) {
//         super(attachTo, "Select auction sale (i/a):");
        
//         this._select = document.createElement("select");
//         this._select.id = this._input_id;
//         this._select.className = "select2-hidden-accessible";
//         this._form_group.append(this._select);

//         if (auctionSaleID !== null) {
//             let option = document.createElement("option");
//             option.value = auctionSaleID;
//             option.textContent = auctionSaleName;
//             this._select.append(option);
//         }

//         $(this._select).select2({
//             ajax: {
//                 url: "/widgets/data/search_auction_sales",
//                 data: (params) => {
//                     return JSON.stringify({
//                         "term": params.term
//                     })
//                 },
//                 contentType: 'application/json',
//                 method: "POST",
//                 delay: 250,
//                 processResults: function (data) {
//                     let results = [];
//                     for (const auction_sale of data.auction_sales) {
//                         results.push({
//                             id: auction_sale.id,
//                             text: (
//                                 auction_sale.name + " (" +
//                                 auction_sale.account_name + ")"
//                             )
//                         });
//                     }
//                     return { results };
//                 },
//             },
//             placeholder: 'Type here to search...',
//             minimumInputLength: 3,
//             allowClear: true
//         });
//     }

//     /**
//      * Gets the ID of the auction sale selected.
//      */
//     getID() {
//         if (this._select.value === null || this._select.value === "") {
//             return null;
//         }
//         return parseInt(this._select.value);
//     }
// }
