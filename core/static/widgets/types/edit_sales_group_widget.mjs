import { ProgressBar } from '../../js/core/progress_bar.mjs';
import { BasicFileEditor } from '../../js/files/basic_file_editor.mjs';
import { Widget } from '../widget.mjs';
import { AsyncForm } from '/static/global/async_form.mjs';

// /<\s*[a-zA-Z\s/=\"0-9]*>\s*/g
// ([a-z0-9A-Z])""
// $1",
// \t"
let commonBreedNames = [
    "Amerifax",
	"Angus",
	"Angus Cross",
	"Angus F1",
	"Angus Plus",
	"Aubrac",
	"Balancer",
	"Barzona",
	"Beef Friesian",
	"Beefalo",
	"Beefmaster",
	"Beefmaster Cross",
	"Belgian Blue",
	"Belted Galloway",
	"Black Angus",
	"Black Hereford",
	"Black Simmental",
	"Blonde d' Aquitaine",
	"Braford",
	"Brahman",
	"Brahman Cross",
	"Brahman F1",
	"Brahmousin",
	"Brangus",
	"Brangus Cross",
	"Braunvieh",
	"Braunvieh F1",
	"British White",
	"Charbray",
	"Charloais F1",
	"Charolais",
	"Charolais Cross",
	"Chianina",
	"Corriente",
	"Criollo",
	"Crossbred",
	"Devon",
	"Dexter",
	"Fleckvieh",
	"Galloway",
	"Gelbvieh",
	"Gelbvieh Cross",
	"Gelbvieh F1",
	"Hereford",
	"Hereford Cross",
	"Hereford F1",
	"Holstein",
	"Irish Blacks",
	"Jersey",
	"LimFlex",
	"Limousin",
	"Limousin Cross",
	"Limousin F1",
	"Longhorn",
	"Lowline",
	"Maine-Anjou",
	"Murray Grey",
	"Piedmontese",
	"Pinzgauer",
	"Polled Hereford",
	"Randall",
	"Red Angus",
	"Red Angus Cross",
	"Red Brangus",
	"Red Poll",
	"Romagnola",
	"Salers",
	"Santa Cruz",
	"Santa Gertrudis",
	"Santa Gertrudis Cross",
	"Scottish Highlander",
	"Senepol",
	"Shorthorn",
	"Shorthorn Cross",
	"Shorthorn F1",
	"SimAngus",
	"Simbrah",
	"Simmental",
	"Simmental Cross",
	"Simmental F1",
	"South Devon",
	"South Poll",
	"Star 5",
	"Tarentaise",
	"Texas Cross",
	"Tigerstripe",
	"Wagyu",
	"White Park",
	"Not Reported",
]

let commonPVPProgramNames = [
    "None",
    "American Certified Brands",
    "AzTx Cattle Co.",
    "BeefTraxx",
    "Big Blue Sale Barn Passport Program®",
    "Cal Poly State Univ Animal Science",
    "Frost PLLC dba FACTA",
    "IdentiGEN North America",
    "IMI Global",
    "Legacy Verified",
    "Ranchers Connecting Ranchers",
    "Red Angus Association of America",
    "Samson",
    "TechniTrack",
    "Zoetis Genetics",
    "Other"
];

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
            },
            (data) => {
                this.data = data;
                this.makeForm();
            }
        );


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
            let id = "domuid" + window.DOMUIDNext++;

            let group = createGroup(row, name, id);
            let input = document.createElement("input");
            input.type = "date";
            if (epoch === null) {
                input.value = null;
            }
            else {
                let d = new Date(epoch * 1000);
                function setWidth(val) {
                    if (val < 10)
                        return "0" + val;
                    return val;
                }
                input.value = d.getFullYear() + "-" + setWidth(d.getMonth() + 1) + "-" + setWidth(d.getDate());
            }
            input.className = "form-control";
            input.id = id;
            group.append(input);
            return input;
        }

        function fromDate(node) {
            let values = node.value.split("-");
            let d = new Date(values[0], values[1] - 1, values[2]);
            return Math.floor(d.getTime() / 1000);
        }

        function createSelect(row, name, options, values, multiple, tags, placeholder) {
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

        // Characteristics
        
        let characteristicsRow = createSection(form, "Characteristics");

        let characteristicBreeds = createSelect(
            characteristicsRow,
            "Breed",
            commonBreedNames,
            this.data.reported.breeds || [],
            true,
            true,
            "Select Applicable Breeds"
        );
        let characteristicsWeight = createNumber(characteristicsRow, "Base Weight", this.data.reported.weight || null);
        let characteristicsWeightVariance = createText(characteristicsRow, "Weight Variance", this.data.reported.weight_variance || null);
        let characteristicsFrame = createSelect(
            characteristicsRow,
            "Frame",
            ["Small", "Medium", "Large"],
            this.data.reported.usda_frame_size || "Small",
            false,
            false,
            "Select Frame"
        );
        let characteristicsMuscling = createSelect(
            characteristicsRow,
            "Muscling",
            ["Light", "Heavy"],
            this.data.reported.muscling || "Light",
            false,
            false,
            "Select Muscling"
        );
        let characteristicsHorns = createSelect(
            characteristicsRow,
            "Horns",
            ["Horns", "No Horns"],
            this.data.reported.horns || "Horns",
            false,
            false,
            "Select Horns"
        );

        // Maintenance

        let maintenanceRow = createSection(form, "Maintenance");

        let maintenancePreconditioningProgram = createSelect(
            maintenanceRow,
            "Precon Program",
            ["None", "Health Track", "Value Added Calf-45", "OQBN Vac-45 Program", "JRS Wean-Vac 45"],
            this.data.reported.preconditioning_program || "None",
            false,
            true,
            "Select Precon Program"
        );
        let maintenanceVaccinations = createSelect(
            maintenanceRow,
            "Vaccinations",
            ["Covexin 8", "One Shot BVD", "Infor"],
            this.data.reported.vaccinations || [],
            true,
            true,
            "Select Vaccinations"
        );
        let maintenanceFeedingProgram = createSelect(
            maintenanceRow,
            "Feeding Program",
            ["Native Range", "Improved Pasture"],
            this.data.reported.feeding_programs || [],
            true,
            true,
            "Select Feeding Program"
        );
        let maintenanceImplants = createSelect(
            maintenanceRow,
            "Implants",
            ["Raigro"],
            this.data.reported.implants || [],
            true,
            true,
            "Select Implants"
        );
        let maintenanceCastrated = createSelect(
            maintenanceRow,
            "Castrated",
            ["Not Castrated", "Banded", "Blade", "Chemicals", "Other"],
            this.data.reported.castrated || "Not Castrated",
            false,
            false,
            "Select Castration Method"
        );
        let maintenanceProcessVerifiedProgram = createSelect(
            maintenanceRow,
            "PVP Program",
            commonPVPProgramNames,
            this.data.reported.process_verified_program || "None",
            false,
            false,
            "Select Process Verified Program"
        );

        // Media

        let mediaRow = createSection(form, "Media");

        let mediaGroup = document.createElement("div");
        mediaGroup.className = "form-group col-12";
        mediaRow.append(mediaGroup);

        let mediaLabel = document.createElement("label")
        mediaLabel.textContent = "Add images here to make the post look more attractive!";
        mediaGroup.append(mediaLabel);

        let fileEditorFrame = document.createElement("div");
        this.fileEditor = new BasicFileEditor({}, fileEditorFrame, this.data.reported.images || [], this.data.file_auths);
        mediaGroup.append(fileEditorFrame);

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
        
        let eidsLabel = document.createElement("label")
        eidsGroup.append(eidsLabel);

        let eidsTA = document.createElement("textarea");
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

        let publishFormGroup = document.createElement("div");
        publishFormGroup.className = "form-group";
        form.append(publishFormGroup);

        let publishSwitchRegion = document.createElement("div");
        publishSwitchRegion.className = "switch switch-success d-inline m-r-10";
        publishFormGroup.append(publishSwitchRegion);

        let publishSwitchInput = document.createElement("input");
        publishSwitchInput.className = "";
        publishSwitchInput.type = "checkbox";
        publishSwitchInput.id = "sw" + (window.DOMUIDNext++);
        publishSwitchInput.checked = this.data.published != 0;
        publishSwitchRegion.append(publishSwitchInput);

        let publishSwitchLabel = document.createElement("label");
        publishSwitchLabel.className = "cr";
        publishSwitchLabel.htmlFor = publishSwitchInput.id;
        publishSwitchRegion.append(publishSwitchLabel);

        let publishSwitchLabelLabel = document.createElement("label");
        publishSwitchLabelLabel.htmlFor = publishSwitchInput.id;
        publishSwitchLabelLabel.textContent = "Publish";
        publishFormGroup.append(publishSwitchLabelLabel);

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

        // Setup

        this.frame.append(card);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                function safeInt(v) {
                    return Math.floor(parseFloat(v));
                }

                return {
                    action: "save_sales_group",
                    params: {
                        id: that.salesGroupID,
                        published: publishSwitchInput.checked,
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
                        },
                        "zip": parseInt(marketingZIP.value),
                        "start": fromDate(marketingStart),
                        "end": fromDate(marketingEnd),
                    } 
                }
            }
        });     
        
        submitButton.addEventListener("click", ()=>{
            function progress(perc) {
                that.progressBar.setProgress(perc);
            }
            that.progressBar.show();
            this.fileEditor.upload(progress)
            .then(()=>{
                this.asyncForm.submit();
            });
        });
    }
}