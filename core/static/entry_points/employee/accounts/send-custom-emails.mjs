import {AsyncForm} from '/static/global/async_form.mjs';

let customEmailForm = $("#welcome_email_form");
let statusMessage = customEmailForm.find("#email_status_message");
let errorMessage = customEmailForm.find("#email_error_message");

let accountId = customEmailForm.find("#accounts_select");
let sendEmailToAdminOnly = customEmailForm.find("#send-to-admin-only");
let emailSubject = customEmailForm.find("#email-subject");
let emailHeader = customEmailForm.find("#email-header");
let emailBody = customEmailForm.find("#email-body");

let customEmailAsyncForm = new AsyncForm({
    action: "/employee/dashboard/emails/send-custom-emails",
    form: customEmailForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Email Sent!",
    loadingMessage: "Sending Email...",
    getData: () => {
        return {
            account_id: accountId.val(),
            send_email_to_admin_only: sendEmailToAdminOnly[0].checked,
            email_subject: emailSubject.val(),
            email_header: emailHeader.val(),
            email_body: emailBody.val()
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    $("#accounts_select").select2({multiple: false, placeholder: "Select Account"});
});