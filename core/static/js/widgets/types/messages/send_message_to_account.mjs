import { InfoModal } from '../../../core/info_modal.mjs';

export let promptAccountsAndNewMessage = (accounts) => {

    let infoModal = new InfoModal("New Message");
    let modalBody = infoModal.getBody();

    let form = document.createElement("form");
    modalBody.append(form);

    let formGroup = document.createElement("div");
    formGroup.className = "form-group";
    form.append(formGroup);

    let labelRecipient = document.createElement("label");
    labelRecipient.textContent = "Recipient:";
    formGroup.append(labelRecipient);

    let recipients=document.createElement("select");
    recipients.className = "form-control";
    for(let val in accounts){
        if(accounts[val].company!==null && accounts[val].company!==""){
        var option = document.createElement("option");
        option.value = accounts[val].id;
        option.text = accounts[val].company.charAt(0).toUpperCase()+accounts[val].company.slice(1);
        recipients.appendChild(option);
        }
    }

    formGroup.append(recipients);


    let labelMessage = document.createElement("label");
    labelMessage.textContent = "Message:";
    formGroup.append(labelMessage);

    let textArea = document.createElement("textarea");
    textArea.className = "form-control";
    textArea.setAttribute("maxlength", 1000);
    formGroup.append(textArea);

    let submitButton = document.createElement("button");
    submitButton.textContent = "Send";
    submitButton.className = "btn btn-primary";
    infoModal.getFooter().append(submitButton);

    submitButton.addEventListener("click", ()=>{
        submitButton.disabled = true;
        submitButton.textContent = "Sending";
        $.ajax({
            url: "/widgets/data/send_message",
            data: JSON.stringify({
                "action": "send_message",
                "params": {
                    "to_account": recipients.value,
                    "data": textArea.value
                }
            }),
            contentType: 'application/json',
            method: "POST"
        })
        .fail((jqXHR, textStatus) => {
            let e = "HTTP error " + jqXHR.status + " " + textStatus + ": " + jqXHR.responseText;
            let alert = document.createElement("div");
            alert.className = "alert alert-danger";
            alert.textContent = "Error occurred while sending: " + e;
            modalBody.append(alert);
        })
        .then(()=>{
            let alert = document.createElement("div");
            alert.className = "alert alert-success";
            alert.textContent = "Message sent!";
            modalBody.append(alert);
            window.location.reload();
        })
        .always(()=>{
            submitButton.disabled = false;
            submitButton.textContent = "Send";
        });
    });
}