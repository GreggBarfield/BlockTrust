import {AsyncForm} from '/static/global/async_form.mjs';

let signupForm = $("#signup_form");
let statusMessage = signupForm.find("#signup_status_message");
let errorMessage = signupForm.find("#signup_error_message");

let username = signupForm.find("#signup_form_username");
let email = signupForm.find("#signup_form_email");
let password = signupForm.find("#signup_form_password");
let confirm_password = signupForm.find("#signup_form_confirm_password");
let first_name = signupForm.find("#signup_form_first");
let last_name = signupForm.find("#signup_form_last");
let phone = signupForm.find("#signup_form_phone");
let affiliate_id = signupForm.find("#signup_form_affiliate_id");
let company = signupForm.find("#signup_form_company");
let sector = signupForm.find("#signup_form_sector")
let city = signupForm.find("#signup_form_city");
let state = signupForm.find("#signup_form_state");
let zip_code = signupForm.find("#signup_form_zip");

let form = new AsyncForm({
    action: "/signup/action",
    form: signupForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Signed up successfully!",
    loadingMessage: "Hang on, we're setting up your account...",
    getData: () => {
        return {
            username: username.val(),
            password: password.val(),
            email: email.val(),
            confirm_password: confirm_password.val(),
            first_name: first_name.val(),
            last_name: last_name.val(),
            phone: phone.val(),
            affiliate_id: affiliate_id.val(),
            sector: sector.val(),
            company: company.val(),
            city: city.val(),
            state: state.val(),
            zip_code: zip_code.val()
        }
    }
});
