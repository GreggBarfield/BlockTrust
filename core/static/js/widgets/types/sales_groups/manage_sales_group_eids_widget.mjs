import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class ManageSalesGroupEIDsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));

        // TODO: This is a bad data request, optimize later
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
        eids_selected.push(...this.data.eids)
        function addTooltip(dataToggle,title,position){
            let toolTip = document.createElement("a");
            toolTip.className="feather icon-info";
            toolTip.style = "color:#2962FF;padding-left:6px;width:100%; vertical-align:-1px";
            toolTip.setAttribute("data-toggle" ,dataToggle);
            toolTip.setAttribute("data-placement" ,"right");
            toolTip.setAttribute("title" ,title);
            position.append(toolTip);           
            $(document).ready(function(){
                $('[data-toggle='+dataToggle+']').tooltip(); 
            });
        }
       

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

        function createGroup(row, name, htmlFor,hasTooltip,dataToggle,tooltipText) {
            let group = document.createElement("div");
            group.className = "form-group col-md-6";
            row.append(group);


            let groupLabel = document.createElement("label");
            groupLabel.className = "form-label";
            groupLabel.textContent = name;
            if (hasTooltip)
                addTooltip(dataToggle,tooltipText,groupLabel);
            if (htmlFor !== null) {
                groupLabel.htmlFor = htmlFor;
            }
            group.append(groupLabel);
            return group;
        }

        function createCheckList({row, name, values, sales_group_eids},hasTooltip=false,dataToggle="",tooltipText=""){
            //This is custom for the eids checklist. Can be generalized later
            let id = "domuid" + window.DOMUIDNext++;
            let group = createGroup(row, name, id,hasTooltip,dataToggle,tooltipText);
            let eid_group = createGroup(row, "Assigned EIDs:", id,hasTooltip,dataToggle,tooltipText);
            eid_group.appendChild(document.createElement("br"));
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
                   
                console.log(eids_selected); 
                if($("#select-all-eid-checkbox").is(":checked")){
                    $(".eid-checkbox").prop("checked",true);
                    eids_selected=[];
                    for (const value in values) {
                        eids_selected.push(values[value].eid)
                    }
                    for(const i in sales_group_eids){
                        eids_selected.push(sales_group_eids[i]);
                    }   
                    console.log(eids_selected);             
                }
                else{
                    $(".eid-checkbox").prop("checked",false); 
                    eids_selected=[];
                    console.log(eids_selected); 
                }
            }
            var label = document.createElement('label')
            label.htmlFor = "Select All";
            label.className  = "form-label float-right font-weight-bold";
            label.appendChild(document.createTextNode("Select All")); 
            group.appendChild(label);
            group.appendChild(selectAllCheckbox);
            group.appendChild(document.createElement("br"));

            // Adding already existing eids to eids_selected
            for (const value in values) {
                let rowTag = document.createElement("tr");
                tableBody.appendChild(rowTag);

                let tdCheckbox = document.createElement("td");
                var checkbox = document.createElement("input");
                checkbox.type="checkbox";
                checkbox.name = "eid-checkbox";
                checkbox.className="eid-checkbox"
                checkbox.id=values[value].eid;
                checkbox.value = values[value].eid;
                checkbox.onchange = ()=>{
                    if($("#"+values[value].eid).is(":checked")){
                    eids_selected.push(values[value].eid);
                    }
                    else{
                        for(var i=0;i<eids_selected.length;i++){
                            if(eids_selected[i]==values[value].eid){eids_selected.splice(i,1);}
                        }
                    }
                }
                tdCheckbox.appendChild(checkbox);
                rowTag.appendChild(tdCheckbox);
                
                let tdEID = document.createElement("td");
                tdEID.textContent = values[value].eid;
                rowTag.appendChild(tdEID);

                let tdEIDDatetime = document.createElement("td");
                tdEIDDatetime.textContent = values[value].created_timestamp;
                rowTag.appendChild(tdEIDDatetime);
            }
            for(const i in sales_group_eids){ 
                let rowTag = document.createElement("tr");
                assigned_eids_tableBody.appendChild(rowTag);

                
                let tdCheckbox = document.createElement("td");
                var checkbox = document.createElement("input");
                checkbox.type="checkbox";
                checkbox.name = "eid-checkbox";
                checkbox.className="eid-checkbox"
                checkbox.id=sales_group_eids[i];
                checkbox.value = sales_group_eids[i];
                checkbox.checked = true;
                checkbox.onchange = ()=>{
                    if($("#"+sales_group_eids[i]).is(":checked")){
                    eids_selected.push(sales_group_eids[i]);
                    }
                    else{
                        for(var j=0;j<eids_selected.length;j++){
                            if(eids_selected[j]==sales_group_eids[i]){eids_selected.splice(j,1);}
                        }
                    }
                }
                tdCheckbox.appendChild(checkbox);
                rowTag.appendChild(tdCheckbox);

                let tdEID = document.createElement("td");
                tdEID.textContent = sales_group_eids[i];
                rowTag.appendChild(tdEID);
            }

            table.value = eids_selected;
            group.append(table);
            eid_group.append(assigned_eids_table);
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
        let eidSelector = createCheckList({
            row: eidsRow,
            name: "Available EIDs:",
            values: this.data.available_eids,
            sales_group_eids: this.data.eids
        },false,"","",this.data.eid_created_dates || []);

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

