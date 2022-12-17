from django.db import models
from artikal.models import Artikal
from prodavac.models import Prodavac

# Create your models here.
class Porudzbenica(models.Model):
    ime = models.CharField(max_length=100)
    prezime = models.CharField(max_length=100) 
    email = models.CharField(max_length=100)
    adresa = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    mesto = models.CharField(max_length=100)
    telefon = models.CharField(max_length=100) 
    napravljena = models.DateTimeField(auto_now_add=True)
    placen_iznos = models.DecimalField(max_digits=8, decimal_places=2)
    prodavci = models.ManyToManyField(Prodavac, related_name="porudzbenice")

    class Meta:
        ordering = ['-napravljena']

    def __str__(self):
        return self.ime

class PoruceniArtikal(models.Model):
    porudzbenica = models.ForeignKey(Porudzbenica, related_name="stvari", on_delete=models.CASCADE)
    artikal = models.ForeignKey(Artikal, related_name="stvari", on_delete=models.CASCADE)
    prodavac = models.ForeignKey(Prodavac, related_name="stvari", on_delete=models.CASCADE)
    prodavac_platio = models.BooleanField(default=False)
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    kolicina = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_ukupna_cena(self):
        return self.cena * self.kolicina
