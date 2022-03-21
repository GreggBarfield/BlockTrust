document.addEventListener('DOMContentLoaded', async () => {
    const {publishableKey} = await fetch('/stripe/config/'+account_id).then((r) => r.json());
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
      let sales_group_price = document.getElementById("amount").value;
      // Make a call to the server to create a new payment intent and store its client_secret.
      const {error: backendError, clientSecret} = await fetch(
        '/stripe/create-payment-intent/sales-group/'+account_id,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            currency: 'usd',
            paymentMethodType: 'card',
            amount: sales_group_price,
            sales_group_id: sales_group_id
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
          '/dashboard/sales-group/transaction/log-transaction-details',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              sales_group_id: sales_group_id,
              paymentIntent: paymentIntent.id,
              to_account_id: account_id,
              amount: sales_group_price
            }),
          }
        ).then((r) => r.json());
      }
      form.querySelector('button').textContent = "Success! Redirecting...";
      //partner_id must be set in the parent page
      window.location.href = '/dashboard/sales-groups';
    });
});

const addMessage = (message) => {
    const messagesDiv = document.querySelector('#messages');
    messagesDiv.style.display = 'block';
    messagesDiv.innerHTML += `${message}<br>`;
    console.log(`Debug: ${message}`);
  };