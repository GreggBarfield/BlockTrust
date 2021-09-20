import {AsyncForm} from '/static/global/async_form.mjs';

$(document).ready(function () {
    for(let val in account_users){
        if(account_users[val].name!=="" && account_users[val].company!==null){
            $("#user").append(`<option value="${account_users[val].id}">${account_users[val].first_name} ${account_users[val].last_name}</option>`)
        }
}
});

let userForm = $("#select_user_form");
let statusMessage = userForm.find("#user_status_message");
let errorMessage = userForm.find("#user_error_message");

let user = userForm.find("#user");

let form = new AsyncForm({
    action: "/employee/dashboard/login-as-user/action",
    form: userForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Redirecting to User Dashboard...",
    loadingMessage: "Logging you in...",
    getData: () => {
        return {
            user: user.val()
        }
    }
})