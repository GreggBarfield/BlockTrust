const updateShoppingCartTotalsInLocalStorage = () =>{
    let shoppingCartString = localStorage.getItem("shoppingCart");
    let shoppingCart = JSON.parse(shoppingCartString);
    let totalPrice = 0;
    for(let productData of Object.values(shoppingCart)){
        totalPrice = totalPrice + productData.price * productData.quantity;
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
                let productPrice = productData.price * productData.quantity;
                totalDiscount = totalDiscount + productPrice * discountPercentages[productData.product_id]/100;
            }
        }
    }
    totalDiscount = Math.round(totalDiscount*100)/100;
    let totalTax = Math.round((totalPrice-totalDiscount)*0.065*100)/100;
    let grandTotal = Math.round((totalPrice+totalTax-totalDiscount+20)*100)/100;
    let totalShipping = calculateTotalShipping(shoppingCart);
    localStorage.setItem('shipping', totalShipping);
    localStorage.setItem('discount', totalDiscount);
    localStorage.setItem('totalTax', totalTax);
    localStorage.setItem('grandTotal', grandTotal);
}

const calculateTotalShipping = (shoppingCart) =>{
    let totalShipping = 0;
    let totalTags = 0;
    for(let productData of Object.values(shoppingCart)){
        totalTags = totalTags + productData.quantity * productData.product_units_per_order;
    }
    if(totalTags <= 1000){
        totalShipping = getShippingBasedOnQuantity(totalTags);
    }
    else{
        totalShipping = 40 * Math.floor(totalTags/1000) + getShippingBasedOnQuantity(totalTags%1000);
    }
    return totalShipping;
}

const getShippingBasedOnQuantity = (quantity) =>{
    let shipping = 0;
    if(quantity<300){
        shipping = 15;
    }
    else if(quantity >= 300 && quantity <= 500){
        shipping = 20;
    }
    else if(quantity > 500 && quantity <=1000){
        shipping = 40;
    }
    return shipping;
}

const makeShoppingCartTotalsContainer = (shoppingCartTotalsData) =>{
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
            subtotal: {name: "Subtotal", value: parseFloat(localStorage.getItem("totalPrice")).toFixed(2)},
            shipping: {name: "Shipping", value: localStorage.getItem("shipping")},
            tax: {name: "Tax", value: parseFloat(localStorage.getItem("totalTax")).toFixed(2)},
            discount: {name: "Discount", value: localStorage.getItem("discount")},
            total: {name: "Total", value: parseFloat(localStorage.getItem("grandTotal")).toFixed(2)}
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
        location.reload();
    }
    return removeButton;
}

const makeShoppingCartTable = (shoppingCart, includeRemoveProductButton, shopHomepageLink) =>{
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
    if(shoppingCart == null){
        window.location.href = shopHomepageLink;
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
    let productQuantityCell = generateTableCell(productData.quantity+" "+productData.product_units, "td", "h6");
    tableProductRow.append(productQuantityCell);
    let productPriceCell = generateTableCell("$" + productData.price.toFixed(2), "td", "h6");
    tableProductRow.append(productPriceCell);
    let productTotal = productData.price * productData.quantity;
    let productTotalCell = generateTableCell("$" + productTotal.toFixed(2), "td", "h6");
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

const validateFormCompletion = (formResponseInputs) =>{
    let formCompletionStatus = true;
    for(let input of formResponseInputs){
        if(input.value == "" || input.value == -1){
            formCompletionStatus = false;
        }
    }
    return formCompletionStatus;
}

const generateAccountAndShippingInformationContainer = (orderDetails) =>{
    let accountAndShippingInformationContainer = document.createElement("div");
    accountAndShippingInformationContainer.className = "col-md-12 d-flex m-2";
    let accountInformationContainer = document.createElement("div");
    accountInformationContainer.className = "col-md-6 m-0 p-0";
    let headerLine = generateFormattedTextLine("Account Information", "h6", "font-weight-bold text-secondary");
    accountInformationContainer.append(headerLine);
    let nameLine = generateFormattedTextLine(orderDetails.first_name + " " + orderDetails.last_name, "h6", "font-weight-bold text-primary");
    accountInformationContainer.append(nameLine);
    let addressLine = generateFormattedTextLine(orderDetails.address_line, "h6", "font-weight-bold text-primary");
    accountInformationContainer.append(addressLine);
    let cityLine = generateFormattedTextLine(orderDetails.city + ", " + orderDetails.state + " " +orderDetails.zip_code,"h6", "font-weight-bold text-primary");
    accountInformationContainer.append(cityLine);
    accountAndShippingInformationContainer.append(accountInformationContainer);
    let shippingInformationContainer = document.createElement("div");
    shippingInformationContainer.className = "col-md-6 m-0 p-0";
    let shippingHeaderLine = generateFormattedTextLine("Shipping Information", "h6", "font-weight-bold text-secondary");
    shippingInformationContainer.append(shippingHeaderLine);
    let shippingNameLine = generateFormattedTextLine(orderDetails.first_name + " " + orderDetails.last_name, "h6", "font-weight-bold text-primary");
    shippingInformationContainer.append(shippingNameLine);
    let shippingAddressLine = generateFormattedTextLine(orderDetails.address_line, "h6", "font-weight-bold text-primary");
    shippingInformationContainer.append(shippingAddressLine);
    let shippingCityLine = generateFormattedTextLine(orderDetails.city + ", " + orderDetails.state + " " +orderDetails.zip_code,"h6", "font-weight-bold text-primary");
    shippingInformationContainer.append(shippingCityLine);
    accountAndShippingInformationContainer.append(shippingInformationContainer);

    return accountAndShippingInformationContainer;
}

const generateFormattedTextLine = (textContent, textSize, textClassName) =>{
    let customText = document.createElement(textSize);
    customText.textContent = textContent;
    customText.className = textClassName;
    let lineBreak = document.createElement("br");
    customText.appendChild(lineBreak);
    return customText;
}

export {
    updateShoppingCartTotalsInLocalStorage,
    makeShoppingCartTotalsContainer,
    getShoppingCartTotalsData,
    generateButtonLink,
    generateRemoveProductButton,
    makeShoppingCartTable,
    generateCheckoutFormTextInput,
    validateFormCompletion,
    generateAccountAndShippingInformationContainer,
    generateFormattedTextLine
};