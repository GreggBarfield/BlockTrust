import {AsyncForm} from '/static/global/async_form.mjs';

$(document).ready(function() {
    var shopCartString=localStorage.getItem('shoppingCart');
    if(shopCartString==null){
        window.location.href = '/external/shop/'+ partner_id;
        return false;
    }
    if(localStorage.shoppingCart){
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString);
    var size = Object.keys(shopCart).length;
    if(size==0){
        //partner id has to be set in the parent page
        window.location.href = '/external/shop/'+ partner_id;
        return false;
    }
    Object.values(shopCart).forEach(val=>{
        var total_product_price=Math.round((val.price*val.quantity)*100)/100;
        if(val.quantity===1){
        $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + ' Bag of 20</td><td>$'+ val.price.toFixed(2) +'</td><td>$'+ total_product_price.toFixed(2) +'</td><td><a href="/external/cart/'+partner_id+'"><button href="/external/cart/'+partner_id+'" class="removeItem" style="  color: #fff;background-color: #8B4513;border-color: #8B4513;" value="'+ val.prod_no +'">Remove</button></a></td></tr>');
        }
        else{        
        $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + ' Bags of 20</td><td>$'+ val.price.toFixed(2) +'</td><td>$'+ total_product_price.toFixed(2) +'</td><td><a href="/external/cart/'+partner_id+'"><button href="/external/cart/'+partner_id+'" class="removeItem" style="  color: #fff;background-color: #8B4513;border-color: #8B4513;" value="'+ val.prod_no +'">Remove</button></a></td></tr>');
        }
    });
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

    if(localStorage.getItem("discountApplied")==="Y"){
    $("#coupon_applied").text("Coupon applied!")
    }
    let hours=1;
    let saved=localStorage.getItem('saved');
    if(saved && (new Date().getTime()-saved>hours*60*60*1000)){
        localStorage.clear();
    }
    $(".removeItem").click(function(e){
        var idClicked=e.target.value;
        var shopCartString=localStorage.getItem('shoppingCart');
        var shopCart= JSON.parse(shopCartString);
        var discountApplied=localStorage.getItem('discountApplied');
        if(discountApplied==="Y"){
        var discountPercentageString=localStorage.getItem('discountPercentage');
        var discountPercentages=JSON.parse(discountPercentageString);
        }
        delete shopCart[idClicked];
        localStorage.setItem('shoppingCart', JSON.stringify(shopCart));
        // Recalculating the total price of all products on deletion of product
        var total_price=0
        Object.values(shopCart).forEach(val=>{
        total_price=total_price+(val.price*val.quantity)
        });
        total_price=Math.round(total_price*100)/100;
        // Calculating tax and discount
        var total_discount = 0;
        if(discountApplied==="Y"){
        for(var key in shopCart){
            // Checking if product is applicable for discount
            if(discountPercentages.hasOwnProperty(key)){
                var product_price=shopCart[key].price*shopCart[key].quantity;
                total_discount=total_discount+product_price*discountPercentages[key]/100;
            }
        }
        }
        total_discount=Math.round(total_discount*100)/100;
        var total_tax=Math.round((total_price-total_discount)*0.065*100)/100;
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
            //partner id has to be set in the parent page
            window.location.href = '/external/checkout/'+ partner_id;
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
        localStorage.setItem('discountPercentage', "{}");
        // Recalculating the total price of all products on removing coupon
        var total_price=0
        Object.values(shopCart).forEach(val=>{
        total_price=total_price+(val.price*val.quantity)
        });
        total_price=Math.round(total_price*100)/100;
        // Calculating tax
        var total_tax=Math.round((total_price)*0.065*100)/100;
        // Grand total after adding total price, total tax and shipping
        var grand_total=Math.round((total_price+total_tax+15)*100)/100;     
        //Setting new values in localStorage
        localStorage.setItem('totalPrice', total_price);
        localStorage.setItem('totalTax', total_tax);
        localStorage.setItem('grandTotal', grand_total);
        window.location.href = '/external/cart/'+partner_id;
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
        
        var discountPercentages=data.discount_percentages;
        console.log(discountPercentages)
        //Setting the discount percentage in localStorage
        localStorage.setItem('discountPercentage', JSON.stringify(discountPercentages));
        //Changing total price based on discount and recomputing tax
        var total_price=parseFloat(localStorage.getItem('totalPrice'));
        // Calculating discount
        //var total_discount=Math.round(total_price*discountPercentage*100/100)/100;
        var total_discount = 0;
        var shopCartString=localStorage.getItem('shoppingCart');
        var shopCart= JSON.parse(shopCartString);
        for(var key in shopCart){
            // Checking if product is applicable for discount
            if(discountPercentages.hasOwnProperty(key)){
                var product_price=shopCart[key].price*shopCart[key].quantity;
                total_discount=total_discount+product_price*discountPercentages[key]/100;
            }
        }
        total_discount=Math.round(total_discount*100)/100;
        // Calculating tax
        var total_tax=Math.round((total_price-total_discount)*0.065*100)/100;
        // Grand total after adding total price, total tax and shipping      
        var grand_total=Math.round((total_price+total_tax-total_discount+15)*100)/100;
        localStorage.setItem('discount', total_discount);
        localStorage.setItem('totalTax', total_tax);
        localStorage.setItem('grandTotal', grand_total); 
        localStorage.setItem('discountApplied', "Y");
        window.location.href = '/external/cart/'+partner_id;
        }
    }
});
