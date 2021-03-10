import { preventEnter } from '../core/form.mjs';
import {ajax} from '../core/network.mjs';

/**
 * Handler for submit event (AJAX)
 * 
 * @param e HTML Event
 */
function onSubmit(e) {
    e.preventDefault();
    let form = e.target;
    let submitter = e.submitter;

    let first = "", last = "", phone = "", email = "", message = "";

    if ('first' in form.elements)
        first = form.elements.first.value;
    if ('last' in form.elements)
        last = form.elements.last.value;
    if ('phone' in form.elements)
        phone = form.elements.phone.value;
    if ('email' in form.elements)
        email = form.elements.email.value;
    if ('message' in form.elements)
        message = form.elements.message.value;

    if ('name' in form.elements) {
        first += " " + form.elements.name.value + " (name box, no first/last box)";
    }

    if (submitter) {
        submitter.disabled = true;
        submitter.textContent = "Sending...";
    }

    ajax({
        method: 'POST',
        url: '/outside/contact_response',
        contentType: 'application/json',
        data: JSON.stringify({
            'first': first,
            'last': last,
            'phone': phone,
            'email': email,
            'message': message,
        }),
    })
    .then(() => {
        let alert = document.createElement("div");
        alert.className = "alert alert-success mt-2";
        alert.textContent = "Message sent!";
        form.append(alert);

        if (submitter) {
            submitter.textContent = "Sent";
        }
    })
    .catch((err) => {
        let alert = document.createElement("div");
        alert.className = "alert alert-danger mt-2";
        alert.textContent = err;
        form.append(alert);
        if (submitter) {
            submitter.textContent = "Failed to send";
        }
    })
    .finally(()=>{
        if (submitter) {
            submitter.disabled = false;
        }
    });
}

/**
 * Attaches contact us logic to existing dom
 * 
 * @param form The form to attach to
 */
export function attach(form) {
    preventEnter(form);
    form.addEventListener("submit", onSubmit);
}

