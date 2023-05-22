import {AsyncForm} from '/static/global/async_form.mjs';
import { InfoModal } from '../../../js/core/info_modal.mjs';

let editaccountForm = $("#edit_account_form");
let statusMessage = editaccountForm.find("#edit_account_status_message");
let errorMessage = editaccountForm.find("#edit_account_error_message");

let company = editaccountForm.find("#edit_account_company");
let address = editaccountForm.find("#edit_account_address");
let city = editaccountForm.find("#edit_account_city");
let state = editaccountForm.find("#edit_account_state");
let zip = editaccountForm.find("#edit_account_zip");
let phone = editaccountForm.find("#edit_account_phone");
let showRealName = editaccountForm.find("#edit_account_show_real_name");

let form = new AsyncForm({
    action: "/dashboard/edit/edit-account",
    form: editaccountForm[0],
    status: statusMessage[0],
    error: errorMessage[0],
    redirectMessage: "Updated successfully!",
    loadingMessage: "Hang on, we're updating your account...",
    getData: () => {
        return {
            company: company.val(),
            address: address.val(),
            city: city.val(),
            state: state.val(),
            zip: zip.val(),
            phone: phone.val(),
            show_real_name: showRealName.is(":checked")? 1:0
        }
    }
});

document.getElementsByName("reset-password-user").forEach((element) => {
    element.addEventListener("click", async() => {
        let [userID, userName] = [element.getAttribute("user-id"),element.getAttribute("user-name")];
        document.getElementById(`spinner-${userID}`).classList.toggle("d-inline");

        const response = await fetch(`/dashboard/user/${userID}`, {
            method: 'PUT',
            body: JSON.stringify({reset_password: true}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        })

        document.getElementById(`spinner-${userID}`).classList.toggle("d-inline");
        let infoModal = response.ok ? new InfoModal(`Reset password was successful for ${userName}`)
            : infoModal = new InfoModal(`Operation failed. Please try again later or contact support`);            
        infoModal.getBody().classList.add("d-none");
        infoModal.getHeader().classList.add("text-center", "p-4")
    })
});


