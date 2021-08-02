$( ".form-inline" ).submit(function( event ) { 
    event.preventDefault();
    // Adding cart to local storage if not present
    if(!localStorage.shoppingCart){
        localStorage.setItem('shoppingCart', JSON.stringify({}));
    }
    // Adding total price, shipping, tax and grand total to local storage if not present
    if(!localStorage.shipping){
    localStorage.setItem('shipping', 15.00)
    }
    if(!localStorage.totalPrice){
    localStorage.setItem('totalPrice', 0);
    }
    if(!localStorage.discount){  
    localStorage.setItem('discount', 0);
    }
    if(!localStorage.discountPercentage){  
        localStorage.setItem('discountPercentage', {});
    }
    if(!localStorage.discountApplied){  
        localStorage.setItem('discountApplied', "N");
    }
    let hours=1;
    let saved=localStorage.getItem('saved');
    if(saved===null){
        localStorage.setItem('saved', new Date().getTime())  
    }
    if(saved && (new Date().getTime()-saved>hours*60*60*1000)){
        localStorage.clear();
    }
    var shopCartString=localStorage.getItem('shoppingCart');
    var shopCart= JSON.parse(shopCartString)
    // Get input values to add products to cart
    var values = $(this).serializeArray();
    // Create tuple to add to shoppingCart object in localStorage
    var product={prod_no: values[0].value, price: parseFloat(values[1].value), product_name: values[2].value, quantity: parseInt(values[3].value)};
    var product_no=values[0].value;
    // Checking if product is already present in the localStorage and performing necessary actions
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
    var total_price=0;
    var discountApplied=localStorage.getItem('discountApplied');
    if(discountApplied==="Y"){   
    var discountPercentageString=localStorage.getItem('discountPercentage');
    var discountPercentages=JSON.parse(discountPercentageString);
    }
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
    var total_tax=Math.round((total_price-total_discount)*0.0825*100)/100;
    // Grand total after adding total price, total tax and shipping
    var grand_total=Math.round((total_price+total_tax-total_discount+15)*100)/100;
    localStorage.setItem('totalPrice', total_price);
    localStorage.setItem('totalTax', total_tax);
    localStorage.setItem('grandTotal', grand_total);
    localStorage.setItem('discount', total_discount);
    //Closing the modal and removing the modal backdrop 
    var modalID='#product'+product_no
    $(modalID).modal('hide');
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
  });

  $(".discountDetails").text(function(e){
      if(e.target.value===8){
          return "50%"
      }
  });

