import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class MarketPlaceWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = () => {
        // The adCategories and adData variables have placeholder data for now. Once the tables and routines have been created the data will be asynchronously fetched using the getData() Widget method.
        // Advertisement data objects will have additional key value pairs based on data to be displayed/stored.   
        let adCategories = {
            genetics: {name: "genetics", header: "Genetics"},
            feed: {name: "feed", header: "Feed"}
        }
        let adData = {"genetics": [{"header": "Partner 1"}, {"header": "Partner 2"}, {"header": "Partner 3"}], "feed": [{"header": "Partner 1"}, {"header": "Partner 2"}, {"header": "Partner 3"}]};
        this.frame.innerHTML = "";
        this.makeAdBanners(adCategories, adData);
        
        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });
    }

    
    makeAdBanners = (adCategories, adData) =>{
        let adsContainer = document.createElement("div");
        for(let category of Object.values(adCategories)){
            let sectionalAdContainer = this.makeSectionalAdBanners(category.header, adData[category.name]);
            adsContainer.append(sectionalAdContainer);
        }
        this.frame.append(adsContainer);
    }

    makeSectionalAdBanners = (headerText, adDataObjects) => {
        let adContainer = document.createElement("div");
        adContainer.className = "card col-md-12";

        let adContainerHeader = document.createElement("h5");
        adContainerHeader.className = "card-header";
        adContainerHeader.textContent = headerText;
        adContainer.append(adContainerHeader);

        let adContainerBody = document.createElement("div");
        adContainerBody.className = "card-body row p-2"

        for(let adData of adDataObjects){
            let adCard = this.generateAdCard(adData);
            adContainerBody.append(adCard);
        }
        adContainer.append(adContainerBody);

        return adContainer;
    }

    generateAdCard = (adData) =>{
        let adCard = document.createElement("div")
        adCard.className = "card col-md-4 border border-dark rounded p-2";

        let adCardHeader = document.createElement("h5");
        adCardHeader.className = "card-header";
        adCardHeader.textContent = adData.header;
        adCard.append(adCardHeader);

        let adCardBody = document.createElement("div");
        adCardBody.className = "card-body";

        let adDescriptionText = document.createElement("p");
        // This will include the description of an ad. 
        adDescriptionText.textContent = "Ad Description";
        adCardBody.append(adDescriptionText);
        adCard.append(adCardBody);

        return adCard;
    }
}