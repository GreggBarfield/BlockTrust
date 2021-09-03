import { InfoModal } from '../../../core/info_modal.mjs';

export let promptNewMessage = (toAccount, toAccountName=null) => {

    let toStr = toAccountName;

    if (toStr === null || toStr == undefined) {
        if (typeof toAccount === "number") {
            toStr = "Account ID " + toAccount;
        }
        else {
            throw "Needs to know who to send the message to";
        }
    }

    let infoModal = new InfoModal("Sending Message To: <span class='text-primary'>" + toStr + "</span>");
    let modalBody = infoModal.getBody();

    let form = document.createElement("form");
    modalBody.append(form);

    let formGroup = document.createElement("div");
    formGroup.className = "form-group";
    form.append(formGroup);

    let label = document.createElement("label");
    label.textContent = "Message:";
    formGroup.append(label);

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
                    "to_account": toAccount,
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