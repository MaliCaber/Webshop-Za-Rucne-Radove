from io import BytesIO
from os import name
from PIL import Image
from django.core.files import File

from django.db import models
from prodavac.models import Prodavac
# Create your models here.


class Kategorija(models.Model):
    naziv = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    porucivanje = models.IntegerField(default=0)

    class Meta:
        ordering = ['porucivanje']

    def __str__(self):
        return self.naziv


class Artikal(models.Model):
    kategorija          = models.ForeignKey(Kategorija, related_name='artikli', on_delete=models.CASCADE)
    prodavac            = models.ForeignKey(Prodavac, related_name="artikli", on_delete=models.CASCADE)
    naziv               = models.CharField(max_length=50)
    opis                = models.TextField(blank=False, null=False)
    slika               = models.ImageField(upload_to='uploads/', blank=True, null=True)
    cena                = models.DecimalField(decimal_places=2, max_digits=10)
    slug                = models.SlugField(max_length=55)
    datum_dodavanja     = models.DateTimeField(auto_now_add=True)
    thumbnail           = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ['-datum_dodavanja']

    def __str__(self):
        return self.naziv
    

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.slika:
                self.thumbnail = self.make_thumbnail(self.slika)
                self.save()
                return self.thumbnail.url
            
            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, slika, size=(300, 200)):
        img = Image.open(slika)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=slika.name)

        return thumbnail
    
