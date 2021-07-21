import {AsyncForm} from '/static/global/async_form.mjs';

$(document).ready(function() {
    if(localStorage.shoppingCart){
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString);
    Object.values(shopCart).forEach(val=>{
        var total_product_price=Math.round((val.price*val.quantity)*100)/100;
        $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + ' Bag(s) of 20</td><td>$'+ val.price +'</td><td>$'+ total_product_price +'</td><td><a href="/external/cart"><button href="/external/cart" class="removeItem" style="  color: #fff;background-color: #8B4513;border-color: #8B4513;" value="'+ val.prod_no +'">Remove</button></a></td></tr>');
    });
    $("#subtotal").text(localStorage.getItem('totalPrice'))
    $("#shipping").text(localStorage.getItem('shipping'))
    $("#tax").text(localStorage.getItem('totalTax'))
    $("#discount").text(localStorage.getItem('discount'))
    $("#grandTotal").text(localStorage.getItem('grandTotal'))
    if(localStorage.getItem("discountApplied")==="Y"){
    $("#coupon_applied").text("Coupon applied!")
    }

    $(".removeItem").click(function(e){
        var idClicked=e.target.value;
        var shopCartString=localStorage.getItem('shoppingCart');
        var shopCart= JSON.parse(shopCartString);
        var discountPercentage=parseFloat(localStorage.getItem('discountPercentage'));
        delete shopCart[idClicked];
        localStorage.setItem('shoppingCart', JSON.stringify(shopCart));
        // Recalculating the total price of all products on deletion of product
        var total_price=0
        Object.values(shopCart).forEach(val=>{
        total_price=total_price+(val.price*val.quantity)
        });
        total_price=Math.round(total_price*100)/100;
        // Calculating tax and discount   
        var total_discount=Math.round(total_price*discountPercentage*100/100)/100;
        var total_tax=Math.round((total_price-total_discount)*0.0825*100)/100;
        // Grand total after adding total price, total tax and shipping
        var grand_total=Math.round((total_price+total_tax-total_discount+15)*100)/100;
        //Setting new values in localStorage
        localStorage.setItem('totalPrice', total_price);
        localStorage.setItem('totalTax', total_tax);
        localStorage.setItem('grandTotal', grand_total);
        localStorage.setItem('discount', total_discount);
        });

    $("#proceedButton").click(function(e){
        // Retrieve cart and check if it is not empty and redirect or alert user
        var shopCartString=localStorage.getItem('shoppingCart');
        var shopCart= JSON.parse(shopCartString);
        var size = Object.keys(shopCart).length;
        if(size>0){
            window.location.href = '/external/checkout';
            return false;
        }
        else{
            alert("Shopping Cart is empty!"); 
        }
    })

    $('#remove-coupon').click(function(e){
        //Checking if discount is applied or not
        if(localStorage.getItem('discountApplied')==="Y"){
        var shopCartString=localStorage.getItem('shoppingCart');
        var shopCart= JSON.parse(shopCartString);
        //Reset the values of discount localStorage data
        localStorage.setItem('discount', 0);
        localStorage.setItem('discountApplied', "N");    
        localStorage.setItem('discountPercentage', 0);
        // Recalculating the total price of all products on removing coupon
        var total_price=0
        Object.values(shopCart).forEach(val=>{
        total_price=total_price+(val.price*val.quantity)
        });
        total_price=Math.round(total_price*100)/100;
        // Calculating tax
        var total_tax=Math.round((total_price)*0.0825*100)/100;
        // Grand total after adding total price, total tax and shipping
        var grand_total=Math.round((total_price+total_tax+15)*100)/100;     
        //Setting new values in localStorage
        localStorage.setItem('totalPrice', total_price);
        localStorage.setItem('totalTax', total_tax);
        localStorage.setItem('grandTotal', grand_total);
        window.location.href = '/external/cart';
    }
    })

}
});

let couponForm = $("#coupon_form");
let statusMessage = couponForm.find("#coupon_status_message");
let errorMessage = couponForm.find("#coupon_error_message");

let requestRedirectTo = null;
if (couponForm[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = couponForm[0].getAttribute("request_redirect_to");
}

let form = new AsyncForm({
    action: "/external/cart",
    form: couponForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Applied coupon!",
    loadingMessage: "Applying coupon...",
    getData: () => {
        return {
            coupon_code: couponForm.find("input[name='coupon-code']").val()
        }
    },
    requestRedirectTo: requestRedirectTo,
    onFinished: (data) =>{
        console.log(data);
        //Checking if discount is already applied
        if(localStorage.getItem('discountApplied')==="N" && !('error' in data)){
        var discountPercentage=data.discount_percentage;
        //Setting the discount percentage in localStorage
        localStorage.setItem('discountPercentage', discountPercentage);
        //Changing total price based on discount and recomputing tax
        var total_price=parseFloat(localStorage.getItem('totalPrice'));
        // Calculating discount
        var total_discount=Math.round(total_price*discountPercentage*100/100)/100;
        // Calculating tax
        var total_tax=Math.round((total_price-total_discount)*0.0825*100)/100;
        // Grand total after adding total price, total tax and shipping
        console.log(typeof(total_price));
        console.log(typeof(total_tax));
        console.log(typeof(total_discount));        
        var grand_total=Math.round((total_price+total_tax-total_discount+15)*100)/100;
        localStorage.setItem('discount', total_discount);
        localStorage.setItem('totalTax', total_tax);
        localStorage.setItem('grandTotal', grand_total); 
        localStorage.setItem('discountApplied', "Y");
        window.location.href = '/external/cart';
        }
    }
});
