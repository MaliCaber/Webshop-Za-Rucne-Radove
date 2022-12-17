from artikal.models import Kategorija


def menu_kategorije(request):
    kategorije = Kategorija.objects.all()
    return {'kategorije': kategorije}