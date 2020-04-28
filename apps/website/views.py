from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from apps.administrador.models import Categorias


def getCategoriasPrincipal():
    return Categorias.objects.filter(
        principal=True)

class Home(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['cat_padres'] = getCategoriasPrincipal()

        return context