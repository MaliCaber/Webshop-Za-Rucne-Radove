from django import forms
from django.forms.fields import IntegerField
from django.forms.forms import Form


class DodajUKorpuForm(forms.Form):
    kolicina = forms.IntegerField()