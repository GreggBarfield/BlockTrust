import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class ManageSalesGroupEIDsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.getData(
            "manage_eids",
            {
                "sales_group": this.salesGroupID
            }
        ).then((data) => {
            this.data = data;
            this.makeForm();
        });


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

    }
    
    makeForm(){
        // Sections
        let eids_selected = [];
        eids_selected.push(...this.data.assigned_eids)
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
            group.className = "form-group col-md-6";
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

        function createCheckList(row, name, salesGroupAvailableEids, salesGroupAssignedEids){
            //This is custom for the eids checklist. Can be generalized later
            let id = "domuid" + window.DOMUIDNext++;
            let availableEidGroup = createGroup(row, name, id);
            let assignedEidGroup = createGroup(row, "Assigned EIDs:", id);
            assignedEidGroup.appendChild(document.createElement("br"));
            // Creating table outline
            let table = document.createElement('table');
            table.className = "table table-striped table-bordered nowrap";
            let tableHead = document.createElement("thead");
            table.appendChild(tableHead);
            //Table header row
            let tableHeadRow0 = document.createElement("tr");
            tableHead.appendChild(tableHeadRow0);
            const headers = ["select", "EID", "Date/Time of Upload"];
            for (const headerText of headers) {
                let th = document.createElement("th");
                th.textContent = headerText;
                tableHeadRow0.appendChild(th);
            }

            let tableBody = document.createElement("tbody");
            table.appendChild(tableBody);
            // Creating assigned EIDs table
            let assigned_eids_table = document.createElement('table');
            assigned_eids_table.className = "table table-striped table-bordered nowrap";
            let assigned_eids_tableHead = document.createElement("thead");
            assigned_eids_table.appendChild(assigned_eids_tableHead);
            //Table header row
            let assigned_eids_tableHeadRow0 = document.createElement("tr");
            assigned_eids_tableHead.appendChild(assigned_eids_tableHeadRow0);
            const assigned_eids_headers = ["select", "EID"];
            for (const assigned_eids_headerText of assigned_eids_headers) {
                let th = document.createElement("th");
                th.textContent = assigned_eids_headerText;
                assigned_eids_tableHeadRow0.appendChild(th);
            }

            let assigned_eids_tableBody = document.createElement("tbody");
            assigned_eids_table.appendChild(assigned_eids_tableBody);

            //Creating select all functionality

            var selectAllCheckbox = document.createElement("input");
            selectAllCheckbox.type="checkbox";
            selectAllCheckbox.name = "select-all-eid-checkbox";
            selectAllCheckbox.className="select-all-eid-checkbox float-right";
            selectAllCheckbox.id="select-all-eid-checkbox";
            selectAllCheckbox.onchange = ()=>{
                if($("#select-all-eid-checkbox").is(":checked")){
                    $(".eid-checkbox").prop("checked",true);
                    eids_selected=[];
                    for (const value in salesGroupAvailableEids) {
                        eids_selected.push(salesGroupAvailableEids[value].eid)
                    }
                    for(const i in salesGroupAssignedEids){
                        eids_selected.push(salesGroupAssignedEids[i]);
                    }            
                }
                else{
                    $(".eid-checkbox").prop("checked",false); 
                    eids_selected=[];
                }
            }
            var label = document.createElement('label')
            label.htmlFor = "Select All";
            label.className  = "form-label float-right font-weight-bold";
            label.appendChild(document.createTextNode("Select All")); 
            availableEidGroup.appendChild(label);
            availableEidGroup.appendChild(selectAllCheckbox);
            availableEidGroup.appendChild(document.createElement("br"));

            // Adding already existing eids to eids_selected
            for (const value in salesGroupAvailableEids) {
                let rowTag = document.createElement("tr");
                tableBody.appendChild(rowTag);

                let tdCheckbox = document.createElement("td");
                var checkbox = document.createElement("input");
                checkbox.type="checkbox";
                checkbox.name = "eid-checkbox";
                checkbox.className="eid-checkbox"
                checkbox.id=salesGroupAvailableEids[value].eid;
                checkbox.value = salesGroupAvailableEids[value].eid;
                checkbox.onchange = ()=>{
                    if($("#"+salesGroupAvailableEids[value].eid).is(":checked")){
                    eids_selected.push(salesGroupAvailableEids[value].eid);
                    }
                    else{
                        for(var i=0;i<eids_selected.length;i++){
                            if(eids_selected[i]==salesGroupAvailableEids[value].eid){eids_selected.splice(i,1);}
                        }
                    }
                }
                tdCheckbox.appendChild(checkbox);
                rowTag.appendChild(tdCheckbox);
                
                let tdEID = document.createElement("td");
                tdEID.textContent = salesGroupAvailableEids[value].eid;
                rowTag.appendChild(tdEID);

                let tdEIDDatetime = document.createElement("td");
                tdEIDDatetime.textContent = salesGroupAvailableEids[value].created_timestamp;
                rowTag.appendChild(tdEIDDatetime);
            }
            for(const i in salesGroupAssignedEids){ 
                let rowTag = document.createElement("tr");
                assigned_eids_tableBody.appendChild(rowTag);

                
                let tdCheckbox = document.createElement("td");
                var checkbox = document.createElement("input");
                checkbox.type="checkbox";
                checkbox.name = "eid-checkbox";
                checkbox.className="eid-checkbox"
                checkbox.id=salesGroupAssignedEids[i];
                checkbox.value = salesGroupAssignedEids[i];
                checkbox.checked = true;
                checkbox.onchange = ()=>{
                    if($("#"+salesGroupAssignedEids[i]).is(":checked")){
                    eids_selected.push(salesGroupAssignedEids[i]);
                    }
                    else{
                        for(var j=0;j<eids_selected.length;j++){
                            if(eids_selected[j]==salesGroupAssignedEids[i]){eids_selected.splice(j,1);}
                        }
                    }
                }
                tdCheckbox.appendChild(checkbox);
                rowTag.appendChild(tdCheckbox);

                let tdEID = document.createElement("td");
                tdEID.textContent = salesGroupAssignedEids[i];
                rowTag.appendChild(tdEID);
            }

            table.value = eids_selected;
            availableEidGroup.append(table);
            assignedEidGroup.append(assigned_eids_table);
            return table;
        }

        let that = this;
        let card = document.createElement("div");
        card.className = "card";
        let cardHeader = document.createElement("h3");
        cardHeader.className = "col-form-label";
        cardHeader.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;"
        cardHeader.textContent = "Edit Sales Group EIDs " + this.data.id + ":  ";

        let editGroupName = document.createElement("div");
        editGroupName.className = "card-header form-group row";
        editGroupName.style = "padding:5px;padding-left: 15px;"

        editGroupName.append(cardHeader);
        card.append(editGroupName);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);

        let form = document.createElement("form");
        cardBody.append(form);

        let eidsRow = createSection(form, "");
        let eidSelector = createCheckList(eidsRow,"Available EIDs:",this.data.available_eids_with_timestamps,this.data.assigned_eids);

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
            action: "/widgets/data/save_sales_group_eids",
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
                    eids: eids_selected
                }
            }
        });

        submitButton.addEventListener("click", () => {
            
            this.asyncForm.submit();
        });
    }
}

