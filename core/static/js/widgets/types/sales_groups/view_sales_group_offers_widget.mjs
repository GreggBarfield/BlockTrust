import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class ViewSalesGroupOffersWidget extends Widget{
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.salesGroupID = parseInt(this.frame.getAttribute("data-widget-sales-group"));
        this.getData(
            "get_sales_groups_offers",
            {
                sales_group_id: this.salesGroupID
            }
        ).then((data) => {
            this.data = data;
            console.log(this.data);
            //this.makeForm();
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });
    }
}