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
        let advertisements = advertisementData.advertisements;

        this.frame.innerHTML = "";
        let advertisementContainer = this.makeAdvertisementContainer(advertisementCategoryIdsToNames, advertisementCompanies, advertisements);
        this.frame.append(advertisementContainer);
    }

    formatAdvertisementCompaniesData = (advertisementCompaniesData) =>{
        let advertisementCompanies = {};
        for(let advertisementCompany of advertisementCompaniesData){
            advertisementCompanies[advertisementCompany.id] = advertisementCompany;
        }
        return advertisementCompanies;
    }

    makeAdvertisementContainer = (advertisementCategoryIdsToNames, advertisementCompanies, advertisements) =>{
        let advertisementsContainer = document.createElement("div");
        for(let [advertisementCategoryId, advertisementCategoryName] of Object.entries(advertisementCategoryIdsToNames)){
            let sectionalAdvertisementsContainer = this.makeSectionalAdvertisementContainer(advertisementCategoryId, advertisementCategoryName, advertisementCompanies, advertisements);
            advertisementsContainer.append(sectionalAdvertisementsContainer);
        }
        return advertisementsContainer;
    }

    makeSectionalAdvertisementContainer = (advertisementCategoryId, advertisementCategoryName, advertisementCompanies, advertisements) =>{
        let sectionalAdvertisementContainer = document.createElement("div");
        sectionalAdvertisementContainer.className = "card col-md-12";

        let sectionalAdvertisementContainerHeader = document.createElement("h5");
        sectionalAdvertisementContainerHeader.className = "card-header";
        sectionalAdvertisementContainerHeader.textContent = advertisementCategoryName;
        sectionalAdvertisementContainer.append(sectionalAdvertisementContainerHeader);

        let sectionalAdvertisementContainerBody = document.createElement("div");
        sectionalAdvertisementContainerBody.className = "card-body row p-2";

        for(let advertisement of advertisements){
            if(advertisement.ad_category_id == advertisementCategoryId){
                let advertisementCard = this.generateAdvertisementCard(advertisement, advertisementCompanies);
                sectionalAdvertisementContainerBody.append(advertisementCard);
            }
        }
        sectionalAdvertisementContainer.append(sectionalAdvertisementContainerBody);

        return sectionalAdvertisementContainer;
    }

    generateAdvertisementCard = (advertisement, advertisementCompanies) =>{
        let advertisementCardContainer = document.createElement("div");
        advertisementCardContainer.className = "col-md-4";
        let advertisementCard = document.createElement("div")
        advertisementCard.className = "card border border-dark rounded p-2";

        let advertisementCardHeader = document.createElement("h5");
        advertisementCardHeader.className = "card-header";
        advertisementCardHeader.textContent = advertisement.short_description;
        advertisementCard.append(advertisementCardHeader);

        let advertisementCardBody = document.createElement("div");
        advertisementCardBody.className = "card-body";

        let adDescriptionText = document.createElement("p");
        // This will include the description of an ad. 
        adDescriptionText.textContent = advertisement.long_description;
        advertisementCardBody.append(adDescriptionText);
        advertisementCard.append(advertisementCardBody);

        advertisementCardContainer.append(advertisementCard);
        return advertisementCardContainer;
    }

}