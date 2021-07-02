import {AsyncForm} from '/static/global/async_form.mjs';

let checkoutForm=$("#checkout_form");
let statusMessage=checkoutForm.find("#cart_status_message");
let errorMessage=checkoutForm.find("#cart_error_message");

let requestRedirectTo=null;

if(checkoutForm[0].hasAttribute("request_redirect_to")){
    requestRedirectTo=checkoutForm[0].getAttribute("request_redirect_to");
}

let shoppingCartString=""
if(localStorage.shoppingCart){
shoppingCartString=localStorage.getItem("shoppingCart")
}

let form1 = new AsyncForm({
    action:"/checkout_register/action",
    form: checkoutForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectmessage: "Payment details submitted",
    loadingMessage:"Hang on, submitting your payment...", 
    getData: ()=>{
        return {
            first_name: checkoutForm.find("input[name='first_name']").val(),
            last_name: checkoutForm.find("input[name='last_name']").val(),
            email: checkoutForm.find("input[name='email']").val(),
            username: heckOutForm.find("input[name='username']").val(),
            tel: checkoutForm.find("input[name='tel']").val(),
            company: checkoutForm.find("input[name='company']").val(),
            address_line: checkoutForm.find("input[name='address-line']").val(),
            city: checkoutForm.find("input[name='city']").val(),
            state: checkoutForm.find("input[name='state']").val(),
            country: checkoutForm.find("input[name='country']").val(),
            zip_code: checkoutForm.find("input[name='zip_code']").val(),
            password: checkoutForm.find("input[name='password']").val(),
            confirm_password: checkoutForm.find("input[name='confirm_password']").val(),
            sector: checkoutForm.find("input[name='sector']").val(),
            shoppingCart: shoppingCartString
        }
    },
    requestRedirectTo: requestRedirectTo
});

//$("#subtotal").text(localStorage.getItem('totalPrice'))
//$("#shipping").text(localStorage.getItem('shipping'))
//$("#tax").text(localStorage.getItem('totalTax'))
//$("#grandTotal").text(localStorage.getItem('grandTotal'))