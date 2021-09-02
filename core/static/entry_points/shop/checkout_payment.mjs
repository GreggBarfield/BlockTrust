import {AsyncForm} from '/static/global/async_form.mjs';

$("#subtotal").text(localStorage.getItem('totalPrice'))
$("#shipping").text(localStorage.getItem('shipping'))
$("#tax").text(localStorage.getItem('totalTax'))
$("#grandTotal").text(localStorage.getItem('grandTotal'))

let paymentForm = $("#payment_form");
let statusMessage = paymentForm.find("#payment_status_message");
let errorMessage = paymentForm.find("#payment_error_message");

let requestRedirectTo = null;

if (paymentForm[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = oaymentForm[0].getAttribute("request_redirect_to");
}


let form = new AsyncForm({
    action: "/payment/action",
    form: paymentForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Signed up successfully!",
    loadingMessage: "Hang on, we're setting up your account...",
    getData: () => {
        return {
            card_type: paymentForm.find("input[name='card_type']").val(),
            card_number: paymentForm.find("input[name='card_number']").val(),
            exp_month: paymenttForm.find("input[name='exp_month']").val(),
            exp_year: paymentForm.find("input[name='exp_year']").val(),
            cvv: paymentForm.find("input[name='cvv']").val(),
            address_checkbox: paymentForm.find("input[name='same_address']").val()
        }
    },
    requestRedirectTo: requestRedirectTo
});