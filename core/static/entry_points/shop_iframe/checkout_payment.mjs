var subTotal=parseFloat(localStorage.getItem('totalPrice'));
var subTotalDisplay=subTotal.toFixed(2);
var ship=parseFloat(localStorage.getItem('shipping'));
var shipDisplay=ship.toFixed(2);
var tax=parseFloat(localStorage.getItem('totalTax'));
var taxDisplay=tax.toFixed(2);
var discount=parseFloat(localStorage.getItem('discount'));
var discountDisplay=discount.toFixed(2);
var grandTotal=parseFloat(localStorage.getItem('grandTotal'));
var grandTotalDisplay=grandTotal.toFixed(2);
$("#subtotal").text(subTotalDisplay);
$("#shipping").text(shipDisplay);
$("#tax").text(taxDisplay);
$("#discount").text(discountDisplay);
$("#grandTotal").text(grandTotalDisplay);
$("#grand-total-warning-text").text(grandTotalDisplay) 

let paymentForm = $("#payment-form");
let statusMessage = paymentForm.find("#payment_status_message");
let errorMessage = paymentForm.find("#payment_error_message");
let orderDetailsString=""
if(localStorage.orderDetails){
    orderDetailsString=localStorage.getItem("orderDetails") 
    let orderDetails = JSON.parse(orderDetailsString)
    $("#name").val(orderDetails['first_name'] + " " + orderDetails['last_name'])
}

let requestRedirectTo = null;

if (paymentForm[0].hasAttribute("request_redirect_to")) {
    requestRedirectTo = paymentForm[0].getAttribute("request_redirect_to");
}


document.addEventListener('DOMContentLoaded', async () => {
    const {publishableKey} = await fetch('/stripe/config/'+partner_id).then((r) => r.json());
    if (!publishableKey) {
      addMessage(
        'No publishable key returned from the server. Please contact system administrator'
      );
      alert('Something is wrong. Please contact system administrator');
    }
  
    const stripe = Stripe(publishableKey);
    // , {
    //     apiVersion: '2020-08-27',
    //   }
    const elements = stripe.elements();
    const card = elements.create('card');
    card.mount('#card-element');
  
    const form = document.getElementById('payment-form');
    let submitted = false;
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      // Disable double submission of the form
      if(submitted) { return; }
      submitted = true;
      form.querySelector('button').disabled = true;
      form.querySelector('button').textContent = "Processing...";
      
    // Make a call to the server to create a new order
    const {error, orderId} = await fetch(
        '/shop/external/create-order',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            orderDetails: localStorage.getItem("orderDetails"),
          }),
        }
      ).then((r) => r.json());
    
      if (error) {
        addMessage(error);
  
        // reenable the form.
        submitted = false;
        form.querySelector('button').disabled = false;
        form.querySelector('button').textContent = "Pay";
        return;
      }

      // Make a call to the server to create a new payment intent and store its client_secret.
      const {error: backendError, clientSecret} = await fetch(
        '/stripe/create-payment-intent/'+partner_id,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            currency: 'usd',
            paymentMethodType: 'card',
            amount: localStorage.getItem('grandTotal'),
            orderId: orderId
          }),
        }
      ).then((r) => r.json());
  
      if (backendError) {
        addMessage(backendError.message);
  
        // reenable the form.
        submitted = false;
        form.querySelector('button').disabled = false;
        form.querySelector('button').textContent = "Pay";
        return;
      }
  
      const nameInput = document.querySelector('#name');
  
      // Confirm the card payment given the clientSecret from the payment intent that was just created on the server
      const {error: stripeError, paymentIntent} = await stripe.confirmCardPayment(
        clientSecret,
        {
          payment_method: {
            card: card,
            billing_details: {
              name: nameInput.value,
            },
          },
        }
      );
  
      if (stripeError) {
        addMessage(stripeError.message);
  
        // reenable the form.
        submitted = false;
        form.querySelector('button').disabled = false;
        form.querySelector('button').textContent = "Pay";
        return;
      }
  
      if(paymentIntent.status === 'succeeded'){
        //Not using the error or success here. Just sending the POST request
        const {error, success} = await fetch(
          '/shop/external/update-order',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              orderId: orderId,
              paymentIntent: paymentIntent.id,
              orderDetails: localStorage.getItem("orderDetails")
            }),
          }
        ).then((r) => r.json());
      }
      form.querySelector('button').textContent = "Success! Redirecting...";
      //partner_id must be set in the parent page
      window.location.href = '/external/invoice/'+partner_id;
    });
  });
  
  const addMessage = (message) => {
    const messagesDiv = document.querySelector('#messages');
    messagesDiv.style.display = 'block';
    messagesDiv.innerHTML += `${message}<br>`;
    console.log(`Debug: ${message}`);
  };