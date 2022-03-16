import { Widget } from '../../widget.mjs';

export class MarketDataTableWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.slug_id = this.frame.getAttribute('slug_id');
        this.state = this.frame.getAttribute('state');

        Promise.all([
            this.getData(
                "get_usda_favorites_for_account",
                {}
            ).then((data) => {
                this.isFavorite = false;
                this.favorite = null;
    
                for (const item of data.favorites) {
                    if(item.slug_id == this.slug_id) {
                        this.isFavorite = true;
                        this.favorite = item;
                    }
                }
            }),

            this.getData(
                "get_market_data/" + this.slug_id,
                {}
            ).then((data) => {
                this.match_rows = data.market_data;
            })

        ]).then(() => {
            this.frame.innerHTML = "";
            this.makeFavoriteBtn();
            this.makeTable();
        });
    }

    makeFavoriteBtn() {
        let btnDiv = document.createElement("div");
        let button = document.createElement("a");
        button.id = "fav-btn";
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
            handle = "remove_usda_favorites_for_account";
            requestData = {
                "state": this.state,
                "slug_id": this.slug_id
            };
            btnText = "Add to favorites";
            this.isFavorite = false;
        } else {
            handle = "save_usda_favorites_for_account";
            requestData = {
                "state": this.state,
                "slug_id": this.slug_id
            };
            btnText = "Remove from favorites";
            this.isFavorite = true;
        }

        let options = {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        };

        fetch("/widgets/data/" + handle, options).then(() => {
            let button = document.getElementById("fav-btn");
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
            if (!headerText.includes("office")){
                let th = document.createElement("th");
                th.textContent = headerText;
                this.mainTableHeadRow0.appendChild(th);
            }
        }

        // Body
        this.mainTableBody = document.createElement("tbody");
        this.mainTable.appendChild(this.mainTableBody);

        for (const row in this.match_rows) {
            let rowTag = document.createElement("tr");
            this.mainTableBody.appendChild(rowTag);

            for (const item in this.match_rows[row]) {
                if (!item.includes("office")){
                    let td = document.createElement("td");
                    rowTag.append(td);
                    if (item.includes('price') && this.match_rows[row][item] != null){
                        td.textContent = '$' + this.match_rows[row][item];
                    } else {
                        td.textContent = this.match_rows[row][item];
                    }
                }
            }
        }

        // Put HTML in frame
        this.frame.appendChild(this.divTableResponsive);
        $(this.mainTable).DataTable();
    }
}