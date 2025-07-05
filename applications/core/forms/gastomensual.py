from django import forms
from applications.core.models import GastoMensual

class GastoMensualForm(forms.ModelForm):
    class Meta:
        model = GastoMensual
        fields = ['tipo_gasto', 'fecha', 'valor', 'observacion']
        widgets = {
            'tipo_gasto': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
