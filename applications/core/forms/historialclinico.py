from django import forms
from applications.core.models import HistorialClinico

class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = ['paciente', 'antecedentes', 'alergias', 'enfermedades_cronicas']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'antecedentes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'enfermedades_cronicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


