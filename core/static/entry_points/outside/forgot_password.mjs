import {AsyncForm} from '/static/global/async_form.mjs';

let resetPasswordForm=$("#password_reset_form");
let statusMessage=resetPasswordForm.find("#reset_status_message")
let errorMessage=resetPasswordForm.find("#reset_error_message")

let requestRedirectTo= null;

if(resetPasswordForm[0].hasAttribute("request_redirect_to")){
    requestRedirectTo=resetPasswordForm[0].getAttribute("request_redirect_to")
}

let form=new AsyncForm({
    action: "/request-password-reset",
    form: resetPasswordForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Email sent!",
    loadingMessage: "Hang on, sending you a mail...",
    getData: ()=>{
        return {
            email: resetPasswordForm.find("input[name='email']").val()
        }
    },
    requestRedirectTo: requestRedirectTo
});