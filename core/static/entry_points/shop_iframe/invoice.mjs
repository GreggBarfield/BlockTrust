$(document).ready(function() {
    if(localStorage.shoppingCart){
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString)
    var orderDetailsString=localStorage.getItem('orderDetails');
    var orderDetails=JSON.parse(orderDetailsString)
    // Printing out the shopping cart information
    Object.values(shopCart).forEach(val=>{
        var total_product_price=Math.round((val.price*val.quantity)*100)/100;
        $('#shopping-cart > tbody:last-child').append('<tr><td>' + val.product_name + '</td><td>' + val.quantity + '</td><td>'+ val.price +'</td><td>'+ total_product_price +'</td></tr>');
    });
    //Printing out subtotals and other transaction values
    $("#subtotal").text(localStorage.getItem('totalPrice'))
    $("#shipping").text(localStorage.getItem('shipping'))
    $("#tax").text(localStorage.getItem('totalTax'))
    $("#grandTotal").text(localStorage.getItem('grandTotal'))
    $("#payment").text(localStorage.getItem('grandTotal'))
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
    // Generating Invoice report
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


