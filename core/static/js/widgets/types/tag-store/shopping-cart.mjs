import { Widget } from '../../widget.mjs';
import { makeShoppingCartTotalsContainer, generateButtonLink, getShoppingCartTotalsData, makeShoppingCartTable } from '../../utilities/tag_store_utilities.mjs';

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

        let shoppingCartString = localStorage.getItem("shoppingCart");
        let shoppingCart = JSON.parse(shoppingCartString);
        let shoppingCartTable = makeShoppingCartTable(shoppingCart, true);
        cardBody.append(shoppingCartTable);
        let shoppingCartTotalsContainer = document.createElement("div");
        shoppingCartTotalsContainer.className = "col-md-6";
        let shoppingCartTotalsData = getShoppingCartTotalsData();
        let shoppingCartTotals = makeShoppingCartTotalsContainer(shoppingCartTotalsData);
        shoppingCartTotalsContainer.append(shoppingCartTotals);
        cardBody.append(shoppingCartTotalsContainer);
        let shoppingCartPageLinks = this.makeShoppingCartPageLinksContainer();
        cardBody.append(shoppingCartPageLinks);

        card.append(cardBody);
        return card;
    }

    makeShoppingCartPageLinksContainer = () =>{
        let linksContainer = document.createElement("div");
        linksContainer.className = "col-md-12 d-flex justify-content-end";

        let continueShoppingButton = generateButtonLink("CONTINUE SHOPPING  ", "/shop/tag-store", true, "fas fa-shopping-cart");
        linksContainer.append(continueShoppingButton);
        let proceedToCheckoutButton = generateButtonLink("PROCEED TO CHECKOUT  ", "/shop/checkout", true, "fas fa-credit-card");
        linksContainer.append(proceedToCheckoutButton);
        return linksContainer;
    }
}