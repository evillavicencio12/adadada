from django import forms
from applications.doctor.models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'primer_nombre',
            'apellido',
            'dni',
            'birth_date',
            'gender',
            'phone',
            'email',
            'address',
            'blood_type',
        ]
        widgets = {
            'primer_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'primer_nombre': 'Nombres',
            'apellido': 'Apellidos',
            'dni': 'Cédula',
            'birth_date': 'Fecha de Nacimiento',
            'gender': 'Género',
            'phone': 'Teléfono',
            'email': 'Correo Electrónico',
            'address': 'Dirección',
            'blood_type': 'Tipo de Sangre',
        }

    def clean_primer_nombre(self):
        primer_nombre = self.cleaned_data.get('primer_nombre')
        if not primer_nombre:
            raise forms.ValidationError("Este campo es obligatorio.")
        return primer_nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if not apellido:
            raise forms.ValidationError("Este campo es obligatorio.")
        return apellido

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni:
            raise forms.ValidationError("Este campo es obligatorio.")
        # Add any DNI validation logic if necessary
        return dni

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if not birth_date:
            raise forms.ValidationError("Este campo es obligatorio.")
        # Add any birth_date validation logic if necessary
        return birth_date

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Este campo es obligatorio.")
        return gender
