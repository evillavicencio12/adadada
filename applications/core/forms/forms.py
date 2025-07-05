# aplicacion/core/forms.py
from django import forms
from  applications.core.models import TipoGasto, GastoMensual 
from django import forms

from django.core.exceptions import ValidationError
from django.utils import timezone

class TipoGastoForm(forms.ModelForm):
    class Meta:
        model = TipoGasto
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class GastoMensualForm(forms.ModelForm):
    class Meta:
        model = GastoMensual
        fields = ['tipo_gasto', 'fecha', 'valor', 'observacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'observacion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtramos solo los tipos de gasto activos
        self.fields['tipo_gasto'].queryset = TipoGasto.objects.filter(activo=True)


