import {AsyncForm} from '/static/global/async_form.mjs';

//Modify the Shopping Cart
let modifyCartForm=$("#shopping_cart_modify");
let statusMessage=modifyCartForm.find("#cart_status_message");
let errorMessage=modifyCartForm.find("#cart_error_message");

let requestRedirectTo="/shopping-cart";

if(modifyCartForm[0].hasAttribute("request_redirect_to")){
    requestRedirectTo=modifyCartForm[0].getAttribute("request_redirect_to");
}

let form1 = new AsyncForm({
    action:"/delete/",
    form: modifyCartForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectmessage: "Removed from cart!",
    loadingMessage:"Removing items from cart...", 
    getData: ()=>{
        return {
            code: modifyCartForm.find("input[name='code']").val()
        }
    },
    requestRedirectTo: requestRedirectTo
});