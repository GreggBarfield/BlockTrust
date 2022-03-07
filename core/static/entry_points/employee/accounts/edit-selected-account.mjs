import {AsyncForm} from '/static/global/async_form.mjs';

document.getElementById("edit_state").value = account_state;
if(account_partner === "None"){
    document.getElementById("edit_partner").value="";
}
else{
    document.getElementById("edit_partner").value = account_partner;
}
if(account_affiliate_id === "None"){
    document.getElementById("edit_affiliate_id").value = "";
}
else{
    document.getElementById("edit_affiliate_id").value = account_affiliate_id;
}

let editAccountForm = $("#edit_account_form");
let statusMessage = editAccountForm.find("#edit_account_status_message");
let errorMessage = editAccountForm.find("#edit_account_error_message");

let id = editAccountForm.find("#edit_id");
let partner = editAccountForm.find("#edit_partner");
let affiliate_id = editAccountForm.find("#edit_affiliate_id");
let phone = editAccountForm.find("#edit_phone");
let company = editAccountForm.find("#edit_company");
let address = editAccountForm.find("#edit_address");
let city = editAccountForm.find("#edit_city");
let state = editAccountForm.find("#edit_state");
let zip_code = editAccountForm.find("#edit_zip");
let action_route = "/employee/dashboard/edit-account/"+account_id+"/action"

let form = new AsyncForm({
    action: action_route,
    form: editAccountForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Account changes saved!",
    loadingMessage: "Hang on, saving your changes...",
    getData: () => {
        return {
            id: id.val(),
            partner: partner.val(),
            affiliate_id: affiliate_id.val(),
            phone: phone.val(),
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip_code: zip_code.val(),
        }
    }
});
