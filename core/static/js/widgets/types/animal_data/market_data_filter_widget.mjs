import { Widget } from '../../widget.mjs';

export class MarketDataFilterWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.getData(
            "get_usda_favorites",
            {}
        ).then((data) => {
            this.favorites = data.favorites;
            if(this.favorites != null && this.favorites.length > 0)
                this.makeFavorites();
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
            
            let firstRow = document.createElement("div");
            firstRow.id = "first";
            this.frame.append(firstRow);

            let secondRow = document.createElement("div");
            secondRow.id = "second";
            this.frame.append(secondRow);            
        });

        this.getData(
            "data_request",
            {
                request: {
                    type: 'market_data_cache',
                    params: {}
                }
            }
        ).then((data) => {
            this.state_rows = data.result.states;
            this.city_rows = data.result.cities_per_state;
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

    createSelect(group, name, values, val_ids="", placeholder="") {
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

        let textPlaceHolder = "Select a State";
        if(placeholder != "")
            textPlaceHolder = placeholder
        $(select).select2({
            data: optionsStacked,
            multiple: false,
            tags: false,
            placeholder: textPlaceHolder
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
        this.divCityDropDown.innerHTML = "";

        let cities = [];
        let city_ids = {};
        for (const row in this.city_rows[this.state]) {
            let item = this.city_rows[this.state][row]['market_location_city'] 
                + " (" + this.city_rows[this.state][row]['slug_id'] + ")";
            cities.push(item);
            city_ids[item] = this.city_rows[this.state][row]['slug_id'];
        }
        cities.sort();
        let select = this.createSelect(this.divCityDropDown, "City", cities, city_ids);
        
        let self = this;

        $(select).on("change", function() {
            //since createFilterViewBtn() is invoked on change of city dropdown, 'this' argument will be the city dropdown itself.
            self.createFilterViewBtn(this);
            self.filterRow.append(self.divFilterBtn);
        });

        // Put HTML in frame
        this.filterRow.append(this.divCityDropDown);
    }

    makeStateDropDown() {
        this.divStateDropDown = document.createElement("div");
        this.divStateDropDown.className = "col-4";
        this.divCityDropDown = document.createElement("div");
        this.divCityDropDown.className = "col-4";

        let values = [];
        for (const row in this.state_rows) {
            values.push(this.state_rows[row]['market_location_state']);
        }
        values.sort();

        let secondRow = document.getElementById("second");
        this.filterRow = this.createSection(secondRow, "Filter")
        let select = this.createSelect(this.divStateDropDown, "State", values)

        let self = this;

        $(select).on("change", function() {
            //since makeCityDropDown() is invoked on change of state dropdown, 'this' argument will be the state dropdown itself.
            self.resetFilterRowBtns();
            self.makeCityDropDown(this);
        });

        this.filterRow.append(this.divStateDropDown);
    }

    makeFavorites() {
        this.divFavDropDown = document.createElement("div");
        this.divFavDropDown.className = "col-4";

        let cities = [];
        let city_ids = {};
        for (const row in this.favorites) {
            let item = this.favorites[row]['city_name'] 
                + ", " + this.favorites[row]['state']
                + " (" + this.favorites[row]['city_id'] + ")";
            cities.push(item);
            city_ids[item] = this.favorites[row]['city_id'];
        }
        cities.sort();

        let firstRow = document.getElementById("first");
        this.favRow = this.createSection(firstRow, "Favorites")
        let select = this.createSelect(this.divFavDropDown, "", 
            cities, city_ids, "Select a favorite location");

        let self = this;
        
        $(select).on("change", function() {
            //since createFavViewBtn() is invoked on change of state dropdown, 'this' argument will be the state dropdown itself.
            self.createFavRowBtns();
            self.createFavViewBtn(this);
            self.createRemoveFavBtn(this);
        });

        this.favRow.append(this.divFavDropDown);
    }

    resetFilterRowBtns() {
        let viewBtn = document.getElementById("filter-view-btn");
        if(viewBtn != null)
            viewBtn.remove();

        if(this.divFilterBtn != null)
            this.divFilterBtn.remove();
    }

    resetFavRowBtns() {
        let viewBtn = document.getElementById("fav-view-btn");
        if(viewBtn != null)
            viewBtn.remove();
        
        let removeBtn = document.getElementById("remove-fav-btn");
        if(removeBtn != null)
            removeBtn.remove();

        if(this.divFavBtn != null)
            this.divFavBtn.remove();
    }

    createFavRowBtns() {
        if(this.divFavBtn == null || this.favRow.lastChild != this.divFavBtn) {
            this.divFavBtn = document.createElement("div");
            this.divFavBtn.className = "col-4 text-left align-self-end";
            this.favRow.append(this.divFavBtn);
        }
    }

    makeCityDropDown(selectSelf) {
        if(selectSelf.value == "") {
            return;
        }
    
        this.state = selectSelf.value;
    
        this.divCityDropDown.innerHTML = '\
        <div class="d-flex justify-content-center">\
            <div class="spinner-border" role="status">\
                <span class="sr-only">Loading...</span>\
            </div>\
        </div>';
    
        this.getCityData();
        this.filterRow.append(this.divCityDropDown);
    }

    createFilterViewBtn(selectSelf) {    
        if(this.divFilterBtn == null) {
            this.divFilterBtn = document.createElement("div");
            this.divFilterBtn.className = "col-4 text-left align-self-end";
        }
    
        if(selectSelf.value == "") {
            return;
        }
        let selectedItem = selectSelf.options[selectSelf.options.selectedIndex];
        let button = document.getElementById("filter-view-btn");
    
        if (button == null) {
            button = document.createElement("a");
            button.id = "filter-view-btn";
            button.className = "btn btn-outline-secondary btn-sm mb-0";
            button.setAttribute("href", "/dashboard/data/market/" + 
                this.state + "/" + selectedItem.value);
                button.textContent = "View";
        } else {
            button.setAttribute("href", "/dashboard/data/market/" + 
                this.state + "/" + selectedItem.value);        
        }
    
        this.divFilterBtn.append(button);
    }

    createFavViewBtn(selectSelf) {    
        if(selectSelf.value == "") {
            return;
        }
        let selectedItem = selectSelf.options[selectSelf.options.selectedIndex];
        let button = document.getElementById("fav-view-btn");

        // Parse state from text
        let state = selectedItem.text.split(", ")[1];
        state = state.split(" (")[0];
    
        if (button == null) {
            button = document.createElement("a");
            button.id = "fav-view-btn";
            button.className = "btn btn-outline-secondary btn-sm mb-0";
            button.setAttribute("href", "/dashboard/data/market/" + 
                state + "/" + selectedItem.value);
                button.textContent = "View";
        } else {
            button.setAttribute("href", "/dashboard/data/market/" + 
                state + "/" + selectedItem.value);        
        }
    
        this.divFavBtn.append(button);
    }

    createRemoveFavBtn(selectSelf) {
        if(selectSelf.value == "") {
            return;
        }
        let selectedItem = selectSelf.options[selectSelf.options.selectedIndex];
        let button = document.getElementById("remove-fav-btn");
    
        if (button == null) {
            button = document.createElement("a");
            button.id = "remove-fav-btn";
            button.className = "btn btn-outline-secondary btn-sm mb-0";
            button.textContent = "Remove from favorites";
            button.style = "cursor: pointer"; 
        }

        // Parse state from text
        let state = selectedItem.text.split(", ")[1];
        state = state.split(" (")[0];

        button.addEventListener("click", () => {
            $.ajax({
                url: "/widgets/data/remove_usda_favorite",
                data: JSON.stringify({
                    "state": state,
                    "city_id": selectedItem.value
                }),
                contentType: 'application/json',
                method: "POST"
            }).then(()=>{
                selectSelf.remove(selectSelf.options.selectedIndex);
                $(selectSelf).select2('val', 0);
                this.resetFavRowBtns();
            });
        });
    
        this.divFavBtn.append(button);
    }
}
