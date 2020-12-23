import { TableWidget } from './types/animal_data/table_widget.mjs';
import { MapWidget } from './types/animal_data/map_widget.mjs';
import { DataTableWidget } from './types/animal_data/data_table_widget.mjs';
import { GradeWidget } from './types/animal_data/grade_widget.mjs';
import { TimelineWidget } from './types/animal_data/timeline_widget.mjs';
import { HealthTableWidget } from './types/animal_data/health_table_widget.mjs';
import { SectorsWidget } from './types/animal_data/sectors_widget.mjs';
import { EditSalesGroupWidget } from './types/sales_groups/edit_sales_group_widget.mjs';
import { ViewSalesGroupWidget } from './types/sales_groups/view_sales_group_widget.mjs';
import { AccountSalesGroupsWidget } from './types/sales_groups/account_sales_groups_widget.mjs';
import { SearchSalesGroupsWidget } from './types/sales_groups/search_sales_groups_widget.mjs';
import { MessagesListWidget } from './types/messages/messages_list_widget.mjs';


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
        else if (widgetType == "messages list") {
            w = new MessagesListWidget(this);
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