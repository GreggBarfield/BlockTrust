import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class ManageSalesGroupEIDsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.getData(
            "get_eids_for_sales_group",
            {
                "sales_group": this.salesGroupID
            }
        ).then((data) => {
            this.data = data;
            this.eids_and_visual_ids_selected=this.data.assigned_animals;
            this.makeForm();
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

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
  
    createGroup(row, name, htmlFor) {
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

    /**
     * Returns a checklist of EIDs along with corresponding Visual ID
     * @param {Array} eidAndVisualIDList The list of EID/Visual ID objects
     * @param {Array} checkedEidAndVisualIDList The list of EID/Visual ID objects which need to be checked
     * @param {String} checkboxName The name for the checkboxes being created
     * @returns 
     */
    createCheckList(eidAndVisualIDList, checkedEidAndVisualIDList, checkboxName){
        // Creating checklist table
        let checkListTable = document.createElement('table');
        checkListTable.className = "table table-striped table-bordered nowrap";
        let checkListTableHead = document.createElement("thead");
        checkListTable.appendChild(checkListTableHead);
        //Table header row
        let checkListTableHeadRow0 = document.createElement("tr");
        checkListTableHead.appendChild(checkListTableHeadRow0);
        const checkListTableHeaders = ["select", "EID", "Visual ID"];
        for (const checkListTableHeaderText of checkListTableHeaders) {
            let th = document.createElement("th");
            th.textContent = checkListTableHeaderText;
            checkListTableHeadRow0.appendChild(th);
        }
        let checkListTableBody = document.createElement("tbody");
        checkListTable.appendChild(checkListTableBody);
        //Creating checklist table body
        for (const eidAndVisualID of eidAndVisualIDList) {
            let rowTag = document.createElement("tr");
            checkListTableBody.appendChild(rowTag);
            let tdCheckbox = document.createElement("td");
            var checkbox = document.createElement("input");
            checkbox.type="checkbox";
            checkbox.name = checkboxName;
            checkbox.className = "checkbox"
            checkbox.id = eidAndVisualID.eid;
            checkbox.value = eidAndVisualID;
            if(checkedEidAndVisualIDList.indexOf(eidAndVisualID)!=-1){
                checkbox.checked=true;
            }
            checkbox.onchange = ()=>{
                var selectedCheckbox = document.getElementById(eidAndVisualID.eid);
                if(selectedCheckbox.checked==true){
                this.eids_and_visual_ids_selected.push(eidAndVisualID);
                }
                else{
                    for(var i=0;i<this.eids_and_visual_ids_selected.length;i++){
                        if(this.eids_and_visual_ids_selected[i].eid==eidAndVisualID.eid){
                            this.eids_and_visual_ids_selected.splice(i,1);
                        }
                    }
                }
            }
            tdCheckbox.appendChild(checkbox);
            rowTag.appendChild(tdCheckbox);
            let tdEID = document.createElement("td");
            tdEID.textContent = eidAndVisualID.eid;
            rowTag.appendChild(tdEID);
            let tdVisualID = document.createElement("td")
            tdVisualID.textContent = eidAndVisualID.visual_id != null ? eidAndVisualID.visual_id : "N/A";
            rowTag.appendChild(tdVisualID);
        }
        return checkListTable;
    }

    createSelectAllCheckbox(checkboxName){         
        let selectAll = document.createElement("div");
        selectAll.className = "d-inline"
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
                    this.eids_and_visual_ids_selected.push(specifiedCheckbox.value);
                }          
            }
            else{
                var specifiedCheckboxes = document.getElementsByName(checkboxName);
                for(const specifiedCheckbox of specifiedCheckboxes){
                    specifiedCheckbox.checked=false;
                }
                this.eids_and_visual_ids_selected=[];
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

    makeForm(){
        let that=this;
        let card = document.createElement("div");
        card.className = "card";

        let editGroupName = document.createElement("h5");
        editGroupName.className = "mt-2";
        editGroupName.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;"
        editGroupName.textContent = `Edit Sales Group ${this.salesGroupID} EIDs`;

        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between";
        cardHeader.style = "padding:5px;padding-left: 15px;"
        cardHeader.append(editGroupName);

        if(this.data.mfa_healthtrack_partner){
            let applicationIDButtonDiv = document.createElement("div");
            applicationIDButtonDiv.className = "d-flex align-items-end flex-row";
    
            let applicationIDButton = document.createElement("button");
            applicationIDButton.className = "btn btn-outline-primary btn-sm";
            applicationIDButton.innerHTML = "Select EIDs by Application ID";
            applicationIDButton.onclick = function () {
            window.location.href = '/dashboard/sales-groups/select-eids-by-application-id/'+that.salesGroupID;
            };
            applicationIDButtonDiv.append(applicationIDButton);
            cardHeader.append(applicationIDButtonDiv);
        }
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);

        let form = document.createElement("form");
        cardBody.append(form);

        let eidsRow = this.createSection(form, "");
        let id = "domuid" + window.DOMUIDNext++;
        let availableEidGroup = this.createGroup(eidsRow,"Available EIDs:", id);
        let assignedEidGroup = this.createGroup(eidsRow, "Assigned EIDs:", id);

        let availableEidsChecklist = this.createCheckList(this.data.available_eids_with_visual_ids, [], "eidCheckBox") ;
        let assignedEidsCheckList = this.createCheckList(this.data.assigned_animals, this.data.assigned_animals, "eidCheckBox");
        let selectAll = this.createSelectAllCheckbox("eidCheckBox");
        
        availableEidGroup.append(selectAll);
        availableEidGroup.append(availableEidsChecklist);
        assignedEidGroup.append(assignedEidsCheckList);

        $(availableEidsChecklist).DataTable();
        $(assignedEidsCheckList).DataTable();

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
            action: "/widgets/data/save_eids_for_sales_group",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            asJSON: true,
            getData: () => {
                return {
                    id: this.salesGroupID,
                    eids_and_visual_ids: this.eids_and_visual_ids_selected
                }
            }
        });

        submitButton.addEventListener("click", () => {   
            this.asyncForm.submit();
        });
    }
}

