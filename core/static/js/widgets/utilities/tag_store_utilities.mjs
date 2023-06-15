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

const makeShoppingCartTable = (includeRemoveProductButton) =>{
    let shoppingCartTable = document.createElement("table");
    shoppingCartTable.className = "table table-striped";
    let shoppingCartTableHead = document.createElement("thead");
    shoppingCartTableHead.className = "thead thead-primary";
    let shoppingCartTableHeadRow = document.createElement("tr");
    let shoppingCartHeaderElements = ["PRODUCT", "QUANTITY", "PRICE", "TOTAL"];
    if(includeRemoveProductButton){
        shoppingCartHeaderElements = ["PRODUCT", "QUANTITY", "PRICE", "TOTAL", ""];
    }  
    for(let headerElement of shoppingCartHeaderElements){
        let headerCell = generateTableCell(headerElement, "th", "h5");
        shoppingCartTableHeadRow.appendChild(headerCell);
    }
    shoppingCartTableHead.append(shoppingCartTableHeadRow);
    shoppingCartTable.append(shoppingCartTableHead);

    let shoppingCartTableBody = document.createElement("tbody"); 
    let shoppingCartString = localStorage.getItem("shoppingCart");
    let shoppingCart = JSON.parse(shoppingCartString);
    if(shoppingCart == null){
        window.location.href = "/shop/tag-store";
        return;
    }
    for(let productData of Object.values(shoppingCart)){
        let shoppingCartTableProductRow = makeShoppingCartTableProductRow(productData, includeRemoveProductButton);
        shoppingCartTableBody.append(shoppingCartTableProductRow);
    }
    shoppingCartTable.append(shoppingCartTableBody);
    return shoppingCartTable;
}

const makeShoppingCartTableProductRow = (productData, includeRemoveProductButton) =>{
    let tableProductRow = document.createElement("tr");

    let productNameCell = generateTableCell(productData.product_name, "td", "h6");
    tableProductRow.append(productNameCell);
    let productQuantityCell = generateTableCell(productData.product_quantity+" "+productData.product_units, "td", "h6");
    tableProductRow.append(productQuantityCell);
    let productPriceCell = generateTableCell("$" + productData.product_price, "td", "h6");
    tableProductRow.append(productPriceCell);
    let productTotalCell = generateTableCell("$" + productData.product_price * productData.product_quantity, "td", "h6");
    tableProductRow.append(productTotalCell);
    if(includeRemoveProductButton){
        let removeProductButtonCell = document.createElement("td");
        let removeProductButton = generateRemoveProductButton(productData.product_id);
        removeProductButtonCell.append(removeProductButton);
        tableProductRow.append(removeProductButtonCell);
    }
    return tableProductRow;
}

const generateTableCell = (cellText, cellType, textSize) =>{
    let tableCell = document.createElement(cellType);
    let tableCellText = document.createElement(textSize);
    tableCellText.textContent = cellText;
    tableCell.appendChild(tableCellText);
    return tableCell;
}

const generateCheckoutFormTextInput = (inputText, inputType, inputId, inputRequired) =>{
    let inputContainer = document.createElement("div");
    inputContainer.className = "col-md-6";
    let input = document.createElement("input");
    input.placeholder = inputText;
    input.type = inputType;
    input.id = inputId;
    input.className = "form-control m-1";
    input.required = inputRequired;
    inputContainer.append(input);
    return inputContainer;
}

export {
    updateShoppingCartTotalsInLocalStorage,
    makeShoppingCartTotalsContainer,
    getShoppingCartTotalsData,
    generateButtonLink,
    generateRemoveProductButton,
    makeShoppingCartTable,
    generateCheckoutFormTextInput
};