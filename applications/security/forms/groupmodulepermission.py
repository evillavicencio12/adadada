from django import forms
from django.contrib.auth.models import Group, Permission
from applications.security.models import GroupModulePermission, Module

class GroupModulePermissionForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Grupo',
        widget=forms.Select(attrs={'class': 'rounded border-gray-300 text-indigo-600 shadow-sm focus:ring-indigo-500 w-full'})
    )
    module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        label='Módulo',
        widget=forms.Select(attrs={'class': 'rounded border-gray-300 text-indigo-600 shadow-sm focus:ring-indigo-500 w-full'})
    )
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),  # Inicialmente vacío, se llena en __init__
        label='Permisos',
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'space-y-1'})
    )

    class Meta:
        model = GroupModulePermission
        fields = ['group', 'module', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si hay módulo seleccionado, filtramos permisos de ese módulo
        module = None
        if 'module' in self.data:
            try:
                module_id = int(self.data.get('module'))
                module = Module.objects.get(pk=module_id)
            except (ValueError, Module.DoesNotExist):
                pass
        elif self.instance and self.instance.pk:
            module = self.instance.module

        if module:
            self.fields['permissions'].queryset = module.permissions.all()
        else:
            self.fields['permissions'].queryset = Permission.objects.none()
