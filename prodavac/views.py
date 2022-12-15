from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Prodavac
from artikal.models import Artikal
from .forms import ArtikalForm

# Converting Title into Slug
from django.utils.text import slugify

# Create your views here.


def prodavci(request):
    return render(request, 'prodavac/prodavci.html')


def postani_prodavac(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            prodavac = Prodavac.objects.create(ime=user.username, created_by=user)

            return redirect('base:home')
    else:
        form = UserCreationForm()   

    return render(request, 'prodavac/postani_prodavac.html', {'form': form})


@login_required
def prodavac_admin(request):
    prodavac = request.user.prodavac
    artikli = prodavac.artikli.all()
    porudzbenice = prodavac.porudzbenice.all()
    for porudzbenica in porudzbenice:
        porudzbenica.prodavac_kolicina = 0
        porudzbenica.prodavac_placeni_iznos = 0
        porudzbenica.fully_paid = True

        for item in porudzbenica.stvari.all():
            if item.prodavac == request.user.prodavac:
                if item.prodavac_platio:
                    porudzbenica.prodavac_placeni_iznos += item.get_ukupna_cena()
                else:
                    porudzbenica.prodavac_kolicina += item.get_ukupna_cena()
                    porudzbenica.fully_paid = False


    return render(request, 'prodavac/prodavac_admin.html', {'prodavac': prodavac, 'artikli': artikli, 'porudzbenice': porudzbenice})

@login_required
def dodaj_artikal(request):
    if request.method == 'POST':
        form = ArtikalForm(request.POST, request.FILES)

        if form.is_valid():
            artikal = form.save(commit=False)
            artikal.prodavac = request.user.prodavac
            artikal.slug = slugify(artikal.naziv)
            artikal.save()

            return redirect('prodavac:prodavac-admin')

    else:
        form = ArtikalForm

    return render(request, 'prodavac/dodaj_artikal.html', {'form': form})


@login_required
def uredi_prodavca(request):
    prodavac = request.user.prodavac

    if request.method == 'POST':
        ime  = request.POST.get('ime', '')
        email = request.POST.get('email', '')

        if ime:
            prodavac.created_by.email = email
            prodavac.created_by.save()

            prodavac.ime = ime
            prodavac.save()

            return redirect('prodavac:prodavac-admin')

    return render(request, 'prodavac/uredi_prodavca.html', {'prodavac': prodavac})


def prodavci(request):
    prodavci = Prodavac.objects.all()
    return render(request, 'prodavac/prodavci.html', {'prodavci': prodavci})

def prodavac(request, prodavac_id):
    prodavac = get_object_or_404(Prodavac, pk=prodavac_id)
    return render(request, 'prodavac/prodavac.html', {'prodavac': prodavac})


