import {AsyncForm} from '/static/global/async_form.mjs';

var subTotal=parseFloat(localStorage.getItem('totalPrice'));
var subTotalDisplay=subTotal.toFixed(2);
var ship=parseFloat(localStorage.getItem('shipping'));
var shipDisplay=ship.toFixed(2);
var tax=parseFloat(localStorage.getItem('totalTax'));
var taxDisplay=tax.toFixed(2);
var discount=parseFloat(localStorage.getItem('discount'));
var discountDisplay=discount.toFixed(2);
var grandTotal=parseFloat(localStorage.getItem('grandTotal'));
var grandTotalDisplay=grandTotal.toFixed(2);
$("#subtotal").text(subTotalDisplay);
$("#shipping").text(shipDisplay);
$("#tax").text(taxDisplay);
$("#discount").text(discountDisplay);
$("#grandTotal").text(grandTotalDisplay);

let paymentForm = $("#payment_form");
let statusMessage = paymentForm.find("#payment_status_message");
let errorMessage = paymentForm.find("#payment_error_message");
let orderDetailsString=""
if(localStorage.orderDetails){
    orderDetailsString=localStorage.getItem("orderDetails") 
    var orderDetails = JSON.parse(orderDetailsString)
    $("#name").val(orderDetails['first_name'] + " " + orderDetails['last_name'])
}
let requestRedirectTo = null;

if (paymentForm[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = paymentForm[0].getAttribute("request_redirect_to");
}


let form = new AsyncForm({
    action: "/dashboard/checkout_payment",
    form: paymentForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Payment successful!",
    loadingMessage: "Hang on, we're processing your payment...",
    getData: () => {
        return {
            card_type: paymentForm.find("input[name='card_type']").val(),
            card_number: paymentForm.find("input[name='card_number']").val(),
            exp_month: paymentForm.find("input[name='exp_month']").val(),
            exp_year: paymentForm.find("input[name='exp_year']").val(),
            cvv: paymentForm.find("input[name='cvv']").val(),
            address_checkbox: paymentForm.find("input[name='same_address']").val(),
            order_details: orderDetailsString,
            shipping_address_line: orderDetails.address_line,
            shipping_city: orderDetails.city,
            shipping_state: orderDetails.state, 
            shipping_zip_code: orderDetails.zip_code
        }
    },
    requestRedirectTo: requestRedirectTo
});