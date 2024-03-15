import { printContainer } from "../../../js/widgets/utilities/general_utilities.mjs";
import { SalesGroupViewer } from "../../../js/sales_groups/view_sales_group.mjs";

let elements = document.getElementsByName("sale-date");
for (let element of elements){
    element.innerText = new Date(element.innerText*1000).toLocaleString("en-US", {
        year:"numeric",
        month:"long",
        day:"numeric"
    });
}

window.printSalesGroup = (salesGroupId) =>{
    let salesGroup = {};
    for(let group of salesGroups){
        if(group.id == parseInt(salesGroupId)){
            salesGroup = group;
        }
    }
    const salesGroupViewerContainer = document.createElement("div");
    new SalesGroupViewer(salesGroup, salesGroupViewerContainer);

    let tempWindowForPrint = window.open('', '', 'width=1100,height=900');
    let breakLine = "<hr style='height:2px;background:black'/>";
    tempWindowForPrint.document.write('<html><head><link rel="stylesheet" href="/static/build/build_dashboard_main.min.css"/><link rel="stylesheet" href="/static/css/dashboard/flashable/flash_able_old/plugins/bootstrap/css/bootstrap.min.css"/></head><body>');
    tempWindowForPrint.document.write(breakLine);
    tempWindowForPrint.document.write(salesGroupViewerContainer);
    tempWindowForPrint.document.write(breakLine);
    tempWindowForPrint.document.write('</body></html>');
    tempWindowForPrint.document.close();
    tempWindowForPrint.focus();
    tempWindowForPrint.addEventListener("load", (e)=>{
        tempWindowForPrint.print();
    })

}

window.downloadSalesGroupsDetailedReport = () =>{
    let tableHeaders = ["ID", "SALES GROUP NAME", "SALE DATE", "ACCOUNT", "PUBLISHED", "DELIVERY TYPE", "DELIVERY LOCATION", "PRICE", "CATEGORY", 
    "EPD", "COUNT", "HORNS", "BREEDS", "WEANED", "BASE WEIGHT", "WEIGHT VARIANCE", "WEIGHING CONDITIONS", "PVP PROGRAM", "IMPLANTS", 
    "MUSCLING", "CASTRATED", "CREEP FEED", "VACCINATIONS", "VERFIFICATION", "GENOMIC TESTING", "MARKETING SLIDE", "USDA FRAME SIZE",
    "COMINGLED STATUS", "FEEDING PROGRAMS", "PREGNANCY STATUS", "CERTIFIED THROUGH", "EXPECTED SHIP DATE", "PRECON PROGRAM",
    "REPRESENTED BY", "BREED PROGRAM CERTIFICATION COMPANY", "MARKETING COMMENTS", "CHARACTERISTICS COMMENTS", "MAINTENANCE COMMENTS", 
    "GENETICS COMMENTS", "PROGRAM COMMENTS", "COMMENTS"];
    let salesGroupsdDataTableExport = [];
    salesGroupsdDataTableExport.push([tableHeaders]);
    salesGroupsdDataTableExport.push([]);

    for(let salesGroup of salesGroups){
        let salesGroupRow = [];
        salesGroupRow.push(
            salesGroup.id,
            salesGroup.group_name,
            new Date(salesGroup.sale_date*1000).toDateString(),
            salesGroup.account,
            salesGroup.published == 1 ? "Yes": "No",
            salesGroup.delivery_location_type,
            salesGroup.delivery_location,
            salesGroup.price,
            salesGroup.category,
            salesGroup.reported.epd ? salesGroup.reported.epd : "N/A",
            salesGroup.reported.count ? salesGroup.reported.count : "N/A",
            salesGroup.reported.horns ? salesGroup.reported.horns : "N/A",
            salesGroup.reported.breeds ? salesGroup.reported.breeds.join("/"): "N/A",
            salesGroup.reported.weaned ? salesGroup.reported.weaned : "N/A",
            salesGroup.reported.weight ? salesGroup.reported.weight : "N/A",
            salesGroup.reported.weight_variance ? salesGroup.reported.weight_variance : "N/A",
            salesGroup.reported.marketing_weighing_conditions ? salesGroup.reported.marketing_weighing_conditions : "N/A",
            salesGroup.reported.program ? salesGroup.reported.program : "N/A",
            salesGroup.reported.implants ? salesGroup.reported.implants.join("/"): "N/A",
            salesGroup.reported.muscling ? salesGroup.reported.muscling : "N/A",
            salesGroup.reported.castrated ? salesGroup.reported.castrated : "N/A",
            salesGroup.reported.creep_feed ? salesGroup.reported.creep_feed : "N/A",
            salesGroup.reported.vaccinations ? salesGroup.reported.vaccinations.join("/"): "N/A",
            salesGroup.reported.verification ? salesGroup.reported.verification : "N/A",
            salesGroup.reported.genomic_testing ? salesGroup.reported.genomic_testing : "N/A",
            salesGroup.reported.marketing_slide ? salesGroup.reported.marketing_slide : "N/A",
            salesGroup.reported.usda_frame_size ? salesGroup.reported.usda_frame_size : "N/A",
            salesGroup.reported.comingled_status ? salesGroup.reported.comingled_status : "N/A",
            salesGroup.reported.feeding_programs ? salesGroup.reported.feeding_programs.join("/") : "N/A",
            salesGroup.reported.pregnancy_status ? salesGroup.reported.pregnancy_status : "N/A",
            salesGroup.reported.certified_through ? salesGroup.reported.certified_through : "N/A",
            salesGroup.reported.expected_Ship_date ? salesGroup.reported.expected_Ship_date : "N/A",
            salesGroup.reported.preconditioning_program ? salesGroup.reported.preconditioning_program : "N/A",
            salesGroup.reported.marketing_represented_by ? salesGroup.reported.marketing_represented_by : "N/A",
            salesGroup.reported.breed_program_certification_co ? salesGroup.reported.breed_program_certification_co : "N/A",
            salesGroup.reported.marketing_comments ? salesGroup.reported.marketing_comments : "N/A",
            salesGroup.reported.characteristics_comments ? salesGroup.reported.characteristics_comments : "N/A",
            salesGroup.reported.maintenance_comments ? salesGroup.reported.maintenance_comments : "N/A",
            salesGroup.reported.genetics_comments ? salesGroup.reported.genetics_comments : "N/A",
            salesGroup.reported.program_comments ? salesGroup.reported.program_comments : "N/A",
            salesGroup.reported.comments ? salesGroup.reported.comments : "N/A"
        )
        salesGroupsdDataTableExport.push(salesGroupRow);
    }
    let csvContent =  salesGroupsdDataTableExport.map(e => e.join(",")).join("\n");
        let encoded = encodeURIComponent(csvContent);
        let downloadElement = document.createElement('a');
        downloadElement.href = 'data:text/csv;charset=utf-8,' + encoded;
        downloadElement.target = '_blank';
        downloadElement.download = "SalesGroupsDetailedReport"+ new Date().toDateString() +".csv";
        downloadElement.click();
}

window.downloadSalesGroupsSummaryReport = () =>{
    let tableHeaders = ["NAME", "NO. OF HEAD", "CATEGORY/SEX", "BREED", "WEIGHT", "MARKET NAME/LOCATION", "SALE DATE"];
    let salesGroupsdDataTableExport = [];
    salesGroupsdDataTableExport.push([tableHeaders]);
    salesGroupsdDataTableExport.push([]);

    for(let salesGroup of salesGroups){
        let salesGroupRow = [];
        salesGroupRow.push(
            salesGroup.group_name,
            salesGroup.reported.count ? salesGroup.reported.count : "N/A",
            salesGroup.category,
            salesGroup.reported.breeds ? salesGroup.reported.breeds.join("/"): "N/A",
            salesGroup.reported.weight ? salesGroup.reported.weight : "N/A",
            salesGroup.delivery_location.replaceAll(",", " "),
            new Date(salesGroup.sale_date*1000).toDateString()
        )
        salesGroupsdDataTableExport.push(salesGroupRow);
    }
    let csvContent =  salesGroupsdDataTableExport.map(e => e.join(",")).join("\n");
        let encoded = encodeURIComponent(csvContent);
        let downloadElement = document.createElement('a');
        downloadElement.href = 'data:text/csv;charset=utf-8,' + encoded;
        downloadElement.target = '_blank';
        downloadElement.download = "SalesGroupsSummaryReport"+ new Date().toDateString() +".csv";
        downloadElement.click();
}

document.addEventListener('DOMContentLoaded', function () {
    let salesGroupsTable = $('#sales-groups-table').DataTable({pageLength:50});
    let dateInput = document.createElement("input");
    dateInput.type = "date";
    dateInput.className = "form-control form-control-sm";
    $('#sales-groups-table_wrapper .dataTables_filter').append(dateInput);
    dateInput.onchange = () =>{
        if(dateInput.value == ""){
            salesGroupsTable.columns().search('').draw();
        }
        else{
            let formattedDate = dateInput.value.split('-');
            let dateInputText = new Date(formattedDate[0], formattedDate[1]-1, formattedDate[2]).toLocaleString("en-US", {
            year:"numeric",
            month:"long",
            day:"numeric"
        });
        salesGroupsTable.columns(4).search(dateInputText).draw();
        }
    }
    let resetFiltersButton = document.createElement("button");
    resetFiltersButton.className = "btn btn-sm btn-primary m-1 p-1";
    resetFiltersButton.textContent = "Reset Filters";
    resetFiltersButton.onclick = () =>{
        dateInput.value = "";
        salesGroupsTable.columns().search('').draw();
    }
    $('#sales-groups-table_wrapper .dataTables_filter').append(resetFiltersButton);
});
