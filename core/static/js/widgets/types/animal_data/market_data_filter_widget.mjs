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

        // Patch
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
            console.log(this.city_rows);
            this.divCityDropDown.innerHTML = "";

            let values = [];
            let val_ids = {};
            for (const row in this.city_rows) {
                let item = this.city_rows[row]['market_location_city'];
                values.push(item);
                val_ids[item] = this.city_rows[row]['slug_id'];
            }
            values.sort();
            let select = this.createSelect(this.divCityDropDown, "City", values, val_ids);

            let that = this;
            function createBtn() {
                console.log(this.value);
                console.log(this.options.selectedIndex);
                if(this.value == "") {
                    return;
                }
                let selectedItem = this.options[this.options.selectedIndex];
                console.log(selectedItem.value);

                let button = document.createElement("a");
                button.className = "btn btn-outline-secondary btn-sm mb-0";
                button.setAttribute("href", "/dashboard/data/market/" + 
                    that.state + "/" + selectedItem.value);
                button.textContent = "View";

                // Put HTML in frame
                that.divBtn.append(button);
                that.row.append(that.divBtn);
            }
            $(select).on("change", createBtn);

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
            values.push(this.state_rows[row]['market_location_state']);
        }
        values.sort();

        this.row = this.createSection(this.form, "Filter")
        let select = this.createSelect(this.divStateDropDown, "State", values)

        let that = this;
        function makeCityDropDown() {
            console.log(this.value);
            if(this.value == "") {
                return;
            }
            that.state = this.value;

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