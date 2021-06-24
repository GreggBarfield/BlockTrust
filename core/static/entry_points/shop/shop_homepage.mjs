$( ".form-inline" ).submit(function( event ) { 
    event.preventDefault();
    // Adding cart to local storage if not present
    if(!localStorage.shoppingCart){
        localStorage.setItem('shoppingCart', JSON.stringify({}));
    }
    // Adding total price, shipping, tax and grand total to local storage if not present
    if(!localStorage.shipping){
    localStorage.setItem('shipping', 15)
    }
    if(!localStorage.totalPrice){
    localStorage.setItem('totalPrice', 0);
    }
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString)
    // Get input values to add products to cart
    var values = $(this).serializeArray();
    // Create tuple to add to shoppingCart object in localStorage
    var product={prod_no: values[0].value, price: parseFloat(values[1].value), product_name: values[2].value, quantity: parseInt(values[3].value)};
    var product_no=values[0].value;
    // Checking if product is already present in the localStorage and performing necessary actions
    console.log("Calculating")
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
    // Recalculating the total price of all products on addition of new product
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

