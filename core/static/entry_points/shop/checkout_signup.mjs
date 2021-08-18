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

//Displaying all the values
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

$( "#checkout_form" ).submit(function( event ) { 
    event.preventDefault();
    console.log("Submitting")
    if(!localStorage.orderDetails){
        localStorage.setItem('orderDetails', JSON.stringify({}));
    }
    let shoppingCartString=""
    let totalPriceString=""
    let totalTaxString=""
    let shippingString=""
    let discountString=""
    let grandTotalString=""
    if(localStorage.shoppingCart){
        shoppingCartString=localStorage.getItem('shoppingCart')
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
    if(localStorage.discount){
        discountString=localStorage.getItem("discount")
    }
    var values = $(this).serializeArray();
    var order={
        first_name: values[0].value,
        last_name: values[1].value,
        phone: values[2].value,
        company: values[3].value,
        email: values[4].value,
        address_line: values[6].value,
        city: values[7].value,
        state: values[8].value,
        zip_code: values[9].value,
        shoppingCart: shoppingCartString,
        total_price:totalPriceString,
        total_tax:totalTaxString,
        discount:discountString,
        shipping:shippingString,
        grand_total:grandTotalString
    }
    localStorage.setItem('orderDetails', JSON.stringify(order));
    //partner_id must be set in the parent page
    window.location.href = '/checkout_payment';
    return false;
});