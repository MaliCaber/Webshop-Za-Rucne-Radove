from django import forms
from django.forms.fields import CharField 

class CheckoutForm(forms.Form):
    ime = forms.CharField(max_length=255)
    prezime = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    telefon = forms.CharField(max_length=255)
    adresa = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    mesto = forms.CharField(max_length=255)
    stripe_token = forms.CharField(max_length=255)