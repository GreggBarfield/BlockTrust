import { Widget } from '../../widget.mjs';
import { makeShoppingCartTotalsContainer, generateButtonLink, generateRemoveProductButton } from '../../utilities/tag_store_utilities.mjs';

export class ShoppingCartWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () =>{
        this.frame.innerHTML = "";
        let shoppingCart = this.makeShoppingCart();
        this.frame.append(shoppingCart);
    }

    makeShoppingCart = () =>{
        let card = document.createElement("div");
        card.className = "card border rounded";
        
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header d-flex justify-content-center p-1";
        let cardHeaderText = document.createElement("h3");
        cardHeaderText.className = "mt-2 p-1";
        cardHeaderText.textContent = "SHOPPING CART";
    
        cardHeader.append(cardHeaderText);
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body row";

        let shoppingCartTable = this.makeShoppingCartTable();
        cardBody.append(shoppingCartTable);
        let shoppingCartTotals = makeShoppingCartTotalsContainer();
        cardBody.append(shoppingCartTotals);
        let shoppingCartPageLinks = this.makeShoppingCartPageLinksContainer();
        cardBody.append(shoppingCartPageLinks);

        card.append(cardBody);
        return card;
    }

    makeShoppingCartTable = () =>{
        let shoppingCartTable = document.createElement("table");
        shoppingCartTable.className = "table table-striped";
        let shoppingCartTableHead = document.createElement("thead");
        shoppingCartTableHead.className = "thead thead-primary";
        let shoppingCartTableHeadRow = document.createElement("tr");
        let shoppingCartHeaderElements = ["PRODUCT", "QUANTITY", "PRICE", "TOTAL", ""];
        for(let headerElement of shoppingCartHeaderElements){
            let headerCell = this.generateTableCell(headerElement, "th", "h5");
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
            let shoppingCartTableProductRow = this.makeShoppingCartTableProductRow(productData);
            shoppingCartTableBody.append(shoppingCartTableProductRow);
        }
        shoppingCartTable.append(shoppingCartTableBody);
        return shoppingCartTable;
    }

    makeShoppingCartTableProductRow = (productData) =>{
        let tableProductRow = document.createElement("tr");

        let productNameCell = this.generateTableCell(productData.product_name, "td", "h6");
        tableProductRow.append(productNameCell);
        let productQuantityCell = this.generateTableCell(productData.product_quantity+" "+productData.product_units, "td", "h6");
        tableProductRow.append(productQuantityCell);
        let productPriceCell = this.generateTableCell("$" + productData.product_price, "td", "h6");
        tableProductRow.append(productPriceCell);
        let productTotalCell = this.generateTableCell("$" + productData.product_price * productData.product_quantity, "td", "h6");
        tableProductRow.append(productTotalCell);
        let removeProductButtonCell = document.createElement("td");
        let removeProductButton = generateRemoveProductButton(productData.product_id);
        removeProductButtonCell.append(removeProductButton);
        tableProductRow.append(removeProductButtonCell);

        return tableProductRow;
    }

    generateTableCell = (cellText, cellType, textSize) =>{
        let tableCell = document.createElement(cellType);
        let tableCellText = document.createElement(textSize);
        tableCellText.textContent = cellText;
        tableCell.appendChild(tableCellText);
        return tableCell;
    }

    makeShoppingCartPageLinksContainer = () =>{
        let linksContainer = document.createElement("div");
        linksContainer.className = "col-md-12 d-flex justify-content-end";

        let continueShoppingButton = generateButtonLink("CONTINUE SHOPPING  ", "/shop/tag-store", true, "fas fa-shopping-cart");
        linksContainer.append(continueShoppingButton);
        let proceedToCheckoutButton = generateButtonLink("PROCEED TO CHECKOUT  ", "/shop/tag-store", true, "fas fa-credit-card");
        linksContainer.append(proceedToCheckoutButton);
        return linksContainer;
    }
}