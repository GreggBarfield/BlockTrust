import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class SelectEIDsByApplicationIDWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.getData(
            "get_eids_and_application_ids_for_account",
        ).then((data) => {
            this.data = data;
            console.log(this.data.eids_and_application_ids.length);
            this.makeForm();
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

    }
    makeForm(){
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

        function createGroup(row, name, htmlFor, groupColumnSize=6) {
            let group = document.createElement("div");
            group.className = `form-group col-md-${groupColumnSize}`;
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

        function createSelect(row, name, options, placeholder, groupColumnSize=6){
            let id = "domuid" + window.DOMUIDNext++;
            let group = createGroup(row, name, id, groupColumnSize);
            let select = document.createElement("select");
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
            $(select).select2({data: optionsStacked, placeholder: placeholder});
            return select;
        }

        function createTable(row, name, columns, groupColumnSize=6){
            let id = "domuid" + window.DOMUIDNext++;
            let group = createGroup(row, name, id, groupColumnSize);
            // Creating checklist table
            let table = document.createElement('table');
            table.className = "table table-striped table-bordered nowrap";
            group.append(table);
            $(table).DataTable({columns: columns});
            return table;
        }

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

        let applicationIDSelectRow = createSection(form, "Application ID");
        let applicationIDSelect = createSelect(applicationIDSelectRow, "Select Application ID", this.data.application_id_list, "Select an Option", 6);
        let eidsAndVisualIDsTableColumns = [{"data": 'eid', "title": "EID"}, {"data": 'visual_id', "title": "Visual ID"}, {"data": "grouping_id", "title": "Grouping ID"}]
        let eidsAndVisualIDsTable = createTable(applicationIDSelectRow, "EIDs and Visual IDs", eidsAndVisualIDsTableColumns, 6);
        
        applicationIDSelect.onchange = () =>{
            $(eidsAndVisualIDsTable).DataTable().clear().draw();
            let eidsAndVisualIDsList = [];
            for(const eid_and_application_id of this.data.eids_and_application_ids){
                if(eid_and_application_id.grouping_id == applicationIDSelect.value){
                    eidsAndVisualIDsList.push({
                        "eid": eid_and_application_id.eid,
                        "visual_id": eid_and_application_id.visual_id,
                        "grouping_id": eid_and_application_id.grouping_id
                    });
                }
            }
            $(eidsAndVisualIDsTable).DataTable().rows.add(eidsAndVisualIDsList).draw();
        }
        applicationIDSelect.onchange();
        
        this.frame.append(card);
    }
}