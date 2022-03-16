import {AsyncForm} from '/static/global/async_form.mjs';

let edituserForm = $("#edituser_form");
let statusMessage = edituserForm.find("#edituser_status_message");
let errorMessage = edituserForm.find("#edituser_error_message");

let username = edituserForm.find("#edituser_form_username");
let password = edituserForm.find("#edituser_form_password");
let email = edituserForm.find("#edituser_form_email");
let confirm_password = edituserForm.find("#edituser_form_confirm_password");
let first = edituserForm.find("#edituser_form_first");
let last = edituserForm.find("#edituser_form_last");
let phone = edituserForm.find("#edituser_form_phone");

let form = new AsyncForm({
    action: "/dashboard/edit/edituser",
    form: edituserForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Updated successfully!",
    loadingMessage: "Hang on, we're updating your account...",
    getData: () => {
        return {
            username: username.val(),
            password: password.val(),
            email: email.val(),
            confirm_password: confirm_password.val(),
            first: first.val(),
            last: last.val(),
            phone: phone.val()
        }
    }
});


