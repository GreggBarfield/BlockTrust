import {AsyncForm} from '/static/global/async_form.mjs';

let signupForm = $("#signup_form");
let statusMessage = signupForm.find("#signup_status_message");
let errorMessage = signupForm.find("#signup_error_message");

let username = signupForm.find("#signup_form_username");
let password = signupForm.find("#signup_form_password");
let email = signupForm.find("#signup_form_email");
let confirm_password = signupForm.find("#signup_form_confirm_password");
let first = signupForm.find("#signup_form_first");
let last = signupForm.find("#signup_form_last");
let phone = signupForm.find("#signup_form_phone");

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
            first: first.val(),
            last: last.val(),
            phone: phone.val(),
        }
    }
});
