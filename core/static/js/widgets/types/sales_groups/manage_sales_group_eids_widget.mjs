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
        function createCheckList(values, valuesHeader, valuesChecked, checkboxName){
            // Creating checklist table
            let checkListTable = document.createElement('table');
            checkListTable.className = "table table-striped table-bordered nowrap";
            let checkListTableHead = document.createElement("thead");
            checkListTable.appendChild(checkListTableHead);
            //Table header row
            let checkListTableHeadRow0 = document.createElement("tr");
            checkListTableHead.appendChild(checkListTableHeadRow0);
            const checkListTableHeaders = ["select", valuesHeader];
            for (const checkListTableHeaderText of checkListTableHeaders) {
                let th = document.createElement("th");
                th.textContent = checkListTableHeaderText;
                checkListTableHeadRow0.appendChild(th);
            }
            let checkListTableBody = document.createElement("tbody");
            checkListTable.appendChild(checkListTableBody);
            //Creating checklist table body
            for (const value of values) {
                let rowTag = document.createElement("tr");
                checkListTableBody.appendChild(rowTag);
                let tdCheckbox = document.createElement("td");
                var checkbox = document.createElement("input");
                checkbox.type="checkbox";
                checkbox.name = checkboxName;
                checkbox.className = "checkbox"
                checkbox.id = value;
                checkbox.value = value;
                if(valuesChecked.indexOf(value)!=-1){
                    checkbox.checked=true;
                }
                checkbox.onchange = ()=>{
                    var selectedCheckbox = document.getElementById(value);
                    if(selectedCheckbox.checked==true){
                    eids_selected.push(value);
                    }
                    else{
                        for(var i=0;i<eids_selected.length;i++){
                            if(eids_selected[i]==value){eids_selected.splice(i,1);}
                        }
                    }
                }
                tdCheckbox.appendChild(checkbox);
                rowTag.appendChild(tdCheckbox);
                let tdEID = document.createElement("td");
                tdEID.textContent = value;
                rowTag.appendChild(tdEID);
            }
            return checkListTable;
        }
        function craeteSelectAllCheckbox(checkboxName){         
            let selectAll = document.createElement("div");
            var selectAllCheckbox = document.createElement("input");
            selectAllCheckbox.type="checkbox";
            selectAllCheckbox.name = "select-all-eid-checkbox";
            selectAllCheckbox.className="checkbox float-right";
            selectAllCheckbox.id="select-all-eid-checkbox";
            selectAllCheckbox.onchange = ()=>{
                if(selectAllCheckbox.checked==true){
                    var specifiedCheckboxes = document.getElementsByName(checkboxName);
                    for(const specifiedCheckbox of specifiedCheckboxes){
                        specifiedCheckbox.checked=true;
                        eids_selected.push(specifiedCheckbox.value);
                    }          
                }
                else{
                    var specifiedCheckboxes = document.getElementsByName(checkboxName);
                    for(const specifiedCheckbox of specifiedCheckboxes){
                        specifiedCheckbox.checked=false;
                    }
                    eids_selected=[];
                }
            }
            var label = document.createElement('label')
            label.htmlFor = "Select All";
            label.className  = "form-label float-right font-weight-bold";
            label.appendChild(document.createTextNode("Select All"));
            selectAll.append(label)
            selectAll.append(selectAllCheckbox)
            return selectAll; 
        }
        function createEidsCheckList(row, name, salesGroupAvailableEids, salesGroupAssignedEids){
            //This is custom for the eids checklist. Can be generalized later
            let id = "domuid" + window.DOMUIDNext++;
            let availableEidGroup = createGroup(row, name, id);
            let assignedEidGroup = createGroup(row, "Assigned EIDs:", id);

            let availableEidsChecklist = createCheckList(salesGroupAvailableEids, "EID", [], "eidCheckBox") ;
            let assignedEidsCheckList = createCheckList(salesGroupAssignedEids, "EID", salesGroupAssignedEids, "eidCheckBox");
            let selectAll = craeteSelectAllCheckbox("eidCheckBox");
            availableEidGroup.append(selectAll);
            availableEidGroup.append(availableEidsChecklist);
            assignedEidGroup.append(assignedEidsCheckList);
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
        let eidSelector = createEidsCheckList(eidsRow,"Available EIDs:",this.data.available_eids,this.data.assigned_eids);

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

