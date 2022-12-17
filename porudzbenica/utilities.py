from korpa.korpa import Korpa

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Artikal

from .models import Porudzbenica, PoruceniArtikal

def checkout(request, ime, prezime, email, adresa, zipcode, mesto, telefon, placeni_iznos):
    porudzbenica = Porudzbenica.objects.create(ime=ime, prezime=prezime, email=email, adresa=adresa, zipcode=zipcode, mesto=mesto, telefon=telefon, placen_iznos=placeni_iznos)

    for item in Korpa(request):
        PoruceniArtikal.objects.create(porudzbenica=porudzbenica, artikal=item['artikal'], prodavac=item['artikal'].prodavac, cena=item['artikal'].cena, kolicina=item['kolicina'])
        porudzbenica.prodavci.add(item['artikal'].prodavac)

        artikal = Artikal.objects.get(id=item['artikal'].id)
        kolicina = item['kolicina']

        artikal.kolicina_na_stanju = artikal.kolicina_na_stanju - kolicina
        artikal.save()
        if artikal.kolicina_na_stanju == 0:
            artikal.nema_na_stanju = True
            artikal.save()

    return porudzbenica

def notify_prodavac(porudzbenica):
    try:
        from_email = settings.DEFAULT_EMAIL_FROM

        for prodavac in porudzbenica.prodavci.all():
            to_email = prodavac.created_by.email
            subject = 'Nova porudzbenica'
            text_content = 'Imate novu porudzbenicu!'
            html_content = render_to_string('porudzbenica/email_notify_prodavac.html', {'porudzbenica': porudzbenica, 'prodavac': prodavac})

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
    except:
        print("nes ne valja u emailu prodavca")

def notify_kupac(porudzbenica):
    try:
        from_email = settings.DEFAULT_EMAIL_FROM

        to_email = porudzbenica.email
        subject = 'Potvrda porudzbenice'
        text_content = 'Hvala na kupovini!'
        html_content = render_to_string('porudzbenica/email_notify_kupac.html', {'porudzbenica': porudzbenica})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    except:
        print("nes ne valja u emailu kupca")