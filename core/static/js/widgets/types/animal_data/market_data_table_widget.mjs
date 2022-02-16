import { Widget } from '../../widget.mjs';

export class MarketDataTableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.slug_id = this.frame.getAttribute('slug_id');
        this.state = this.frame.getAttribute('state');

        this.getData(
            "get_usda_favorites",
            {}
        ).then((data) => {
            this.isFavorite = false;
            this.favorite = null;

            for (const item of data.favorites) {
                if(item.city_id == this.slug_id) {
                    this.isFavorite = true;
                    this.favorite = item;
                }
            }
            this.makeFavoriteBtn();
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

        this.getData(
            "get_market_data/" + this.slug_id,
            {}
        ).then((data) => {
            this.match_rows = data.market_data;
            this.makeTable();
        });
    }

    makeFavoriteBtn() {
        let btnDiv = document.createElement("div");
        let button = document.createElement("a");
        button.id = "add-fav-btn";
        button.className = "btn btn-primary btn-sm text-white mb-3";
        button.style = "cursor: pointer";
        if(this.isFavorite){
            button.textContent = "Remove from favorites";
        } else {
            button.textContent = "Add to favorites";
        }

        button.addEventListener("click", () => this.favoriteBtnOnClickHandler());

        btnDiv.appendChild(button);
        this.frame.appendChild(btnDiv);
    }

    favoriteBtnOnClickHandler() {
        let handle = null;
        let requestData = null;
        let btnText = null;

        if(this.isFavorite) {
            handle = "remove_usda_favorite";
            requestData = {
                "state": this.state,
                "city_id": this.slug_id
            };
            btnText = "Add to favorites";
            this.isFavorite = false;
        } else {
            handle = "save_usda_favorite";
            requestData = {
                "state": this.state,
                "city_id": this.slug_id
            };
            btnText = "Remove from favorites";
            this.isFavorite = true;
        }

        $.ajax({
            url: "/widgets/data/" + handle,
            data: JSON.stringify(requestData),
            contentType: 'application/json',
            method: "POST"
        }).then(()=>{
            let button = document.getElementById("add-fav-btn");
            button.textContent = btnText;
        });
    }

    makeTable() {
        this.divTableResponsive = document.createElement("div");
        this.divTableResponsive.className = "dt-responsive table-responsive";

        this.mainTable = document.createElement("table");
        this.mainTable.className = "table table-striped table-bordered nowrap";
        this.divTableResponsive.appendChild(this.mainTable);

        // Header
        this.mainTableHead = document.createElement("thead");
        this.mainTable.appendChild(this.mainTableHead);

        this.mainTableHeadRow0 = document.createElement("tr");
        this.mainTableHead.appendChild(this.mainTableHeadRow0);
        const headers = Object.keys(this.match_rows[0]);
        for (const headerText of headers) {
            let th = document.createElement("th");
            th.textContent = headerText;
            this.mainTableHeadRow0.appendChild(th);
        }

        // Body
        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        for (const row in this.match_rows) {
            let rowTag = document.createElement("tr");
            this.mainTableBody.appendChild(rowTag);

            for (const item in this.match_rows[row]) {
                let td = document.createElement("td");
                rowTag.append(td);
                if (item.includes('price') && this.match_rows[row][item] != null){
                    td.textContent = '$' + this.match_rows[row][item];
                } else {
                    td.textContent = this.match_rows[row][item];
                }
            }
        }

        // Put HTML in frame
        this.frame.appendChild(this.divTableResponsive);
        $(this.mainTable).DataTable();
    }
}