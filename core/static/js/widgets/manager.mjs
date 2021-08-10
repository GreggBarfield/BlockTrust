import { TableWidget } from './types/animal_data/table_widget.mjs';
import { MapWidget } from './types/animal_data/map_widget.mjs';
import { DataTableWidget } from './types/animal_data/data_table_widget.mjs';
import { GradeWidget } from './types/animal_data/grade_widget.mjs';
import { TimelineWidget } from './types/animal_data/timeline_widget.mjs';
import { HealthTableWidget } from './types/animal_data/health_table_widget.mjs';
import { SectorsWidget } from './types/animal_data/sectors_widget.mjs';
import { SourceSummaryWidget } from './types/animal_data/source_summary_widget.mjs';
import { EditSalesGroupWidget } from './types/sales_groups/edit_sales_group_widget.mjs';
import { ViewSalesGroupWidget } from './types/sales_groups/view_sales_group_widget.mjs';
import { AccountSalesGroupsWidget } from './types/sales_groups/account_sales_groups_widget.mjs';
import { SearchSalesGroupsWidget } from './types/sales_groups/search_sales_groups_widget.mjs';
import { MessagesListWidget } from './types/messages/messages_list_widget.mjs';
import { ManageAuctionSalesWidget } from './types/auction_sales/manage_auction_sales_widget.mjs';
import { ViewUpcomingAuctionsWidget } from './types/auction_sales/view_upcoming_auctions_widget.mjs';
import { MatchVisibilitySettingsWidget } from './types/manage_matches_data/match_visibility_settings_widget.mjs';
import { SearchEIDsWidget } from './types/animal_data/search_eids_widget.mjs';
import { InfoModal } from '../core/info_modal.mjs';
import { PlansWidget } from './types/stripe/plans.mjs';
import { SubscribeWidget } from './types/stripe/subscribe.mjs';
// import { SustainabilityQuestionaireWidget } from "./types/sustainability/sustainability_questionaire.mjs";
import { CertificatesWidget } from "./types/animal_data/certificates_widget.mjs";
import { SustainabilityQuestionaireWidget } from "./types/sustainability/sustainability_questionaire.mjs";


// Immediately invoked
(function () {

    let widgets = [];

    let attachTable = {};

    function attach(symbol, widget) {
        if (symbol in attachTable) {
            throw "Symbol duplication in widget attach table: " + symbol;
        }
        attachTable[symbol] = widget;
    }

    attach("map", MapWidget);
    attach("table", TableWidget);
    attach("data table", DataTableWidget);
    attach("grade", GradeWidget);
    attach("timeline", TimelineWidget);
    attach("health table", HealthTableWidget);
    attach("edit sales group", EditSalesGroupWidget);
    attach("sectors", SectorsWidget);
    attach("account sales groups", AccountSalesGroupsWidget);
    attach("view sales group", ViewSalesGroupWidget);
    attach("search sales groups", SearchSalesGroupsWidget);
    attach("messages list", MessagesListWidget);
    attach("manage auction sales", ManageAuctionSalesWidget);
    attach("view upcoming auction sales", ViewUpcomingAuctionsWidget);
    attach("match visibility settings", MatchVisibilitySettingsWidget);
    attach("source summary", SourceSummaryWidget);
    attach("plans", PlansWidget);
    attach("subscribe", SubscribeWidget);
    // attach("sustainability questionaire", SustainabilityQuestionaireWidget);
    attach("certificates", CertificatesWidget);
    attach("sustainability questionaire", SustainabilityQuestionaireWidget);

    // Find widgets
    $(".widget").each(function () {
        let widgetType = $(this).attr("data-widget-type");
        let w = null;

        if (widgetType in attachTable) {
            w = new attachTable[widgetType](this);
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

    $("#icon-search").click(() => {
        let infoModal = new InfoModal("Search By EID");
        let widget = new SearchEIDsWidget(infoModal.getBody(), infoModal.getFooter());
        widget.init(); // TODO: Fix (This will break in the future when networking is optimized)
    });

})()