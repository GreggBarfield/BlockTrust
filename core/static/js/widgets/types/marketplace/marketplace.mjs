import { Widget } from '../../widget.mjs';

export class MarketPlaceWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        let advertisementData = await this.getData("get_advertisements");
        let advertisements = this.formatAdvertisementData(advertisementData.advertisements, advertisementData.advertisement_category_ids_to_names);

        this.frame.innerHTML = "";
        let advertisementContainer = this.makeAdvertisementContainer(advertisements);
        this.frame.append(advertisementContainer);
    }

    formatAdvertisementData = (advertisements, advertisementCategoryIdsToNames) =>{
        for(let advertisement of advertisements){
            advertisement.advertisementCategoryName = advertisementCategoryIdsToNames[advertisement.ad_category_id];
        }
        // Sorting the advertisment data by advertisement category name and by advertisement company name.
        advertisements.sort((a, b) => 
        (a.advertisementCategoryName > b.advertisementCategoryName) ? 1
            : (a.advertisementCategoryName === b.advertisementCategoryName)? ((a.name > b.name) ? 1: -1)
            : -1
        );
        return advertisements;
    }

    makeAdvertisementContainer = (advertisements) =>{
        let advertisementsContainer = document.createElement("div");
        advertisementsContainer.className = "card col-md-12";
        
        let advertisementsContainerBody = document.createElement("div");
        advertisementsContainerBody.className = "card-body row p-2";

        for(let advertisement of advertisements){
            let advertisementCard = this.generateAdvertisementCard(advertisement); 
            advertisementsContainerBody.append(advertisementCard);
        }
        advertisementsContainer.append(advertisementsContainerBody);
        return advertisementsContainer;
    }

    generateAdvertisementCard = (advertisement) =>{
        let advertisementCardContainer = document.createElement("div");
        advertisementCardContainer.className = "col-md-4";
        let advertisementCard = document.createElement("div")
        advertisementCard.className = "card border border-dark rounded p-2";

        let advertisementCardHeader = document.createElement("div");
        advertisementCardHeader.className = "card-header row p-0";

        if(advertisement.logo_url !== null){
            let advertisementCardHeaderLogoContainer = document.createElement("div");
            advertisementCardHeaderLogoContainer.className = "col-md-3";
            let advertisementLogo = document.createElement("img");
            advertisementLogo.className = "img img-fluid";
            advertisementLogo.src = advertisement.logo_url;
            advertisementCardHeaderLogoContainer.append(advertisementLogo);
            advertisementCardHeader.append(advertisementCardHeaderLogoContainer);
        }

        let advertisementCardHeaderTextContainer = document.createElement("div");
        advertisementCardHeaderTextContainer.className = "col-md-9";
        let advertisementCardHeaderText = document.createElement("h4");
        advertisementCardHeaderText.className = "row m-1 p-1";
        advertisementCardHeaderText.textContent = advertisement.name + " (" + advertisement.advertisementCategoryName + ")";
        advertisementCardHeaderTextContainer.append(advertisementCardHeaderText);

        let advertismentCardHeaderSecondaryText = document.createElement("h5");
        advertismentCardHeaderSecondaryText.className = "row m-1 p-1";
        advertismentCardHeaderSecondaryText.textContent = advertisement.short_description;
        advertisementCardHeaderTextContainer.append(advertismentCardHeaderSecondaryText);

        advertisementCardHeader.append(advertisementCardHeaderTextContainer);
        advertisementCard.append(advertisementCardHeader);

        let advertisementCardBody = document.createElement("div");
        advertisementCardBody.className = "card-body";

        let advertisementDescriptionContainer = document.createElement("div");
        let advertisementDescriptionText = document.createElement("h5");
        advertisementDescriptionText.className = "font-weight-normal";
        advertisementDescriptionText.textContent = advertisement.long_description;
        advertisementDescriptionContainer.append(advertisementDescriptionText);
        advertisementCardBody.append(advertisementDescriptionContainer);

        let horizontalRule = document.createElement("hr");
        advertisementCardBody.append(horizontalRule);

        let companyInformationContainer = this.generateCompanyInformationContainer(advertisement);
        advertisementCardBody.append(companyInformationContainer);

        advertisementCard.append(advertisementCardBody);
        advertisementCardContainer.append(advertisementCard);
        return advertisementCardContainer;
    }

    generateCompanyInformationContainer = (advertisement) =>{
        let companyInformationContainer = document.createElement("div");
        let addressLine = this.generateFormattedTextLine(advertisement.address, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(addressLine);
        let cityLine = this.generateFormattedTextLine(advertisement.city + ", " + advertisement.state + " " +advertisement.zip_code, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(cityLine);
        let contactNameLine = this.generateFormattedTextLine(advertisement.contact_name, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(contactNameLine);
        let phoneLine = this.generateFormattedTextLine(advertisement.phone, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(phoneLine);
        let emailLine = this.generateFormattedTextLine(advertisement.email, "h6", "font-weight-bold text-secondary m-0");
        companyInformationContainer.append(emailLine);
        if(advertisement.website_url !== null){
            let websiteButton = this.generateWebsiteLink(advertisement.website_url);
            companyInformationContainer.append(websiteButton);
        }

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

    generateWebsiteLink = (websiteURL) =>{
        let linkContainer = document.createElement("div");
        linkContainer.className = "mt-1 pt-1";
        let link = document.createElement("a");
        link.href = websiteURL;
        link.className = "btn btn-primary";
        link.textContent = "Website";
        link.target = "_blank";
        linkContainer.append(link)
        return linkContainer;
    }
}