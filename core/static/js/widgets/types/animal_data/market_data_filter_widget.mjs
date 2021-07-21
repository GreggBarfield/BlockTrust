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
            console.log(this.state_rows);
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

    createSelect(group, name, values, placeholder, isCity=false) {
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
            if (isCity) {
                optionsStacked.push({
                    id: value.slug_id,
                    text: value.city + " (id: " + value.slug_id + ")"
                });
            } else {
                optionsStacked.push({
                    id: value,
                    text: value
                });
            }
        }

        $(select).select2({
            data: optionsStacked,
            multiple: false,
            tags: false,
            placeholder: placeholder
        });

        // Patch
        $(select).val([optionsStacked[0]]);
        $(select).trigger('change');
        setTimeout(function () {
            $(select).val([]);
            $(select).trigger('change');
        }, 1);

        return select;
    }

    compareItem(left, right) {
        if (left.city < right.city){
            return -1;
        }
        if (left.city > right.city){
            return 1;
        }
        return 0;
    }

    getCityData() {
        this.getData(
            "get_market_city_data/" + this.state,
            {}
        ).then((data) => {
            this.city_rows = data.market_data;
            console.log(this.city_rows);
            this.divCityDropDown.innerHTML = "";

            let values = [];
            for (const row in this.city_rows) {
                let item = {
                    'city' : this.city_rows[row]['market_location_city'],
                    'slug_id' : this.city_rows[row]['slug_id']
                    }
                values.push(item);
            }
            values.sort(this.compareItem);
            let select = this.createSelect(this.divCityDropDown, "City", 
                values, "Select a city", true);

            let that = this;
            let button = document.createElement("a");
            function createBtn() {
                console.log(this.value);
                console.log(this.options.selectedIndex);
                if(this.value == "") {
                    return;
                }
                let selectedItem = this.options[this.options.selectedIndex];
                console.log(selectedItem.value);

                button.className = "btn btn-outline-secondary btn-sm mb-0";
                button.setAttribute("href", "/dashboard/data/market/" + 
                    that.state + "/" + selectedItem.value);
                button.textContent = "View";

                // Put HTML in frame
                that.divBtn.append(button);
            }
            $(select).on("change", createBtn);
            
            // Put HTML in frame
            this.row.append(this.divCityDropDown);
            this.row.append(that.divBtn);
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
            values.push(this.state_rows[row]['market_location_state']);
        }
        values.sort();

        this.row = this.createSection(this.form, "Filter")
        let select = this.createSelect(this.divStateDropDown, "State", 
            values, "Select a State")

        let that = this;
        function makeCityDropDown() {
            console.log(this.value);
            if(this.value == "") {
                return;
            }
            that.state = this.value;

            that.divBtn.innerHTML = '';
            that.divCityDropDown.innerHTML = '\
            <div class="d-flex justify-content-center">\
                <div class="spinner-border" role="status">\
                    <span class="sr-only">Loading...</span>\
                </div>\
            </div>';

            that.getCityData(this.value);

            // Put HTML in frame
            that.row.append(that.divCityDropDown);
        }
        $(select).on("change", makeCityDropDown);

        // Put HTML in frame
        this.row.append(this.divStateDropDown);
    }
}