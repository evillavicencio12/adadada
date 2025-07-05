from django import forms
from applications.doctor.models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
        widgets = {
            'atencion': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_pago': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'nombre_pagador': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia_externa': forms.TextInput(attrs={'class': 'form-control'}),
            'evidencia_pago': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
