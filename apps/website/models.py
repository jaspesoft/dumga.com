from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from apps.administrador.models import Paises, Ciudades, Estados


class Clientes(models.Model):
    """
        Definición de Cliente Vima.
        Basado en el modelo User de Django, agrega país, documento de identidad
        y teléfono a un usuario
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pais = models.ForeignKey(Paises, on_delete=models.PROTECT, related_name='pk_usuario_pais')
    documento_identidad = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Documento de Identificación'))
    telefono = models.CharField(max_length=40, null=True, blank=True, verbose_name=_('Número de teléfono'))

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_pk(self):
        self.pk

    class Meta:
        db_table = 'dg_clientes'
        verbose_name = _('cliente')
        verbose_name_plural = _('clientes')

class DireccionesCliente(models.Model):
    """
        Direcciones adicionales del cliente
    """
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True, blank=True)
    pais = models.ForeignKey(Paises, on_delete=models.PROTECT, related_name='pk_pais_direccion', verbose_name=_('País'))
    ciudad = models.ForeignKey(Ciudades, on_delete=models.PROTECT, null=True, blank=True, related_name='pk_direccion_estado',
        verbose_name=_('City'))
    estado = models.ForeignKey(Estados, on_delete=models.PROTECT, null=False, blank=False, related_name='pk_direccion_estado',
        verbose_name=_('State / Province'))
    telefono = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Teléfono'))
    zip_code = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Código postal'))
    direccion = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('Dirección'))
    direccion2 = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('Dirección 2 (Opcional)'))
    es_principal = models.BooleanField(
        default=False,
        verbose_name=_('¿Dirección principal?'))

    class Meta:
        db_table = 'dg_clientes_direcciones'

class Articulos(models.Model):
    pass