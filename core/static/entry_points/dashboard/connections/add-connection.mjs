import {AsyncForm} from '/static/global/async_form.mjs';

$(document).ready(function () {
    $('#sector').change(function () {
        $('#company_name').empty();
        $('#company_name').append(`<option disabled selected value> -- Select an option -- </option>`)
        $('#company_name').append(`<option value=0>Not Listed</option>`);
        if($(this).val() == 4){
            for(let val in accounts){
                if(accounts[val].company!=="" && accounts[val].sector==4){
                    $('#company_name').append(`<option value="${accounts[val].id}">${accounts[val].company}</option>`);
                }
            }
        }
        if($(this).val() == 5){
            for(let val in accounts){
                if(accounts[val].company!=="" && accounts[val].sector==5){
                    $('#company_name').append(`<option value="${accounts[val].id}">${accounts[val].company}</option>`);
                }
            }
        }
        if($(this).val() == 6){
            for(let val in accounts){
                if(accounts[val].company!=="" && accounts[val].sector==6){
                    $('#company_name').append(`<option value="${accounts[val].id}">${accounts[val].company}</option>`);
                }
            } 
        }
        if($(this).val() == 7){
            for(let val in accounts){
                if(accounts[val].company!=="" && accounts[val].sector==7){
                    $('#company_name').append(`<option value="${accounts[val].id}">${accounts[val].company}</option>`);
                }
            } 
        }

    });

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
            company_id: company_name.val(),
            new_company_name: new_company_name.val(),
            new_company_contact: new_company_contact.val(),
            new_company_email: new_company_email.val()
        }
    }
});
