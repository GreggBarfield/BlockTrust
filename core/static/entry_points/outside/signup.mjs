import {AsyncForm} from '/static/global/async_form.mjs';

let signupForm = $("#signup_form");
let statusMessage = signupForm.find("#signup_status_message");
let errorMessage = signupForm.find("#signup_error_message");

let email = signupForm.find("#signup_form_email");
let password = signupForm.find("#signup_form_password");
let confirm_password = signupForm.find("#signup_form_confirm_password");
let first_name = signupForm.find("#signup_form_first");
let last_name = signupForm.find("#signup_form_last");
let phone = signupForm.find("#signup_form_phone");
let sector = signupForm.find("#signup_form_sector");
let partner = signupForm.find("#signup_form_partner");
let partner_id = signupForm.find("#signup_form_partner_id");
let company = signupForm.find("#signup_form_company");
let address = signupForm.find("#signup_form_address");
let city = signupForm.find("#signup_form_city");
let state = signupForm.find("#signup_form_state");
let zip_code = signupForm.find("#signup_form_zip");
let personal_phone = signupForm.find("#signup_form_personal_phone");
let are_auction_market_utilized = signupForm.find("#signup_form_are_auction_market_utilizied");
let auction_markets = signupForm.find("#signup_form_auction_markets");
let preconditioning_programs = signupForm.find("#signup_form_preconditioning_programs");
let pvp_programs = signupForm.find("#signup_form_pvp_programs")

let ip="", country="";
if(checkIP.toLowerCase() === "true") {
    const response = await fetch("https://ipinfo.io/json?token=" + ipInfoAccessToken);
    const clientMachineDetails = await response.json();
    if ("ip" in clientMachineDetails && "country" in clientMachineDetails){
        ip = clientMachineDetails.ip;
        country = clientMachineDetails.country;
    }
}

let preconditioningProgramsList = [];
let pvpProgramsList = [];
let auctionMarketsList = [];
let preconditioningPrograms = [
	"Health Track",
	"Value Added Calf-45",
	"OQBN Vac-45 Program",
	"JRS Wean-Vac 45",
	"Superior Livestock Vac-45",
	"TAMU Vac-45",
	"Integrity Beef Alliance Vac-45",
	"Health Track Vac-45",
	"NMSU Vac-45",
	"MCA Vac-45",
	"PrimeVac Vac-45",
	"SelectVac WeanVac"
];
let pvpPrograms = [
    "American Certified Brands",
    "AzTx Cattle Co.",
    "BeefTraxx",
    "Big Blue Sale Barn Passport Program®",
    "Cal Poly State Univ Animal Science",
    "Frost PLLC dba FACTA",
    "IdentiGEN North America",
    "IMI Global",
    "Legacy Verified",
    "Ranchers Connecting Ranchers",
    "Red Angus Association of America",
    "Samson",
    "TechniTrack",
    "Zoetis Genetics",
    "Other"
];
for(let auctionMarket of auctionMarkets){
    auctionMarketsList.push({id: auctionMarket.id, text: auctionMarket.name + ", " + auctionMarket.city + ", "  + auctionMarket.state});
}
for(let preconditioningProgram of preconditioningPrograms){
    preconditioningProgramsList.push({id: preconditioningProgram, text: preconditioningProgram});
}
for(let pvpProgram of pvpPrograms){
    pvpProgramsList.push({id: pvpProgram, text: pvpProgram});
}
$("#signup_form_auction_markets").select2({data: auctionMarketsList, multiple: true, placeholder: "Select Auction Markets"});
$("#signup_form_preconditioning_programs").select2({data: preconditioningProgramsList, multiple: true, placeholder: "Select Preconditioning Programs"});
$("#signup_form_pvp_programs").select2({data: pvpProgramsList, multiple: true, placeholder: "Select PVP Programs"});

let form = new AsyncForm({
    action: "/signup/action",
    form: signupForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Signed up successfully!",
    loadingMessage: "Hang on, we're setting up your account...",
    reCaptcha: true,
    reCaptchaAction: "registration",
    reCaptchaSiteKey: siteKey,
    getData: () => {
        return {
            username: email.val(),
            password: password.val(),
            email: email.val(),
            confirm_password: confirm_password.val(),
            first_name: first_name.val(),
            last_name: last_name.val(),
            phone: phone.val(),
            partner: partner.val(),
            affiliate_id: partner_id.val(),
            sector: sector.val(), 
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip_code: zip_code.val(),
            personal_phone: personal_phone.val(),
            ip_address: ip,
            ip_country: country,
            are_auction_markets_used_by_account: are_auction_market_utilized.val(),
            auction_markets: JSON.stringify(auction_markets.val()),
            preconditioning_programs: JSON.stringify(preconditioning_programs.val()),
            pvp_programs: JSON.stringify(pvp_programs.val())
        }
    }
});

partner.on('change', function() {
    if (partner.find(":selected").text() == "No Partner") {
        partner_id.prop('disabled', true);
    } else {
        partner_id.prop('disabled', false);
    }
});

are_auction_market_utilized.on('change', function(){
    if(are_auction_market_utilized.val() == "0"){
        auction_markets.prop('disabled', true);
        auction_markets.val(null).trigger("change");
    }
    else{
        auction_markets.prop('disabled', false);
    }
});