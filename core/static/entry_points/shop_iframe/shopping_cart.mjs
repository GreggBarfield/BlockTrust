$(document).ready(function() {
    if(localStorage.shoppingCart){
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString)

    Object.values(shopCart).forEach(val=>{
        var total_product_price=Math.round((val.price*val.quantity)*100)/100;
        $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + '</td><td>$'+ val.price +'</td><td>$'+ total_product_price +'</td><td><a href="/external/cart"><button href="/external/cart" class="removeItem" style="  color: #fff;background-color: #8B4513;border-color: #8B4513;" value="'+ val.prod_no +'">Remove</button></a></td></tr>');
    });
    $("#subtotal").text(localStorage.getItem('totalPrice'))
    $("#shipping").text(localStorage.getItem('shipping'))
    $("#tax").text(localStorage.getItem('totalTax'))
    $("#grandTotal").text(localStorage.getItem('grandTotal'))


    $(".removeItem").click(function(e){
        var idClicked=e.target.value;
        var shopCartString=localStorage.getItem('shoppingCart');
        var shopCart= JSON.parse(shopCartString);
        delete shopCart[idClicked];
        localStorage.setItem('shoppingCart', JSON.stringify(shopCart));

        // Recalculating the total price of all products on deletion of product
        var total_price=0
        Object.values(shopCart).forEach(val=>{
        total_price=total_price+(val.price*val.quantity)
        });
        total_price=Math.round(total_price*100)/100;
        // Calculating tax
        var total_tax=Math.round(total_price*0.0825*100)/100;
        // Grand total after adding total price, total tax and shipping
        var grand_total=Math.round((total_price+total_tax+15)*100)/100;
        localStorage.setItem('totalPrice', total_price);
        localStorage.setItem('totalTax', total_tax);
        localStorage.setItem('grandTotal', grand_total); 
        });

    $("#proceedButton").click(function(e){
        // Retrieve cart and check if it is not empty and redirect or alert user
        var shopCartString=localStorage.getItem('shoppingCart');
        var shopCart= JSON.parse(shopCartString);
        var size = Object.keys(shopCart).length;
        console.log("proceed")
        if(size>0){
            window.location.href = '/external/checkout';
            return false;
        }
        else{
            alert("Shopping Cart is empty!"); 
        }
    })

}
});
