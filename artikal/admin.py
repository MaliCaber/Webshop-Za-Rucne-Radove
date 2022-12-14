from django.contrib import admin

# Register your models here.

from .models import Kategorija, Artikal

admin.site.register(Kategorija)
admin.site.register(Artikal)