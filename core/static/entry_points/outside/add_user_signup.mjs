import {AsyncForm} from '/static/global/async_form.mjs';

let invitedUserSignup = $("#invited_user_form");
let statusMessage = invitedUserSignup.find("#inviteduser_status_message");
let errorMessage = invitedUserSignup.find("#inviteduser_error_message");

let first_name = invitedUserSignup.find("#invite_first");
let last_name = invitedUserSignup.find("#invite_last");
let username = invitedUserSignup.find("#invite_username");
let password = invitedUserSignup.find("#invite_password");
let confirm_password = invitedUserSignup.find("#invite_confirm_password");
let user_email = invitedUserSignup.find("#user_email");
let account_name = invitedUserSignup.find("#account_name");
let account_id = invitedUserSignup.find("#account_id");

let form = new AsyncForm({
    action: "/adduser",
    form: invitedUserSignup[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Signed up!",
    loadingMessage: "Hang on, we're submitting your details...",
    getData: () => {
        return {
            first_name: first_name.val(),
            last_name: last_name.val(),
            username: username.val(),
            password: password.val(),
            confirm_password: confirm_password.val(),
            user_email: user_email.val(),
            account_name: account_name.val(),
            account_id: account_id.val()
        }
    }
});