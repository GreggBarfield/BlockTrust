import {AsyncForm} from '/static/global/async_form.mjs';

$("#subtotal").text(localStorage.getItem('totalPrice'))
$("#shipping").text(localStorage.getItem('shipping'))
$("#tax").text(localStorage.getItem('totalTax'))
$("#grandTotal").text(localStorage.getItem('grandTotal'))

let LIcheckoutForm = $("#loggedIncheckout_form");
let statusMessage = LIcheckoutForm.find("#signup_status_message");
let errorMessage = LIcheckoutForm.find("#signup_error_message");

let requestRedirectTo = null;

if (LIcheckoutForm[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = LIcheckoutForm[0].getAttribute("request_redirect_to");
}

let form = new AsyncForm({
    action: "/loggedInCheckout/action",
    form: LIcheckoutForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Signed up successfully!",
    loadingMessage: "Hang on, we're setting up your account...",
    getData: () => {
        return {
            first_name: LIcheckoutForm.find("input[name='first_name']").val(),
            last_name: LIcheckoutForm.find("input[name='last_name']").val(),
            email: LIcheckoutForm.find("input[name='email']").val(),
            phone: LIcheckoutForm.find("input[name='phone']").val(),
            company: LIcheckoutForm.find("input[name='company']").val(),
            address: LIcheckoutForm.find("input[name='address']").val(),
            city: LIcheckoutForm.find("input[name='city']").val(),
            state: LIcheckoutForm.find("input[name='state']").val(),
            country: LIcheckoutForm.find("input[name='country']").val(),
            zip_code: LIcheckoutForm.find("input[name='zip_code']").val()
        }
    },
    requestRedirectTo: requestRedirectTo
});