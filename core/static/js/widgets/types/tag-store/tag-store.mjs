import { InfoModal } from '../../../core/info_modal.mjs';
import { Widget } from '../../widget.mjs';

export class TagStoreWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {

        this.allProductData = JSON.parse(this.frame.getAttribute("data-widget-all-product-data"));
        this.productCategories = JSON.parse(this.frame.getAttribute("data-widget-product-categories"));
        this.productVendorIdsToNames = JSON.parse(this.frame.getAttribute("data-widget-product-vendor-ids-to-names"));

        this.frame.innerHTML = "";
        this.makeTagStore();
    }

    makeTagStore = () => {
        for(let productCategory of this.productCategories){
            let sectionalContainer = this.makeCategoryContainer(productCategory);
            this.appendProductsToCategoryContainer(sectionalContainer, productCategory);
            this.frame.append(sectionalContainer);
        }
    }

    makeCategoryContainer = (productCategory) => {
        let card = document.createElement("div");
        card.className = "card border rounded";
        let createGroupName = document.createElement("h3");
        createGroupName.className = "mt-2 p-1";
        createGroupName.textContent = productCategory.category_name;
    
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between p-1";
        cardHeader.append(createGroupName);
        card.append(cardHeader);
        return card;
    }

    appendProductsToCategoryContainer = (sectionalContainer, productCategory) =>{
        let cardBody = document.createElement("div");
        cardBody.className = "card-body row";
        sectionalContainer.append(cardBody);
        for(let product of this.allProductData){
            if(product.is_active == 1 && product.product_category_id == productCategory.id){
                let productCard = document.createElement("div");
                productCard.className = "card col-md-4 border border-dark rounded";

                let productCardBody = document.createElement("div");
                productCardBody.className = "card-body";

                let productImage = document.createElement("img");
                productImage.className = "img img-fluid";
                productImage.src = product.pic_1_url;
                productCardBody.append(productImage);
                productCard.append(productCardBody);

                let productCardFooter = document.createElement("div");
                productCardFooter.className = "card-footer text-center row p-1";

                let productCardFooterDetails = document.createElement("div");
                productCardFooterDetails.className = "col-md-8 text-center";
                let productCardFooterProductName = document.createElement("h4");
                productCardFooterProductName.textContent = product.product;
                let productCardFooterVendor = document.createElement("h6");
                productCardFooterVendor.textContent = "Offered by " + this.productVendorIdsToNames[product.product_vendor_id];
                productCardFooterDetails.append(productCardFooterProductName);
                productCardFooterDetails.append(productCardFooterVendor);
                productCardFooter.append(productCardFooterDetails);

                let productCardFooterModalButtonContainer = document.createElement("div");
                productCardFooterModalButtonContainer.className = "col-md-4 pt-2";
                let addToCartButton = document.createElement("button");

                addToCartButton.className = "btn btn-outline-primary m-0 p-1";
                addToCartButton.textContent = "Add to Cart";
                addToCartButton.onclick = () =>{
                    this.generateProductInfoModal(product.id);
                }
                productCardFooterModalButtonContainer.append(addToCartButton);
                productCardFooter.append(productCardFooterModalButtonContainer);
                productCard.append(productCardFooter);
                    
                cardBody.append(productCard);
            }
        }
    }

    generateProductInfoModal = (productID) =>{
        let productData = {};
        for(let product of this.allProductData){
            if(product.id === productID){
                productData = product;
            }
        }
        let infoModal = new InfoModal(productData.product, null, true);
        let modalBody = infoModal.getBody();
        
        let modalContainer = document.createElement("div");
        modalContainer.className = "row vcenter";
        let imageContainer = document.createElement("div");
        imageContainer.className = "col-md-6";
        let secondaryImage = document.createElement("img");
        secondaryImage.className = "img img-fluid";
        secondaryImage.src = productData.pic_2_url;
        imageContainer.append(secondaryImage);
        modalContainer.append(imageContainer);

        let productDetailsContainer = document.createElement("div");
        productDetailsContainer.className = "col-md-6";
        let productTitle = document.createElement("h4");
        productTitle.textContent = productData.product;
        productDetailsContainer.append(productTitle);

        let productDescriptionList = productData.details.split(";");
        let productDescriptionListElement = document.createElement("ul");
        for(const description of productDescriptionList){
            let listElement = document.createElement("li");
            listElement.textContent = description;
            productDescriptionListElement.appendChild(listElement);
        }
        productDetailsContainer.append(productDescriptionListElement);
        
        let productPriceContainer = document.createElement("p");
        productPriceContainer.className = "m-2 d-flex";
        let productPriceIcon = document.createElement("i");
        productPriceIcon.className = "far fa-bookmark mr-1";
        productPriceContainer.append(productPriceIcon);
        let productPrice = document.createElement("h6");
        productPrice.textContent = "Price: $" + productData.price;
        productPriceContainer.append(productPrice);
        productDetailsContainer.append(productPriceContainer);

        
        let productUnitsContainer = document.createElement("p");
        productUnitsContainer.className = "m-2 d-flex";
        let productUnitsIcon = document.createElement("i");
        productUnitsIcon.className = "far fa-bookmark mr-1";
        productUnitsContainer.append(productUnitsIcon);
        let productUnits = document.createElement("h6");
        productUnits.textContent = "Units: " + productData.unit;
        productUnitsContainer.append(productUnits);
        productDetailsContainer.append(productUnitsContainer);

        modalContainer.append(productDetailsContainer);

        let modalFooter = infoModal.getFooter();

        let addProductToCartButton = document.createElement("button");
        addProductToCartButton.className = "btn btn-primary"
        addProductToCartButton.textContent = "Add To Cart";
        modalFooter.prepend(addProductToCartButton);

        let productQuantityInput = document.createElement("input");
        productQuantityInput.className = "m-2 col-sm-2";
        productQuantityInput.value = 1;
        productQuantityInput.type = "number";
        productQuantityInput.min = 1;
        modalFooter.prepend(productQuantityInput);
        
        let productQuantityText = document.createElement("p");
        productQuantityText.className = "m-0 p-1";
        productQuantityText.textContent = "Select Quantity: ";
        modalFooter.prepend(productQuantityText);
        addProductToCartButton.onclick = () => {
            this.updateShoppingCart(productData.id, parseInt(productQuantityInput.value));
            infoModal.close();
        } 

        modalBody.append(modalContainer);
    }

    updateShoppingCart = (productID, productQuantity) => {
        let shoppingCartAge=localStorage.getItem('shoppingCartAge');
        if(shoppingCartAge===null){
            localStorage.setItem('shoppingCartAge', new Date().getTime())  
        }
        if(shoppingCartAge && (new Date().getTime()-shoppingCartAge>60*60*1000)){
            localStorage.clear();
        }
        if(!localStorage.shoppingCart){
            localStorage.setItem('shoppingCart', JSON.stringify({}));
            localStorage.setItem('shipping', 20.00)
            localStorage.setItem('totalPrice', 0);
            localStorage.setItem('discount', 0);
            localStorage.setItem('discountPercentage', JSON.stringify({}));
            localStorage.setItem('discountApplied', "N");
            localStorage.setItem('isPremiseIdRequired', 0);
        }
        this.updateShoppingCartDataInLocalStorage(productID, productQuantity);
        this.updateShoppingCartTotalsInLocalStorage();
    }

    updateShoppingCartDataInLocalStorage = (productID, productQuantity) =>{
        let shoppingCartString = localStorage.getItem("shoppingCart");
        let shoppingCart = JSON.parse(shoppingCartString);
        let selectedProductData = {};
        for(let productData of this.allProductData){
            if(productData.id === productID){
                selectedProductData = productData;
            }
        }
        let productDataToBeStored = {
            product_id: productID,
            product_price: parseFloat(selectedProductData.price),
            product_name: selectedProductData.product,
            product_quantity: parseInt(productQuantity),
            is_premise_id_required_for_product: parseInt(selectedProductData.is_premise_id_required),
            product_units: selectedProductData.unit
        }
        if(!(productID in shoppingCart)){
            shoppingCart[productID] = productDataToBeStored;
            localStorage.setItem("shoppingCart", JSON.stringify(shoppingCart));
        }
        else{
            let previousProductData = shoppingCart[productID];
            let previousQuantity = parseInt(previousProductData.product_quantity);
            productDataToBeStored.product_quantity = productQuantity + previousQuantity;
            shoppingCart[productID] = productDataToBeStored;
            localStorage.setItem("shoppingCart", JSON.stringify(shoppingCart));
        }
    }

    updateShoppingCartTotalsInLocalStorage = () =>{
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
}