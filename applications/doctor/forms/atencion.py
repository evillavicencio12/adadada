from django import forms
from applications.doctor.models import Atencion, DetalleAtencion
from applications.core.models import Paciente, Diagnostico, Medicamento
from django.forms import inlineformset_factory

class AtencionForm(forms.ModelForm):
    paciente_nombre = forms.CharField(
        label='Paciente',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'paciente_nombre', 'readonly': 'readonly'})
    )
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.filter(activo=True), # Filtrar por pacientes activos
        widget=forms.HiddenInput(),
        required=False # Se popula desde la búsqueda o selección
    )
    diagnostico = forms.ModelMultipleChoiceField(
        queryset=Diagnostico.objects.filter(activo=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'multiple': 'multiple'}),
        required=False,
        label="Diagnósticos"
    )

    class Meta:
        model = Atencion
        fields = [
            'paciente', 'paciente_nombre', # paciente_nombre para mostrar, paciente (oculto) para el ID
            'presion_arterial', 'pulso', 'temperatura', 'frecuencia_respiratoria',
            'saturacion_oxigeno', 'peso', 'altura',
            'motivo_consulta', 'sintomas', 'tratamiento', 'diagnostico',
            'examen_fisico', 'examenes_enviados', 'comentario_adicional', 'es_control'
        ]
        widgets = {
            'presion_arterial': forms.TextInput(attrs={'class': 'form-control'}),
            'pulso': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control'}),
            'saturacion_oxigeno': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'examen_fisico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'examenes_enviados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comentario_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'es_control': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.paciente:
            self.fields['paciente_nombre'].initial = self.instance.paciente.nombre_completo
            self.fields['paciente'].initial = self.instance.paciente.pk

        # Personalizar etiquetas
        self.fields['es_control'].label = "¿Es consulta de control?"
        self.fields['saturacion_oxigeno'].label = "Sat. O₂ (%)"
        self.fields['frecuencia_respiratoria'].label = "Frec. Resp. (rpm)"
        self.fields['pulso'].label = "Pulso (ppm)"
        self.fields['temperatura'].label = "Temp. (°C)"
        self.fields['diagnostico'].widget.attrs.update({'data-placeholder': 'Seleccione diagnósticos'})


class DetalleAtencionForm(forms.ModelForm):
    # Campo para buscar y mostrar el nombre del medicamento, no directamente ligado al modelo
    medicamento_nombre = forms.CharField(
        label='Medicamento',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control medicamento-autocomplete', # Clase para el JS de autocompletar
            'placeholder': 'Buscar o agregar medicamento...'
        })
    )
    # Campo oculto para el ID del medicamento, este sí se guarda en el modelo
    medicamento = forms.ModelChoiceField(
        queryset=Medicamento.objects.filter(activo=True),
        widget=forms.HiddenInput(),
        required=False # Puede ser nuevo o no existir inicialmente
    )

    class Meta:
        model = DetalleAtencion
        fields = ['medicamento_nombre', 'medicamento', 'cantidad', 'prescripcion', 'duracion_tratamiento', 'frecuencia_diaria']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'prescripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'duracion_tratamiento': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'frecuencia_diaria': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay una instancia (editando), popular el campo medicamento_nombre
        if self.instance and self.instance.pk and self.instance.medicamento:
            self.fields['medicamento_nombre'].initial = self.instance.medicamento.nombre
            self.fields['medicamento'].initial = self.instance.medicamento.pk # Asegurar que el ID oculto también se popule

# Formset para manejar múltiples Detalles de Atención dentro del formulario de Atención
DetalleAtencionFormSet = inlineformset_factory(
    Atencion,
    DetalleAtencion,
    form=DetalleAtencionForm,
    extra=1, # Número de formularios extra vacíos
    can_delete=True, # Permitir eliminar detalles existentes
    can_delete_extra=True, # Permitir eliminar formularios extra que se hayan añadido y luego no se quieran
    fields=['medicamento_nombre', 'medicamento', 'cantidad', 'prescripcion', 'duracion_tratamiento', 'frecuencia_diaria'],
)


class AtencionFilterForm(forms.Form):
    paciente = forms.CharField(
        required=False,
        label="Paciente",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o cédula'})
    )
    fecha_desde = forms.DateField(
        required=False,
        label="Fecha Desde",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    fecha_hasta = forms.DateField(
        required=False,
        label="Fecha Hasta",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    diagnostico = forms.ModelChoiceField(
        queryset=Diagnostico.objects.filter(activo=True),
        required=False,
        label="Diagnóstico",
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
