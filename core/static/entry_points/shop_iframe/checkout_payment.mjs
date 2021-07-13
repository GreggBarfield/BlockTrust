import {AsyncForm} from '/static/global/async_form.mjs';

$("#subtotal").text(localStorage.getItem('totalPrice'))
$("#shipping").text(localStorage.getItem('shipping'))
$("#tax").text(localStorage.getItem('totalTax'))
$("#grandTotal").text(localStorage.getItem('grandTotal'))

let paymentForm = $("#payment_form");
let statusMessage = paymentForm.find("#payment_status_message");
let errorMessage = paymentForm.find("#payment_error_message");
let orderDetailsString=""
if(localStorage.orderDetails){
    orderDetailsString=localStorage.getItem("orderDetails")
}

let requestRedirectTo = null;

if (paymentForm[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = paymentForm[0].getAttribute("request_redirect_to");
}


let form = new AsyncForm({
    action: "/external/checkout_payment",
    form: paymentForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Payment successfull!",
    loadingMessage: "Hang on, we're processing your payment...",
    getData: () => {
        return {
            card_type: paymentForm.find("input[name='card-type']").val(),
            card_number: paymentForm.find("input[name='card-number']").val(),
            exp_month: paymentForm.find("input[name='exp-month']").val(),
            exp_year: paymentForm.find("input[name='exp-year']").val(),
            cvv: paymentForm.find("input[name='cvv']").val(),
            address_checkbox: paymentForm.find("input[name='same_address']").val(),
            address_line: paymentForm.find("input[name='address']").val(),
            city: paymentForm.find("input[name='city']").val(),
            state: paymentForm.find("input[name='state']").val(),
            country: paymentForm.find("input[name='country']").val(),
            zip_code: paymentForm.find("input[name='zip_code']").val(),
            order_details: orderDetailsString
        }
    },
    requestRedirectTo: requestRedirectTo
});