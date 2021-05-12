import {AsyncForm} from '/static/global/async_form.mjs';

let passwordChangeForm=$("#password_change_confirmation_form");
let statusMessage=passwordChangeForm.find("#password_change_status_message")
let errorMessage=passwordChangeForm.find("#password_change_error_message")

let requestRedirectTo="";

if(passwordChangeForm[0].hasAttribute("request_redirec_to")){
    requestRedirectTo=passwordChangeForm[0].getAttribute("request_redirect_to")
}

let form=new AsyncForm({
    action: "/reset_password/action",
    form=passwordChangeForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Changed password successfully!",
    loadingMessage: "Hang on, we're changing your password...",
    getData: ()=>{
        return {
            password: passwordChangeForm.find("input[name='password']").val(),
            confirm_password: passwordChangeForm.find("input[name='confirm_password']").val()
        }
    }
});