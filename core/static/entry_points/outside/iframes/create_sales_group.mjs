import { SalesGroupFields } from "../../../js/sales_groups/sales_group_fields.mjs";

let auctionMarketsList = []
auctionMarketsList.push("None")
for(let auctionMarket of auctionMarkets){
    let optionText = auctionMarket.name+", "+auctionMarket.city+", "+auctionMarket.state;
    auctionMarketsList.push(optionText);
}

$("#marketing-delivery-location-type").select2({data: SalesGroupFields.commonDeliveryLocationTypes, multiple: false});
$("#marketing-auction-market").select2({data: auctionMarketsList, multiple: false});
$("#characteristics-category").select2({data: SalesGroupFields.commonCategoryNames, multiple: false});
$("#characteristics-breeds").select2({data: SalesGroupFields.commonBreedNames, multiple: true, placeholder: "Select Applicable Breeds"});
$("#characteristics-frame").select2({data: SalesGroupFields.commonFrames, multiple: false});
$("#characteristics-muscling").select2({data: SalesGroupFields.commonMusclings, multiple: false});
$("#characteristics-horns").select2({data: SalesGroupFields.commonHorns, multiple: false});
$("#genetics-genomic-testing").select2({data: ["Yes", "No"], multiple: false});
$("#genetics-epd").select2({data: ["Yes", "No"], multiple: false});
$("#maintenance-preconditioning-program").select2({data: SalesGroupFields.commonPreconditioningProgramNames, multiple: false});
$("#maintenance-vaccinations").select2({data: SalesGroupFields.commonVaccinations, multiple: true, placeholder: "Select Vaccinations"});
$("#maintenance-annual-cattle-herd-vaccinations").select2({data: ["Yes", "No"], multiple: false});
$("#maintenance-feeding-program").select2({data: SalesGroupFields.commonFeedingPrograms, multiple: true, placeholder: "Select Feeding Programs"});
$("#maintenance-implants").select2({data: SalesGroupFields.commonImplants, multiple: true, placeholder: "Select Implants"});
$("#maintenance-castrated").select2({data: SalesGroupFields.commonCastrated, multiple: false});
$("#maintenance-pvp-program").select2({data: SalesGroupFields.commonPVPProgramNames, multiple: false});

// TO-DO: Create a method to submit the form and authenticate account submitting the sales group
// let salesGroupForm = $("#create-sales-group-form");