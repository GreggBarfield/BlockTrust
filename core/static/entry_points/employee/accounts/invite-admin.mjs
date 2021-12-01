import {AsyncForm} from '/static/global/async_form.mjs';

let supportForm = $("#admin-email");
let statusMessage = supportForm.find("#admin_invite_message");
let errorMessage = supportForm.find("#admin_invite_error");

let email = supportForm.find("#email");
let action_route = "/employee/dashboard/invite-admin/"+account_id+"/action"

let form = new AsyncForm({
    action: action_route,
    form: supportForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Invite sent!",
    loadingMessage: "Sending Invite...",
    getData: () => {
        return {
            email: email.val()
        }
    }
});