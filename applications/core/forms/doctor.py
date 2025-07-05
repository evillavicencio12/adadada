from django import forms
from applications.core.models import Doctor, Especialidad

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'nombres',
            'apellidos',
            'ruc',
            'fecha_nacimiento',
            'direccion',
            'latitud',
            'longitud',
            'codigo_unico_doctor',
            'especialidad',
            'telefonos',
            'email',
            'horario_atencion',
            'duracion_atencion',
            'curriculum',
            'firma_digital',
            'foto',
            'imagen_receta',
            'activo',
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_unico_doctor': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.SelectMultiple(attrs={'class': 'form-control select2', 'multiple': 'multiple'}),
            'telefonos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'horario_atencion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duracion_atencion': forms.NumberInput(attrs={'class': 'form-control'}),
            'curriculum': forms.FileInput(attrs={'class': 'form-control-file'}),
            'firma_digital': forms.FileInput(attrs={'class': 'form-control-file'}),
            'foto': forms.FileInput(attrs={'class': 'form-control-file'}),
            'imagen_receta': forms.FileInput(attrs={'class': 'form-control-file'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'ruc': 'Ingrese un RUC válido (persona natural, sociedad o extranjero).',
            'especialidad': 'Seleccione una o más especialidades médicas.',
            'horario_atencion': 'Ejemplo: Lunes a Viernes, 08h00 - 13h00',
        }
        labels = {
            'ruc': 'RUC',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'codigo_unico_doctor': 'Código Único del Doctor',
            'duracion_atencion': 'Duración de Cita (minutos)',
            'curriculum': 'Currículum Vitae',
            'firma_digital': 'Firma Digital',
            'imagen_receta': 'Imagen para Recetas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especialidad'].queryset = Especialidad.objects.filter(activo=True).order_by('nombre')
        # Asegurar que los campos opcionales no se marquen como requeridos si el modelo lo permite
        # ModelForm ya hace esto basado en `blank` del modelo, pero se puede forzar si es necesario.
        # Ejemplo: self.fields['email'].required = False
        pass
