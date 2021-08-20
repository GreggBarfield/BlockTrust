import {AsyncForm} from '/static/global/async_form.mjs';

let inviteUserForm = $("#invite_user_form");
let statusMessage = inviteUserForm.find("#inviteuser_status_message");
let errorMessage = inviteUserForm.find("#inviteuser_error_message");
let email = inviteUserForm.find("#invite_user_email");

let form = new AsyncForm({
    action: "/dashboard/inviteuser",
    form: inviteUserForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Email sent!",
    loadingMessage: "Hang on, we're sending an invite...",
    getData: () => {
        return {
            email: email.val(),
            current_account : current_account,
            current_account_id: current_account_id
        }
    }
});