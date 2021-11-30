import {AsyncForm} from '/static/global/async_form.mjs';

let supportForm = $("#admin-email");
let statusMessage = supportForm.find("#admin_invite_message");
let errorMessage = supportForm.find("#admin_invite_error");

let account_id = supportForm.find("#account_id");
let email = supportForm.find("#email");

let form = new AsyncForm({
    action: "/dashboard/invite-account-admin/action",
    form: supportForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Invite sent!",
    loadingMessage: "Sending Invite...",
    getData: () => {
        return {
            account_id: account_id.val(),
            email: email.val()
        }
    }
});