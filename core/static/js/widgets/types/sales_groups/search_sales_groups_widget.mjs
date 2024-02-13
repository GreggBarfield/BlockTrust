import { Widget } from '../../widget.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';
import { SalesGroupFields } from './sales_group_fields.mjs';
import { InfoModal } from '../../../core/info_modal.mjs';

export class SearchSalesGroupsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";

        this.inputs = {};

        this.generate(
            JSON.parse(this.frame.getAttribute("data-widget-search")), 
            this.frame.getAttribute("data-widget-link"),
            JSON.parse(this.frame.getAttribute("data-widget-dates")),
            this.frame.getAttribute("data-widget-view-link")
        );
    }

    async generate(searchValues, searchLink, dates, viewLink) {

        this.frame.append(await this.generateSummaryTable(viewLink));
        this.frame.append(await this.generateSavedSearchesTable(searchLink));

        let searchName, searchID;
        if(Object.keys(searchValues).length){
            searchName = searchValues.name;
            searchID = searchValues.id;
        }

        this.form = document.createElement("form");
        this.form.addEventListener("submit", (e)=>{
            e.preventDefault();
            this.search();
        });
        
        let locationHeader = document.createElement("h6");
        locationHeader.innerHTML = `Search Options ${
            searchName?"<span class='text-brown'>(options loaded from: " + searchName + ")</span>":""
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
        zipCodeLabel.textContent = "Buyer Zip Code";
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

        function createSearchControl(name, on, isMultiple) {
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

            if(isMultiple){
                select.setAttribute("multiple", "multiple");
                $(select).select2();
            }
            else {
                addOption("", "", true);
            }

            for (const value of on) {
                addOption(value, value);
            }
            return select;
        }

        this.inputs.category = createSearchControl("Category/Sex", SalesGroupFields.commonCategoryNames, true);
        this.inputs.breed = createSearchControl("Breed", SalesGroupFields.commonBreedNames, true);
        this.inputs.minimumWeight = createSearchControl("Minimum Weight", SalesGroupFields.commonWeights);
        this.inputs.maximumWeight = createSearchControl("Maximum Weight", SalesGroupFields.commonWeights.map(w => w + 100));
        this.inputs.preconditioningProgram = createSearchControl("Precon Program", SalesGroupFields.commonPreconditioningProgramNames);
        this.inputs.program = createSearchControl("Program", SalesGroupFields.commonProgramNames, true);
        this.inputs.targetDate = createSearchControl("Target Delivery Date", dates);

        if(Object.keys(searchValues).length){
            this.inputs.milesSelect.value = searchValues.radius;
            this.inputs.zipCode.value = searchValues.zip;
            if(searchValues.multi_select_fields){
                if(searchValues.multi_select_fields.categories){
                    $(this.inputs.category).val(searchValues.multi_select_fields.categories).trigger("change");
                }
                if(searchValues.multi_select_fields.breeds){
                    $(this.inputs.breed).val(searchValues.multi_select_fields.breeds).trigger("change");
                }
                if(searchValues.multi_select_fields.programs){
                    $(this.inputs.program).val(searchValues.multi_select_fields.programs).trigger("change");
                }
            }
            if(searchValues.minimum_weight){
                this.inputs.minimumWeight.value = searchValues.minimum_weight;
            }
            if(searchValues.maximum_weight){
                this.inputs.maximumWeight.value = searchValues.maximum_weight;
            }
            if(searchValues.preconditioning_program){
                this.inputs.preconditioningProgram.value = searchValues.preconditioning_program;
            }
            if(searchValues.target_date_description){
                this.inputs.targetDate.value = searchValues.target_date_description;
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

        this.createSaveButtons(searchLink, submitFormGroup, searchID, searchName);

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

    createSaveButtons(link, submitFormGroup, searchID, searchName){
        let saveButton = document.createElement("input");
        saveButton.className = "btn btn-info";
        saveButton.type = "button";
        saveButton.value = "Save";

        if (searchID) {
            saveButton.addEventListener("click", ()=>{
                this.save(link, searchID, searchName);
            });
            submitFormGroup.append(saveButton); 
            let saveAsButton = saveButton.cloneNode(true);
            saveAsButton.value = "Save As New";
            saveAsButton.addEventListener("click", ()=>{
                this.save(link);
            });           
            submitFormGroup.append(saveAsButton);
        }
        else {
            saveButton.addEventListener("click", ()=>{
                this.save(link);
            });
            submitFormGroup.append(saveButton); 
        }
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
                        categories: $(this.inputs.category).val() != "" ? $(this.inputs.category).val() : null,
                        breeds: $(this.inputs.breed).val() != "" ? $(this.inputs.breed).val() : null,
                        minimum_weight: this.processDropdown(this.inputs.minimumWeight.value, true),
                        maximum_weight: this.processDropdown(this.inputs.maximumWeight.value, true),
                        preconditioning_program: this.processDropdown(this.inputs.preconditioningProgram.value),
                        programs: $(this.inputs.program).val() != "" ? $(this.inputs.program).val() : null,
                        target_date: this.processDropdown(this.inputs.targetDate.value)
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

    async generateSummaryTable(viewLink) {
        let container = document.createElement("div");
        container.className = "mb-5  table-responsive";

        let table = document.createElement("table");
        table.className = "table table-sm text-center mt-3 table-bordered";
        let thead = document.createElement("thead");
        thead.classList += "thead-light";
        let tr = document.createElement("tr");
        const headers = ["Name", "No. Head", "Category/Sex", "Breed", "Weight", "Market Name/Location","Sale Date", ""];
        for(const header of headers){
            let th = document.createElement("th");
            th.innerText = header;
            tr.append(th);
        }
        thead.append(tr);
        table.append(thead);
        const salesGroups = await this.getData("search_summary", [], false, "GET");
        if(salesGroups.length > 0){
            for(let salesGroup of salesGroups){
                let tr = document.createElement("tr");
                let td = document.createElement("td");
                td.innerText = salesGroup["group_name"];
                tr.append(td);
                td = document.createElement("td");
                td.innerText = salesGroup["reported"]["count"];
                tr.append(td);
                td = document.createElement("td");
                td.innerText = salesGroup["category"];
                tr.append(td);
                td = document.createElement("td");
                td.innerText = salesGroup["reported"]["breeds"];
                tr.append(td);
                td = document.createElement("td");
                td.innerText = salesGroup["reported"]["weight"];
                tr.append(td);
                td = document.createElement("td");
                td.innerText = salesGroup["delivery_location_type"] == "Auction"? salesGroup["delivery_location"] : salesGroup["delivery_location_type"];
                tr.append(td);
                td = document.createElement("td");
                td.innerText = new Date(salesGroup["sale_date"]*1000).toLocaleString("en-US", {
                    year: 'numeric',
                    month: 'numeric',
                    day: 'numeric',
                });
                tr.append(td);
                td = document.createElement("td");
                let loadLink = document.createElement("a");
                loadLink.className = "btn btn-sm btn-info";
                loadLink.href = `${viewLink}${salesGroup["id"]}`;
                loadLink.target = "_blank";
                loadLink.innerText = "View";
                td.append(loadLink);

                let notInterestedButton = document.createElement("button");
                notInterestedButton.className = "btn btn-sm btn-secondary";
                notInterestedButton.innerText = "Not Interested";
                td.append(notInterestedButton);
                notInterestedButton.onclick = async() =>{
                    const response = await fetch(
                        "/widgets/not-interested-in-sales-group",{
                            method: "POST",
                            body: JSON.stringify({"sales_group_search_id": 1, "sales_group_id": salesGroup.id}),
                            headers: {"Content-type": "application/json; charset=UTF-8"}
                        }
                    );
                    if(response.ok == true){
                        location.reload();
                    }
                }

                tr.append(td);
                table.append(tr);            
            }
        }
        else {
            let tr = document.createElement("tr");
            let td = document.createElement("td");
            td.setAttribute("colspan", "7");
            td.innerText = "Nothing to show currently";
            td.className = "font-italic";
            tr.append(td);
            table.append(tr);            
        }
        let expandControl = document.createElement("a");
        expandControl.innerHTML = "Search Results Quick Summary";
        expandControl.href = "javascript:void(0);";
        expandControl.title = "Toggle saved searches";
        expandControl.className = "h6";
        expandControl.addEventListener("click", (e)=>{
            e.preventDefault();
            table.classList.toggle("d-none");
        });
        container.append(expandControl);
        container.append(table);
        return container;
    }

    async generateSavedSearchesTable(searchLink) {

        let tableContainer = document.createElement("div");
        tableContainer.className = "mb-5 table-responsive";

        let table = document.createElement("table");
        table.className = "table table-sm text-center mt-3 table-bordered";
        let thead = document.createElement("thead");
        thead.classList += "thead-light";
        let tr = document.createElement("tr");
        const headers = ["Name", "Category/Sex", "Breed", "Saved Date", ""];
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
            td.innerText = search["multi_select_fields"]? ("categories" in search["multi_select_fields"]? search["multi_select_fields"]["categories"].join(", "): "" ): "";
            tr.append(td);
            td = document.createElement("td");
            td.innerText = search["multi_select_fields"]? ("breeds" in search["multi_select_fields"]? search["multi_select_fields"]["breeds"].join(", "): "" ) : "";
            tr.append(td);
            td = document.createElement("td");
            let UTCDate = new Date(search["last_updated_timestamp"] + " UTC");
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
            loadLink.className = "btn btn-sm btn-info";
            loadLink.href = `${this.frame.getAttribute("data-widget-link")}${search["id"]}`;
            loadLink.innerText = "Load";
            td.append(loadLink);
            let buttonDelete = document.createElement("button");
            buttonDelete.className = "btn btn-danger btn-sm";
            let icon = document.createElement("i");
            icon.className = "fa fa-trash";
            buttonDelete.append(icon);
            buttonDelete.title = "Delete search";
            buttonDelete.onclick = () => this.deleteSearch(search.id, searchLink);
            td.append(buttonDelete);
            tr.append(td);
            table.append(tr);
        }
        if( table.rows.length == 1){
            let tr = document.createElement("tr");
            let td = document.createElement("td");
            td.setAttribute("colspan", "5");
            td.innerText = "Nothing to show currently";
            td.className = "font-italic";
            tr.append(td);
            table.append(tr);     
        }

        let expandControl = document.createElement("a");
        expandControl.innerHTML = "Saved Searches";
        expandControl.href = "javascript:void(0);";
        expandControl.title = "Toggle saved searches";
        expandControl.className = "h6";
        expandControl.addEventListener("click", (e)=>{
            e.preventDefault();
            table.classList.toggle("d-none");
        });
        tableContainer.append(expandControl);
        tableContainer.append(table);
        return tableContainer;
    }

    async save(link, searchID=null, searchName=null) {

        if (this.validateForm()){

            let url, name, method;
            if(searchID){
                url = `sales_group_searches/${searchID}`;
                name = searchName;
                method = "PUT";
            }
            else {
                url = `sales_group_searches`;
                name = "";
                method = "POST";
            }
            let infoModal = new InfoModal("Enter a search name");
            let modalBody = infoModal.getBody();

            let form = document.createElement("form");

            let formGroup = document.createElement("div");
            formGroup.className = "form-group";

            let label = document.createElement("label");
            label.textContent = "Name:";
            formGroup.append(label);

            let nameInput = document.createElement("input");
            nameInput.className = "form-control";
            nameInput.value = name;
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
                if(!nameInput.value){
                    alert.className = "alert alert-danger";
                    alert.textContent = "Please enter a valid name";
                    saveButton.disabled = false;
                }
                else{
                    try {
                        let response = await this.getData(url, 
                            {
                                search: {
                                    name: nameInput.value,
                                    zip: parseInt(this.inputs.zipCode.value),
                                    radius: parseInt(this.inputs.milesSelect.value),
                                    categories: $(this.inputs.category).val() != "" ? $(this.inputs.category).val() : null,
                                    breeds: $(this.inputs.breed).val() != "" ? $(this.inputs.breed).val() : null,
                                    minimum_weight: this.processDropdown(this.inputs.minimumWeight.value, true),
                                    maximum_weight: this.processDropdown(this.inputs.maximumWeight.value, true),
                                    preconditioning_program: this.processDropdown(this.inputs.preconditioningProgram.value),
                                    programs: $(this.inputs.program).val() != "" ? $(this.inputs.program).val() : null,
                                    target_date: this.processDropdown(this.inputs.targetDate.value)
                                }
                            }, true, method
                        )
                        alert.className = "alert alert-success";
                        alert.textContent = "Saved! Redirecting...";
                        setTimeout(() => window.location.href = `${link}/${searchID ? searchID : response}`, 1000);
                    }
                    catch(err){
                        console.log(err);
                        alert.className = "alert alert-danger";
                        alert.textContent = "An unexpected error occured. Please try again after sometime";
                        saveButton.disabled = false;
                    }
                }
            });
        }
    }

    async deleteSearch(id, link){
        this.getData(`sales_group_searches`, [id], false, "DELETE");
        new InfoModal(`Search deleted successfully!`, null, false, "d-none", () => window.location.href = link);
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
