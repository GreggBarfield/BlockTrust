import {AsyncForm} from '/static/global/async_form.mjs';

let editaccountForm = $("#edit_account_form");
let statusMessage = editaccountForm.find("#edit_account_status_message");
let errorMessage = editaccountForm.find("#edit_account_error_message");

let company = editaccountForm.find("#edit_account_company");
let address = editaccountForm.find("#edit_account_address");
let city = editaccountForm.find("#edit_account_city");
let state = editaccountForm.find("#edit_account_state");
let zip = editaccountForm.find("#edit_account_zip");
let phone = editaccountForm.find("#edit_account_phone");
let showRealName = editaccountForm.find("#edit_account_show_real_name");

let form = new AsyncForm({
    action: "/dashboard/edit/edit-account",
    form: editaccountForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Updated successfully!",
    loadingMessage: "Hang on, we're updating your account...",
    getData: () => {
        return {
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip: zip.val(),
            phone: phone.val(),
            show_real_name: showRealName.is(":checked")? 1:0
        }
    }
});


