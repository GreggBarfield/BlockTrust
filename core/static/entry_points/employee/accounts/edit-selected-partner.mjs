import {AsyncForm} from '/static/global/async_form.mjs';

document.addEventListener("DOMContentLoaded", function() { 
    document.getElementById("edit_state").value = partner_state;
});

let editPartnerAccountForm = $("#edit_partner_account_form");
let statusMessage = editPartnerAccountForm.find("#edit_account_status_message");
let errorMessage = editPartnerAccountForm.find("#edit_account_error_message");

let id = editPartnerAccountForm.find("#edit_id");
let phone = editPartnerAccountForm.find("#edit_phone");
let company = editPartnerAccountForm.find("#edit_company");
let address = editPartnerAccountForm.find("#edit_address");
let city = editPartnerAccountForm.find("#edit_city");
let state = editPartnerAccountForm.find("#edit_state");
let zip_code = editPartnerAccountForm.find("#edit_zip");
let is_partner_used_for_signup = document.getElementById("is_partner_used_for_signup");
let action_route = "/employee/dashboard/edit-partner/"+partner_id+"/action"

let form = new AsyncForm({
    action: action_route,
    form: editPartnerAccountForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Account changes saved!",
    loadingMessage: "Hang on, saving your changes...",
    getData: () => {
        return {
            id: id.val(),
            phone: phone.val(),
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip_code: zip_code.val(),
            is_partner_used_for_signup: is_partner_used_for_signup.checked
        }
    }
});
