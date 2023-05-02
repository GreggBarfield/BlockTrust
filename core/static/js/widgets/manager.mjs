import { TableWidget } from './types/animal_data/table_widget.mjs';
import { MapWidget } from './types/animal_data/map_widget.mjs';
import { GradeWidget } from './types/animal_data/grade_widget.mjs';
import { TimelineWidget } from './types/animal_data/timeline_widget.mjs';
import { HealthTableWidget } from './types/animal_data/health_table_widget.mjs';
import { SectorsWidget } from './types/animal_data/sectors_widget.mjs';
import { SourceSummaryWidget } from './types/animal_data/source_summary_widget.mjs';
import { EditSalesGroupWidget } from './types/sales_groups/edit_sales_group_widget.mjs';
import { ViewSalesGroupWidget } from './types/sales_groups/view_sales_group_widget.mjs';
import { AccountSalesGroupsWidget } from './types/sales_groups/account_sales_groups_widget.mjs';
import { CreateSalesGroupWidget } from './types/sales_groups/create_sales_group_widget.mjs';
import { SearchSalesGroupsWidget } from './types/sales_groups/search_sales_groups_widget.mjs';
import { MessagesListWidget } from './types/messages/messages_list_widget.mjs';
import { ManageAuctionSalesWidget } from './types/auction_sales/manage_auction_sales_widget.mjs';
import { ViewUpcomingAuctionsWidget } from './types/auction_sales/view_upcoming_auctions_widget.mjs';
import { MatchVisibilitySettingsWidget } from './types/manage_matches_data/match_visibility_settings_widget.mjs';
import { SearchEIDsWidget } from './types/animal_data/search_eids_widget.mjs';
import { InfoModal } from '../core/info_modal.mjs';
import { PlansWidget } from './types/stripe/plans.mjs';
import { SubscribeWidget } from './types/stripe/subscribe.mjs';
import { CertificatesWidget } from "./types/animal_data/certificates_widget.mjs";
import { MarketDataTableWidget } from './types/animal_data/market_data_table_widget.mjs';
import { MarketDataFilterWidget } from './types/animal_data/market_data_filter_widget.mjs';
import { ManageSalesGroupEIDsWidget } from './types/sales_groups/manage_sales_group_eids_widget.mjs';
import { ArchivedSalesGroupWidget } from './types/sales_groups/archived_sales_group.mjs';
import { SummaryGraphWidget } from './types/employee/summary_graphs.mjs';
import { TagDistributionSectorAtAccountWidget } from './types/animal_data/tag_distribution_sector_at_account_widget.mjs';
import { SelectEIDsByGroupingIDWidget } from './types/sales_groups/select_eids_by_grouping_id_widget.mjs';
import { AddConnectionsWidget } from './types/connections/add_connections_widget.mjs'
import { CowCalfQuestionnaireV2Widget } from "./types/sustainability/cow_calf_questionnaire_v2_widget.mjs"
import { AuctionHouseQuestionnaireV2Widget } from "./types/sustainability/auction_house_questionnaire_v2_widget.mjs"
import { FeedlotQuestionnaireV2Widget } from "./types/sustainability/feedlot_questionnaire_v2_widget.mjs"
import { StockerBackgrounderQuestionnaireV2Widget } from "./types/sustainability/stocker_backgrounder_questionnaire_v2_widget.mjs"
import { PackerQuestionnaireV2Widget } from "./types/sustainability/packer_questionnaire_v2_widget.mjs"
import { SustainabilityTimelineV2Widget } from "./types/sustainability/sustainability_timeline_v2_widget.mjs"
import { SustainabilitySummaryWidget } from './types/sustainability/sustainability_summary.mjs';
import { EPDTableWidget } from './types/animal_data/epd_table_widget.mjs';
import { EditAccountRetailDataWidget } from './types/edit_account/edit_account_retail_data_widget.mjs';
import { AccountSustainabilityScores } from './types/sustainability/view_account_sustainability_scores.mjs';
import { TagStoreWidget } from './types/tag-store/tag-store.mjs';
import { MarketPlaceWidget } from './types/marketplace/marketplace.mjs';
import { PartnerCountDistributionWidget } from './types/animal_data/partner_count_distribution.mjs';
import { CheckoutWidget } from './types/tag-store/checkout.mjs';
import { ShoppingCartWidget } from './types/tag-store/shopping-cart.mjs';
import { InvoiceWidget } from './types/tag-store/invoice.mjs';


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
    attach("grade", GradeWidget);
    attach("timeline", TimelineWidget);
    attach("health table", HealthTableWidget);
    attach("edit sales group", EditSalesGroupWidget);
    attach("sectors", SectorsWidget);
    attach("account sales groups", AccountSalesGroupsWidget);
    attach("create sales group", CreateSalesGroupWidget);
    attach("view sales group", ViewSalesGroupWidget);
    attach("search sales groups", SearchSalesGroupsWidget);
    attach("messages list", MessagesListWidget);
    attach("manage auction sales", ManageAuctionSalesWidget);
    attach("view upcoming auction sales", ViewUpcomingAuctionsWidget);
    attach("match visibility settings", MatchVisibilitySettingsWidget);
    attach("source summary", SourceSummaryWidget);
    attach("plans", PlansWidget);
    attach("subscribe", SubscribeWidget);
    attach("certificates", CertificatesWidget);
    attach("market data table", MarketDataTableWidget);
    attach("market data filter table", MarketDataFilterWidget);
    attach("manage sales group eids", ManageSalesGroupEIDsWidget)
    attach("archive sales group", ArchivedSalesGroupWidget);
    attach("summary graphs", SummaryGraphWidget);
    attach("tag distribution sector at account", TagDistributionSectorAtAccountWidget);
    attach("select eids by grouping id",SelectEIDsByGroupingIDWidget)
    attach("add connections", AddConnectionsWidget);
    attach("cow-calf questionnaire v2", CowCalfQuestionnaireV2Widget);
    attach("auction house questionnaire v2", AuctionHouseQuestionnaireV2Widget);
    attach("feedlot questionnaire v2", FeedlotQuestionnaireV2Widget);
    attach("stocker/backgrounder questionnaire v2", StockerBackgrounderQuestionnaireV2Widget);
    attach("packer questionnaire v2", PackerQuestionnaireV2Widget);
    attach("sustainability timeline v2", SustainabilityTimelineV2Widget);
    attach("sustainability summary", SustainabilitySummaryWidget);
    attach("epd table", EPDTableWidget);
    attach("edit account retail data", EditAccountRetailDataWidget);
    attach("account sustainability scores", AccountSustainabilityScores);
    attach("tag store", TagStoreWidget);
    attach("marketplace", MarketPlaceWidget);
    attach("partner count distribution", PartnerCountDistributionWidget);
    attach("checkout", CheckoutWidget);
    attach("shopping cart", ShoppingCartWidget);
    attach("invoice", InvoiceWidget);

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
        let widget = new SearchEIDsWidget(infoModal.getBody(), infoModal.getFooter(), "search_by_eid_and_visual_id_for_account");
        widget.init(); // TODO: Fix (This will break in the future when networking is optimized)
    });

    $("#eid-search").click(() => {
        let infoModal = new InfoModal("Search By EID");
        let widget = new SearchEIDsWidget(infoModal.getBody(), infoModal.getFooter(), "search_by_eid_and_visual_id");
        widget.init();
    });

})()