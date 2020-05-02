from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, CreateView

from apps.administrador.models import Categorias, Banners
from apps.website.forms import UserCreateForm
from apps.website.models import Clientes


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

class AuthSignUp(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'website/auth.html'
    success_url = '/auth/signin'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            usuario = form.save()
            Clientes(
                user=usuario
            ).save()
            return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, cliente_form):
        return self.render_to_response(
            self.get_context_data(form=form, cliente_form=cliente_form))

    def get_context_data(self, **kwargs):
        context = super(AuthSignUp, self).get_context_data(**kwargs)

        return context

class AuthSignin(TemplateView):
    template_name = 'website/auth.html'