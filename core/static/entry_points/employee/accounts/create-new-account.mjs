import {AsyncForm} from '/static/global/async_form.mjs';

$(document).ready(function(){
    $('#signup_form_sector').change(function(){
        $("#signup_form_partner").empty();
        $("#signup_form_partner").append('<option disabled selected value>-- Select an option --</option>');
        $("#signup_form_partner").append('<option value="">No Partner</option>')
        if($(this).val()==sectors_name_to_id["Cow-Calf"]){
            for(let val in partners){
                if(partners[val].name!=="" && partners[val].name!==null && partners[val].sector==sectors_name_to_id["Cow-Calf"]){
                    $("#signup_form_partner").append(`<option value="${partners[val].id}">${partners[val].name}</option>`);
                }
            }
        }
        if($(this).val()==sectors_name_to_id["Auction House"]){
            for(let val in partners){
                if(partners[val].name!=="" && partners[val].name!==null && partners[val].sector==sectors_name_to_id["Auction House"]){
                    $("#signup_form_partner").append(`<option value="${partners[val].id}">${partners[val].name}</option>`);
                }
            }
        }
        if($(this).val()==sectors_name_to_id["Feedlot"]){
            for(let val in partners){
                if(partners[val].name!=="" && partners[val].name!==null && partners[val].sector==sectors_name_to_id["Feedlot"]){
                    $("#signup_form_partner").append(`<option value="${partners[val].id}">${partners[val].name}</option>`);
                }
            }
        }
        if($(this).val()==sectors_name_to_id["Packer"]){
            for(let val in partners){
                if(partners[val].name!=="" && partners[val].name!==null && partners[val].sector==sectors_name_to_id["Packer"]){
                    $("#signup_form_partner").append(`<option value="${partners[val].id}">${partners[val].name}</option>`);
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
let signupForm = $("#employee_signup_form");
let statusMessage = signupForm.find("#signup_status_message");
let errorMessage = signupForm.find("#signup_error_message");

let sector = signupForm.find('#signup_form_sector');
let phone = signupForm.find("#signup_form_phone");
let partner = signupForm.find("#signup_form_partner");
let partner_id = signupForm.find("#signup_form_partner_id");
let company = signupForm.find("#signup_form_company");
let address = signupForm.find("#signup_form_address");
let city = signupForm.find("#signup_form_city");
let state = signupForm.find("#signup_form_state");
let zip_code = signupForm.find("#signup_form_zip");

let form = new AsyncForm({
    action: "/employee/dashboard/create-new-account/action",
    form: signupForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Account created successfully!",
    loadingMessage: "Hang on, setting up the account...",
    getData: () => {
        return {
            phone: phone.val(),
            partner: partner.val(),
            affiliate_id: partner_id.val(),
            sector: sector.val(),
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip_code: zip_code.val()
        }
    }
});