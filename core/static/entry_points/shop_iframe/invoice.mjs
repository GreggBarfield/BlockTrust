$(document).ready(function() {
    if(localStorage.shoppingCart){
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString)
    var orderDetailsString=localStorage.getItem('orderDetails');
    var orderDetails=JSON.parse(orderDetailsString)
    // Printing out the shopping cart information
    Object.values(shopCart).forEach(val=>{
        var total_product_price=Math.round((val.price*val.quantity)*100)/100;
        if(val.quantity===1){
            $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + ' Bag of 20</td><td>$'+ val.price.toFixed(2) +'</td><td>$'+ total_product_price.toFixed(2) +'</td></tr>');
        }
        else{        
            $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + ' Bags of 20</td><td>$'+ val.price.toFixed(2) +'</td><td>$'+ total_product_price.toFixed(2) +'</td></tr>');
        }
    });
    //Printing out subtotals and other transaction values
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
    $("#subtotal").text(subTotalDisplay)
    $("#shipping").text(shipDisplay)
    $("#tax").text(taxDisplay)
    $("#discount").text(discountDisplay)
    $("#grandTotal").text(grandTotalDisplay)
    //Printing out account details and address
    $("#account_name").text(orderDetails.first_name+" "+orderDetails.last_name)
    $("#account_address").text(orderDetails.address_line)
    $("#account_address_continued").text(orderDetails.city+", "+orderDetails.state+" "+orderDetails.zip_code)
    //Printing out shipping details and address
    $("#shipping_name").text(orderDetails.first_name+" "+orderDetails.last_name)
    $("#shipping_address").text(orderDetails.address_line)
    $("#shipping_address_continued").text(orderDetails.city+", "+orderDetails.state+" "+orderDetails.zip_code)
    //Printing out current date
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = mm + '/' + dd + '/' + yyyy;
    $("#date").text(today)
    }
    //Clearing out localStorage on completion of transaction
    $("#return-button").click(function(e){
        localStorage.clear();
        //partner_id must be set in the parent page
        window.location.href = '/external/shop/'+partner_id;
    });

    $(window).bind('beforeunload',function(){
        alert("Please make sure to save your order confirmation");
       localStorage.clear();
   });

});


