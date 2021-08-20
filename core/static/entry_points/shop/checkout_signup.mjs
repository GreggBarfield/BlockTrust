import {AsyncForm} from '/static/global/async_form.mjs';

let checkoutForm = $("#checkout_form");
let statusMessage = checkoutForm.find("#signup_status_message");
let errorMessage = checkoutForm.find("#signup_error_message");
let password = checkoutForm.find("#password");
let confirm_password = checkoutForm.find("#confirm_password");
let affiliate_id = checkoutForm.find("#affiliate_id");

let requestRedirectTo = null;

if (checkoutForm[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = checkoutForm[0].getAttribute("request_redirect_to");
}

let form = new AsyncForm({
    action: "/checkout_register/action",
    form: checkoutForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Signed up successfully!",
    loadingMessage: "Hang on, we're setting up your account...",
    getData: () => {
        return {
            first_name: checkoutForm.find("input[name='first_name']").val(),
            last_name: checkoutForm.find("input[name='last_name']").val(),
            email: checkoutForm.find("input[name='email']").val(),
            username: checkoutForm.find("input[name='username']").val(),
            phone: checkoutForm.find("input[name='phone']").val(),
            company: checkoutForm.find("input[name='company']").val(),
            address: checkoutForm.find("input[name='address']").val(),
            city: checkoutForm.find("input[name='city']").val(),
            state: checkoutForm.find("input[name='state']").val(),
            country: checkoutForm.find("input[name='country']").val(),
            zip_code: checkoutForm.find("input[name='zip_code']").val(),
            sector: checkoutForm.find("input[name='sector']").val(),
            password: password.val(),
            confirm_password: confirm_password.val(),
            affiliate_id: checkoutForm.find("input[name='affiliate_id']").val(),
            partner: checkoutForm.find("input[name='partner']").val()
        }
    },
    requestRedirectTo: requestRedirectTo
});

$("#subtotal").text(localStorage.getItem('totalPrice'))
$("#shipping").text(localStorage.getItem('shipping'))
$("#tax").text(localStorage.getItem('totalTax'))
$("#grandTotal").text(localStorage.getItem('grandTotal'))

$(document).ready(function() {
    if(g.user){
        console.log("User is logged in")
    }
});