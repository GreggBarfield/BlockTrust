import {AsyncForm} from '/static/global/async_form.mjs';

$(document).ready(function(){
    $('#signup_form_sector').change(function(){
        $("#signup_form_partner").empty();
        $("#signup_form_partner").append('<option disabled selected value>-- Select an option --</option>');
        $("#signup_form_partner").append('<option value=0>No Partner</option>')
        if($(this).val()==4){
            for(let val in partners){
                if(partners[val].company!=="" && partners[val].company!==null && partners[val].sector==4){
                    $("#signup_form_partner").append(`<option value="${partners[val].id}">${partners[val].company}</option>`);
                }
            }
        }
        if($(this).val()==5){
            for(let val in partners){
                if(partners[val].company!=="" && partners[val].company!==null && partners[val].sector==5){
                    $("#signup_form_partner").append(`<option value="${partners[val].id}">${partners[val].company}</option>`);
                }
            }
        }
        if($(this).val()==6){
            for(let val in partners){
                if(partners[val].company!=="" && partners[val].company!==null && partners[val].sector==6){
                    $("#signup_form_partner").append(`<option value="${partners[val].id}">${partners[val].company}</option>`);
                }
            }
        }
        if($(this).val()==7){
            for(let val in partners){
                if(partners[val].company!=="" && partners[val].company!==null && partners[val].sector==7){
                    $("#signup_form_partner").append(`<option value="${partners[val].id}">${partners[val].company}</option>`);
                }
            }
        }
    })

    $("#signup_form_partner").change(function(){
        if($(this).val() == 0){
            $("#signup_form_partner_id").prop('disabled', true);
        }
        else{
            $("#signup_form_partner_id").prop('disabled', false);
        }
    })
})


let signupForm = $("#internal_signup_form");
let statusMessage = signupForm.find("#signup_status_message");
let errorMessage = signupForm.find("#signup_error_message");

let sector = signupForm.find('#signup_form_sector')
let email = signupForm.find("#signup_form_email");
let password = signupForm.find("#signup_form_password");
let confirm_password = signupForm.find("#signup_form_confirm_password");
let first_name = signupForm.find("#signup_form_first");
let last_name = signupForm.find("#signup_form_last");
let phone = signupForm.find("#signup_form_phone");
let partner = signupForm.find("#signup_form_partner");
let partner_id = signupForm.find("#signup_form_partner_id");
let company = signupForm.find("#signup_form_company");
let address = signupForm.find("#signup_form_address");
let city = signupForm.find("#signup_form_city");
let state = signupForm.find("#signup_form_state");
let zip_code = signupForm.find("#signup_form_zip");
let personal_phone = signupForm.find("#signup_form_personal_phone")

let form = new AsyncForm({
    action: "/internal/signup/action",
    form: signupForm[0],
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
            phone: phone.val(),
            partner: partner.val(),
            affiliate_id: partner_id.val(),
            sector: sector.val(),
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip_code: zip_code.val(),
            personal_phone: personal_phone.val()
        }
    }
});
