$(document).ready(function() {
    if(localStorage.shoppingCart){
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString)

    Object.values(shopCart).forEach(val=>{
        $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + '</td><td>'+ val.price +'</td><td>'+ val.price*val.quantity +'</td><td><a href="/shopping-cart"><button href="/shopping-cart" class="removeItem" value="'+ val.prod_no +'">Remove</button></a></td></tr>');
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
        //$('#shopping-cart>tbody').empty();
        //Object.values(shopCart).forEach(val=>{
        //    $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + '</td><td>'+ val.price +'</td><td>'+ val.price*val.quantity +'</td><td><button class="removeItem" value="'+ val.prod_no +'">Remove</button></td></tr>');
        //});
    });

}
});
