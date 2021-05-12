import {AsyncForm} from '/static/global/async_form.mjs';

let resetPasswordForm=$("#password_reset_form");
let statusMessage=resetPasswordForm.find("#reset_status_message")
let errorMessage=resetPasswordForm.find("#reset_error_message")

let requestredirectTo= null;

if(resetPasswordForm[0].hasAttribute("request_redirect_to")){
    requestRedirectTo=resetPasswordForm[0].getAttribute("request_redirect_to")
}

let form=new AsyncForm({
    action="/request_password_reset",
    form: resetPasswordForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "",
    loadingMessage: "",
    getData: ()=>{
        return {
            email: resetPasswordForm.find("input[name='email']").val()
        }
    }
});