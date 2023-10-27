import { Widget } from '../../widget.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';
import { SalesGroupFields } from '../../../sales_groups/sales_group_fields.mjs';
import { InfoModal } from '../../../core/info_modal.mjs';

export class SearchSalesGroupsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";

        this.inputs = {};
        this.generate(JSON.parse(this.frame.getAttribute("data-widget-search")));
    }

    async generate(searchValues) {

        this.frame.append(await this.generateSavedSearchesTable());

        this.form = document.createElement("form");
        this.form.addEventListener("submit", (e)=>{
            e.preventDefault();
            this.search();
        });
        
        let locationHeader = document.createElement("h6");
        locationHeader.innerHTML = `Search Options ${
            Object.keys(searchValues).length > 0?"<span class='text-brown'>(options loaded from: " + searchValues.name + ")</span>":""
        }` ;
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

        
        let expandControlFormGroup = document.createElement("div");
        expandControlFormGroup.className = "form-group";
        let expandControl = document.createElement("a");
        expandControl.textContent = "More Options";
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

        if(Object.keys(searchValues).length){
            this.inputs.milesSelect.value = searchValues.radius;
            this.inputs.zipCode.value = searchValues.zip;
            if(searchValues.category){
                this.inputs.category.value = searchValues.category;
            }
            if(searchValues.breed){
                this.inputs.breed.value = searchValues.breed;
            }
            if(searchValues.minimum_weight){
                this.inputs.minimumWeight.value = searchValues.minimum_weight;
            }
            if(searchValues.preconditioning_program){
                this.inputs.preconditioningProgram.value = searchValues.preconditioning_program;
            }
            if(searchValues.process_verified_program){
                this.inputs.processVerifiedProgram.value = searchValues.process_verified_program;
            }
            expandContainer.style.display = "block";
        }
        
        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        this.form.append(submitFormGroup);

        let submitButton = document.createElement("input");
        submitButton.className = "btn btn-primary";
        submitButton.type = "submit";
        submitButton.value = "Search";
        submitFormGroup.append(submitButton);

        let saveButton = document.createElement("input");
        saveButton.className = "btn btn-info";
        saveButton.type = "button";
        saveButton.value = "Save";
        saveButton.addEventListener("click", (e)=>{
            this.save();
        });
        submitFormGroup.append(saveButton);

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

    processDropdown(value, isInt=false) {
        if (value == "") {
            return null;
        }

        if (isInt) {
            return parseInt(value);
        }

        return value;
    }

    validateForm(){
        this.searchErrorAlert.style.display = "none";
        if (this.inputs.milesSelect.value == "") {
            this.showError("Please select a radius (in miles).");
            return false;
        }

        if (this.inputs.zipCode.value == "") {
            this.showError("Please enter a valid ZIP Code.");
            return false;
        }

        return true;
    }

    search() {

        if(this.validateForm()) {
            this.resultsHr.style.display = "block";
            this.results.style.display = "block";
            this.results.innerHTML = '\
                <div class="d-flex justify-content-center">\
                    <div class="spinner-border" role="status">\
                        <span class="sr-only">Loading...</span>\
                    </div>\
                </div>';

            this.getData(
                "search_sales_groups_2",
                {
                    search: {
                        zip: parseInt(this.inputs.zipCode.value),
                        radius: parseInt(this.inputs.milesSelect.value),
                        category: this.processDropdown(this.inputs.category.value),
                        breed: this.processDropdown(this.inputs.breed.value),
                        minimum_weight: this.processDropdown(this.inputs.minimumWeight.value, true),
                        preconditioning_program: this.processDropdown(this.inputs.preconditioningProgram.value),
                        process_verified_program: this.processDropdown(this.inputs.processVerifiedProgram.value),
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
    }

    async generateSavedSearchesTable() {

        let tableContainer = document.createElement("div");
        tableContainer.className = "mb-5";

        let expandControl = document.createElement("a");
        expandControl.innerHTML = "Saved Searches";
        expandControl.href = "javascript:void(0);";
        expandControl.title = "Toggle saved searches";
        expandControl.className = "h6";
        tableContainer.append(expandControl);

        let table = document.createElement("table");
        table.className = "table table-sm text-center mt-3";
        let thead = document.createElement("thead");
        thead.classList += "thead-light";
        let tr = document.createElement("tr");
        const headers = ["Name", "Saved Date", ""];
        for(const header of headers){
            let th = document.createElement("th");
            th.innerText = header;
            tr.append(th);
        }
        thead.append(tr);
        table.append(thead);
        
        const response = await this.getData("sales_group_searches", [], false, "GET");
        for(let search of response){
            let tr = document.createElement("tr");
            let td = document.createElement("td");
            td.innerText = search["name"];
            tr.append(td);
            td = document.createElement("td");
            let UTCDate = new Date(search["created_timestamp"] + " UTC");
            td.innerText = UTCDate.toLocaleString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric'
            });
            tr.append(td);
            td = document.createElement("td");
            let loadLink = document.createElement("a");
            loadLink.className = "btn btn-sm btn-secondary";
            loadLink.href = `${this.frame.getAttribute("data-widget-link")}${search["id"]}`;
            loadLink.innerText = "Load";
            td.append(loadLink);
            tr.append(td);
            table.append(tr);
        }
        if( table.rows.length == 1){
            let tr = document.createElement("tr");
            let td = document.createElement("td");
            td.setAttribute("colspan", "3");
            td.innerText = "Nothing to show currently";
            td.className = "font-italic";
            tr.append(td);
            table.append(tr);     
        }
        tableContainer.append(table);

        expandControl.addEventListener("click", (e)=>{
            e.preventDefault();
            table.classList.toggle("d-none");
        });
        return tableContainer;
    }

    async save() {

        if (this.validateForm()){

            let infoModal = new InfoModal(`Enter a name to save`);
            let modalBody = infoModal.getBody();

            let form = document.createElement("form");

            let formGroup = document.createElement("div");
            formGroup.className = "form-group";

            let label = document.createElement("label");
            label.textContent = "Name:";
            formGroup.append(label);

            let nameInput = document.createElement("input");
            nameInput.className = "form-control";
            formGroup.append(nameInput);
    
            form.append(formGroup);       
            modalBody.append(form);

            let saveButton = document.createElement("button");
            saveButton.textContent = "Save";
            saveButton.className = "btn btn-primary";
            infoModal.getActionButtonDiv().append(saveButton);

            let alert = document.createElement("div");
            modalBody.append(alert);

            saveButton.addEventListener("click", async()=>{
                saveButton.disabled = true;
                alert.className = "d-none";
                try {
                    await this.getData(`sales_group_searches`, 
                        {
                            search: {
                                name: nameInput.value,
                                zip: parseInt(this.inputs.zipCode.value),
                                radius: parseInt(this.inputs.milesSelect.value),
                                category: this.processDropdown(this.inputs.category.value),
                                breed: this.processDropdown(this.inputs.breed.value),
                                minimum_weight: this.processDropdown(this.inputs.minimumWeight.value, true),
                                preconditioning_program: this.processDropdown(this.inputs.preconditioningProgram.value),
                                process_verified_program: this.processDropdown(this.inputs.processVerifiedProgram.value),
                            }
                        }, true
                    )
                    alert.className = "alert alert-success";
                    alert.textContent = "Saved. Reloading...";
                    setTimeout(() => window.location.reload(), 1000);
                }
                catch(err){
                    alert.className = "alert alert-danger";
                    alert.textContent = "An unexpected error occured. Please try again after sometime";
                    saveButton.disabled = false;
                }
            });
        }
    }

    handleSearchResults(data) {
        let sales_groups = data.sales_groups;

        this.results.innerHTML = "";

        let isFirst = true;
        for (const sales_group of sales_groups) {
            let container = document.createElement("p");
            if (!isFirst) {
                container.style.marginTop = "50px";
            }
            isFirst = false;
            this.results.append(container);
            new SalesGroupViewer(sales_group, container);
        }

        if (sales_groups.length == 0) {
            this.results.innerHTML = "<div style='text-align:center;'>0 results</div>";
        }
    }
}
