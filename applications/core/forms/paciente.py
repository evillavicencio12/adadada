from django import forms
from applications.core.models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model=Paciente
        fields='__all__'