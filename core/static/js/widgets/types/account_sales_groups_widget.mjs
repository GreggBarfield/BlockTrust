import { Widget } from '../widget.mjs';
import { Table } from '../../core/table.mjs';

export class AccountSalesGroupsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.account = parseInt(this.frame.getAttribute("data-widget-account"));

        // TODO: This is a bad data request, optimize later
        this.getData(
            "search_sales_groups",
            {
                search: {
                    "type": "Account ID",
                    "params": {
                        "ID": this.account
                    },
                    "or": null,
                    "and": null
                },
                file_auths: false
            },
            (data) => {
                this.sales_groups = data.sales_groups;
                this.displaySalesGroups();
            }
        );


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

    }

    displaySalesGroups() {
        this.table = new Table();

        this.table.setHeader(["ID", "Name", "Published", "Options"]);

        for (const salesGroup of this.sales_groups) {
            let optionsGroup = document.createElement("div");
            let optionView = document.createElement("a");
            optionView.className = "btn btn-sm btn-info";
            optionView.type = "button";
            optionView.textContent = "View";
            optionView.style.color = "white";
            optionView.href = "/dashboard/sales-groups/view/" + salesGroup.id;
            optionsGroup.append(optionView);
            let optionsEdit = document.createElement("a");
            optionsEdit.className = "btn btn-sm btn-info";
            optionsEdit.type = "button";
            optionsEdit.textContent = "Edit";
            optionsEdit.style.color = "white";
            optionsEdit.href = "/dashboard/sales-groups/edit/" + salesGroup.id;
            optionsGroup.append(optionsEdit);
            this.table.addRow([salesGroup.id, salesGroup.name, salesGroup.published ? "Yes" : "No", optionsGroup]);
        }

        this.table.attach(this.frame);

        if (this.sales_groups.length == 0) {
            let centerText = document.createElement("div");
            centerText.style.textAlign = "center";
            centerText.textContent = "No sales groups owned by this account";
            this.frame.append(centerText);
        }
    }
}