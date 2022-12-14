import stripe #pip install stripe 

from django. conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from .korpa import Korpa
from .forms import CheckoutForm

from porudzbenica.utilities import checkout, notify_prodavac, notify_kupac

# Create your views here.
def detalji_korpe(request):
    korpa = Korpa(request)


    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            try:
                charge = stripe.Charge.create(
                    amount=int(korpa.get_ukupna_cena() * 100), # Amount in Cents
                    currency='USD',
                    description='Racun od prodavnice',
                    source=stripe_token
                )

                ime = form.cleaned_data['ime']
                prezime = form.cleaned_data['prezime']
                email = form.cleaned_data['email']
                telefon = form.cleaned_data['telefon']
                adresa = form.cleaned_data['adresa']
                zipcode = form.cleaned_data['zipcode']
                mesto = form.cleaned_data['mesto']

                porudzbenica = checkout(request, ime, prezime, email, telefon, adresa, zipcode, mesto, korpa.get_ukupna_cena())

                korpa.ocisti()

                # SEnd Email Notification
                notify_kupac(porudzbenica)
                notify_prodavac(porudzbenica)

                return redirect('korpa:uspesno')
            
            except Exception:
                messages.error(request, "Greska prilikom obrade kupovine")
            
    else:
        form = CheckoutForm()

    ukloni_iz_korpe = request.GET.get('ukloni_iz_korpe', '')
    azuriraj_kolicinu = request.GET.get('azuriraj_kolicinu', '')
    kolicina = request.GET.get('kolicina', 0)

    if ukloni_iz_korpe:
        korpa.ukloni(ukloni_iz_korpe)
        return redirect('korpa:korpa')
    
    if azuriraj_kolicinu:
        korpa.dodaj(azuriraj_kolicinu, kolicina, True)
        return redirect('korpa:korpa')
        
    return render(request, 'korpa/korpa.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})


def success(request):
    return render(request, 'korpa/uspesno.html')