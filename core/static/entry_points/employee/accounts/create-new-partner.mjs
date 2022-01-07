import {AsyncForm} from '/static/global/async_form.mjs';

let partnerForm = $("#partner_form");
let statusMessage = partnerForm.find("#partner_status_message");
let errorMessage = partnerForm.find("#partner_error_message");

let sector = partnerForm.find('#partner_form_sector');
let phone = partnerForm.find("#partner_form_phone");
let company = partnerForm.find("#partner_form_company");
let address = partnerForm.find("#partner_form_address");
let city = partnerForm.find("#partner_form_city");
let state = partnerForm.find("#partner_form_state");
let zip_code = partnerForm.find("#partner_form_zip");
let contact_name = partnerForm.find("#partner_form_contact_name");
let contact_email = partnerForm.find("#partner_form_contact_email");
let show_on_signup = partnerForm.find("#partner_form_show_on_signup");
let form = new AsyncForm({
    action: "/employee/dashboard/create-new-partner/action",
    form: partnerForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Partner created successfully!",
    loadingMessage: "Hang on, setting up the partner account...",
    getData: () => {
        return {
            phone: phone.val(),
            sector: sector.val(),
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip_code: zip_code.val(),
            contact_name: contact_name.val(),
            contact_email: contact_email.val(),
            show_on_signup: show_on_signup[0].checked
        }
    }
});


