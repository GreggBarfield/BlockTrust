import { Widget } from '../../widget.mjs';

export class SeedstockProducersWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        let seedstockProducers = JSON.parse(this.frame.getAttribute("data-widget-seedstock-producers"));
        this.frame.innerHTML = "";
        let seedstockProducersContainer = this.makeSeedstockProducersContainer(seedstockProducers);
        this.frame.append(seedstockProducersContainer);
    }

    makeSeedstockProducersContainer = (seedstockProducers) =>{
        let seedstockProducersContainer = document.createElement("div");
        seedstockProducersContainer.className = "card col-md-12";
        
        let seedstockProducersContainerBody = document.createElement("div");
        seedstockProducersContainerBody.className = "card-body row p-2";

        for(let seedstockProducer of seedstockProducers){
            let seedstockProducerCard = this.generateSeedstockProducerCard(seedstockProducer); 
            seedstockProducersContainerBody.append(seedstockProducerCard);
        }
        seedstockProducersContainer.append(seedstockProducersContainerBody);
        return seedstockProducersContainer;
    }

    generateSeedstockProducerCard = (seedstockProducer) =>{
        let cardContainer = document.createElement("card");
        cardContainer.className = "col-md-4";
        let card = document.createElement("div");
        card.className = "card border border-dark rounded p-2";

        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header row p-0";

        if(seedstockProducer.logo_url !== null){
            let cardHeaderLogoContainer = document.createElement("div");
            cardHeaderLogoContainer.className = "col-md-3";
            let logo = document.createElement("img");
            logo.className = "img img-fluid";
            logo.src = seedstockProducer.logo_url;
            cardHeaderLogoContainer.append(logo);
            cardHeader.append(cardHeaderLogoContainer);
        }

        let cardHeaderTextContainer = document.createElement("div");
        cardHeaderTextContainer.className = "col-md-9";
        let cardHeaderText = document.createElement("h4");
        cardHeaderText.className = "row m-1 p-1";
        cardHeaderText.textContent = seedstockProducer.marketplace_account_name;
        cardHeaderTextContainer.append(cardHeaderText);

        let cardHeaderSecondaryText = document.createElement("h5");
        cardHeaderSecondaryText.className = "row m-1 p-1";
        cardHeaderSecondaryText.textContent = seedstockProducer.short_description;
        cardHeaderTextContainer.append(cardHeaderSecondaryText);

        cardHeader.append(cardHeaderTextContainer);
        card.append(cardHeader);

        let cardBody = document.createElement("card-body");
        cardBody.className = "card-body";

        let descriptionContainer = document.createElement("div");
        let descriptionText = document.createElement("h5");
        descriptionText.className = "font-weight-normal";
        descriptionText.textContent = seedstockProducer.long_description;
        descriptionContainer.append(descriptionText);
        cardBody.append(descriptionContainer);

        let horizontalRule = document.createElement("hr");
        cardBody.append(horizontalRule);

        let companyInformationContainer = this.generateCompanyInformationContainer(seedstockProducer);
        cardBody.append(companyInformationContainer);

        card.append(cardBody);
        cardContainer.append(card);
        return cardContainer;
    }

    generateCompanyInformationContainer = (seedstockProducer) =>{
        let companyInformationContainer = document.createElement("div");
        let addressLine = this.generateFormattedTextLine(seedstockProducer.address, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(addressLine);
        let cityLine = this.generateFormattedTextLine(seedstockProducer.city + ", " + seedstockProducer.state + " " +seedstockProducer.zip_code, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(cityLine);
        let contactNameLine = this.generateFormattedTextLine(seedstockProducer.marketplace_account_contact_name, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(contactNameLine);
        let phoneLine = this.generateFormattedTextLine(seedstockProducer.marketplace_account_phone, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(phoneLine);
        let emailLine = this.generateFormattedTextLine(seedstockProducer.marketplace_account_email, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(emailLine);

        return companyInformationContainer;
    }

    generateFormattedTextLine = (textContent, textSize, textClassName) =>{
        let customText = document.createElement(textSize);
        customText.textContent = textContent;
        customText.className = textClassName;
        let lineBreak = document.createElement("br");
        customText.appendChild(lineBreak);
        return customText;
    }
}