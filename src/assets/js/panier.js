function updateCart(itemId, quantity, itemPrice) {

    const totalPrice = itemPrice * quantity;

    const totalPriceProduct = document.getElementById(`totalPrice-${itemId}`);
    totalPriceProduct.textContent = totalPrice.toFixed(2) + ' TND';

    const priceElements = document.querySelectorAll('.price-product');

    let totalSum = 0;

    priceElements.forEach(element => {
        const priceText = element.textContent.trim().replace(' TND', '');
        
        const price = parseFloat(priceText);
        
        if (!isNaN(price)) {
            totalSum += price;
        }
    });

    const totalPriceTotal = document.getElementById('total'); 
    totalPriceTotal.textContent = totalSum.toFixed(2) + ' TND';  


    fetch('update-cart/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), 
        },
        body: JSON.stringify({
            product_id: itemId,
            quantity: quantity,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Cart updated:', data); 
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

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