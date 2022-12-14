from . import views
from django.urls import path



app_name = 'artikal'


urlpatterns = [
    path('pretraga', views.pretraga, name="pretraga"),
    path('<slug:kategorija_slug>/<slug:artikal_slug>/', views.artikal, name="artikal"),
    path('<slug:kategorija_slug>/', views.kategorija, name="kategorija"),
    
]
