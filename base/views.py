from django.shortcuts import render
from artikal.models import Artikal

# Create your views here.

def frontpage(request):
    najnoviji_artikli = []
    for item in Artikal.objects.all():
        if item.nema_na_stanju is True:
            continue
        najnoviji_artikli.append(item)
        if len(najnoviji_artikli) > 7:
            break
    context = {
        'najnoviji_artikli': najnoviji_artikli,
    }
    return render(request, 'base/frontpage.html', context)


def kontaktpage(request):
    return render(request, 'base/kontakt.html')