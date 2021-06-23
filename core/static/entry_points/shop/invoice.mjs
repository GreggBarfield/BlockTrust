$(document).ready(function() {
    if(localStorage.shoppingCart){
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString)

    Object.values(shopCart).forEach(val=>{
        $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + '</td><td>'+ val.price +'</td><td>'+ val.price*val.quantity +'</td></tr>');
    });
    $("#subtotal").text(localStorage.getItem('totalPrice'))
    $("#shipping").text(localStorage.getItem('shipping'))
    $("#tax").text(localStorage.getItem('totalTax'))
    $("#grandTotal").text(localStorage.getItem('grandTotal'))
    $("#payment").text(localStorage.getItem('grandTotal'))
    
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = mm + '/' + dd + '/' + yyyy;
    $("#date").text(today)
    }

    function printPageArea(areaID){
        var printContent = document.getElementById(areaID);
        var WinPrint = window.open('', '', 'width=900,height=650');
        WinPrint.document.write(printContent.innerHTML);
        WinPrint.document.close();
        WinPrint.focus();
        WinPrint.print();
        WinPrint.close();
        console.log("printing")
    }

});


