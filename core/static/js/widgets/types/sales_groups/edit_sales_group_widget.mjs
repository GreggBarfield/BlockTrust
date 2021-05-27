import { ProgressBar } from '../../../core/progress_bar.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';
import { SwitchFormGroup } from '../../../ui/switch.mjs';
import { FormGroup, DateFormGroup } from '../../../ui/inputs.mjs';
import {VideoSession  } from '../../../files/video_links.mjs';
export class EditSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
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

        let that = this;

        let card = document.createElement("div");
        card.className = "card";

        let cardHeader = document.createElement("h5");
        cardHeader.className = "card-header";
        cardHeader.textContent = "Edit Sales Group " + this.salesGroupID;
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);


        let form = document.createElement("form");
        cardBody.append(form);
        
        // Sections

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

        function createGroup(row, name, htmlFor) {
            let group = document.createElement("div");
            group.className = "form-group col-md-4";
            row.append(group);

            let groupLabel = document.createElement("label");
            groupLabel.className = "form-label";
            groupLabel.textContent = name;
            if (htmlFor !== null) {
                groupLabel.htmlFor = htmlFor;
            }
            group.append(groupLabel);
            return group;
        }

        function createNumber(row, name, value) {
            let id = "domuid" + window.DOMUIDNext++;

            let group = createGroup(row, name, id);
            let input = document.createElement("input");
            input.type = "number";
            input.value = value;
            input.className = "form-control";
            input.id = id;
            group.append(input);
            return input;
        }

        function createText(row, name, value) {
            let id = "domuid" + window.DOMUIDNext++;

            let group = createGroup(row, name, id);
            let input = document.createElement("input");
            input.type = "text";
            input.value = value;
            input.className = "form-control";
            input.id = id;
            group.append(input);
            return input;
        }

        function createDate(row, name, epoch) {
            let dateFormGroup = new DateFormGroup(row, name, epoch);
            dateFormGroup.getFormGroup().classList.add("col-md-4");
            return dateFormGroup;
        }

        function createSelect({row, name, options, values, multiple, tags, placeholder}) {
            let id = "domuid" + window.DOMUIDNext++;

            if (!Array.isArray(values)) {
                values = [values];
            }

            let group = createGroup(row, name, id);
            let select = document.createElement("select");
            select.className = "select2-hidden-accessible";
            select.id = id;
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
                setTimeout(function(){
                    $(select).val([]);
                    $(select).trigger('change');
                }, 1);
            }
            return select;
        }

        // Marketing

        let marketingRow = createSection(form, "Marketing");

        let marketingCount = createNumber(marketingRow, "Total Animals", this.data.reported.count || null);
        let marketingZIP = createNumber(marketingRow, "Market ZIP Code", this.data.zip || null);
        let marketingStart = createDate(marketingRow, "Market Start Date", this.data.start || null);
        let marketingEnd = createDate(marketingRow, "Market End Date", this.data.end || null);
        let marketingLocation = createText(marketingRow,"Delivery Location",this.data.delivery || null);
        let marketingAuctionSale = new SelectAuctionSaleFormGroup(
            marketingRow,
            this.data.auction_sale || null,
            this.data.auction_sale_name || null
        );
        marketingAuctionSale.getFormGroup().classList.add("col-md-4");

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
        });
        let characteristicsWeight = createNumber(characteristicsRow, "Base Weight", this.data.reported.weight || null);
        let characteristicsWeightVariance = createText(characteristicsRow, "Weight Variance", this.data.reported.weight_variance || null);
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
        });
        let maintenanceVaccinations = createSelect({
            row: maintenanceRow,
            name: "Vaccinations",
            options: ["Covexin 8", "One Shot BVD", "Infor"],
            values: this.data.reported.vaccinations || [],
            multiple: true,
            tags: true,
            placeholder: "Select Vaccinations"
        });
        let maintenanceFeedingProgram = createSelect({
            row: maintenanceRow,
            name: "Feeding Program",
            options: ["Native Range", "Improved Pasture"],
            values: this.data.reported.feeding_programs || [],
            multiple: true,
            tags: true,
            placeholder: "Select Feeding Program"
        });
        let maintenanceImplants = createSelect({
            row: maintenanceRow,
            name: "Implants",
            options: ["Raigro"],
            values: this.data.reported.implants || [],
            multiple: true,
            tags: true,
            placeholder: "Select Implants"
        });
        let maintenanceCastrated = createSelect({
            row: maintenanceRow,
            name: "Castrated",
            options: ["Not Castrated", "Banded", "Blade", "Chemicals", "Other"],
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
        });

        // Media

        let mediaRow = createSection(form, "Image");

        let mediaGroup = document.createElement("div");
        mediaGroup.className = "form-group col-12";
        mediaRow.append(mediaGroup);

        let mediaLabel = document.createElement("label")
        mediaLabel.textContent = "Add images here to make the post look more attractive!";
        mediaGroup.append(mediaLabel);

        let fileEditorFrame = document.createElement("div");
        this.fileEditor = new BasicFileEditor({}, fileEditorFrame, this.data.reported.images || [], this.data.file_auths);
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

        let eidsHeader = document.createElement("h6");
        eidsHeader.textContent = "EIDs";
        form.append(eidsHeader);

        let eidsRow = document.createElement("div");
        eidsRow.className = "form-row";
        form.append(eidsRow);
        
        let eidsGroup = document.createElement("div")
        eidsGroup.className = "form-group col";
        eidsRow.append(eidsGroup);

        function parseEIDs(ta) {
            let eidStr = eidsTA.value.replace(/[^0-9,]/g, "");
            let eidStrs = eidStr.split(",");
            let eids= [];
            for (const eidStr of eidStrs) {
                if (!isNaN(parseInt(eidStr))) {
                    eids.push(parseInt(eidStr));
                }
            }
            return eids;
        }
        this.parseEIDs = parseEIDs;
        
        let eidsLabel = document.createElement("label")
        eidsGroup.append(eidsLabel);

        let eidsTA = document.createElement("textarea");
        this.eidsTA = eidsTA;
        eidsTA.maxLength = 10000;
        eidsTA.className = "form-control max-textarea";
        eidsTA.rows = 4;
        eidsTA.placeholder = "Ex. 982000418411463, 982000423277824, 982000423277825"
        eidsTA.value = (this.data.eids || []).join(", ");
        function eidsTALabelChange() {
            eidsLabel.textContent = "Enter your animals' EIDs below.";
            let eids = parseEIDs(eidsTA);
            if (eids.length > 0) {
                eidsLabel.textContent = eids.length + " EIDs entered";
                let v = parseInt(marketingCount.value);
                if (!isNaN(v) && eids.length != v) {
                    eidsLabel.textContent += " (not equal to the total number of animals, which is " + v + ")";
                }
            }
        }
        eidsTA.addEventListener("change", eidsTALabelChange);
        marketingCount.addEventListener("change", eidsTALabelChange);
        eidsGroup.append(eidsTA);
        eidsTALabelChange();

        form.append(document.createElement("br"));

        // Publish

        let publishSwitch = new SwitchFormGroup(form, "Publish", this.data.published);

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
                    eids: parseEIDs(eidsTA),
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
                        videos: that.VideoEditor.getLinks(),
                    },
                    "delivery_location": marketingLocation.value,
                    "zip": parseInt(marketingZIP.value),
                    "start": marketingStart.getTime(),
                    "end": marketingEnd.getTime(),
                    auction_sale: marketingAuctionSale.getID()
                }
            }
        });     
        
        submitButton.addEventListener("click", ()=>{
            this.internalErrorMessage.style.display = "none";
            if (this.allGood()) {
                function progress(perc) {
                    that.progressBar.setProgress(perc);
                }
                that.progressBar.show();
                this.fileEditor.upload(progress)
                .then(()=>{
                    this.asyncForm.submit();
                });
            }
        });
    }

    showError(error) {
        this.internalErrorMessage.style.display = "block";
        this.internalErrorMessage.textContent = error;
    }

    allGood() {
        try {
            let eids = this.parseEIDs();
            for (const eid of eids) {
                let str = eid.toString();
                if (str.length != 15) {
                    throw "The following EID is invalid, please check it: " + eid;
                }
            }

            for (let i = 0; i< eids.length;i++) {
                for (let i2 =i+1;i2<eids.length;i2++) {
                    if (eids[i] == eids[i2]) {
                        throw "The following EIDs are the same: #" + (i + 1) + " and #" + (i2 + 1) + " (" + eids[i] + ")";
                    }
                }
            }
        }
        catch(error) {
            this.showError(error);
            return false;
        }
        return true;
    }
}

/**
 * Presents a selector for auction sale.
 */
class SelectAuctionSaleFormGroup extends FormGroup {

    /**
     * Constructs SelectAuctionSale.
     * 
     * @param {Node} attachTo Where to place DOM elements
     * @param {number|null} auctionSaleID The ID for the auction sale or null
     * @param {string|null} auctionSaleName The auction sale name or null
     */
    constructor(attachTo, auctionSaleID, auctionSaleName) {
        super(attachTo, "Select auction sale (i/a):");

        this._select = document.createElement("select");
        this._select.id = this._input_id;
        this._select.className = "select2-hidden-accessible";
        this._form_group.append(this._select);

        if (auctionSaleID !== null) {
            let option = document.createElement("option");
            option.value = auctionSaleID;
            option.textContent = auctionSaleName;
            this._select.append(option);
        }

        $(this._select).select2({
            ajax: {
                url: "/widgets/data/search_auction_sales",
                data: (params) => {
                    return JSON.stringify({
                        "term": params.term
                    })
                },
                contentType: 'application/json',
                method: "POST",
                delay: 250,
                processResults: function (data) {
                    let results = [];
                    for (const auction_sale of data.auction_sales) {
                        results.push({
                            id: auction_sale.id,
                            text: (
                                auction_sale.name + " (" +
                                auction_sale.account_name + ")"
                            )
                        });
                    }
                    return {results};
                },
            },
            placeholder: 'Type here to search...',
            minimumInputLength: 3,
            allowClear: true
        });
    }
    
    /**
     * Gets the ID of the auction sale selected.
     */
    getID() {
        if (this._select.value === null || this._select.value === "") {
            return null;
        }
        return parseInt(this._select.value);
    }
}
