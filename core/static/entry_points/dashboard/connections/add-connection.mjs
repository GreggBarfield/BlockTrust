import {AsyncForm} from '/static/global/async_form.mjs';

$(document).ready(function () {
    $('#sector').change(function () {
        $('#company_name').empty();
        $('#company_name').append(`<option value=0>Not Listed</option>`);
        if($(this).val() == "3"){
            for(let account in accounts){
                if(accounts[account].name !== ""){
                    $('#company_name').append(`<option value="${accounts[account].id}">${accounts[account].name}</option>`);
                }
            }
        }
        else{
            for(let account in accounts){
                if(accounts[account].name !== "" && accounts[account].sector == $(this).val()){
                    $('#company_name').append(`<option value="${accounts[account].id}">${accounts[account].name}</option>`);
                }
            }
        } 
    });

    $('#company_name').select2({multiple: true, placeholder: "Select companies"});

    $('#company_name').change(function () {
        if($(this).val() == 0){
            $("#new_company_name").prop('disabled', false);
            $("#new_company_contact").prop('disabled', false);
            $("#new_company_email").prop('disabled', false);
        }
        else{
            $("#new_company_name").prop('disabled', true);
            $("#new_company_contact").prop('disabled', true);
            $("#new_company_email").prop('disabled', true);
        }
    });
})

let addConnectionForm = $("#add_connection_form");
let statusMessage = addConnectionForm.find("#add_connection_status_message");
let errorMessage = addConnectionForm.find("#add_connection_error_message");

let sector = addConnectionForm.find("#sector");
let company_name = addConnectionForm.find("#company_name");
let new_company_name = addConnectionForm.find("#new_company_name");
let new_company_contact = addConnectionForm.find("#new_company_contact");
let new_company_email = addConnectionForm.find("#new_company_email");

let form = new AsyncForm({
    action: "/dashboard/add-connection",
    form: addConnectionForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Connection Invite sent!",
    loadingMessage: "Hang on, we're sending an invite...",
    getData: () => {
        return {
            sector: sector.val(),
            company_id: company_name.value,
            new_company_name: new_company_name.val(),
            new_company_contact: new_company_contact.val(),
            new_company_email: new_company_email.val()
        }
    }
});

let selectAll = document.getElementById("select_all");
selectAll.onchange = () =>{
    if(selectAll.checked==true){
        let sectorSelect = document.getElementById("sector");
        sectorSelect.value = "3";  
        var event = new UIEvent("change", {"view": window,"bubbles": true,"cancelable": true});  
        sectorSelect.dispatchEvent(event);
        let feedlotAndPackerAccounts = [];
        for(let account in accounts){
            if(accounts[account].sector == "6" || accounts[account].sector == "7"){
                feedlotAndPackerAccounts.push(accounts[account].id)
            }
        }
        $('#company_name').val(feedlotAndPackerAccounts);
    }
    else{
        let sectorSelect = document.getElementById("sector");
        sectorSelect.value = "0";  
        var event = new UIEvent("change", {"view": window,"bubbles": true,"cancelable": true});  
        sectorSelect.dispatchEvent(event);
    }
}

let unlistedCompany = document.getElementById("unlisted_company");
unlistedCompany.onchange = () =>{
    if(unlistedCompany.checked==true){
        document.getElementById("new_company_name").disabled = false;
        document.getElementById("new_company_contact").disabled = false;
        document.getElementById("new_company_email").disabled = false;
    }else{
        document.getElementById("new_company_name").disabled = true;
        document.getElementById("new_company_contact").disabled = true;
        document.getElementById("new_company_email").disabled = true;

    }
}