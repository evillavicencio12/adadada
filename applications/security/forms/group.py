from django import forms
from django.contrib.auth.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labels = {
            'name': 'Nombre del grupo',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingrese nombre del grupo',
                'class': 'form-input',  # o tus clases CSS personalizadas
            }),
        }
        error_messages = {
            'name': {
                'unique': 'Ya existe un grupo con este nombre.',
                'required': 'El nombre del grupo es obligatorio.',
            }
        }
