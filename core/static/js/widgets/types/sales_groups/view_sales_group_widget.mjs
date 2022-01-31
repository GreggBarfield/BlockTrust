import { Widget } from '../../widget.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';
import { PrintFlyerButton } from '../../../sales_groups/create_sales_group_flyer.mjs';

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
            }
        ).then((data) => {
            this.sales_group = data;
            this.printFlyerButton = PrintFlyerButton(data);
            this.frame.appendChild(this.printFlyerButton);
            this.displaySalesGroup();
        });


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

    }

    displaySalesGroup() {
        this.salesGroupViewer = new SalesGroupViewer(this.sales_group, this.frame);
    }
}