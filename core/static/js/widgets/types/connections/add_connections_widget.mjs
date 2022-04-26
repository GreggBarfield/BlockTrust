import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class AddConnectionsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
    this.getData(
        "get_accounts"
    ).then((data) => {
        this.account_rows = data.account_rows;
        this.makeForm();
    });

    this.onSomeDataLoaded(function () {
        this.frame.innerHTML = "";
    });
    }

    makeForm(){
        let card = document.createElement("div");
        card.className = "card";
    
        let createGroupName = document.createElement("h5");
        createGroupName.className = "mt-2";
        createGroupName.style = "text-align: center;  font-size: 25px; padding-left: 15px;padding-right: 15px;"
    
        createGroupName.textContent = "Add Connections by Invitation";
    
        let cardHeader = document.createElement("div");
        cardHeader.className = "card-header form-group d-flex justify-content-between";
        cardHeader.style = "padding:5px;padding-left: 15px;"
        cardHeader.append(createGroupName);
        card.append(cardHeader)
    
        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        card.append(cardBody);
        this.frame.append(card);
        let form = document.createElement("form");

        let selectAllFeedersPackersFormGroup = document.createElement("div");
        selectAllFeedersPackersFormGroup.className = "form-group col-md-6";
        form.append(selectAllFeedersPackersFormGroup)
        let selectAllFeedersPackersCheckBox = document.createElement("input");
        selectAllFeedersPackersCheckBox.type = "checkbox";
        selectAllFeedersPackersCheckBox.id = "select_all_feeders_packers";
        selectAllFeedersPackersCheckBox.className = "checkbox";
        let selectAllFeedersPackersLabel = document.createElement("label");
        selectAllFeedersPackersLabel.textContent = "Select All Feeders and Packers in Network";
        selectAllFeedersPackersFormGroup.append(selectAllFeedersPackersCheckBox);
        selectAllFeedersPackersFormGroup.append(selectAllFeedersPackersLabel);
        selectAllFeedersPackersCheckBox.onchange = () => {
            if(document.getElementById("select_all_feeders_packers").checked == true){
                $(companyOptions).empty().trigger('change');
                let selectedCompanyData = [];
                sectorOptions.value = 3;
                //$(sectorOptions).trigger('change');
                sectorOptions.onchange();
                for(const account_row of this.account_rows){
                    if(account_row.sector == "6" || account_row.sector == "7"){
                        selectedCompanyData.push(account_row.id);
                    } 
                }
                $(companyOptions).val(selectedCompanyData);
                $(companyOptions).trigger('change');
            }
            else{
                sectorOptions.value = 0;
                $(sectorOptions).trigger('change');
                $(companyOptions).trigger('change');
            }
            
        }

        let sectors = [{id: 4, name: "Cow-Calf"}, {id: 5, name: "Auction House"}, {id: 6, name: "Feedlot"}, {id: 7, name: "Packer"}, {id: 3, name: "All Sectors"}];
        let sectorOptionsFormGroup = document.createElement("div");
        sectorOptionsFormGroup.className = "form-group col-md-6";
        form.append(sectorOptionsFormGroup);

        let sectorOptionsLabel = document.createElement("label");
        sectorOptionsLabel.textContent = "Sector";
        let sectorOptions = document.createElement("select");
        sectorOptions.id = "sector";
        sectorOptions.className = "form-control";
        $(sectorOptions).append('<option disabled selected value="0"> -- Select an option -- </option>');
        for (var sector of sectors) {
            $(sectorOptions).append('<option value=' + sector.id + '>' + sector.name + '</option>');
        }
        sectorOptionsFormGroup.append(sectorOptionsLabel);
        sectorOptionsFormGroup.append(sectorOptions);
        sectorOptions.onchange = () =>{
            $(companyOptions).empty().trigger("change");
            let companyData = [];
            if(sectorOptions.value == 3){
                for(const account_row of this.account_rows){
                        companyData.push({id: account_row.id, text: account_row.name});
                }
            }
            else{
                for(const account_row of this.account_rows){
                    if(sectorOptions.value == account_row.sector){
                        companyData.push({id: account_row.id, text: account_row.name});
                    } 
                }
            }
            $(companyOptions).select2({
                data: companyData,
                multiple: true,
                placeholder: "Select companies"
            });
        }

        let companiesFormGroup = document.createElement("div")
        companiesFormGroup.className = "form-group col-md-6";
        form.append(companiesFormGroup);

        let companiesLabel = document.createElement("label");
        companiesLabel.textContent = "Companies";
        let companyOptions = document.createElement("select");
        companyOptions.id = "companies";
        companyOptions.className = "select2-hidden-accessible";
        companiesFormGroup.append(companiesLabel);
        companiesFormGroup.append(companyOptions);
        $(companyOptions).select2({multiple: true, placeholder: "Select companies"});

        let notListedCheckBoxFormGroup = document.createElement("div");
        notListedCheckBoxFormGroup.className = "form-group col-md-6";
        form.append(notListedCheckBoxFormGroup)
        let notListedCheckBox = document.createElement("input");
        notListedCheckBox.type = "checkbox";
        notListedCheckBox.id = "not_listed";
        notListedCheckBox.className = "checkbox";
        let notListedLabel = document.createElement("label");
        notListedLabel.textContent = "Company Not Listed?";
        notListedCheckBoxFormGroup.append(notListedCheckBox);
        notListedCheckBoxFormGroup.append(notListedLabel);
        notListedCheckBox.onchange = () => {
            if(document.getElementById("not_listed").checked == true){
                newCompanySectorOptions.disabled = false;
                newCompanyNameInput.disabled = false;
                newCompanyContactNameInput.disabled = false;
                newCompanyEmailInput.disabled = false;
            }
            else{
                newCompanySectorOptions.disabled = true;
                newCompanyNameInput.disabled = true;
                newCompanyContactNameInput.disabled = true;
                newCompanyEmailInput.disabled = true;
            }
        };

        let newCompanySectors = [{id: 4, name: "Cow-Calf"}, {id: 5, name: "Auction House"}, {id: 6, name: "Feedlot"}, {id: 7, name: "Packer"}];
        let newCompanySectorOptionsFormGroup = document.createElement("div");
        newCompanySectorOptionsFormGroup.className = "form-group col-md-6";
        form.append(newCompanySectorOptionsFormGroup);

        let newCompanySectorOptionsLabel = document.createElement("label");
        newCompanySectorOptionsLabel.textContent = "New Company Sector";
        let newCompanySectorOptions = document.createElement("select");
        newCompanySectorOptions.id = "new_company_sector";
        newCompanySectorOptions.className = "form-control";
        newCompanySectorOptions.disabled = true;
        $(newCompanySectorOptions).append('<option disabled selected value="0"> -- Select an option -- </option>');
        for (var sector of newCompanySectors) {
            $(newCompanySectorOptions).append('<option value=' + sector.id + '>' + sector.name + '</option>');
        }
        newCompanySectorOptionsFormGroup.append(newCompanySectorOptionsLabel);
        newCompanySectorOptionsFormGroup.append(newCompanySectorOptions);

        let newCompanyNameFormGroup = document.createElement("div")
        newCompanyNameFormGroup.className = "form-group col-md-6";
        form.append(newCompanyNameFormGroup);

        let newCompanyNameLabel = document.createElement("label");
        newCompanyNameLabel.textContent = "New Company name";
        let newCompanyNameInput = document.createElement("input");
        newCompanyNameInput.id = "new_company_name";
        newCompanyNameInput.className = "form-control";
        newCompanyNameInput.placeholder = "XYZ Feedyard";
        newCompanyNameInput.disabled = true;
        newCompanyNameFormGroup.append(newCompanyNameLabel);
        newCompanyNameFormGroup.append(newCompanyNameInput);

        let newCompanyContactNameFormGroup = document.createElement("div")
        newCompanyContactNameFormGroup.className = "form-group col-md-6";
        form.append(newCompanyContactNameFormGroup);

        let newCompanyContactNameLabel = document.createElement("label");
        newCompanyContactNameLabel.textContent = "Company Contact name";
        let newCompanyContactNameInput = document.createElement("input");
        newCompanyContactNameInput.id = "new_company_contact_name";
        newCompanyContactNameInput.className = "form-control";
        newCompanyContactNameInput.placeholder = "John Smith";
        newCompanyContactNameInput.disabled = true;
        newCompanyContactNameFormGroup.append(newCompanyContactNameLabel);
        newCompanyContactNameFormGroup.append(newCompanyContactNameInput);

        let newCompanyEmailFormGroup = document.createElement("div")
        newCompanyEmailFormGroup.className = "form-group col-md-6";
        form.append(newCompanyEmailFormGroup);

        let newCompanyEmailLabel = document.createElement("label");
        newCompanyEmailLabel.textContent = "New Company Email";
        let newCompanyEmailInput = document.createElement("input");
        newCompanyEmailInput.id = "new_company_email";
        newCompanyEmailInput.className = "form-control";
        newCompanyEmailInput.placeholder = "jsmith@xyzfeedyard.com";
        newCompanyEmailInput.disabled = true;
        newCompanyEmailFormGroup.append(newCompanyEmailLabel);
        newCompanyEmailFormGroup.append(newCompanyEmailInput);

        let submitButton = document.createElement("button");
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Save";
        submitButton.addEventListener("click", (e)=>{
            this.asyncForm.submit();
        });
        form.append(submitButton);
        
        let statusMessage = document.createElement("p");
        statusMessage.style.display = "none";
        statusMessage.className = "mt-2 mb-0";
        form.append(statusMessage);
        let errorMessage = document.createElement("p");
        errorMessage.style.display = "none";
        errorMessage.className = "mt-2 mb-0 alert alert-danger";
        form.append(errorMessage);
        cardBody.append(form);

        this.asyncForm = new AsyncForm({
            action: "/widgets/data/add-connection-request",
            form: form,
            status: statusMessage,
            error: errorMessage,
            redirectMessage: "Invite(s) sent!",
            loadingMessage: "Sending Invite(s)...",
            asJSON: true,
            getData: () => {
                return {
                    companies_list: $(companyOptions).val(),
                    new_company_sector: new_company_sector.value,
                    unlisted_company: notListedCheckBox.checked,
                    new_company_name: newCompanyNameInput.value,
                    new_company_contact_name: newCompanyContactNameInput.value,
                    new_company_email: newCompanyEmailInput.value           
                }
            }
        });    
    }
}