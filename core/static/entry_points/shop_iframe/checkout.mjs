$("#subtotal").text(localStorage.getItem('totalPrice'))
$("#shipping").text(localStorage.getItem('shipping'))
$("#tax").text(localStorage.getItem('totalTax'))
$("#grandTotal").text(localStorage.getItem('grandTotal'))

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
    var values = $(this).serializeArray();
    var order={
        first_name: values[0].value,
        last_name: values[1].value,
        phone: values[2].value,
        company: values[3].value,
        email: values[4].value,
        address_line: values[5].value,
        city: values[6].value,
        state: values[7].value,
        country: values[8].value,
        zip_code: values[9].value,
        shoppingCart: shoppingCartString,
        total_price:totalPriceString,
        total_tax:totalTaxString,
        shipping:shippingString,
        grand_total:grandTotalString
    }
    localStorage.setItem('orderDetails', JSON.stringify(order));
    window.location.href = '/external/checkout_payment';
    return false;
});
