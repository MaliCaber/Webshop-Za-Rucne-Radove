from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'prodavac'


urlpatterns = [
    path('', views.prodavci, name="prodavci"),
    path('postani-prodavac/', views.postani_prodavac, name="postani-prodavac"),
    path('prodavac-admin/', views.prodavac_admin, name="prodavac-admin"),
    path('uredi-prodavca/', views.uredi_prodavca, name="uredi-prodavca"),

    path('dodaj-artikal/', views.dodaj_artikal, name="dodaj-artikal"),

    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='prodavac/login.html'), name="login"),

    path('<int:prodavac_id>/', views.prodavac, name="prodavac"),
]
