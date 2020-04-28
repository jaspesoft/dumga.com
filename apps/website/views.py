from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from apps.administrador.models import Categorias, Banners


def getCategoriasPrincipal():
    return Categorias.objects.filter(
        principal=True)

def getBanners():
    return Banners.objects.filter(activo=True)

class Home(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['cat_padres'] = getCategoriasPrincipal()
        context['banners'] = getBanners()

        return context