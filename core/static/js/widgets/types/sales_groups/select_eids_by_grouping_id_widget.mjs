import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class SelectEIDsByGroupingIDWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.getData(
            "get_animals_and_grouping_ids_for_account",
        ).then((data) => {
            this.data = data;
            this.eidsAndVisualIDsList = [];
            this.groupingIDsList = this.filterGroupingIDs(this.data.available_animals_and_grouping_ids);
            this.makeForm();
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });
    }

    filterGroupingIDs(animalAndGroupingIDsList){
        let groupingIDsList = [];
        for(const animalAndGroupingID of animalAndGroupingIDsList){
            if(!groupingIDsList.includes(animalAndGroupingID.grouping_id) && animalAndGroupingID.grouping_id != null){
                groupingIDsList.push(animalAndGroupingID.grouping_id)
            }
        }
        return groupingIDsList;
    }

    createSection(form, name) {
        let header = document.createElement("h6");
        header.textContent = name;
        form.append(header);
        let row = document.createElement("div");
        row.className = "form-row";
        form.append(row);
        form.append(document.createElement("br"));
        return row;
    }

    createGroup(row, name, groupColumnSize=6) {
        let group = document.createElement("div");
        group.className = `form-group col-md-${groupColumnSize}`;
        row.append(group);
        let groupLabel = document.createElement("label");
        groupLabel.className = "form-label font-weight-bold";
        groupLabel.textContent = name;
        group.append(groupLabel);
        return group;
    }

    createSelect(row, name, options, placeholder, groupColumnSize=6){
        let group = this.createGroup(row, name, groupColumnSize);
        let select = document.createElement("select");
        select.required = true
        group.append(select);
        let optionsStacked = [];
        for (const option of options) {
            optionsStacked.push({
                id: option,
                text: option
            })
        }
        $(select).select2({data: optionsStacked, placeholder: placeholder});
        return select;
    }

    createTable(row, name, columns, groupColumnSize=6){
        let group = this.createGroup(row, name, groupColumnSize);
        // Create an empty table which can be populated dynamically
        let table = document.createElement('table');
        table.className = "table table-striped table-bordered nowrap";
        group.append(table);
        $(table).DataTable({columns: columns});
        return table;
    }

    makeForm(){
        let card = document.createElement("div");
        card.className = "card";

        let editGroupName = document.createElement("h5");
        editGroupName.className = "mt-2";
        editGroupName.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;";
        editGroupName.textContent = `Select EIDs by Application ID for Sales Group ${this.salesGroupID}`;

        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between";
        cardHeader.style = "padding:5px;padding-left: 15px;";
        
        cardHeader.append(editGroupName);
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);

        let form = document.createElement("form");
        cardBody.append(form);

        let applicationIDSelectRow = this.createSection(form, "Application ID");
        let applicationIDSelect = this.createSelect(applicationIDSelectRow, "Select Application ID", this.groupingIDsList, "Select an Option", 6);
        let eidsAndVisualIDsTableColumns = [{"data": 'eid', "title": "EID"}, {"data": 'visual_id', "title": "Visual ID"}, {"data": "grouping_id", "title": "Application ID"}]
        let eidsAndVisualIDsTable = this.createTable(applicationIDSelectRow, "EIDs and Visual IDs", eidsAndVisualIDsTableColumns, 6);
        
        applicationIDSelect.onchange = () =>{
            // Clearing out the EID's table and adding relevant EID's with application ID on change of Application ID select drop down
            $(eidsAndVisualIDsTable).DataTable().clear().draw();
            let animalsAndGroupingIDsList = [];
            for(const animal_and_grouping_id of this.data.available_animals_and_grouping_ids){
                if(animal_and_grouping_id.grouping_id == applicationIDSelect.value){
                    animalsAndGroupingIDsList.push({
                        "eid": animal_and_grouping_id.eid,
                        "visual_id": animal_and_grouping_id.visual_id != null ? animal_and_grouping_id.visual_id : "N/A",
                        "grouping_id": animal_and_grouping_id.grouping_id
                    });
                }
            }
            $(eidsAndVisualIDsTable).DataTable().rows.add(animalsAndGroupingIDsList).draw();
        }
        applicationIDSelect.onchange();

        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        form.append(submitFormGroup);
        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.type = "button";
        submitFormGroup.append(submitButton);
        this.frame.append(card);

        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);
        
        this.asyncForm = new AsyncForm({
            action: "/widgets/data/save_eids_by_application_id_for_sales_group",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    sales_group_id: this.salesGroupID,
                    eids_and_visual_ids_list: this.eidsAndVisualIDsList
                }
            }
        });

        submitButton.addEventListener("click", () => {
            for(const animal_and_grouping_id of this.data.available_animals_and_grouping_ids){
                if(animal_and_grouping_id.grouping_id == applicationIDSelect.value){
                    this.eidsAndVisualIDsList.push({
                        "eid": animal_and_grouping_id.eid,
                        "visual_id": animal_and_grouping_id.visual_id
                    });
                }
            }
            this.asyncForm.submit();
        });
        this.frame.append(card);
    }
}