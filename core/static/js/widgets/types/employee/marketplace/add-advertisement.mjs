import { AsyncForm } from '../../../../../global/async_form.mjs';
import { Widget } from "../../../widget.mjs";
import { generateDropDownInput, generateTextInput } from "../../../utilities/advertisement_utilities.mjs";

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
            let allQuestionsAnswered = true;
            let ad_company_id = document.getElementById("ad_company").value;
            let ad_category_id = document.getElementById("ad_category").value;
            let short_description = document.getElementById("short_description").value;
            let long_description = document.getElementById("long_description").value;
            if(ad_company_id == "-Please select Company-"){ allQuestionsAnswered=false; }
            if(ad_category_id == "-Please select Advertisement Category-"){ allQuestionsAnswered=false; }
            if(short_description == ""){ allQuestionsAnswered=false; }
            if(long_description == ""){ allQuestionsAnswered=false; }
            if(allQuestionsAnswered){
                let newAdvertisementAsyncForm = new AsyncForm({
                    action: "/widgets/data/save_new_advertisement",
                    form: form,
                    status: statusMessage,
                    error: errorMessage,
                    redirectMessage: "Saved!",
                    loadingMessage: "Saving...",
                    getData: () => {
                        return {
                            ad_company_id: ad_company_id,
                            ad_category_id: ad_category_id,
                            short_description: short_description,
                            long_description: long_description
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

    submitAdvertisementForm = (form) =>{
        let asyncForm = new AsyncForm({
            action: "/widgets/data/save_new_advertisement",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Saved!",
            loadingMessage: "Saving...",
            getData: () => {
                return {
                    scores: this.scores,
                    uploaded_file_ids: this.uploadedFileIDList,
                    total_score: this.totalScore,
                    responses: this.responses,
                    is_partial_response: this.isPartialResponse,
                    sustainability_response_id: sustainabilityResponseId
                };
            }
        });
    }
}