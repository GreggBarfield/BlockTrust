import {AsyncForm} from '/static/global/async_form.mjs';

let employeeForm = $("#employee_form");
let statusMessage = employeeForm.find("#employee_status_message");
let errorMessage = employeeForm.find("#employee_error_message");

let email = employeeForm.find("#employee_form_email");
let password = employeeForm.find("#employee_form_password");
let confirm_password = employeeForm.find("#employee_form_confirm_password");
let first_name = employeeForm.find("#employee_form_first");
let last_name = employeeForm.find("#employee_form_last");
let phone = employeeForm.find("#employee_form_phone");

let form = new AsyncForm({
    action: "/employee/dashboard/signup/action",
    form: employeeForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Account created successfully!",
    loadingMessage: "Hang on, setting up the account...",
    getData: () => {
        return {
            username: email.val(), //the email will be stored here in the backend
            password: password.val(),
            email: email.val(),
            confirm_password: confirm_password.val(),
            first_name: first_name.val(),
            last_name: last_name.val(),
            phone: phone.val()
        }
    }
});