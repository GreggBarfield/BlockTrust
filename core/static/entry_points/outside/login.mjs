import {AsyncForm} from '/static/global/async_form.mjs';

let loginForm = $("#login_form");
let statusMessage = loginForm.find("#login_status_message");
let errorMessage = loginForm.find("#login_error_message");

let requestRedirectTo = null;

if (loginForm[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = loginForm[0].getAttribute("request_redirect_to");
}

let form = new AsyncForm({
    action: "/login/action",
    form: loginForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Logged in successfully!",
    loadingMessage: "Hang on, we're logging you in...",
    getData: () => {
        return {
            identifier: loginForm.find("input[name='identifier']").val(),
            password: loginForm.find("input[name='password']").val()
        }
    },
    requestRedirectTo: requestRedirectTo
});

$(function() {
    if ("rememberMe" in localStorage && localStorage.rememberMe) {
        $('#remember_me').attr('checked', 'checked');
        $('#login_username').val(localStorage.userName);
        $('#login_password').val(localStorage.password);
    } else {
        $('#remember_me').removeAttr('checked');
        $('#login_username').val('');
        $('#login_password').val('');
    }

    $("form").submit(function(){
        if ($('#remember_me').is(':checked')) {
            // save username and password
            localStorage.userName = $('#login_username').val();
            localStorage.password = $('#login_password').val();
            localStorage.rememberMe = true;
        }
        else {
            localStorage.removeItem("userName");
            localStorage.removeItem("password");
            localStorage.removeItem("rememberMe")
        }
    });
});