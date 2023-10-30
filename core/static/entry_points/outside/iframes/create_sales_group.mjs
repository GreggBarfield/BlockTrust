import { AsyncForm } from "../../../global/async_form.mjs";
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
$("#maintenance-pvp-program").select2({data: SalesGroupFields.commonProgramNames, multiple: false});

let salesGroupForm = document.getElementById("create-sales-group-form");

let salesGroupName = document.getElementById("marketing-name");
let totalAnimals = document.getElementById("marketing-total-animals");
let zipCode = document.getElementById("marketing-zip");
let startDate = document.getElementById("marketing-start-date");
let endDate = document.getElementById("marketing-end-date");
let deliveryLocationType = document.getElementById("marketing-delivery-location-type");
let auctionMarketLocation = document.getElementById("marketing-auction-market");
let offRanchDeliveryLocation = document.getElementById("marketing-delivery-location");
let slide = document.getElementById("marketing-slide");
let weighingConditions = document.getElementById("marketing-weighing-conditions");
let representedBy = document.getElementById("marketing-represented-by");
let category = document.getElementById("characteristics-category");
let breeds = document.getElementById("characteristics-breeds");
let breedComments = document.getElementById("characteristics-breed-comments");
let baseWeight = document.getElementById("characteristics-base-weight");
let charcateristicsWeighingConditions = document.getElementById("characteristics-weighing-conditions");
let weightVariance = document.getElementById("characteristics-weight-variance")
let frame = document.getElementById("characteristics-frame");
let muscling = document.getElementById("characteristics-muscling");
let horns = document.getElementById("characteristics-horns");
let genomicTesting = document.getElementById("genetics-genomic-testing");
let epd = document.getElementById("genetics-epd");
let geneticsComments = document.getElementById("genetics-comments");
let preconPrograms = document.getElementById("maintenance-preconditioning-program");
let vaccinations = document.getElementById("maintenance-vaccinations");
let annualCattleHErdVaccinations = document.getElementById("maintenance-annual-cattle-herd-vaccinations");
let feedingProgram = document.getElementById("maintenance-feeding-program");
let implants = document.getElementById("maintenance-implants");
let castrated = document.getElementById("maintenance-castrated");
let pvpProgram = document.getElementById("maintenance-pvp-program");
let comments = document.getElementById("sales-group-comments");
let publish = document.getElementById("publish");
let showCarcassData = document.getElementById("show-carcass-data");

let statusMessage = document.getElementById("status-message");
let errorMessage = document.getElementById("error-message");
let submitButton = document.getElementById("submit-button");

deliveryLocationType.onchange = () =>{
    slide.disabled = true;
    weighingConditions.disabled = true;
    auctionMarketLocation.disabled = true;
    offRanchDeliveryLocation.disabled = true;

    slide.value = "";
    weighingConditions.value = "";
    offRanchDeliveryLocation.value = "";
    auctionMarketLocation.value = "None";
    if(deliveryLocationType.value === "Off Ranch"){
        offRanchDeliveryLocation.disabled = false;
    }
    else if(deliveryLocationType.value == "Auction"){
        auctionMarketLocation.disabled = false;
    }
    else if(deliveryLocationType.value == "Video Auction"){
        slide.disabled = false;
        weighingConditions.disabled = false;
    }
}

let getEpochTime = (dateValue) =>{
    if(dateValue === undefined || dateValue === "" || dateValue === null){
        return null
    }
    let values = dateValue.split("-");
    let d = new Date(values[0], values[1] - 1, values[2]);
    return Math.floor(d.getTime() / 1000);
}
deliveryLocationType.onchange();


let asyncForm = new AsyncForm({
    action: postRoute,
    form: salesGroupForm,
    status: statusMessage,
    error: errorMessage,
    redirectMessage: "Saved!",
    loadingMessage: "Saving...",
    asJSON: true,
    getData: () => {
        function safeInt(v) {
            if (v === "") {
                return null;
            }
            return Math.floor(parseFloat(v));
        }

        return {
            id: null,
            published: publish.checked,
            show_account_carcass_data: showCarcassData.checked,
            eids: [],
            reported: {
                comments: comments.value,
                count: safeInt(totalAnimals.value),
                weight: safeInt(baseWeight.value),
                weight_variance: weightVariance.value,
                breeds: $(breeds).val(),
                horns: horns.value,
                muscling: muscling.value,
                usda_frame_size: frame.value,
                preconditioning_program: preconPrograms.value,
                vaccinations: $(vaccinations).val(),
                feeding_programs: $(feedingProgram).val(),
                implants: $(implants).val(),
                castrated: castrated.value,
                process_verified_program: pvpProgram.value,
                images: [],
                videos: [],
                marketing_slide: slide.value,
                marketing_weighing_conditions: weighingConditions.value,
                marketing_represented_by: representedBy.value,
                genomic_testing: genomicTesting.value,
                epd: epd.value,
                genetics_comments: geneticsComments.value
            },
            "delivery_location_type": deliveryLocationType.value,
            "delivery_location": offRanchDeliveryLocation.value,
            "zip": parseInt(zipCode.value),
            "start": getEpochTime(startDate.value),
            "end": getEpochTime(endDate.value),
            "group_name": salesGroupName.value,
            "price": 0, //marketingPrice.value,
            "auction_market_location": auctionMarketLocation.value,
            "category": category.value,
            "breed_comments": breedComments.value,
            "weighing_conditions": charcateristicsWeighingConditions.value,
            "are_annual_cattle_herd_vaccinations_given": annualCattleHErdVaccinations.value=="Yes"?1:0,
            //TODO: Removed auction_sale for now. Retained incase needed in future.
            //auction_sale: marketingAuctionSale.getID()
            auction_sale: null                   
        }
    }
});

submitButton.addEventListener("click", () => {
    asyncForm.submit();
})