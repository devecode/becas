from django import forms
from .models import Solicitud


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['nombre', 'ap', 'am', 'domicilio', 'colonia', 'telefono', 'fn', 'ga', 'matricula',
                  'formacion_artistica', 'modalidad', 'genero', 'correo', 'entrega']
        widget = {'fn': forms.DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
