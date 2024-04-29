import {AsyncForm} from '/static/global/async_form.mjs';

let welcomeEmailForm = $("#welcome_email_form");
let statusMessage = welcomeEmailForm.find("#email_status_message");
let errorMessage = welcomeEmailForm.find("#email_error_message");
let accountId = welcomeEmailForm.find("#accounts_select");

let welcomeEmailAsyncForm = new AsyncForm({
    action: "/employee/dashboard/emails/send-welcome-email",
    form: welcomeEmailForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Email Sent!",
    loadingMessage: "Sending Email...",
    getData: () => {
        return {
            account_id: accountId.val()
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    $("#accounts_select").select2({multiple: false, placeholder: "Select Account"});
});