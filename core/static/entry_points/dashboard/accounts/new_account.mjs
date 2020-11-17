import {AsyncForm} from '/static/global/async_form.mjs';

let newAccountForm = $("#new_account_form");
let statusMessage = newAccountForm.find("#new_account_status_message");
let errorMessage = newAccountForm.find("#new_account_error_message");

let form = new AsyncForm({
    action: "/dashboard/accounts/new-account/action",
    form: newAccountForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Created the account successfully!",
    loadingMessage: "Hang on, we're creating your account...",
    getData: () => {
        return {
            name: newAccountForm.find("#new_account_name").val(),
            company: newAccountForm.find("#new_account_company").val(),
            sector: newAccountForm.find("#new_account_sector").val(),
        }
    }
});
