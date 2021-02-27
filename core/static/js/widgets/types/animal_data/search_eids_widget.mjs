import { Widget } from '../../widget.mjs';

export class SearchEIDsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.frame.innerHTML = "";

        this.inputs = {};

        this.generate();

    }

    generate() {
        this.form = document.createElement("form");
        this.form.addEventListener("submit", (e)=>{
            e.preventDefault();
            this.search();
        });

        let firstFormRow = document.createElement("div");
        firstFormRow.className = "form-row";
        this.form.append(firstFormRow);

        let eidNumberFormGroup = document.createElement("div");
        eidNumberFormGroup.className = "form-group col-md-6";
        firstFormRow.append(eidNumberFormGroup);
        let eidLabel = document.createElement("label");
        eidLabel.textContent = "EID";
        eidNumberFormGroup.append(eidLabel);

        this.inputs.eidNumber = document.createElement("input");
        this.inputs.eidNumber.className = "form-control";
        this.inputs.eidNumber.type = "number";
        this.inputs.eidNumber.placeholder = "12345"
        eidNumberFormGroup.append(this.inputs.eidNumber);
        
        let submitFormGroup = document.createElement("div");
        submitFormGroup.className = "form-group";
        submitFormGroup.style.marginTop = "2em";
        firstFormRow.append(submitFormGroup);

        let submitButton = document.createElement("input");
        submitButton.className = "btn btn-primary";
        submitButton.type = "submit";
        submitButton.value = "Search";
        submitFormGroup.append(submitButton);
      
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

    search() {
        this.searchErrorAlert.style.display = "none";

        if (this.inputs.eidNumber.value == "") {
            this.showError("Please enter a EID number.");
            return;
        }
        else if(this.inputs.eidNumber.value.length < 15) {
            this.showError("EID number must be of 15 digits.");
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
            "search_by_eid_if_visible",  
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
        if(data.matches === 0)
            this.results.innerHTML = "<div style='text-align:center;'>0 results</div>";
        else
            window.location.href = location.protocol + "//" + location.host + "/dashboard/animals/" + this.inputs.eidNumber.value;
    }
}
