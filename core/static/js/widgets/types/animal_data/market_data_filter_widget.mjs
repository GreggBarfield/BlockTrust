import { Widget } from '../../widget.mjs';

export class MarketDataFilterWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.getData(
            "get_market_state_data",
            {}
        ).then((data) => {
            this.state_rows = data.market_data;
            this.frame.innerHTML = "";
            this.makeStateDropDown();
        });
    }

    createSection(form, name) {
        let header = document.createElement("h6");
        header.textContent = name;
        form.append(header);
        let row = document.createElement("div");
        row.className = "form-row row";
        form.append(row);

        form.append(document.createElement("br"));
        return row;
    }

    createSelect(group, name, values, val_ids="") {
        if (!Array.isArray(values)) {
            values = [values];
        }

        let groupLabel = document.createElement("label");
        groupLabel.className = "form-label";
        groupLabel.textContent = name;
        group.append(groupLabel);

        let select = document.createElement("select");
        select.className = "select2-hidden-accessible";
        group.append(select);

        let optionsStacked = [];
        for (const value of values) {
            if (val_ids == "") {
                optionsStacked.push({
                    id: value,
                    text: value
                });
            } else {
                optionsStacked.push({
                    id: val_ids[value],
                    text: value
                });
            }
        }

        $(select).select2({
            data: optionsStacked,
            multiple: false,
            tags: false,
            placeholder: "Select a State"
        });

        // Add event handler - on change
        $(select).val([optionsStacked[0]]);
        $(select).trigger('change');
        setTimeout(function () {
            $(select).val([]);
            $(select).trigger('change');
        }, 1);

        return select;
    }

    getCityData() {
        this.getData(
            "get_market_city_data/" + this.state,
            {}
        ).then((data) => {
            this.city_rows = data.market_data;
            this.divCityDropDown.innerHTML = "";

            let cities = [];
            let city_ids = {};
            for (const row in this.city_rows) {
                let item = this.city_rows[row]['market_location_city'] 
                    + " (" + this.city_rows[row]['slug_id'] + ")";
                cities.push(item);
                city_ids[item] = this.city_rows[row]['slug_id'];
            }
            cities.sort();
            let select = this.createSelect(this.divCityDropDown, "City", cities, city_ids);
            
            let self = this;

            $(select).on("change", function() {
                //since createBtn is invoked on change of city dropdown, 'this' argument will be the city dropdown itself.
                createBtn(self, this);
            });

            // Put HTML in frame
            this.row.append(this.divCityDropDown);
        });
    }

    makeStateDropDown() {
        this.form = document.createElement("form");
        this.frame.append(this.form);

        this.divStateDropDown = document.createElement("div");
        this.divStateDropDown.className = "col-5";
        this.divCityDropDown = document.createElement("div");
        this.divCityDropDown.className = "col-5";
        this.divBtn = document.createElement("div");
        this.divBtn.className = "col-2 text-left align-self-end";

        let values = [];
        for (const row in this.state_rows) {
            values.push(this.state_rows[row]);
        }
        values.sort();

        this.row = this.createSection(this.form, "Filter")
        let select = this.createSelect(this.divStateDropDown, "State", values)

        let self = this;

        $(select).on("change", function() {
            //since makeCityDropDown() is invoked on change of state dropdown, 'this' argument will be the state dropdown itself.
            makeCityDropDown(self, this);
        });

        // Put HTML in frame
        this.row.append(this.divStateDropDown);
    }
}

//Note that both below routines are outside the class
function makeCityDropDown(self, selectSelf) {
    if(selectSelf.value == "") {
        return;
    }

    self.state = selectSelf.value;

    self.divCityDropDown.innerHTML = '\
    <div class="d-flex justify-content-center">\
        <div class="spinner-border" role="status">\
            <span class="sr-only">Loading...</span>\
        </div>\
    </div>';

    //class object passed in is used to invoke getCityData() method of the same class
    self.getCityData();

    // Put HTML in frame
    self.row.append(self.divCityDropDown);
}

function createBtn(self, selectSelf) {
    if(selectSelf.value == "") {
        return;
    }
    let selectedItem = selectSelf.options[selectSelf.options.selectedIndex];

    let button = document.createElement("a");
    button.className = "btn btn-outline-secondary btn-sm mb-0";
    button.setAttribute("href", "/dashboard/data/market/" + 
        self.state + "/" + selectedItem.value);
    button.textContent = "View";

    // Put HTML in frame
    self.divBtn.append(button);
    self.row.append(self.divBtn);
}