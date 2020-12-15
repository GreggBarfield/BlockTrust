import { Widget } from '../widget.mjs';
import { SalesGroupViewer } from '../../js/sales_groups/view_sales_group.mjs';

export class ViewSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));

        // TODO: This is a bad data request, optimize later
        this.getData(
            "sales_group",
            {
                "sales_group": this.salesGroupID
            },
            (data) => {
                this.sales_group = data;
                this.displaySalesGroup();
            }
        );


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

    }

    displaySalesGroup() {
        this.salesGroupViewer = new SalesGroupViewer(this.sales_group, this.frame);
    }
}