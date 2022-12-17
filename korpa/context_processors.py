from .korpa import Korpa


def korpa(request):
    return {'korpa': Korpa(request)}