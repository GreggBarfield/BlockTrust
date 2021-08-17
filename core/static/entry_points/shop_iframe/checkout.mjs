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
    console.log("In submit!")
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
    var order={
        first_name: values[0].value,
        last_name: values[1].value,
        company: values[2].value,
        address_line: values[3].value,
        city: values[4].value,
        state: values[5].value,
        zip_code: values[6].value,
        phone: values[7].value,
        email: values[8].value,
        shoppingCart: shoppingCartString,
        total_price:totalPriceString,
        total_tax:totalTaxString,
        discount:discountString,
        shipping:shippingString,
        grand_total:grandTotalString
    }
    localStorage.setItem('orderDetails', JSON.stringify(order));
    //partner_id must be set in the parent page
    window.location.href = '/external/checkout_payment/'+partner_id;
    return false;
});
