from django.shortcuts import render
from artikal.models import Artikal

# Create your views here.

def frontpage(request):
    najnoviji_artikli  = Artikal.objects.all()[0:8]
    context = {
        'najnoviji_artikli': najnoviji_artikli,
    }
    return render(request, 'base/frontpage.html', context)


def kontaktpage(request):
    return render(request, 'base/kontakt.html')