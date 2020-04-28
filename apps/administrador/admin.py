from django.contrib import admin

# Register your models here.
from apps.administrador.models import Categorias


@admin.register(Categorias)
class AdminCategorias(admin.ModelAdmin):
    list_display = ('descripcion', 'url_categoria', 'cantidad_productos', 'activa')
    list_filter = ['principal', 'activa']
