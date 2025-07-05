from django import forms
from applications.core.models import TipoSangre

class TipoSangreForm(forms.ModelForm):
    class Meta:
        model = TipoSangre
        fields = ['tipo', 'descripcion']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'tipo': 'Tipo de Sangre',
            'descripcion': 'Descripción',
        }
