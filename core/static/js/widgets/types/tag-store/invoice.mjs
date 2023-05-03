import { Widget } from '../../widget.mjs';
import { makeShoppingCartTable, makeShoppingCartTotalsContainer } from '../../utilities/tag_store_utilities.mjs';

export class InvoiceWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () =>{
        this.frame.innerHTML = "";
        if(localStorage.shoppingCart == null || localStorage.orderDetails == null){
            window.location.href = "/shop/tag-store";
        }
        else{
            let invoiceContainer = this.makeInvoiceContainer();
            this.frame.append(invoiceContainer);
            let returnToShopButton = this.generateReturnToShopButton();
            this.frame.append(returnToShopButton);
        }
        window.addEventListener('beforeunload', ()=>{
            localStorage.clear();
        });
    }

    makeInvoiceContainer = () =>{
        let card = document.createElement("div");
        card.className = "card border rounded";
        card.id = "invoicePage";
        
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header d-flex justify-content-center p-1";
        let cardHeaderText = document.createElement("h3");
        cardHeaderText.className = "mt-2 p-1";
        cardHeaderText.textContent = "INVOICE";
    
        cardHeader.append(cardHeaderText);
        card.append(cardHeader);

        let cardBody = document.createElement("div");
        cardBody.className = "card-body row";

        let orderConfirmationContainer = this.generateOrderConfirmationContainer();
        cardBody.append(orderConfirmationContainer);
        cardBody.append(this.generateHorizontalRule());

        let addressAndPrintButtonContainer = this.generateAddressAndPrintButtonContainer();
        cardBody.append(addressAndPrintButtonContainer);
        cardBody.append(this.generateHorizontalRule());

        let dateContainer = this.generateDateContainer();
        cardBody.append(dateContainer);
        cardBody.append(this.generateHorizontalRule());

        let accountAndShippingInformationContainer = this.generateAccountAndShippingInformationContainer();
        cardBody.append(accountAndShippingInformationContainer);
        cardBody.append(this.generateHorizontalRule());

        let shoppingCartTableContainer = document.createElement("div");
        shoppingCartTableContainer.className = "col-md-12 m-2";
        let shoppingCartTable = makeShoppingCartTable(false);
        shoppingCartTableContainer.append(shoppingCartTable);
        cardBody.append(shoppingCartTableContainer);
        cardBody.append(this.generateHorizontalRule());

        let shoppingCartTotalsContainer = document.createElement("div");
        shoppingCartTotalsContainer.className = "col-md-6 m-2";
        let shoppingCartTotals = makeShoppingCartTotalsContainer();
        shoppingCartTotalsContainer.append(shoppingCartTotals);
        cardBody.append(shoppingCartTotalsContainer);

        card.append(cardBody);
        return card;
    }

    generateOrderConfirmationContainer = () =>{
        let orderConfirmationContainer = document.createElement("div");
        orderConfirmationContainer.className = "col-md-12 m-2";
        let orderConfirmationText = document.createElement("h3");
        orderConfirmationText.textContent = "Order Confirmation:";
        orderConfirmationContainer.append(orderConfirmationText);
        let subText = document.createElement("h5");
        subText.textContent = "Thank you for your order.If you have any questions please ";
        let contactUsLink = document.createElement("a");
        contactUsLink.textContent = "contact us.";
        contactUsLink.href = "/about-us/contact-us";
        subText.appendChild(contactUsLink);
        orderConfirmationContainer.append(subText);
        return orderConfirmationContainer;
    }

    generateAddressAndPrintButtonContainer = () =>{
        let addressAndPrintButtonContainer = document.createElement("div");
        addressAndPrintButtonContainer.className = "col-md-12 d-inline-flex m-2";
        let addressContainer = document.createElement("div");
        addressContainer.className = "col-md-6 p-0 m-0";
        let nameLine = this.generateFormattedTextLine("U.S. CattleTrace", "h6", "font-weight-bold text-secondary");
        addressContainer.append(nameLine);
        let streetLine = this.generateFormattedTextLine("414 Lincoln Ave", "h6", "font-weight-bold text-secondary");
        addressContainer.append(streetLine);
        let cityLine = this.generateFormattedTextLine("Wamego, KS 66475", "h6", "font-weight-bold text-secondary");
        addressContainer.append(cityLine);
        let phoneLine = this.generateFormattedTextLine("785-456-8472", "h6", "font-weight-bold text-secondary");
        addressContainer.append(phoneLine);
        let emailLine = this.generateFormattedTextLine("info@uscattletrace.org", "h6", "font-weight-bold text-secondary");
        addressContainer.append(emailLine);
        addressAndPrintButtonContainer.append(addressContainer);

        let printButtonContainer = document.createElement("div");
        printButtonContainer.className = "col-md-6 d-flex justify-content-end p-0";
        let printButton = this.generatePrintInvoiceButton();
        printButtonContainer.append(printButton);
        addressAndPrintButtonContainer.append(printButtonContainer);

        return addressAndPrintButtonContainer;
    }

    generateDateContainer = () =>{
        let dateContainer = document.createElement("div");
        dateContainer.className = "col-md-12 m-2";
        let currentDate = new Date();
        let date = String(currentDate.getDate()).padStart(2, '0');
        let month = String(currentDate.getMonth() + 1).padStart(2, '0');
        let year = currentDate.getFullYear();
        currentDate = month + "/" + date + "/" + year;
        let dateTextLine = this.generateFormattedTextLine("Date:  " + currentDate, "h6", "font-weight-bold text-secondary");
        dateContainer.append(dateTextLine);
        return dateContainer;
    }

    generateAccountAndShippingInformationContainer = () =>{
        let orderDetailsString=localStorage.getItem("orderDetails");
        let orderDetails=JSON.parse(orderDetailsString);

        let accountAndShippingInformationContainer = document.createElement("div");
        accountAndShippingInformationContainer.className = "col-md-12 d-flex m-2";
        let accountInformationContainer = document.createElement("div");
        accountInformationContainer.className = "col-md-6 m-0 p-0";
        let headerLine = this.generateFormattedTextLine("Account Information", "h6", "font-weight-bold text-secondary");
        accountInformationContainer.append(headerLine);
        let nameLine = this.generateFormattedTextLine(orderDetails.first_name + " " + orderDetails.last_name, "h6", "font-weight-bold text-primary");
        accountInformationContainer.append(nameLine);
        let addressLine = this.generateFormattedTextLine(orderDetails.address_line, "h6", "font-weight-bold text-primary");
        accountInformationContainer.append(addressLine);
        let cityLine = this.generateFormattedTextLine(orderDetails.city + ", " + orderDetails.state + " " +orderDetails.zip_code,"h6", "font-weight-bold text-primary");
        accountInformationContainer.append(cityLine);
        accountAndShippingInformationContainer.append(accountInformationContainer);

        
        let shippingInformationContainer = document.createElement("div");
        shippingInformationContainer.className = "col-md-6 m-0 p-0";
        let shippingHeaderLine = this.generateFormattedTextLine("Shipping Information", "h6", "font-weight-bold text-secondary");
        shippingInformationContainer.append(shippingHeaderLine);
        let shippingNameLine = this.generateFormattedTextLine(orderDetails.first_name + " " + orderDetails.last_name, "h6", "font-weight-bold text-primary");
        shippingInformationContainer.append(shippingNameLine);
        let shippingAddressLine = this.generateFormattedTextLine(orderDetails.address_line, "h6", "font-weight-bold text-primary");
        shippingInformationContainer.append(shippingAddressLine);
        let shippingCityLine = this.generateFormattedTextLine(orderDetails.city + ", " + orderDetails.state + " " +orderDetails.zip_code,"h6", "font-weight-bold text-primary");
        shippingInformationContainer.append(shippingCityLine);
        accountAndShippingInformationContainer.append(shippingInformationContainer);

        return accountAndShippingInformationContainer;
    }

    generateFormattedTextLine = (textContent, textSize, textClassName) =>{
        let customText = document.createElement(textSize);
        customText.textContent = textContent;
        customText.className = textClassName;
        let lineBreak = document.createElement("br");
        customText.appendChild(lineBreak);
        return customText;
    }

    generatePrintInvoiceButton = () =>{ 
        let button = document.createElement("button");
        button.className = "btn btn-outline-primary h-25 rounded p-2";
        button.textContent = "PRINT";
        button.onclick = () =>{
            let invoicePage = document.getElementById("invoicePage");
            let printWindow = window.open('', '', 'width=1100,height=900');
            printWindow.document.write('<html><head><title>Print Invoice</title><link rel="stylesheet" href="/static/build/build_dashboard_main.min.css" /></head><body>');
            printWindow.document.write(invoicePage.innerHTML);
            printWindow.document.write('</body></html>');
            printWindow.document.close();
            printWindow.focus();
            setTimeout(function() {
                printWindow.print();
                printWindow.close();
            }, 1000);
        }
        return button;
    }

    generateHorizontalRule = () =>{
        let horizontalRule = document.createElement("div");
        horizontalRule.className = "d-inline-block w-100 border-top";
        return horizontalRule;
    }

    generateReturnToShopButton = () =>{
        let button = document.createElement("button");
        button.className = "btn btn-outline-primary rounded";
        button.textContent = "RETURN TO SHOP";
        let icon = document.createElement("i");
        icon.className = "fas fa-shopping-cart";
        button.appendChild(icon);
        button.onclick = () =>{
            localStorage.clear();
            window.location.href = "/shop/tag-store";
        }
        return button;
    }
}