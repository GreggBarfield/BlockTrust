import { AsyncForm } from '/static/global/async_form.mjs';

for(const account_data of accounts_retail_data){
    let contactForm = $("#contact_form_"+account_data.id);
    let statusMessage = contactForm.find("#contact_form_status_message_"+account_data.id);
    let errorMessage = contactForm.find("#contact_form_error_message_"+account_data.id);

    let name = contactForm.find("#name_"+account_data.id);
    let email = contactForm.find("#email_"+account_data.id);
    let phone = contactForm.find("#phone_"+account_data.id);
    let message = contactForm.find("#message_"+account_data.id);

    let form = new AsyncForm({
        action: "/contact_account/action",
        form: contactForm[0],
        status: statusMessage[0],
        error: errorMessage[0],
        redirectMessage: "Message Sent!",
        loadingMessage: "Sending Message....",
        getData: () => {
            return {
                name: name.val(),
                email: email.val(),
                phone: phone.val(),
                message: message.val(),
                account_id: account_data.id,
            }
        },
        requestRedirectTo: window.location.href
    });
}