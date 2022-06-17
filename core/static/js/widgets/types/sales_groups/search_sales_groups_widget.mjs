import { Widget } from '../../widget.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';

export class SearchSalesGroupsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";

        this.inputs = {};
        this.generate();

    }

    generate() {
        this.form = document.createElement("form");
        this.form.addEventListener("submit", (e)=>{
            e.preventDefault();
            this.search();
        });

        let locationHeader = document.createElement("h6");
        locationHeader.textContent = "Location";
        this.form.append(locationHeader);

        let firstFormRow = document.createElement("div");
        firstFormRow.className = "form-row";
        this.form.append(firstFormRow);

        let milesFormGroup = document.createElement("div");
        milesFormGroup.className = "form-group col-md-6";
        firstFormRow.append(milesFormGroup);

        let milesLabel = document.createElement("label");
        milesLabel.textContent = "Search Radius";
        milesFormGroup.append(milesLabel);

        this.inputs.milesSelect = document.createElement("select");
        this.inputs.milesSelect.className = "form-control";
        milesFormGroup.append(this.inputs.milesSelect);

        for (const miles of SalesGroupFields.commonMiles) {
            let milesOption = document.createElement("option");
            milesOption.value = miles;
            milesOption.textContent = miles + " Miles";
            this.inputs.milesSelect.append(milesOption);
        }

        this.inputs.milesSelect.children[0].setAttribute("selected", true);

        let zipCodeFormGroup = document.createElement("div");
        zipCodeFormGroup.className = "form-group col-md-6";
        firstFormRow.append(zipCodeFormGroup);

        let zipCodeLabel = document.createElement("label");
        zipCodeLabel.textContent = "Center Zip Code";
        zipCodeFormGroup.append(zipCodeLabel);

        this.inputs.zipCode = document.createElement("input");
        this.inputs.zipCode.className = "form-control";
        this.inputs.zipCode.type = "number";
        this.inputs.zipCode.placeholder = "12345"
        zipCodeFormGroup.append(this.inputs.zipCode);

        {
            let expandControlFormGroup = document.createElement("div");
            expandControlFormGroup.className = "form-group";
            let expandControl = document.createElement("a");
            expandControl.textContent = "More Search Options";
            expandControl.href = "#";
            expandControlFormGroup.append(expandControl);
            this.form.append(expandControlFormGroup);

            let expandContainer = document.createElement("div");
            expandContainer.style.display = "none";
            this.form.append(expandContainer);

            expandControl.addEventListener("click", (e)=>{
                e.preventDefault();
                if (expandContainer.style.display == "none") {
                    expandContainer.style.display = "block";
                }
                else {
                    expandContainer.style.display = "none";
                }
            });

            let additionalRow = document.createElement("div");
            additionalRow.className = "form-row";
            expandContainer.append(additionalRow);

            function createSearchControl(name, on) {
                let formGroup = document.createElement("div");
                formGroup.className = "form-group col-md-3";
                additionalRow.append(formGroup);

                let label = document.createElement("label");
                label.textContent = name;
                formGroup.append(label);

                let select = document.createElement("select");
                select.className = "form-control";
                formGroup.append(select);

                function addOption(text, value=null, selected=false) {
                    let option = document.createElement("option");
                    select.append(option);

                    option.textContent = text;

                    if (value == null) {
                        option.value = text;
                    }
                    else {
                        option.value = value;
                    }

                    if (selected) {
                        option.selected = true;
                    }
                }
                addOption("", "", true);

                for (const value of on) {
                    addOption(value, value);
                }

                return select;
            }

            this.inputs.category = createSearchControl("Category", SalesGroupFields.commonCategoryNames);
            this.inputs.breed = createSearchControl("Breed", SalesGroupFields.commonBreedNames);
            this.inputs.minimumWeight = createSearchControl("Minimum Weight", SalesGroupFields.commonWeights);
            this.inputs.preconditioningProgram = createSearchControl("Precon Program", SalesGroupFields.commonPreconditioningProgramNames);
            this.inputs.processVerifiedProgram = createSearchControl("PVP Program", SalesGroupFields.commonPVPProgramNames);
        }
        
        {
            let submitFormGroup = document.createElement("div");
            submitFormGroup.className = "form-group";
            this.form.append(submitFormGroup);

            let submitButton = document.createElement("input");
            submitButton.className = "btn btn-primary";
            submitButton.type = "submit";
            submitButton.value = "Search";
            submitFormGroup.append(submitButton);
        }

        this.searchErrorAlert = document.createElement("div");
        this.searchErrorAlert.className = "alert alert-danger";
        this.searchErrorAlert.style.display = "none";
        this.form.append(this.searchErrorAlert);

        this.frame.append(this.form);

        this.resultsHr = document.createElement("hr");
        this.resultsHr.style.display = "none";
        this.resultsHr.style.marginLeft = "-25px";
        this.resultsHr.style.marginRight = "-25px";
        this.frame.append(this.resultsHr);

        this.results = document.createElement("div");
        this.results.style.display = "none";
        this.frame.append(this.results);
    }

    showError(error) {
        this.searchErrorAlert.style.display = "block";
        this.searchErrorAlert.textContent = error;
    }

    search() {
        this.searchErrorAlert.style.display = "none";

        if (this.inputs.milesSelect.value == "") {
            this.showError("Please select a radius (in miles).");
            return;
        }

        if (this.inputs.zipCode.value == "") {
            this.showError("Please enter a valid ZIP Code.");
            return;
        }

        this.resultsHr.style.display = "block";
        this.results.style.display = "block";
        this.results.innerHTML = '\
            <div class="d-flex justify-content-center">\
                <div class="spinner-border" role="status">\
                    <span class="sr-only">Loading...</span>\
                </div>\
            </div>';
        
        function processDropdown(value, isInt=false) {
            if (value == "") {
                return null;
            }

            if (isInt) {
                return parseInt(value);
            }

            return value;
        }

        this.getData(
            "search_sales_groups_2",
            {
                search: {
                    zip: parseInt(this.inputs.zipCode.value),
                    radius: parseInt(this.inputs.milesSelect.value),
                    category: processDropdown(this.inputs.category.value),
                    breed: processDropdown(this.inputs.breed.value),
                    minimum_weight: processDropdown(this.inputs.minimumWeight.value, true),
                    preconditioning_program: processDropdown(this.inputs.preconditioningProgram.value),
                    process_verified_program: processDropdown(this.inputs.processVerifiedProgram.value),
                }
            },
            true
        ).then((data) => {
            this.handleSearchResults(data);
        }).catch((message) => {
            this.results.innerHTML = "";
            this.showError(message.toString());
        });
    }

    handleSearchResults(data) {
        let sales_groups = data.sales_groups;
        let current_account_id = data.current_account_id;

        this.results.innerHTML = "";

        let isFirst = true;
        for (const sales_group of sales_groups) {
            let container = document.createElement("p");
            if (!isFirst) {
                container.style.marginTop = "50px";
            }
            isFirst = false;
            this.results.append(container);
            new SalesGroupViewer(sales_group, container, current_account_id);
        }

        if (sales_groups.length == 0) {
            this.results.innerHTML = "<div style='text-align:center;'>0 results</div>";
        }
    }
}
