import re
from django import forms
from django.forms import ModelForm

from applications.security.models import User
from django.contrib.auth.models import Group
from django.forms import ModelMultipleChoiceField

class UserForm(ModelForm):
    groups = ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
        }),
        label="Grupos",
    )
    
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "dni",
            "image",
            "email",
            "direction",
            "phone",
            "groups",
        ]
        error_messages = {
            "username": {
                "unique": "Ya existe un usuario con este nombre de usuario.",
                "required": "El nombre de usuario es obligatorio.",
            },
            "email": {
                "unique": "Ya existe un usuario con este email.",
                "required": "El email es obligatorio.",
            },
        }
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Ingrese nombre de usuario",
                "id": "id_username",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }),
            "first_name": forms.TextInput(attrs={
                "placeholder": "Ingrese nombre",
                "id": "id_first_name",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Ingrese apellido",
                "id": "id_last_name",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5",
            }),
            "dni": forms.TextInput(attrs={
                "placeholder": "Ingrese DNI del usuario",
                "id": "id_dni",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Ingrese email del usuario",
                "id": "id_email",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5",
            }),
            "direction": forms.TextInput(attrs={
                "placeholder": "Ingrese dirección del usuario",
                "id": "id_direction",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Ingrese teléfono del usuario",
                "id": "id_phone",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5",
            }),
        }
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "dni": "DNI",
            "email": "Email",
            "direction": "Dirección",
            "phone": "Teléfono",
            "groups": "Grupos"
        }

    def clean_dni(self):
        dni = self.cleaned_data.get("dni")
        if dni:
            return dni.upper()
        return dni
