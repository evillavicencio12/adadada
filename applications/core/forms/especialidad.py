from django import forms
from applications.core.models import Especialidad

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = [
            'nombre',
            'descripcion',
            'activo',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la especialidad'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción detallada (opcional)'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # Tailwind puede requerir clases adicionales para estilizarlo bien
        }
        help_texts = {
            'nombre': 'Ejemplo: Cardiología, Pediatría, Ginecología.',
            'descripcion': 'Breve explicación o enfoque de la especialidad (opcional).',
            'activo': 'Desmarcar para ocultar esta especialidad en el sistema (no se podrá asignar a nuevos doctores).',
        }
        labels = {
            'nombre': 'Nombre de la Especialidad',
            'descripcion': 'Descripción',
            'activo': 'Especialidad Activa',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí podrías añadir lógica adicional si fuera necesario,
        # como validaciones personalizadas que dependan de varios campos, etc.
        # Ejemplo: self.fields['nombre'].widget.attrs.update({'class': 'mi-clase-tailwind adicional'})
        pass
