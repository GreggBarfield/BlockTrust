import {AsyncForm} from '/static/global/async_form.mjs';

$(document).ready(function () {
    for(let val in accounts){
        if(accounts[val].name!=="" && accounts[val].company!==null){
            $("#account").append(`<option value="${accounts[val].id}">${accounts[val].company}</option>`)
        }
}
});


let accountForm = $("#select_account_form");
let statusMessage = accountForm.find("#account_status_message");
let errorMessage = accountForm.find("#account_error_message");

let account = accountForm.find("#account");

let form = new AsyncForm({
    action: "/employee/dashboard/edit-an-account/action",
    form: accountForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Loading account...",
    loadingMessage: "Loading account...",
    getData: () => {
        return {
            account: account.val()
        }
    }
})