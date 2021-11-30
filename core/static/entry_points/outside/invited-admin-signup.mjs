import {AsyncForm} from '/static/global/async_form.mjs';

let invitedAdminSignup = $("#invited_admin_signup");
let statusMessage = invitedAdminSignup.find("#invited_admin_status_message");
let errorMessage = invitedAdminSignup.find("#invited_admin_error_message");

let first_name = invitedAdminSignup.find("#admin_first");
let last_name = invitedAdminSignup.find("#admin_last");
let password = invitedAdminSignup.find("#admin_password");
let confirm_password = invitedAdminSignup.find("#admin_confirm_password");
let admin_email = invitedAdminSignup.find("#admin_email");
let phone = invitedAdminSignup.find("#admin_phone");
let account_name = invitedAdminSignup.find("#account_name");
let account_id = invitedAdminSignup.find("#account_id");

let form = new AsyncForm({
    action: "/add-account-admin/action",
    form: invitedAdminSignup[0],
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
            admin_email: admin_email.val(),
            account_name: account_name.val(),
            account_id: account_id.val(),
            admin_phone: phone.val()
        }
    }
});