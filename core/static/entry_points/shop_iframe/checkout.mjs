import {AsyncForm} from '/static/global/async_form.mjs';

let checkoutForm=$("#checkout_form");
let statusMessage=checkoutForm.find("#checkout_status_message");
let errorMessage=checkoutForm.find("#checkout_error_message");

let requestRedirectTo=null;

if(checkoutForm[0].hasAttribute("request_redirect_to")){
    requestRedirectTo=checkoutForm[0].getAttribute("request_redirect_to");
}

let shoppingCartString=""
let totalPriceString=""
let totalTaxString=""
let shippingString=""
let grandTotalString=""
if(localStorage.shoppingCart){
shoppingCartString=localStorage.getItem("shoppingCart")
}
if(localStorage.totalTax){
    totalTaxString=localStorage.getItem("totalTax")
}
if(localStorage.totalPrice){
    totalPriceString=localStorage.getItem("totalPrice")
}
if(localStorage.shipping){
    shippingString=localStorage.getItem("shipping")
}
if(localStorage.grandTotal){
    grandTotalString=localStorage.getItem("grandTotal")
}


let form = new AsyncForm({
    action:"/external/checkout",
    form: checkoutForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectmessage: "Details submitted",
    loadingMessage:"Hang on, submitting your details...", 
    getData: ()=>{
        return {
            first_name: checkoutForm.find("input[name='first_name']").val(),
            last_name: checkoutForm.find("input[name='last_name']").val(),
            email: checkoutForm.find("input[name='email']").val(),
            tel: checkoutForm.find("input[name='phone']").val(),
            company: checkoutForm.find("input[name='company']").val(),
            address_line: checkoutForm.find("input[name='address']").val(),
            city: checkoutForm.find("input[name='city']").val(),
            state: checkoutForm.find("input[name='state']").val(),
            country: checkoutForm.find("input[name='country']").val(),
            zip_code: checkoutForm.find("input[name='zip_code']").val(),
            shoppingCart: shoppingCartString,
            total_price:totalPriceString,
            total_tax:totalTaxString,
            shipping:shippingString,
            grand_total:grandTotalString

        }
    },
    requestRedirectTo: requestRedirectTo
});

$("#subtotal").text(localStorage.getItem('totalPrice'))
$("#shipping").text(localStorage.getItem('shipping'))
$("#tax").text(localStorage.getItem('totalTax'))
$("#grandTotal").text(localStorage.getItem('grandTotal'))