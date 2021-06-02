import {AsyncForm} from '/static/global/async_form.mjs';

let cartForm=$("#shopping_cart_form");
let statusMessage=cartForm.find("#cart_status_message");
let errorMessage=cartForm.find("#cart_error_message");

let requestRedirectTo="/shop";

if(cartForm[0].hasAttribute("request_redirect_to")){
    requestRedirectTo=cartForm[0].getAttribute("request_redirect_to");
}

let form = new AsyncForm({
    action:"/shop",
    form: cartForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectmessage: "Added to cart!",
    loadingMessage:"Adding your items to cart...", 
    getData: ()=>{
        return {
            code: cartForm.find("input[name='code']").val(),
            quantity_1: cartForm.find("input[name='quantity_1']").val()
        }
    },
    requestRedirectTo: requestRedirectTo
});

