from django.forms import ModelForm, models

from artikal.models import Artikal


class ArtikalForm(ModelForm):
    class Meta:
        model = Artikal
        fields = ['kategorija', 'slika', 'naziv', 'opis', 'kolicina_na_stanju', 'cena']