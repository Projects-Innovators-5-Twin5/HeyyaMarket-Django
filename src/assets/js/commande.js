const stepElement = document.getElementsByClassName("step")[0]; 
const stepElement1 = document.getElementsByClassName("step")[1];

const step2Element = document.getElementsByClassName("step2")[0]; 
const step3Element = document.getElementsByClassName("step3")[0];

const step2Element1 = document.getElementsByClassName("step2")[1]; 
const step3Element1 = document.getElementsByClassName("step3")[1];

const adresse = document.getElementById('adressep')
const info = document.getElementById('infop')
const paiement = document.getElementById('paiementp')


const firstname = document.getElementById('first_namep')
const lastname = document.getElementById('last_namep')
const email = document.getElementById('emailp')
const adresseinput = document.getElementById('adresse_inputp')
const tel = document.getElementById('telp')
const alert = document.getElementById('alert-paiement')
const texterror = document.getElementById('text-errorp')

stepElement.addEventListener("click", function() {
    step2Element.classList.remove("active");
    step2Element1.classList.remove("active");
    step3Element.classList.remove("active");
    step3Element1.classList.remove("active");
    adresse.classList.add('d-none')
    info.classList.remove('d-none')
    paiement.classList.add('d-none')
});

step2Element.addEventListener("click", function() {
    if (firstname.value.trim() === '' || lastname.value.trim() === '' || email.value.trim() === '') {
        alert.classList.remove('d-none');
        texterror.textContent = 'Veuillez remplir tous les champs obligatoires.'
        return; 
    }
    alert.classList.add('d-none');
    step2Element.classList.add("active");
    step2Element1.classList.add("active");
    step3Element.classList.remove("active");
    step3Element1.classList.remove("active");
    adresse.classList.remove('d-none')
    info.classList.add('d-none')
    paiement.classList.add('d-none')
});


step3Element.addEventListener("click", function() {
    if (firstname.value.trim() === '' || lastname.value.trim() === '' || email.value.trim() === '' || adresseinput.value.trim() === '' || tel.value.trim() === '') {
        alert.classList.remove('d-none');
        texterror.textContent = 'Veuillez remplir tous les champs obligatoires.'
        return; 
    }
    alert.classList.add('d-none');
    step2Element.classList.add("active");
    step2Element1.classList.add("active");
    step3Element.classList.add("active");
    step3Element1.classList.add("active");
    adresse.classList.add('d-none')
    info.classList.add('d-none')
    paiement.classList.remove('d-none')
});
