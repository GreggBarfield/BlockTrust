import { InfoModal } from '../../../core/info_modal.mjs';
import { Widget } from '../../widget.mjs';
import { updateShoppingCartTotalsInLocalStorage, generateButtonLink } from '../../utilities/tag_store_utilities.mjs';

export class TagStoreWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {

        let products = JSON.parse(this.frame.getAttribute("data-widget-all-product-data"));
        let productCategories = JSON.parse(this.frame.getAttribute("data-widget-product-categories"));
        let productVendorIdsToNames = JSON.parse(this.frame.getAttribute("data-widget-product-vendor-ids-to-names"));

        this.frame.innerHTML = "";
        let shoppingCartLinkContainer = this.makeShoppingCartLinkContainer();
        this.frame.append(shoppingCartLinkContainer);
        for(let productCategory of productCategories){
            let productCategoryContainer = this.makeProductCategoryContainer(productCategory, products, productVendorIdsToNames);
            this.frame.append(productCategoryContainer);
        }
    }

    makeShoppingCartLinkContainer = () =>{
        let shoppingCartLinkContainer = document.createElement("div");
        shoppingCartLinkContainer.className = "col-md-12 d-flex justify-content-end";
        let shoppingCartLinkButton = generateButtonLink("VIEW CART", "/shop/shopping-cart", true, "fas fa-shopping-cart");
        shoppingCartLinkContainer.append(shoppingCartLinkButton);
        return shoppingCartLinkContainer;
    }

    makeProductCategoryContainer = (productCategory, products, productVendorIdsToNames) => {
        let card = document.createElement("div");
        card.className = "card border rounded";
        let createGroupName = document.createElement("h3");
        createGroupName.className = "mt-2 p-1";
        createGroupName.textContent = productCategory.category_name;
    
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between p-1";
        cardHeader.append(createGroupName);
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body row";
        for(let product of products){
            if(product.is_active == 1 && product.product_category_id == productCategory.id){
                let productCardContainer = document.createElement("div");
                productCardContainer.className = "col-md-4";
                let productCard = document.createElement("div");
                productCard.className = "card border border-dark rounded m-1 p-1";

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
                productCardFooterVendor.textContent = "Offered by " + productVendorIdsToNames[product.product_vendor_id];
                productCardFooterDetails.append(productCardFooterProductName);
                productCardFooterDetails.append(productCardFooterVendor);
                productCardFooter.append(productCardFooterDetails);

                let productCardFooterModalButtonContainer = document.createElement("div");
                productCardFooterModalButtonContainer.className = "col-md-4 pt-2";
                let addToCartButton = document.createElement("button");

                addToCartButton.className = "btn btn-outline-primary m-0 p-2";
                addToCartButton.textContent = "More Details";
                addToCartButton.onclick = () =>{
                    this.generateProductInfoModal(product);
                }
                productCardFooterModalButtonContainer.append(addToCartButton);
                productCardFooter.append(productCardFooterModalButtonContainer);
                productCard.append(productCardFooter);
                productCardContainer.append(productCard);
                
                cardBody.append(productCardContainer);
            }
        }
        // Hide Product category cards that have no products
        if(cardBody.innerHTML.trim() == ""){
            card.className = "d-none";
        }
        card.append(cardBody);
        return card;
    }

    generateProductInfoModal = (productData) =>{
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
        productPrice.textContent = "Price: $" + productData.price.toFixed(2);
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
            this.updateShoppingCart(productData, parseInt(productQuantityInput.value));
            infoModal.close();
        } 

        modalBody.append(modalContainer);
    }

    updateShoppingCart = (productData, productQuantity) => {
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
        this.updateShoppingCartDataInLocalStorage(productData, productQuantity);
        updateShoppingCartTotalsInLocalStorage();
    }

    updateShoppingCartDataInLocalStorage = (productData, productQuantity) =>{
        let shoppingCartString = localStorage.getItem("shoppingCart");
        let shoppingCart = JSON.parse(shoppingCartString);
        let productDataToBeStored = {
            product_id: productData.id,
            price: parseFloat(productData.price),
            product_name: productData.product,
            quantity: parseInt(productQuantity),
            is_premise_id_required_for_product: parseInt(productData.is_premise_id_required),
            product_units: productData.unit,
            vendor_product_reference_id: productData.vendor_product_reference_id,
            product_units_per_order: productData.units_per_order,
            product_vendor_id: productData.product_vendor_id
        }
        if(!(productData.id in shoppingCart)){
            shoppingCart[productData.id] = productDataToBeStored;
            localStorage.setItem("shoppingCart", JSON.stringify(shoppingCart));
        }
        else{
            let previousProductData = shoppingCart[productData.id];
            let previousQuantity = parseInt(previousProductData.quantity);
            productDataToBeStored.quantity = productQuantity + previousQuantity;
            shoppingCart[productData.id] = productDataToBeStored;
            localStorage.setItem("shoppingCart", JSON.stringify(shoppingCart));
        }
    }
}