from django import forms

from apps.website.models import Clientes


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields:
            if campo != 'foto':
                self.fields[campo].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Clientes
        fields = ['first_name', 'last_name', ]