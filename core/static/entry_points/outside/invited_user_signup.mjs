import {AsyncForm} from '/static/global/async_form.mjs';

let invitedUserSignup = $("#invited_user_form");
let statusMessage = invitedUserSignup.find("#login_status_message");
let errorMessage = invitedUserSignup.find("#login_error_message");

let requestRedirectTo = null;
if (invitedUserSignup[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = invitedUserSignup[0].getAttribute("request_redirect_to");
}

let first_name = invitedUserSignup.find("#invite_first");
let last_name = invitedUserSignup.find("#invite_last");
let password = invitedUserSignup.find("#invite_password");
let confirm_password = invitedUserSignup.find("#invite_confirm_password");
let user_email = invitedUserSignup.find("#user_email");
let account_name = invitedUserSignup.find("#account_name");

let form = new AsyncForm({
    action: "/dashboard/adduser",
    form: invitedUserSignup[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Signed up!",
    loadingMessage: "Hang on, we're submitting your details...",
    getData: () => {
        return {
            first_name: first_name.val(),
            last_name: last_name.val(),
            password: password.val(),
            confirm_password: confirm_password.val(),
            user_email: user_email.val(),
            account_name: account_name.val()
        }
    },
    requestRedirectTo: requestRedirectTo
});