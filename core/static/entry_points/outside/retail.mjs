import { AsyncForm } from '/static/global/async_form.mjs';

for(const retail_data of accounts_retail_data){
    let contactForm = $("#contact_form_"+retail_data.retail_reference_number);
    let statusMessage = contactForm.find("#contact_form_status_message_"+retail_data.retail_reference_number);
    let errorMessage = contactForm.find("#contact_form_error_message_"+retail_data.retail_reference_number);

    let name = contactForm.find("#name_"+retail_data.retail_reference_number);
    let email = contactForm.find("#email_"+retail_data.retail_reference_number);
    let phone = contactForm.find("#phone_"+retail_data.retail_reference_number);
    let message = contactForm.find("#message_"+retail_data.retail_reference_number);

    let form = new AsyncForm({
        action: "/contact-account",
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
                retail_reference_number: retail_data.retail_reference_number,
                eid: eid
            }
        }
    });
}