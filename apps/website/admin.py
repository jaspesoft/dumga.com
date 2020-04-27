from django.contrib import admin

# Register your models here.
from apps.website.models import Clientes


@admin.register(Clientes)
class AdminClientes(admin.ModelAdmin):
    list_display = ['documento_identidad', 'get_email', 'get_username']
    list_filter = ['pais', ]