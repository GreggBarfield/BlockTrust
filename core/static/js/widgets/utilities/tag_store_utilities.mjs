const updateShoppingCartTotalsInLocalStorage = () =>{
    let shoppingCartString = localStorage.getItem("shoppingCart");
    let shoppingCart = JSON.parse(shoppingCartString);
    let totalPrice = 0;
    for(let productData of Object.values(shoppingCart)){
        totalPrice = totalPrice + productData.product_price * productData.product_quantity;
        if(productData.is_premise_id_required == 1){
            localStorage.setItem("isPremiseIdRequired", 1);
        }
    }
    totalPrice=Math.round(totalPrice*100)/100;
    localStorage.setItem('totalPrice', totalPrice);

    let totalDiscount = 0;
    let discountApplied = localStorage.getItem("discountApplied");   
    let discountPercentageString = localStorage.getItem("discountPercentage");
    let discountPercentages = JSON.parse(discountPercentageString);
    if(discountApplied === "Y"){
        for(let productData of Object.values(shoppingCart)){
            if(discountPercentages[productData.product_id] !== null){
                let productPrice = productData.product_price * productData.product_quantity;
                totalDiscount = totalDiscount + productPrice * discountPercentages[productData.product_id]/100;
            }
        }
    }
    totalDiscount = Math.round(totalDiscount*100)/100;
    let totalTax = Math.round((totalPrice-totalDiscount)*0.065*100)/100;
    let grandTotal = Math.round((totalPrice+totalTax-totalDiscount+20)*100)/100;
    localStorage.setItem('discount', totalDiscount);
    localStorage.setItem('totalTax', totalTax);
    localStorage.setItem('grandTotal', grandTotal);
}

const makeShoppingCartTotalsContainer = () =>{
    let totalsContainer = document.createElement("div");

    let totalsCardHeader = document.createElement("div");
    totalsCardHeader.className = "card-header d-flex justify-content-center p-1";
    let totalsCardHeaderText = document.createElement("h4");
    totalsCardHeaderText.className = "mt-2 p-1";
    totalsCardHeaderText.textContent = "CART TOTAL";

    totalsCardHeader.append(totalsCardHeaderText);
    totalsContainer.append(totalsCardHeader);

    let totalsCardBody = document.createElement("div");
    totalsCardBody.className = "card-body row";

    let leftSubColumn = document.createElement("div");
    leftSubColumn.className = "col sub-col-left";
    let rightSubColumn = document.createElement("div");
    rightSubColumn.className = "col sub-col-right";

    let shoppingCartTotalsData = getShoppingCartTotalsData();
    for(let shoppingCartDataField of Object.values(shoppingCartTotalsData)){
        let leftColumnCell = document.createElement("p");
        leftColumnCell.textContent = shoppingCartDataField.name;
        leftColumnCell.className = "border-bottom";
        leftSubColumn.append(leftColumnCell);
        let rightColumnCell = document.createElement("p");
        rightColumnCell.textContent = "$" + shoppingCartDataField.value;
        rightColumnCell.className = "text-primary border-bottom";
        rightSubColumn.append(rightColumnCell);
    }
    totalsCardBody.appendChild(leftSubColumn);
    totalsCardBody.appendChild(rightSubColumn);
    totalsContainer.append(totalsCardBody);

    return totalsContainer;
}

const getShoppingCartTotalsData = () =>{
    let shoppingCartTotalsData = {};
    if(!localStorage.shoppingCart){
        shoppingCartTotalsData = {
            subtotal: {name: "Subtotal", value: 0},
            shipping: {name: "Shipping", value: 20},
            tax: {name: "Tax", value: 0},
            discount: {name: "Discount", value: 0},
            total: {name: "Total", value: 0}
        }
    }
    else{
        shoppingCartTotalsData = {
            subtotal: {name: "Subtotal", value: localStorage.getItem("totalPrice")},
            shipping: {name: "Shipping", value: localStorage.getItem("shipping")},
            tax: {name: "Tax", value: localStorage.getItem("totalTax")},
            discount: {name: "Discount", value: localStorage.getItem("discount")},
            total: {name: "Total", value: localStorage.getItem("grandTotal")}
        }
    }
    return shoppingCartTotalsData;
}

const generateButtonLink = (buttonText, link, addIcon=false, iconType="") =>{
    let button = document.createElement("button");
    button.className = "btn btn-outline-primary rounded";
    button.textContent = buttonText;
    if(addIcon==true){
        let icon = document.createElement("i");
        icon.className = iconType;
        button.appendChild(icon);
    }
    button.onclick = () =>{
        window.location.href = link;
    }
    return button;
}

const generateRemoveProductButton = (product_id) =>{
    let removeButton = document.createElement("button");
    removeButton.className = "btn btn-outline-primary rounded p-1 m-0";
    removeButton.textContent = "Remove";
    removeButton.onclick = () =>{ 
        let shoppingCartString = localStorage.getItem("shoppingCart");
        let shoppingCart = JSON.parse(shoppingCartString);
        delete shoppingCart[product_id];
        localStorage.setItem('shoppingCart', JSON.stringify(shoppingCart));
        updateShoppingCartTotalsInLocalStorage();
        window.location.href = "/shop/shopping-cart";
    }
    return removeButton;
}

export {
    updateShoppingCartTotalsInLocalStorage,
    makeShoppingCartTotalsContainer,
    getShoppingCartTotalsData,
    generateButtonLink,
    generateRemoveProductButton
};