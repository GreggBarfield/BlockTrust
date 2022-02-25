import { Widget } from '../../widget.mjs';

export class MarketDataFilterWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        Promise.all([
            this.getData(
                "get_usda_favorites_for_account",
                {}
            ).then((data) => {
                this.favorites = data.favorites;
            }),

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
            })

        ]).then(() => {
            this.frame.innerHTML = "";
            let favRow = document.createElement("div");
            this.frame.append(favRow);
            let filterRow = document.createElement("div");
            this.frame.append(filterRow);

            if(this.favorites != null && this.favorites.length > 0)
                this.makeFavorites(favRow);
            this.makeStateDropDown(filterRow);
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

        $(select).select2({
            data: optionsStacked,
            multiple: false,
            tags: false,
            placeholder: placeholder !="" ? placeholder : "Select a state"
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

    makeStateDropDown(row) {
        let divStateDropdown = document.createElement("div");
        divStateDropdown.className = "col-4";

        let values = [];
        for (const row in this.state_rows) {
            values.push(this.state_rows[row]['market_location_state']);
        }
        values.sort();

        let filterSection = this.createSection(row, "New Selection")
        let selectStateDropdown = this.createSelect(divStateDropdown, "State", values)

        let divFilterBtn = document.createElement("div");
        divFilterBtn.className = "col-4 text-left align-self-end";
        let divCityDropdown = document.createElement("div");
        divCityDropdown.className = "col-4";

        selectStateDropdown.oninput = () => {
            this.state = selectStateDropdown.value;
            this.resetFilterRowBtns();
            this.makeCityDropDown(filterSection, divFilterBtn, divCityDropdown);
        };

        filterSection.append(divStateDropdown);
        filterSection.append(divCityDropdown);
    }

    makeCityDropDown(section, btnDiv, divCityDropdown) {
        let cities = [];
        let city_ids = {};
        for (const row in this.city_rows[this.state]) {
            let item = this.city_rows[this.state][row]['market_location_city'] 
                + " (" + this.city_rows[this.state][row]['slug_id'] + ")";
            cities.push(item);
            city_ids[item] = this.city_rows[this.state][row]['slug_id'];
        }
        cities.sort();

        let cityDropdown = document.getElementById("city-dropdown");
        if (cityDropdown == null) {
            cityDropdown = document.createElement("div");
            cityDropdown.id = "city-dropdown";
            divCityDropdown.append(cityDropdown);
        }

        let selectCityDropdown = this.createSelect(cityDropdown, "City", cities, city_ids);
        
        selectCityDropdown.oninput = () => {
            this.createApplyFilterBtn(selectCityDropdown, btnDiv);
            section.append(btnDiv);
        };
    }

    makeFavorites(row) {
        let divFavDropdown = document.createElement("div");
        divFavDropdown.className = "col-4";

        let cities = [];
        let city_ids = {};
        for (const row in this.favorites) {
            let item = this.favorites[row]['city_name'] 
                + ", " + this.favorites[row]['state']
                + " (" + this.favorites[row]['slug_id'] + ")";
            cities.push(item);
            city_ids[item] = this.favorites[row]['slug_id'];
        }
        cities.sort();

        let favSection = this.createSection(row, "Favorites");
        favSection.append(divFavDropdown);
        let selectFavDropdown = this.createSelect(divFavDropdown, "", 
            cities, city_ids, "Select a favorite location");

        let divFavBtn = document.createElement("div");
        divFavBtn.className = "col-4 text-left align-self-end";
        favSection.append(divFavBtn);

        selectFavDropdown.oninput = () => {
            this.createFavRowBtns(favSection, divFavBtn);
            this.createFavViewBtn(selectFavDropdown, divFavBtn);
            this.createRemoveFavBtn(selectFavDropdown, divFavBtn);
        };
    }

    resetFilterRowBtns() {
        let viewBtn = document.getElementById("filter-view-btn");
        if(viewBtn != null)
            viewBtn.remove();
        
        let cityDropdown = document.getElementById("city-dropdown");
        if(cityDropdown != null)
            cityDropdown.remove();
    }

    resetFavRowBtns(btnDiv) {
        let viewBtn = document.getElementById("fav-view-btn");
        if(viewBtn != null)
            viewBtn.remove();
        
        let removeBtn = document.getElementById("remove-fav-btn");
        if(removeBtn != null)
            removeBtn.remove();

        if(btnDiv != null)
            btnDiv.remove();
    }

    createFavRowBtns(section, btnDiv) {
        if(btnDiv.childNodes.length > 0 || section.lastChild != btnDiv) {
            section.append(btnDiv);
        }
    }

    createApplyFilterBtn(selectSelf, btnDiv) {
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
    
        btnDiv.append(button);
    }

    createFavViewBtn(selectSelf, btnDiv) {    
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
    
        btnDiv.append(button);
    }

    createRemoveFavBtn(selectSelf, btnDiv) {
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

        button.onclick = () => {
            let options = {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "state": state,
                    "slug_id": selectedItem.value
                })
            };

            let url = "/widgets/data/remove_usda_favorites_for_account";
            fetch(url, options).then(() => {
                selectSelf.remove(selectSelf.options.selectedIndex);
                // resetting the select so the placeholder text appears and there is no selected value
                $(selectSelf).select2('val', 0);
                this.resetFavRowBtns(btnDiv);
            });
        };
    
        btnDiv.append(button);
    }
}
