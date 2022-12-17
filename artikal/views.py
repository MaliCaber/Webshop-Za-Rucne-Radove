import random 
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from .models import Kategorija, Artikal

from django.db.models import Q

from .forms import DodajUKorpuForm
from korpa.korpa import Korpa



def artikal(request, kategorija_slug, artikal_slug):

    korpa = Korpa(request)

    artikal = get_object_or_404(Artikal, kategorija__slug=kategorija_slug, slug=artikal_slug)


    if request.method == 'POST':
        form = DodajUKorpuForm(request.POST)

        if form.is_valid():
            kolicina = form.cleaned_data['kolicina']
            korpa.dodaj(artikal_id=artikal.id, kolicina=kolicina, azuriraj_kolicinu=False)

            messages.success(request, "Artikal je dodat u korpu.")

            return redirect('artikal:artikal', kategorija_slug=kategorija_slug, artikal_slug=artikal_slug)            
    
    else:
        form = DodajUKorpuForm()

    slicni_artikli = list(artikal.kategorija.artikli.exclude(id=artikal.id).exclude(nema_na_stanju=True))


    if len(slicni_artikli) >= 4:
        slicni_artikli = random.sample(slicni_artikli, 4)
        
    
    context = {
        'artikal': artikal,
        'slicni_artikli': slicni_artikli,
        'form': form,
    }

    return render(request, 'artikal/artikal.html', context)


def kategorija(request, kategorija_slug):
    kategorija = get_object_or_404(Kategorija, slug=kategorija_slug)
    return render(request,'artikal/kategorija.html', {'kategorija': kategorija})
	
def pretraga(request):
    query = request.GET.get('query', '')
    artikli = Artikal.objects.filter(Q(naziv__icontains=query) | Q(opis__icontains=query)).exclude(nema_na_stanju=True)
    return render(request, 'artikal/pretraga.html', {'artikli':artikli, 'query': query})
	
def artikal_obrisi(request, id):
    artikal = Artikal.objects.get(id=id)

    if request.method == 'POST':
        artikal.nema_na_stanju = True
        artikal.save()
        return redirect('prodavac:prodavac-admin')
    return render(request, 'artikal/obrisi.html', {'artikal': artikal})