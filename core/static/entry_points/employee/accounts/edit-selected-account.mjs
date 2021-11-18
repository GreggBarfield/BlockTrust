import {AsyncForm} from '/static/global/async_form.mjs';

let edit_state = document.getElementById("edit_state");
edit_state.value = account_state;

let editAccountForm = $("#edit_account_form");
let statusMessage = editAccountForm.find("#edit_account_status_message");
let errorMessage = editAccountForm.find("#edit_account_error_message");

let id = editAccountForm.find("#edit_id");
let phone = editAccountForm.find("#edit_phone");
let company = editAccountForm.find("#edit_company");
let address = editAccountForm.find("#edit_address");
let city = editAccountForm.find("#edit_city");
let state = editAccountForm.find("#edit_state");
let zip_code = editAccountForm.find("#edit_zip");

let form = new AsyncForm({
    action: "/employee/dashboard/edit-account/apply-changes",
    form: editAccountForm[0],
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
        }
    }
});
