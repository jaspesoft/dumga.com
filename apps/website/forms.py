from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, TextInput, EmailInput
from django.utils.translation import ugettext_lazy as _
from apps.website.models import Clientes

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'pais',
            'documento_identidad',
            'telefono',
        ]

class UserCreateForm(forms.ModelForm):
    """
        Formulario para creación de usuario.
    """
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'message': _('The field password is required')}))
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'message': _('The field Confirm Password is required')
        }))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields:
            print(campo)
            self.fields[campo].widget.attrs.update({'class': 'form-control'})

    def clean_password2(self):
        """Validación de contraseñas iguales."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = _('Passwords do not match')
            raise forms.ValidationError(msg)
        return password2

    def clean_username(self):
        value = self.cleaned_data.get("username")
        """Validación de usuario existente."""
        number_occurrences = User.objects.filter(username=value).count()
        if number_occurrences > 0:
            raise forms.ValidationError(_('Username already exists, enter a different one'))
        return value


    def save(self, commit=True):
        """Redefinición de método ``save()`` para guardar la contraseña."""
        try:
            user = super(UserCreateForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password1"])
        except ValidationError:
            msg = _('User could not be saved')
            raise forms.ValidationError(msg)
        if commit:
            user.save()
        return user