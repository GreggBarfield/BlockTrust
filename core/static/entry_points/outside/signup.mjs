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
let partner = signupForm.find("#signup_form_partner");
let partner_id = signupForm.find("#signup_form_partner_id");
let company = signupForm.find("#signup_form_company");
let address = signupForm.find("#signup_form_address");
let city = signupForm.find("#signup_form_city");
let state = signupForm.find("#signup_form_state");
let zip_code = signupForm.find("#signup_form_zip");
let personal_phone = signupForm.find("#signup_form_personal_phone");

let ip="", country="";
if(checkIP.toLowerCase() === "true") {
    const response = await fetch("https://ipinfo.io/json?token=" + ipInfoAccessToken);
    const clientMachineDetails = await response.json();
    if ("ip" in clientMachineDetails && "country" in clientMachineDetails){
        ip = clientMachineDetails.ip;
        country = clientMachineDetails.country;
    }
}

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
            username: email.val(), //the email will be stored here in the backend
            password: password.val(),
            email: email.val(),
            confirm_password: confirm_password.val(),
            first_name: first_name.val(),
            last_name: last_name.val(),
            phone: phone.val(),
            partner: partner.val(),
            affiliate_id: partner_id.val(),
            sector: sectorId, //must be set in the parent page
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip_code: zip_code.val(),
            personal_phone: personal_phone.val(),
            ip_address: ip,
            ip_country: country
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
