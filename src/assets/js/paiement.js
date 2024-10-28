document.addEventListener('DOMContentLoaded', function () {
    const stripe = Stripe('pk_test_51Q9AeFJ8wvBEc7MTo5uzCOgnu9fOZ7CBtsFfSYbZnX6E9cC17MmlTyZsqHxhAAQaaqgccHxIfdmDBlXctnVO2XtV00AQMqxFzM');
    const elements = stripe.elements();

    // Example for setting up a card input
    const card = elements.create('card');
    card.mount('#card-element');

    // Handle form submission
    const form = document.getElementById('payment-form');
    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const {paymentIntent, error} = await stripe.confirmCardPayment(
            clientSecret, {  
                payment_method: {
                    card: card,
                }
            }
        );

        if (error) {
            console.log(error.message);
            document.getElementById('payment-status').classList.add('alert alert-danger')
            document.getElementById('payment-status').textContent = error.message;
            
        } else {
            console.log("Payment successful!");
            document.getElementById('payment-status').classList.add('alert-success')
            document.getElementById('payment-status').textContent = "Paiement réussi !";
            
            fetch('/update-statusPayment/', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'), 
                },
                body: JSON.stringify({
                    order_id: orderId,
                }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Order status updated:', data); 
                setTimeout(()=>{
                    window.location.href = `/confirmation-commande/${orderId}/`; 
                },2000)
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        }

    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}