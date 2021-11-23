import {AsyncForm} from '/static/global/async_form.mjs';

let supportForm = $("#dashboard-support");
let statusMessage = supportForm.find("#support_status_message");
let errorMessage = supportForm.find("#support_error_message");

let first = supportForm.find("#first");
let last = supportForm.find("#last");
let email = supportForm.find("#email");
let phone = supportForm.find("#phone");
let message = supportForm.find("#message");

let form = new AsyncForm({
    action: "/dashboard/support/action",
    form: supportForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Submitted!",
    loadingMessage: "Submitting...",
    getData: () => {
        return {
            first: first.val(),
            last: last.val(),
            email: email.val(),
            phone: phone.val(),
            message: message.val(),
        }
    }
});