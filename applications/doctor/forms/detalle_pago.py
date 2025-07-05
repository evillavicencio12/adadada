from django import forms
from applications.doctor.models import DetallePago, Pago, ServiciosAdicionales

class DetallePagoForm(forms.ModelForm):
    class Meta:
        model = DetallePago
        fields = [
            'pago', 'servicio_adicional', 'cantidad', 'precio_unitario',
            'descuento_porcentaje', 'aplica_seguro', 'valor_seguro', 'descripcion_seguro'
        ]
        widgets = {
            'pago': forms.Select(attrs={'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm'}),
            'servicio_adicional': forms.Select(attrs={'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm'}),
            'cantidad': forms.NumberInput(attrs={'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm', 'step': '0.01'}),
            'descuento_porcentaje': forms.NumberInput(attrs={'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm', 'step': '0.01', 'min': 0, 'max': 100}),
            'aplica_seguro': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'}),
            'valor_seguro': forms.NumberInput(attrs={'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm', 'step': '0.01'}),
            'descripcion_seguro': forms.TextInput(attrs={'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm'}),
        }
        labels = {
            'pago': 'Pago',
            'servicio_adicional': 'Servicio Adicional',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario',
            'descuento_porcentaje': 'Descuento (%)',
            'aplica_seguro': 'Aplica Seguro',
            'valor_seguro': 'Valor Cubierto por Seguro',
            'descripcion_seguro': 'Descripción del Seguro',
        }

    def clean(self):
        cleaned_data = super().clean()
        aplica_seguro = cleaned_data.get('aplica_seguro')
        valor_seguro = cleaned_data.get('valor_seguro')
        descripcion_seguro = cleaned_data.get('descripcion_seguro')

        if aplica_seguro:
            if not valor_seguro:
                self.add_error('valor_seguro', 'Debe especificar el valor cubierto por el seguro si aplica seguro.')
            if not descripcion_seguro:
                self.add_error('descripcion_seguro', 'Debe proporcionar una descripción del seguro si aplica seguro.')
        else:
            cleaned_data['valor_seguro'] = None
            cleaned_data['descripcion_seguro'] = ''
        return cleaned_data