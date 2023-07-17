import { AsyncForm } from '../../../../../global/async_form.mjs';
import { Widget } from "../../../widget.mjs";
import { generateDropDownInput, generateTextInput, validateFormCompletion } from "../../../utilities/advertisement_utilities.mjs";

export class AddAdvertisementWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        this.frame.innerHTML = "";

        let advertisementCompaniesAndCategoriesData = await this.getData("get_advertisement_companies_and_categories");
        let advertisementCompanies = this.formatAdvertisementCompaniesData(advertisementCompaniesAndCategoriesData.advertisement_companies);
        let advertisementCategoryIdsToNames = advertisementCompaniesAndCategoriesData.advertisement_category_ids_to_names
        let addAdvertisementContainer = document.createElement("div");
        addAdvertisementContainer.className = "card";

        let addAdvertisementContainerHeader = document.createElement("h5");
        addAdvertisementContainerHeader.className = "card-header";
        addAdvertisementContainerHeader.textContent = "Add Advertisement";
        addAdvertisementContainer.append(addAdvertisementContainerHeader);

        let addAdvertisementContainerBody = document.createElement("div");
        addAdvertisementContainerBody.className = "card-body";
        let addAdvertisementForm = this.makeAddAdvertisementForm(advertisementCompanies, advertisementCategoryIdsToNames);
        addAdvertisementContainerBody.append(addAdvertisementForm);
        addAdvertisementContainer.append(addAdvertisementContainerBody);

        this.frame.append(addAdvertisementContainer);
    }

    formatAdvertisementCompaniesData = (advertisementCompanies) =>{
        let advertisementCompaniesObject = {};
        for(let company of advertisementCompanies){
            advertisementCompaniesObject[company.id] = company.name;
        }
        return advertisementCompaniesObject;
    }

    makeAddAdvertisementForm = (advertisementCompanies, advertisementCategoryIdsToNames) =>{
        let form = document.createElement("form");

        let inputsRow = document.createElement("div");
        inputsRow.className = "row";

        let companiesInput = generateDropDownInput("ad_company", advertisementCompanies, "-Please select Company-", true);
        inputsRow.append(companiesInput);
        let categoryInput = generateDropDownInput("ad_category", advertisementCategoryIdsToNames, "-Please select Advertisement Category-", true);
        inputsRow.append(categoryInput);
        
        let shortDescriptionInput = generateTextInput("*Short Description", "text", "short_description", true, "col-md-12");
        inputsRow.append(shortDescriptionInput);
        let longDescriptionInput = generateTextInput("*Long Description", "text", "long_description", true, "col-md-12");
        inputsRow.append(longDescriptionInput);
        form.append(inputsRow);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-outline-primary rounded m-1";
        submitButton.textContent = "SAVE";
        form.append(submitButton);

        let statusMessage = document.createElement("p");
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        form.append(errorMessage);

        submitButton.onclick = () =>{
            let formResponseValues = [];
            let adCompanyId = document.getElementById("ad_company").value;
            formResponseValues.push(adCompanyId);
            let adCategoryId = document.getElementById("ad_category").value;
            formResponseValues.push(adCategoryId);
            let shortDescription = document.getElementById("short_description").value;
            formResponseValues.push(shortDescription);
            let longDescription = document.getElementById("long_description").value;
            formResponseValues.push(longDescription);
            let formCompletionStatus = validateFormCompletion(formResponseValues);
            if(formCompletionStatus){
                errorMessage.className = "d-none";
                let newAdvertisementAsyncForm = new AsyncForm({
                    action: window.location.href,
                    form: form,
                    status: statusMessage,
                    error: errorMessage,
                    redirectMessage: "Saved!",
                    loadingMessage: "Saving...",
                    getData: () => {
                        return {
                            ad_company_id: adCompanyId,
                            ad_category_id: adCategoryId,
                            short_description: shortDescription,
                            long_description: longDescription
                        };
                    }
                });
                newAdvertisementAsyncForm.submit();
            }
            else{
                errorMessage.className = "d-block mt-2 mb-0 alert alert-danger";
                errorMessage.textContent = "Please fill in all required fields";
            }
        }
        return form;
    }
}