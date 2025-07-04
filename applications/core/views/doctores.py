from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import Doctor
from applications.core.forms.doctor import DoctorForm
from applications.security.components.mixin_crud import PermissionMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin, ListViewMixin 

# Vistas para el DoctorForm complejo (que se usará después)
class DoctorListView(PermissionMixin, ListViewMixin, ListView):
    model = Doctor
    template_name = 'core/doctor_list.html' # Apuntará a la plantilla final estilizada
    context_object_name = 'doctores'
    permission_required = 'view_doctor'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = self.model.objects.filter(activo=True) 
        if q:
            queryset = queryset.filter(
                Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(ruc__icontains=q) | Q(codigo_unico_doctor__icontains=q) | Q(especialidad__nombre__icontains=q)
            ).distinct()
        return queryset.order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:doctor_create') 
        context['title'] = 'Listado de Doctores' 
        return context

class DoctorCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Doctor
    form_class = DoctorForm 
    template_name = 'core/doctor_form.html' # Plantilla COMPLEJA del usuario
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'add_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Doctor' 
        context['back_url'] = self.success_url
        context['submit_button_text'] = 'Guardar Doctor' # Para la plantilla compleja
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Doctor '{self.object.nombre_completo}' creado con éxito.")
        return response

class DoctorUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm 
    template_name = 'core/doctor_form.html' # Plantilla COMPLEJA del usuario
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'change_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Doctor' 
        context['back_url'] = self.success_url
        context['submit_button_text'] = 'Actualizar Doctor' # Para la plantilla compleja
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Doctor '{self.object.nombre_completo}' actualizado con éxito.")
        return response

class DoctorDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Doctor
    template_name = 'core/delete_confirm.html' # Apuntará a la plantilla final estilizada
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'delete_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Doctor (Simple)' # Ajustado
        context['description'] = f"¿Está seguro de eliminar al doctor '{self.object.nombre_completo}'?"
        context['back_url'] = self.success_url
        # context['confirm_button_text'] = 'Confirmar Eliminación' # No aplica a simple
        return context

    def form_valid(self, form):
        nombre_completo = self.object.nombre_completo
        response = super().form_valid(form)
        messages.success(self.request, f"Doctor '{nombre_completo}' eliminado con éxito.")
        return response

# Vistas "Simple" para pruebas iniciales si fueran necesarias (pueden eliminarse luego)
# O mejor, comentar las de arriba y renombrar estas temporalmente si se quiere probar con simple_doctor_form.html

# class SimpleDoctorListView(PermissionMixin, ListViewMixin, ListView):
#     model = Doctor
#     template_name = 'core/simple_doctor_list.html' 
#     context_object_name = 'doctores'
#     permission_required = 'view_doctor' 

#     def get_queryset(self):
#         q = self.request.GET.get('q', '')
#         queryset = self.model.objects.filter(activo=True) 
#         if q:
#             queryset = queryset.filter(
#                 Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(ruc__icontains=q)
#             ).distinct()
#         return queryset.order_by('apellidos', 'nombres')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['create_url'] = reverse_lazy('core:doctor_create_simple') 
#         context['title'] = 'Listado Simple de Doctores'
#         return context

# class SimpleDoctorCreateView(PermissionMixin, CreateViewMixin, CreateView):
#     model = Doctor
#     form_class = DoctorForm # Usa el mismo form
#     template_name = 'core/simple_doctor_form.html' 
#     success_url = reverse_lazy('core:doctor_list_simple')
#     permission_required = 'add_doctor'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Crear Doctor (Simple)'
#         context['back_url'] = self.success_url
#         return context
# # ... (SimpleDoctorUpdateView y SimpleDoctorDeleteView similarmente) ...
