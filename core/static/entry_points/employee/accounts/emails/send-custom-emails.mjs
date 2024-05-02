import {AsyncForm} from '/static/global/async_form.mjs';

let customEmailForm = $("#email_form");
let statusMessage = customEmailForm.find("#email_status_message");
let errorMessage = customEmailForm.find("#email_error_message");

let emailRecipients = customEmailForm.find("#email-recipients");
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
            email_recipients: emailRecipients.val(),
            email_subject: emailSubject.val(),
            email_header: emailHeader.val(),
            email_body: emailBody.val()
        }
    }
});
