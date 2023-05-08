import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class MarketPlaceWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        let advertisementData = await this.getData("get_advertisements");
        let advertisementCategoryIdsToNames = advertisementData.ad_category_ids_to_names;
        let advertisementCompanies = this.formatAdvertisementCompaniesData(advertisementData.advertisement_companies);
        let advertisements = this.formatAdvertisementsData(advertisementData.advertisements, advertisementCategoryIdsToNames, advertisementCompanies);

        this.frame.innerHTML = "";
        let advertisementContainer = this.makeAdvertisementContainer(advertisements);
        this.frame.append(advertisementContainer);
    }

    formatAdvertisementCompaniesData = (advertisementCompaniesData) =>{
        let advertisementCompanies = {};
        for(let advertisementCompany of advertisementCompaniesData){
            advertisementCompanies[advertisementCompany.id] = advertisementCompany;
        }
        return advertisementCompanies;
    }

    formatAdvertisementsData = (advertisements, advertisementCategoryIdsToNames, advertisementCompanies) =>{
        for(let advertisement of advertisements){
            advertisement.advertisementCategoryName = advertisementCategoryIdsToNames[advertisement.ad_category_id];
            advertisement.advertisingCompany = advertisementCompanies[advertisement.ad_company_id];
        }
        advertisements.sort((a, b) => (a.advertisementCategoryName > b.advertisementCategoryName) ? 1: (a.advertisementCategoryName === b.advertisementCategoryName)? ((a.advertisingCompany.name > b.advertisingCompany.name) ? 1: -1): -1);
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
        advertisementCardHeader.className = "card-header d-flex justify-content-center p-3";
        let advertisementCardHeaderText = document.createElement("h4");
        advertisementCardHeaderText.textContent = advertisement.short_description + " (" + advertisement.advertisementCategoryName + ")";
        advertisementCardHeader.append(advertisementCardHeaderText);
        advertisementCard.append(advertisementCardHeader);

        let advertisementCardBody = document.createElement("div");
        advertisementCardBody.className = "card-body";

        let advertisementDescriptionContainer = document.createElement("div");
        let advertisementDescriptionText = document.createElement("h5");
        advertisementDescriptionText.textContent = advertisement.long_description;
        advertisementDescriptionContainer.append(advertisementDescriptionText);
        advertisementCardBody.append(advertisementDescriptionContainer);

        let companyInformationContainer = this.generateCompanyInformationContainer(advertisement.advertisingCompany)
        advertisementCardBody.append(companyInformationContainer);

        advertisementCard.append(advertisementCardBody);
        advertisementCardContainer.append(advertisementCard);
        return advertisementCardContainer;
    }

    generateCompanyInformationContainer = (adCompany) =>{
        let companyInformationContainer = document.createElement("div");
        let nameLine = this.generateFormattedTextLine(adCompany.name, "h4", "font-weight-bold text-primary");
        companyInformationContainer.append(nameLine);
        let addressLine = this.generateFormattedTextLine(adCompany.address, "h6", "font-weight-bold text-secondary");
        companyInformationContainer.append(addressLine);
        let cityLine = this.generateFormattedTextLine(adCompany.city + ", " + adCompany.state + " " +adCompany.zip_code, "h6", "font-weight-bold text-secondary");
        companyInformationContainer.append(cityLine);
        let contactNameLine = this.generateFormattedTextLine(adCompany.contact_name, "h6", "font-weight-bold text-secondary");
        companyInformationContainer.append(contactNameLine);
        let phoneLine = this.generateFormattedTextLine(adCompany.phone, "h6", "font-weight-bold text-secondary");
        companyInformationContainer.append(phoneLine);
        let emailLine = this.generateFormattedTextLine(adCompany.email, "h6", "font-weight-bold text-secondary");
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