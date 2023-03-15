import { InfoModal } from '../../js/core/info_modal.mjs';

let addUserButtons = document.getElementsByName("add-user-for-partner");
for(let button of addUserButtons) {
    button.onclick =() => {
        let infoModal = new InfoModal(`Invite new user for ${button.getAttribute("partner-name")}`);
        let modalBody = infoModal.getBody();

        let form = document.createElement("form");

        let formGroup = document.createElement("div");
        formGroup.className = "form-group";

        let emailLabel = document.createElement("label");
        emailLabel.textContent = "Email:";
        formGroup.append(emailLabel);

        let emailInput = document.createElement("input");
        emailInput.className = "form-control";
        formGroup.append(emailInput);
 
        form.append(formGroup);       
        modalBody.append(form);

        let inviteButton = document.createElement("button");
        inviteButton.textContent = "Invite";
        inviteButton.className = "btn btn-primary";
        infoModal.getActionButtonDiv().append(inviteButton);

        let alert = document.createElement("div");
        modalBody.append(alert);

        inviteButton.addEventListener("click", ()=>{
            inviteButton.disabled = true;
            inviteButton.textContent = "Inviting...";
            alert.className = "d-none";
            $.ajax({
                url: "/employee/dashboard/invite-user/" + button.id,
                data: JSON.stringify({
                    "email": emailInput.value
                }),
                contentType: 'application/json',
                method: "POST"
            })
            .fail((jqXHR, textStatus) => {
                alert.className = "alert alert-danger";
                alert.textContent = "Error occurred: " + jqXHR.responseText;
                inviteButton.disabled = false;
                inviteButton.textContent = "Invite";
            })
            .then(()=>{
                alert.className = "alert alert-success";
                alert.textContent = "Invitation sent!";
                inviteButton.textContent = "Success";
                window.location.reload();
            })
        });
    };
}