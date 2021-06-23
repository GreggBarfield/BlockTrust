import {AsyncForm} from '/static/global/async_form.mjs';

//Modify the Shopping Cart
let checkoutForm=$("#checkout_form");
let statusMessage=checkoutForm.find("#cart_status_message");
let errorMessage=checkoutForm.find("#cart_error_message");

let requestRedirectTo=null;

if(checkoutForm[0].hasAttribute("request_redirect_to")){
    requestRedirectTo=checkoutForm[0].getAttribute("request_redirect_to");
}

let form1 = new AsyncForm({
    action:"/checkout",
    form: checkoutForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectmessage: "Payment details submitted",
    loadingMessage:"Hang on, submitting your payment...", 
    getData: ()=>{
        return {
            first_name: checkoutForm.find("input[name='first-name']").val(),
            last_name: checkoutForm.find("input[name='last-name']").val(),
            email: checkoutForm.find("input[name='email']").val(),
            tel: checkoutForm.find("input[name='tel']").val(),
            company: checkoutForm.find("input[name='company']").val(),
            address_line: checkoutForm.find("input[name='address-line']").val(),
            country: checkoutForm.find("input[name='conutry']").val(),
            zip: checkoutForm.find("input[name='zip']").val(),
            card_type: checkoutForm.find("input[name='card-type']").val(),
            card_number: checkoutForm.find("input[name='card-number']").val(),
            exp_month: checkoutForm.find("input[name='exp-month']").val(),
            exp_year: checkoutForm.find("input[name='exp-year']").val(),
            cvv: checkoutForm.find("input[name='cvv']").val(),
            message: checkoutForm.find("input[name='message']").val()
        }
    },
    requestRedirectTo: requestRedirectTo
});

$("#grandTotal").text(localStorage.getItem('grandTotal'))