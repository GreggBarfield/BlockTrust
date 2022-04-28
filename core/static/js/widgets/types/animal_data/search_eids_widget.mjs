import { Widget } from '../../widget.mjs';

export class SearchEIDsWidget extends Widget {
    constructor(frame, searchFrame, postRoute, redirectLink) {
        super(frame);
        this.searchFrame = searchFrame;
        this.postRoute = postRoute;
        this.redirectLink = redirectLink;
    }

    initType() {
        this.frame.innerHTML = "";

        this.inputs = {};

        this.generate();

    }

    generate() {
        this.form = document.createElement("form");
   
        let firstFormRow = document.createElement("div");
        firstFormRow.className = "form-row";
        this.form.append(firstFormRow);

        let eidNumberFormGroup = document.createElement("div");
        eidNumberFormGroup.className = "form-group col-md-6";
        firstFormRow.append(eidNumberFormGroup);
        let eidLabel = document.createElement("label");
        eidLabel.textContent = "Enter 15-digit EID or Visual ID Number";
        eidNumberFormGroup.append(eidLabel);

        this.inputs.eidNumber = document.createElement("input");
        this.inputs.eidNumber.className = "form-control";
        this.inputs.eidNumber.type = "number";
        this.inputs.eidNumber.placeholder = "12345"
        eidNumberFormGroup.append(this.inputs.eidNumber);
        
        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Search";
        submitButton.addEventListener("click", (e)=>{
            this.search();
        });
        this.searchFrame.prepend(submitButton);
      
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
        this.results.style.marginLeft = "-0.5rem";
        this.frame.append(this.results);
    }

    showError(error) {
        this.searchErrorAlert.style.display = "block";
        this.searchErrorAlert.textContent = error;
    }

    search() {
        this.searchErrorAlert.style.display = "none";

        if (this.inputs.eidNumber.value == "") {
            this.showError("Please enter a EID number.");
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
      
        this.getData(
            this.postRoute,
            {
                search: {
                    eid: parseInt(this.inputs.eidNumber.value)
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
        if(data.matches.length == 0)
            this.results.innerHTML = "<div style='text-align:center;'>0 results</div>";
        else if(data.matches.length == 1) {  
            window.location.href = location.protocol + "//" + location.host + this.redirectLink + data.matches[0].eid;
        }
        else {
            this.results.innerHTML = "";

            let mainTable = document.createElement("table");
            mainTable.className = "table table-bordered nowrap";

            // Header
            let mainTableHead = document.createElement("thead");
            mainTable.appendChild(mainTableHead);
    
            let mainTableHeadRow = document.createElement("tr");
            mainTableHead.appendChild(mainTableHeadRow);
            const headers = ["EID number", "Visual Id", ""];
            for (const headerText of headers) {
                let th = document.createElement("th");
                th.textContent = headerText;
                mainTableHeadRow.appendChild(th);
            }

             let mainTableBody = document.createElement("tbody");
             mainTable.appendChild(mainTableBody);

            for(const match of data.matches) {
                let rowTag = document.createElement("tr");
                mainTableBody.appendChild(rowTag);

                let tdEID = document.createElement("td");
                tdEID.innerHTML = match.eid;
                rowTag.appendChild(tdEID);

                let tdvisualID = document.createElement("td");
                tdvisualID.innerHTML = match.visual_id;
                rowTag.appendChild(tdvisualID);          

                let tdSelect = document.createElement("td");
                rowTag.appendChild(tdSelect);
                let btnSelect = document.createElement("a");
                btnSelect.className = "btn btn-info btn-md";
                btnSelect.setAttribute("href", this.redirectLink + match.eid);
                btnSelect.textContent = "Select";
                tdSelect.appendChild(btnSelect);
            }
            
            this.results.append(mainTable);
        }
    }
}
