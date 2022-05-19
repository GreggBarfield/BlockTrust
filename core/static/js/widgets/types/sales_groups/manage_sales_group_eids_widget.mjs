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
            this.eidsAndVisualIDsSelected=this.data.assigned_animals;
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
            checkbox.checked = false;
            if(checkedEidAndVisualIDList.indexOf(eidAndVisualID)!=-1){
                checkbox.checked=true;
            }
            checkbox.onchange = ()=>{
                var selectedCheckbox = document.getElementById(eidAndVisualID.eid);
                if(selectedCheckbox.checked==true){
                this.eidsAndVisualIDsSelected.push(eidAndVisualID);
                }
                else{
                    for(var i=0;i<this.eidsAndVisualIDsSelected.length;i++){
                        if(this.eidsAndVisualIDsSelected[i].eid==eidAndVisualID.eid){
                            this.eidsAndVisualIDsSelected.splice(i,1);
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

    createSelectAllCheckbox(nameOfCheckBoxesToBeSelected, availableEidAndVisualIDList, assignedEidAndVisualIDList){         
        let selectAll = document.createElement("div");
        selectAll.className = "d-inline"
        var selectAllCheckbox = document.createElement("input");
        selectAllCheckbox.type="checkbox";
        selectAllCheckbox.name = "select-all-eid-checkbox";
        selectAllCheckbox.className="checkbox float-right";
        selectAllCheckbox.id="select-all-eid-checkbox";
        selectAllCheckbox.onchange = ()=>{
            var checkboxesToBeSelected = document.getElementsByName(nameOfCheckBoxesToBeSelected);
            if(selectAllCheckbox.checked==true){ 
                this.eidsAndVisualIDsSelected=[];
                this.eidsAndVisualIDsSelected=this.eidsAndVisualIDsSelected.concat(assignedEidAndVisualIDList);
                this.eidsAndVisualIDsSelected=this.eidsAndVisualIDsSelected.concat(availableEidAndVisualIDList);
                for(const checkboxToBeSelected of checkboxesToBeSelected){
                    checkboxToBeSelected.checked=true;
                }
                /*
                // This is how we will have to set all the checkboxes to checked
                $(this.availableEIDsChecklist).DataTable().rows().every( function () {
                    var data = this.data();
                    let newCheckBoxString = data[0].substring(0, data[0].length-1) + " checked>";
                    data[0]=newCheckBoxString;
                    this.data(data);
                })
                */
            }
            else{
                this.eidsAndVisualIDsSelected=assignedEidAndVisualIDList;
                for(const checkboxToBeSelected of checkboxesToBeSelected){
                    checkboxToBeSelected.checked=false;
                }
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


        let eidsRow = this.createSection(form, "");
        let id = "domuid" + window.DOMUIDNext++;
        let availableEidGroup = this.createGroup(eidsRow,"Available EIDs:", id);
        let assignedEidGroup = this.createGroup(eidsRow, "Assigned EIDs:", id);

        let availableEIDsCheckBoxName = "availableEIDCheckBox";
        let assignedEIDsCheckBoxName = "assignedEIDCheckBox";
        let availableEIDsChecklist = this.createCheckList(this.data.available_eids_with_visual_ids, [], availableEIDsCheckBoxName);
        let assignedEIDsCheckList = this.createCheckList(this.data.assigned_animals, this.data.assigned_animals, assignedEIDsCheckBoxName);
        let selectAll = this.createSelectAllCheckbox(availableEIDsCheckBoxName, this.data.available_eids_with_visual_ids, this.data.assigned_animals);
        
        availableEidGroup.append(selectAll);
        availableEidGroup.append(availableEIDsChecklist);
        assignedEidGroup.append(assignedEIDsCheckList);

        $(availableEIDsChecklist).DataTable();
        $(assignedEIDsCheckList).DataTable();
        

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
                    eids_and_visual_ids: this.eidsAndVisualIDsSelected
                }
            }
        });

        submitButton.addEventListener("click", () => {
            this.asyncForm.submit();
        });
    }
}

