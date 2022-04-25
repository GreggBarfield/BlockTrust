import { Widget } from '../../widget.mjs';

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

        let sectors = [{id: 4, name: "Cow-Calf"}, {id: 5, name: "Auction House"}, {id: 6, name: "Feedlot"}, {id: 7, name: "Packer"}, {id: 3, name: "All Sectors"}]
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
            $(companiesFormGroup).empty().trigger("change");
            let companyData = [];
            for(const account_row of this.account_rows){
                if(sectorOptions.value == account_row.sector){
                    companyData.push({id: account_row.id, text: account_row.name});
                } 
            }
            $(companiesFormGroup).select2({
                data: companyData,
                multiple: true,
                placeholder: "Select companies",
                width: "auto"
            });
        }

        let companiesFormGroup = document.createElement("div")
        companiesFormGroup.className = "form-group col-md-6";
        form.append(companiesFormGroup);

        let companiesLabel = document.createElement("label");
        companiesLabel.textContent = "Companies";
        let companyOptions = document.createElement("select");
        companyOptions.id = "companies";
        companyOptions.className = "form-control select2-hidden-accessible";
        companiesFormGroup.append(companiesLabel);
        companiesFormGroup.append(companyOptions);
        $(companyOptions).select2({multiple: true, placeholder: "Select companies", width: "auto"});

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
                newCompanyNameInput.disabled = false;
                newCompanyContactNameInput.disabled = false;
                newCompanyEmailInput.disabled = false;
            }
            else{
                newCompanyNameInput.disabled = true;
                newCompanyContactNameInput.disabled = true;
                newCompanyEmailInput.disabled = true;
            }
        };

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
        newCompanyContactNameLabel.textContent = "Company Contatc name";
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

        // Fix select2 auto sizing issue
        cardBody.append(form);

        
    }
}