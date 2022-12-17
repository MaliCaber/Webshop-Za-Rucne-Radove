from django.conf import settings

from artikal.models import Artikal


class Korpa(object):
    def __init__(self, request):
        self.session = request.session
        korpa = self.session.get(settings.CART_SESSION_ID)

        if not korpa:
            korpa = self.session[settings.CART_SESSION_ID] = {}

        self.korpa = korpa

    def __iter__(self):
        for p in self.korpa.keys():
            self.korpa[str(p)]['artikal'] = Artikal.objects.get(pk=p)

        for item in self.korpa.values():
            item['ukupna_cena'] = item['artikal'].cena * item['kolicina']

            yield item

    def __len__(self):
        return sum(item['kolicina'] for item in self.korpa.values())

    def dodaj(self, artikal_id, kolicina=1, azuriraj_kolicinu=False):
        artikal_id = str(artikal_id)
        artikal = Artikal.objects.get(id=int(artikal_id))

        if artikal.nema_na_stanju is False:
            if artikal_id not in self.korpa:
                self.korpa[artikal_id] = {'kolicina': kolicina, 'id': artikal_id}

            if azuriraj_kolicinu:
                if self.korpa[artikal_id]['kolicina'] < artikal.kolicina_na_stanju:
                    self.korpa[artikal_id]['kolicina'] += int(kolicina)

                if int(kolicina) == -1 and self.korpa[artikal_id]['kolicina'] == artikal.kolicina_na_stanju:
                    self.korpa[artikal_id]['kolicina'] += int(kolicina)

                if self.korpa[artikal_id]['kolicina'] == 0:
                    self.ukloni(artikal_id)
        
        self.sacuvaj()

    def ukloni(self, artikal_id):
        if artikal_id in self.korpa:
            del self.korpa[artikal_id]
            self.sacuvaj()

    def sacuvaj(self):
        self.session[settings.CART_SESSION_ID] = self.korpa
        self.session.modified = True

    def ocisti(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_ukupna_cena(self):
        for p in self.korpa.keys():
            self.korpa[str(p)]['artikal'] = Artikal.objects.get(pk=p)

        return sum(item['kolicina'] * item['artikal'].cena for item in self.korpa.values())

        
