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
            shipping_address_line: paymentForm.find("input[name='address']").val(),
            shipping_city: paymentForm.find("input[name='city']").val(),
            shipping_state: paymentForm.find("input[name='state']").val(),
            shipping_zip_code: paymentForm.find("input[name='zip_code']").val(),
            order_details: orderDetailsString
        }
    },
    requestRedirectTo: requestRedirectTo
});

$(document).ready(function(){
    var orderDetailsString=localStorage.getItem('orderDetails');
    var orderDetails=JSON.parse(orderDetailsString)
    $("input[name='same_address']").click(function(){
        if($(this).is(":checked")){
            $("#address").val(orderDetails.address_line).trigger("change"); 
            $("#city").val(orderDetails.city);
            $("#state").val(orderDetails.state);
            $("#zip_code").val(orderDetails.zip_code);
        }
        else if($(this).is(":not(:checked)")){
            $("#address").val("").trigger("change"); 
            $("#city").val("");
            $("#state").val("");
            $("#zip_code").val("");
        }
    });
});