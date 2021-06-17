$( ".form-inline" ).submit(function( event ) { 
    if(!localStorage.shoppingCart){
        localStorage.setItem('shoppingCart', JSON.stringify({}));
    }
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString)
    // Get input values to add products to cart
    var values = $(this).serializeArray();
    // Create tuple to add to shoppingCart object in localStorage
    var product={prod_no: values[0].value, price: parseFloat(values[1].value), quantity: parseInt(values[2].value)};
    var product_no=values[0].value;

    if(!(product_no in shopCart)){
    shopCart[product_no]=product;
    localStorage.setItem('shoppingCart', JSON.stringify(shopCart));
    }
    else{
        var previousValues=shopCart[product_no]
        var previousQuantity=previousValues.quantity
        product.quantity=product.quantity+previousQuantity
        shopCart[product_no]=product
        localStorage.setItem('shoppingCart', JSON.stringify(shopCart));
    }
    
//    if ( $( "input:first" ).val() === 6 ) {  
//        console.log("Added to cart");
//      $( "span" ).text( "Added Successfully." ).show();  
//      return;  
//    }  
//    $( "span" ).text( "Not valid!" ).show().fadeOut( 2000 );  
    event.preventDefault();  
  });

