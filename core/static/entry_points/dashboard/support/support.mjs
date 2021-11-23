import {AsyncForm} from '/static/global/async_form.mjs';

var form = document.createElement("form");
form.className = "bg-white";
form.id = "support-form";

var form_group = document.createElement("div");
form_group.className = "col-lg-8 align-self-center";

var first_name = document.createElement("input");
first_name.type = "text";
first_name.name= "first_name";
first_name.placeholder = "First Name";
first_name.value = first_name_value;
first_name.className = "form-control col-md-6 mb-2";
form_group.appendChild(first_name);

var last_name = document.createElement("input");
last_name.type = "text";
last_name.name= "last_name";
last_name.placeholder = "Last Name";
last_name.value = last_name_value;
last_name.className = "form-control col-md-6 mb-2";
form_group.appendChild(last_name);

var email = document.createElement("input");
email.type = "email";
email.name= "email";
email.placeholder = "Email";
email.value = email_value;
email.className = "form-control col-md-6 mb-2";
form_group.appendChild(email);

var phone = document.createElement("input");
phone.type = "text";
phone.name= "phone";
phone.placeholder = "Phone";
phone.value = phone_value;
phone.className = "form-control col-md-6 mb-2";
form_group.appendChild(phone);

var message = document.createElement("textarea");
message.rows = "5";
message.name= "message";
message.placeholder = "Your Message";
message.className = "form-control col-md-6 mb-2";
form_group.appendChild(message);

let submitButton = document.createElement("button");
submitButton.className = "btn btn-primary";
submitButton.textContent = "Submit";
submitButton.type = "button";

submitButton.addEventListener("click", () => {
            form1.submit();
});

form_group.append(submitButton);
form.appendChild(form_group);


let statusMessage = document.createElement("p");
statusMessage.style.display = "none";
statusMessage.className = "mt-2 mb-0";
form.append(statusMessage);
let errorMessage = document.createElement("p");
errorMessage.style.display = "none";
errorMessage.className = "mt-2 mb-0 alert alert-danger";
form.append(errorMessage);

let form1 = new AsyncForm({
    action: "/dashboard/support/action",
    form: form,
    status: statusMessage,
    error: errorMessage,
    redirectMessage: "Submitted!",
    loadingMessage: "Submitting...",
    getData: () => {
        return {
            first: first_name.value,
            last: last_name.value,
            email: email.value,
            phone: phone.value,
            message: message.value,
        }
    }
});
document.getElementById("card-body").appendChild(form);