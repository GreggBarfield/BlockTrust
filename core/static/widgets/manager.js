import { TableWidget } from './types/table_widget.mjs';
import { MapWidget } from './types/map_widget.mjs';
import { DataTableWidget } from './types/data_table_widget.mjs';
import { GradeWidget } from './types/grade_widget.mjs';
import { TimelineWidget } from './types/timeline_widget.mjs';
import { HealthTableWidget } from './types/health_table_widget.mjs';
import { SectorsWidget } from './types/sectors_widget.mjs';
import { EditSalesGroupWidget } from './types/edit_sales_group_widget.mjs';
import { ViewSalesGroupWidget } from './types/view_sales_group_widget.mjs';
import { AccountSalesGroupsWidget } from './types/account_sales_groups_widget.mjs';
import { SearchSalesGroupsWidget } from './types/search_sales_groups_widget.mjs';


// Immediately invoked
(function () {

    let widgets = [];

    // Find widgets
    $(".widget").each(function () {
        let widgetType = $(this).attr("data-widget-type");
        let w = null;
        if (widgetType == "map") {
            w = new MapWidget(this);
        }
        else if (widgetType == "table") {
            w = new TableWidget(this);
        }
        else if (widgetType == "data table") {
            w = new DataTableWidget(this);
        }
        else if (widgetType == "grade") {
            w = new GradeWidget(this);
        }
        else if (widgetType == "timeline") {
            w = new TimelineWidget(this);
        }
        else if (widgetType == "health table") {
            w = new HealthTableWidget(this);
        }
        else if (widgetType == "edit sales group") {
            w = new EditSalesGroupWidget(this);
        }
        else if (widgetType == "sectors") {
            w = new SectorsWidget(this);
        }
        else if (widgetType == "account sales groups") {
            w = new AccountSalesGroupsWidget(this);
        }
        else if (widgetType == "view sales group") {
            w = new ViewSalesGroupWidget(this);
        }
        else if (widgetType == "search sales groups") {
            w = new SearchSalesGroupsWidget(this);
        }

        if (w === null) {
            console.log("Widget could not be loaded: " + widgetType);
        }
        else {
            widgets.push(w);
        }
    });

    // Init widgets later so that loading symbols can be displayed while everything initializes
    $(function () {
        for (let widget of widgets) {
            widget.init();
        }
    })

})()