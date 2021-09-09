import { ProgressBar } from '../../../core/progress_bar.mjs';
import { BasicFileEditor } from '../../../files/basic_file_editor.mjs';
import { Widget } from '../../widget.mjs';
import { SalesGroupViewer } from '../../../sales_groups/view_sales_group.mjs';

export class ArchivedSalesGroupWidget extends Widget {
    constructor(frame) {
        super(frame);
    }
    initType() {
        // TODO: This is a bad data request, optimize later
        this.account = parseInt(this.frame.getAttribute("data-widget-account"));
        this.getData(
            "achived_sales_group",
            {
                search: {
                    "type": "Account ID",
                    "params": {
                        "ID": this.account
                    },
                    "or": null,
                    "and": null
                }
            }
        ).then((data) => {
            this.sales_groups = data.sales_groups;
            this.displaySalesGroups();
        });


        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });

    }
    displaySalesGroups(){
        for( const sales_group in this.sales_groups){
            this.salesGroupViewer = new SalesGroupViewer(this.sales_groups[sales_group], this.frame);
        }
        
    }
}
