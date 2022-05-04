import { Widget } from '../../widget.mjs';
import { AsyncForm } from '../../../../global/async_form.mjs';

export class AddConnectionsWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        const getInvitableAccounts = this.getData(
            "get_invitable_accounts"
        ).then((data) => {
            this.accountRows = data.account_rows;  
        });
        const getSectorsByName = this.getData(
            "direct/sectors_by_name"
        ).then((data) => {
            this.sectorsByName = data.sectors_by_name;
        }); 
        Promise.all([
            getInvitableAccounts, getSectorsByName
        ]).then(()=> {
            this.makeForm();
        })

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
            if(selectAllFeedersPackersCheckBox.checked == true){
                $(accountsOptionsSelect).empty();
                let selectedCompanyData = [];
                sectorOptionsSelect.value = 0;
                sectorOptionsSelect.onchange();
                for(const accountRow of this.accountRows){
                    if(accountRow.sector == this.sectorsByName["Feedlot"]|| accountRow.sector == this.sectorsByName["Buyer"]){
                        selectedCompanyData.push(accountRow.id);
                    } 
                }
                $(accountsOptionsSelect).val(selectedCompanyData);
                $(accountsOptionsSelect).trigger('change');
            }
            else{
                sectorOptionsSelect.value = 0;
                sectorOptionsSelect.onchange();
            }
        }

        let sectorOptionsFormGroup = document.createElement("div");
        sectorOptionsFormGroup.className = "form-group col-md-6";
        form.append(sectorOptionsFormGroup);

        let sectorOptionsLabel = document.createElement("label");
        sectorOptionsLabel.textContent = "Sector";
        let sectorOptionsSelect = document.createElement("select");
        sectorOptionsSelect.id = "sector";
        sectorOptionsSelect.className = "form-control";
        let defaultOption = new Option("---Select an option---", 0);
        defaultOption.selected = true;
        sectorOptionsSelect.appendChild(defaultOption);
        for (var sectorName in this.sectorsByName) {
            var option = new Option(sectorName, this.sectorsByName[sectorName]);
            sectorOptionsSelect.appendChild(option);
        }
        sectorOptionsFormGroup.append(sectorOptionsLabel);
        sectorOptionsFormGroup.append(sectorOptionsSelect);
        sectorOptionsSelect.onchange = () =>{
            $(accountsOptionsSelect).empty();
            let accountsList = [];
            if(sectorOptionsSelect.value == 0){
                for(const accountRow of this.accountRows){
                        accountsList.push({id: accountRow.id, text: accountRow.name});
                }
            }
            else{
                for(const accountRow of this.accountRows){
                    if(sectorOptionsSelect.value == accountRow.sector){
                        accountsList.push({id: accountRow.id, text: accountRow.name});
                    } 
                }
            }
            $(accountsOptionsSelect).select2({
                data: accountsList,
                multiple: true,
                placeholder: "Select companies"
            });
        }

        let accountsFormGroup = document.createElement("div")
        accountsFormGroup.className = "form-group col-md-6";
        form.append(accountsFormGroup);

        let accountsLabel = document.createElement("label");
        accountsLabel.textContent = "Companies";
        let accountsOptionsSelect = document.createElement("select");
        accountsOptionsSelect.id = "companies";
        accountsFormGroup.append(accountsLabel);
        accountsFormGroup.append(accountsOptionsSelect);
        $(accountsOptionsSelect).select2({multiple: true, placeholder: "Select companies"});
        // Trigger onchange method to populate the accountsOptionsSelect drop-down 
        sectorOptionsSelect.onchange();

        let notListedCheckBoxFormGroup = document.createElement("div");
        notListedCheckBoxFormGroup.className = "form-group col-md-6";
        form.append(notListedCheckBoxFormGroup)
        let notListedCheckBox = document.createElement("input");
        notListedCheckBox.type = "checkbox";
        notListedCheckBox.id = "notListed";
        notListedCheckBox.className = "checkbox";
        let notListedLabel = document.createElement("label");
        notListedLabel.textContent = "Company Not Listed?";
        notListedCheckBoxFormGroup.append(notListedCheckBox);
        notListedCheckBoxFormGroup.append(notListedLabel);
        notListedCheckBox.onchange = () => {
            if(notListedCheckBox.checked == true){
                newAccountSectorOptions.disabled = false;
                newAccountNameInput.disabled = false;
                newAccountContactNameInput.disabled = false;
                newAccountEmailInput.disabled = false;
            }
            else{
                newAccountSectorOptions.disabled = true;
                newAccountNameInput.disabled = true;
                newAccountContactNameInput.disabled = true;
                newAccountEmailInput.disabled = true;
            }
        };

        let newAccountSectorOptionsFormGroup = document.createElement("div");
        newAccountSectorOptionsFormGroup.className = "form-group col-md-6";
        form.append(newAccountSectorOptionsFormGroup);

        let newAccountSectorOptionsLabel = document.createElement("label");
        newAccountSectorOptionsLabel.textContent = "New Company Sector";
        let newAccountSectorOptions = document.createElement("select");
        newAccountSectorOptions.id = "newAccountSector";
        newAccountSectorOptions.className = "form-control";
        newAccountSectorOptions.disabled = true;
        defaultOption = new Option("---Select an option---", 0);
        defaultOption.disabled = true;
        defaultOption.selected = true;
        newAccountSectorOptions.appendChild(defaultOption)
        for (var sectorName in this.sectorsByName) {
            var option = new Option(sectorName, this.sectorsByName[sectorName]);
            newAccountSectorOptions.appendChild(option);
        }
        newAccountSectorOptionsFormGroup.append(newAccountSectorOptionsLabel);
        newAccountSectorOptionsFormGroup.append(newAccountSectorOptions);

        let newAccountNameFormGroup = document.createElement("div")
        newAccountNameFormGroup.className = "form-group col-md-6";
        form.append(newAccountNameFormGroup);

        let newAccountNameLabel = document.createElement("label");
        newAccountNameLabel.textContent = "New Company name";
        let newAccountNameInput = document.createElement("input");
        newAccountNameInput.id = "new_company_name";
        newAccountNameInput.className = "form-control";
        newAccountNameInput.placeholder = "XYZ Feedyard";
        newAccountNameInput.disabled = true;
        newAccountNameFormGroup.append(newAccountNameLabel);
        newAccountNameFormGroup.append(newAccountNameInput);

        let newAccountContactNameFormGroup = document.createElement("div")
        newAccountContactNameFormGroup.className = "form-group col-md-6";
        form.append(newAccountContactNameFormGroup);

        let newAccountContactNameLabel = document.createElement("label");
        newAccountContactNameLabel.textContent = "Company Contact name";
        let newAccountContactNameInput = document.createElement("input");
        newAccountContactNameInput.id = "new_company_contact_name";
        newAccountContactNameInput.className = "form-control";
        newAccountContactNameInput.placeholder = "John Smith";
        newAccountContactNameInput.disabled = true;
        newAccountContactNameFormGroup.append(newAccountContactNameLabel);
        newAccountContactNameFormGroup.append(newAccountContactNameInput);

        let newAccountEmailFormGroup = document.createElement("div")
        newAccountEmailFormGroup.className = "form-group col-md-6";
        form.append(newAccountEmailFormGroup);

        let newAccountEmailLabel = document.createElement("label");
        newAccountEmailLabel.textContent = "New Company Email";
        let newAccountEmailInput = document.createElement("input");
        newAccountEmailInput.id = "new_company_email";
        newAccountEmailInput.className = "form-control";
        newAccountEmailInput.placeholder = "jsmith@xyzfeedyard.com";
        newAccountEmailInput.disabled = true;
        newAccountEmailFormGroup.append(newAccountEmailLabel);
        newAccountEmailFormGroup.append(newAccountEmailInput);

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
                    invited_account_ids_list: $(accountsOptionsSelect).val(),
                    new_account_sector: newAccountSector.value,
                    unlisted_company: notListedCheckBox.checked,
                    new_account_name: newAccountNameInput.value,
                    new_account_contact_name: newAccountContactNameInput.value,
                    new_account_email: newAccountEmailInput.value           
                }
            }
        });    
    }
}