import { Widget } from '../../widget.mjs';
import { generateAccountAndShippingInformationContainer, makeShoppingCartTable, makeShoppingCartTotalsContainer } from '../../utilities/tag_store_utilities.mjs';

export class ViewOrderWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () =>{
        this.frame.innerHTML = "";
        let order = this.transformOrderData(JSON.parse(this.frame.getAttribute("data-widget-order")));
        let shoppingCart = this.transformOrderProductsData(JSON.parse(this.frame.getAttribute("data-widget-order-products")));
        let orderContainer = this.makeOrderContainer(order, shoppingCart);
        this.frame.append(orderContainer);
    }

    transformOrderData = (order) =>{
        order.address_line = order.shipping_address;
        order.city = order.shipping_city;
        order.state = order.shipping_state;
        order.zip_code = order.shipping_zip;
        return order;
    }

    transformOrderProductsData = (orderProducts) =>{
        let formattedProductData = {};
        for(let product of orderProducts){
            let productDetails = product.product_details;
            let productShoppingCartDetails = {
                is_premise_id_required_for_product: productDetails.is_premise_id_required,
                price: productDetails.price,
                product_id: productDetails.id,
                product_name: productDetails.product,
                product_units: productDetails.unit,
                quantity: product.product_quantity,
                vendor_product_reference_id: productDetails.vendor_product_reference_id
            }
            formattedProductData[productDetails.id] = productShoppingCartDetails; 
        }
        return formattedProductData;
    }

    getOrderTotals = (order) =>{
        let orderTotals = {
            subtotal: {name: "Subtotal", value: order.total_cart},
            shipping: {name: "Shipping", value: order.total_shipping},
            tax: {name: "Tax", value: order.total_tax},
            discount: {name: "Discount", value: order.discount},
            total: {name: "Total", value: order.grand_total}
        }
        return orderTotals;
    }

    makeOrderContainer = (order, shoppingCart) =>{
        let orderCard = document.createElement("div");
        orderCard.className = "card border rounded";

        let orderCardHeader = document.createElement("div");
        orderCardHeader.className = "card-header d-flex justify-content-center p-1";
        let orderCardHeaderText = document.createElement("h3");
        orderCardHeaderText.className = "mt-2 p-1";
        orderCardHeaderText.textContent = "ORDER #" + order.id;
        orderCardHeader.append(orderCardHeaderText);
        orderCard.append(orderCardHeader);

        let orderCardBody = document.createElement("div");
        orderCardBody.className = "card-body";
        let accountAndShippingInformationContainer = generateAccountAndShippingInformationContainer(order);
        orderCardBody.append(accountAndShippingInformationContainer);
        let shoppingCartTable = makeShoppingCartTable(shoppingCart, false);
        orderCardBody.append(shoppingCartTable);

        let orderTotalsContainer = document.createElement("div");
        orderTotalsContainer.className = "col-md-6 m-2";
        let orderTotalsData = this.getOrderTotals(order);
        let orderTotalsTable = makeShoppingCartTotalsContainer(orderTotalsData);
        orderTotalsContainer.append(orderTotalsTable);
        orderCardBody.append(orderTotalsContainer);

        orderCard.append(orderCardBody);
        return orderCard;
    }
}