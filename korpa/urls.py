from django.urls import path
from . import views



app_name = 'korpa'

urlpatterns = [
    path('', views.detalji_korpe, name="korpa"),
    path('uspesno/', views.success, name="uspesno"),
]
