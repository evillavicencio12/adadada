from django import forms
from applications.doctor.models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        # Se excluye monto_total porque se calcula automáticamente desde los DetallePago.
        # También se excluyen campos de auditoría que Django maneja o se asignan en la vista.
        exclude = ['monto_total', 'user_creation', 'user_updated', 'date_creation', 'date_updated']
        widgets = {
            'atencion': forms.Select(attrs={'class': 'form-control select2bs4'}), # Añadida clase para Select2 si se usa
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_pago': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'nombre_pagador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de quien realiza el pago'}),
            'referencia_externa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ID de transacción PayPal, Zelle, etc.'}),
            'evidencia_pago': forms.ClearableFileInput(attrs={'class': 'form-control-file'}), # form-control-file para Bootstrap
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_pagador': 'Nombre del Pagador (Opcional)',
            'referencia_externa': 'Referencia Externa (Opcional)',
            'evidencia_pago': 'Evidencia de Pago (Opcional)',
            'activo': 'Pago Activo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Hacer que la atención no sea obligatoria si un pago puede existir sin atención
        # self.fields['atencion'].required = False

        # Si se usa Select2 para el campo atencion, se puede inicializar aquí o en el template
        # Ejemplo si el campo Atencion es muy grande:
        # if 'atencion' in self.fields:
        #     self.fields['atencion'].queryset = Atencion.objects.select_related('paciente').order_by('-fecha_atencion_real')[:200] # Limitar queryset

        # Asegurar que fecha_pago no sea obligatorio si el estado no es PAGADO
        # Esto se maneja mejor en la lógica del modelo o la vista, pero se puede reforzar aquí.
        if self.instance and self.instance.pk and self.instance.estado != 'PAGADO':
             self.fields['fecha_pago'].required = False
