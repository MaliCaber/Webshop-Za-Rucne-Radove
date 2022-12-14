from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import OneToOneField

# Create your models here.

class Prodavac(models.Model):
    ime = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='prodavac', on_delete=models.CASCADE)

    class Meta:
        ordering = ['ime']
    
    def __str__(self):
        return self.ime

    def get_stanje(self):
        stvari = self.stvari.filter(prodavac_platio=False, porudzbenica__prodavci__in=[self.id])
        return sum((item.artikal.cena * item.kolicina) for item in stvari)

    def get_placeni_iznos(self):
        stvari = self.stvari.filter(prodavac_platio=True, porudzbenica__prodavci__in=[self.id])
        return sum((item.artikal.cena * item.kolicina) for item in stvari)

