import {AsyncForm} from '/static/global/async_form.mjs';

let notificationForm = $("#partner_notification_form");
let statusMessage = notificationForm.find("#notification_status_message");
let errorMessage = notificationForm.find("#notification_error_message");

let messageSubject = notificationForm.find('#message_subject');
let message = notificationForm.find("#message");
let partner = notificationForm.find("#partner")

let form = new AsyncForm({
    action: "/employee/dashboard/create-new-notification/partner/action",
    form: notificationForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Notification created successfully!",
    loadingMessage: "Hang on...",
    getData: () => {
        return {
            message_subject: messageSubject.val(),
            message: message.val(),
            partner: partner.val()
        }
    }
});