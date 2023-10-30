import { AsyncForm } from "../../../global/async_form.mjs";
import { SalesGroupFields } from "../../../js/sales_groups/sales_group_fields.mjs";

let auctionMarketsList = [];
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
let annualCattleHerdVaccinations = document.getElementById("maintenance-annual-cattle-herd-vaccinations");
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
deliveryLocationType.onchange();

let getEpochTime = (dateValue) =>{
    if(dateValue === undefined || dateValue === "" || dateValue === null){
        return null
    }
    let values = dateValue.split("-");
    let d = new Date(values[0], values[1] - 1, values[2]);
    return Math.floor(d.getTime() / 1000);
}

let getDateFromEpoch = (epochTime) =>{
    let d = new Date(epochTime * 1000);
    let setWidth = (val) =>{
        if (val < 10)
            return "0" + val;
        return val;
    }
    return d.getFullYear() + "-" + setWidth(d.getMonth() + 1) + "-" + setWidth(d.getDate());    
}

let setSalesGroupFieldsValues = (salesGroup) =>{
    salesGroupName.value = salesGroup.group_name;
    totalAnimals.value = salesGroup.reported.count;
    zipCode.value = salesGroup.zip;
    startDate.value = getDateFromEpoch(salesGroup.start);
    endDate.value = getDateFromEpoch(salesGroup.end);
    $(deliveryLocationType).val(salesGroup.delivery_location_type);
    $(deliveryLocationType).trigger('change');
    if(salesGroup.delivery_location_type == "Auction"){    
        $(auctionMarketLocation).val(salesGroup.delivery_location);
        $(auctionMarketLocation).trigger('change');
    }
    else if(salesGroup.delivery_location_type == "Off Ranch"){
        offRanchDeliveryLocation.value = salesGroup.delivery_location;
    }
    else if(salesGroup.delivery_location_type == "Video Auction"){
        slide.value = salesGroup.reported.marketing_slide;
        weighingConditions.value = salesGroup.reported.marketing_weighing_conditions;
    }
    representedBy.value = salesGroup.reported.marketing_represented_by;
    breedComments.value = salesGroup.breed_comments;
    baseWeight.value = salesGroup.reported.weight;
    weightVariance.value = salesGroup.reported.weight_variance;
    charcateristicsWeighingConditions.value = salesGroup.weighing_conditions;
    geneticsComments.value = salesGroup.reported.genetics_comments;
    comments.value = salesGroup.reported.comments;
    publish.checked = salesGroup.published;
    showCarcassData.checked = salesGroup.show_account_carcass_data;

    $(category).val(salesGroup.category);
    $(category).trigger('change');
    $(breeds).val(salesGroup.reported.breeds);
    $(breeds).trigger('change');
    $(frame).val(salesGroup.reported.usda_frame_size);
    $(frame).trigger('change');
    $(muscling).val(salesGroup.reported.muscling);
    $(muscling).trigger('change');
    $(horns).val(salesGroup.reported.horns);
    $(horns).trigger('change');
    $(genomicTesting).val(salesGroup.reported.genomic_testing);
    $(genomicTesting).trigger('change');
    $(epd).val(salesGroup.reported.epd);
    $(epd).trigger('change');
    $(annualCattleHerdVaccinations).val(Boolean(salesGroup.are_annual_cattle_herd_vaccinations_given)?"Yes":"No");
    $(annualCattleHerdVaccinations).trigger('change');
    $(preconPrograms).val(salesGroup.reported.preconditioning_program);
    $(preconPrograms).trigger('change');
    $(vaccinations).val(salesGroup.reported.vaccinations);
    $(vaccinations).trigger('change');
    $(feedingProgram).val(salesGroup.reported.feeding_programs);
    $(feedingProgram).trigger('change');
    $(implants).val(salesGroup.reported.implants);
    $(implants).trigger('change');
    $(castrated).val(salesGroup.reported.castrated);
    $(castrated).trigger('change');
    $(pvpProgram).val(salesGroup.reported.process_verified_program);
    $(pvpProgram).trigger('change');
}

setSalesGroupFieldsValues(salesGroup)

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
            id: salesGroup.id,
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
            "are_annual_cattle_herd_vaccinations_given": annualCattleHerdVaccinations.value=="Yes"?1:0,
            //TODO: Removed auction_sale for now. Retained incase needed in future.
            //auction_sale: marketingAuctionSale.getID()
            auction_sale: null                   
        }
    }
});

submitButton.addEventListener("click", () => {
    asyncForm.submit();
})