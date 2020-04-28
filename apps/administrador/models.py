from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters
# Create your models here.



class Paises(models.Model):
    """
    Modelo para lista de países.
    """
    codigo_pais = models.CharField(primary_key=True, max_length=3, blank=False, null=False, verbose_name=_('Código de país'))
    nombre_pais = models.CharField(max_length=250, blank=False, null=False, verbose_name=_('Nombre del país'))

    def __str__(self):
        return self.nombre_pais

    class Meta:
        db_table = 'dg_paises'
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ('nombre_pais',)


class Estados(models.Model):
    nombre = models.CharField(max_length=250, null=False, blank=False, verbose_name=_('Estado / Provincia'))
    pais = models.ForeignKey(Paises, on_delete=models.DO_NOTHING, null=False, blank=False, verbose_name=_('País'))

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'dg_estados'
        verbose_name = 'estado / provincia'
        verbose_name_plural = 'estados / provincias'
        ordering = ('nombre',)


class Ciudades(models.Model):
    """
    Modelo para lista de ciudades.
    """
    nombre_ciudad = models.CharField(max_length=250, blank=False, null=False, verbose_name=_('Nombre de la ciudad'))
    estado = models.ForeignKey(Estados, on_delete=models.DO_NOTHING, blank=False, null=False,
        related_name='pk_estados', verbose_name=_('Estado'))
    pais = models.ForeignKey(Paises, on_delete=models.DO_NOTHING, blank=False, null=False,
        related_name='pk_estados', verbose_name=_('País'))

    class Meta:
        db_table = 'dg_ciudades'
        verbose_name = 'ciudad'
        verbose_name_plural = 'ciudades'
        ordering = ('nombre_ciudad',)

    def __str__(self):
        return self.nombre_ciudad


class Categorias(models.Model):
    """
        Definición de Categorias.
    """
    descripcion = models.CharField(max_length=80, null=False, blank=False, verbose_name=_('Categoría'))
    imagen = models.FileField(upload_to='categorias/', null=True, blank=True)
    icono =  models.FileField(upload_to='categorias/icono', null=True, blank=True)
    url_categoria = models.SlugField(max_length=160, db_index=True, verbose_name='URL')
    cantidad_productos = models.IntegerField(default=0, verbose_name=_('Cantidad de productos'))
    principal = models.BooleanField(default=False, )
    mostrar_precio = models.BooleanField(default=True)
    activa = models.BooleanField(blank=False, default=True, verbose_name=_('¿Categoría activa?'))
    categoria_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=1,
        verbose_name=_('Categoría padre'))

    class Meta:
        db_table = 'dg_categorias'
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ('descripcion', 'categoria_padre_id', 'id',)

    def __str__(self):
        return self.descripcion

    def save(self, *args, **kwargs):
        if not self.id:
            self.url_categoria = defaultfilters.slugify(self.descripcion)
            super(Categorias, self).save(*args, **kwargs)
        else:
            super(Categorias, self).save(*args, **kwargs)

    def children(self):
        return Categorias.objects.filter(categoria_padre=self.pk)

    def serializable_object(self):
        obj = {'name': self.descripcion, 'hijos': []}
        for hijo in self.children():
            obj['hijos'].append(hijo.serializable_object())
        return obj

    def get_all_children(self, include_self=True):
        """Recursivamente obtiene todos los hijos de una categoria"""
        lista_hijos = []
        if include_self:
            lista_hijos.append(self)
        for categoria in Categorias.objects.filter(categoria_padre=self):
            _r = categoria.get_all_children(include_self=True)
            if 0 < len(_r):
                lista_hijos.extend(_r)
        return lista_hijos

    def get_ancestors(self):
        """Recursivamente obtiene todos los padres de una categoria"""
        if self.categoria_padre is None:
            return []
        return [self.categoria_padre
                ] + self.categoria_padre.get_ancestors()


class Banners(models.Model):
    archivo = models.FileField(upload_to='banners/%Y/%m/', null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name=_('¿Activo?'))

    class Meta:
        db_table = 'dg_banners'
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'