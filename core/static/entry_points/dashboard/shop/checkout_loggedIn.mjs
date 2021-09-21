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

$( "#loggedInCheckoutForm" ).submit(function( event ) { 
    event.preventDefault();
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
    console.log(values);
    var order={
        first_name: values[0].value,
        last_name: values[1].value,
        phone: values[2].value,
        company: values[3].value,
        email: values[4].value,
        address_line: values[5].value,
        city: values[6].value,
        state: values[7].value,
        zip_code: values[8].value,
        premise_id: values[9].value,
        shoppingCart: shoppingCartString,
        total_price:totalPriceString,
        total_tax:totalTaxString,
        discount:discountString,
        shipping:shippingString,
        grand_total:grandTotalString
    }
    localStorage.setItem('orderDetails', JSON.stringify(order));
    //partner_id must be set in the parent page
    window.location.href = '/dashboard/checkout_payment';
    return false;
});

$(document).ready(function() {
    if(localStorage.shoppingCart){
        var shopCartString=localStorage.getItem('shoppingCart');
        var shopCart= JSON.parse(shopCartString)
        if(1 in shopCart || 2 in shopCart){
           $("#premise_id").prop('disabled', false); 
        }
        else{
            $("#premise_id").prop('disabled', true);
        }
    }

});