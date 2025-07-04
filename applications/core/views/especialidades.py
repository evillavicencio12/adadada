from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q, ProtectedError
from django.shortcuts import redirect

from applications.core.models import Especialidad
from applications.core.forms.especialidad import EspecialidadForm
from applications.security.components.mixin_crud import PermissionMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin, ListViewMixin

class EspecialidadListView(PermissionMixin, ListViewMixin, ListView):
    model = Especialidad
    template_name = 'core/especialidad_list.html' # Django buscará en templates/core/especialidad_list.html
    context_object_name = 'especialidades'
    permission_required = 'view_especialidad'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(descripcion__icontains=q)
            )
        return queryset.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:especialidad_create')
        # context['title'] = 'Listado de Especialidades Médicas' # Dejado al mixin o plantilla
        return context

class EspecialidadCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'core/especialidad_form.html' # Django buscará en templates/core/especialidad_form.html
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'add_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        # context['title'] = 'Crear Especialidad Médica' # Dejado al mixin o plantilla
        # context['submit_button_text'] = 'Guardar Especialidad' # Si la plantilla base lo usa
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Especialidad '{self.object.nombre}' creada con éxito.")
        return response

class EspecialidadUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'core/especialidad_form.html' # Django buscará en templates/core/especialidad_form.html
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'change_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        # context['title'] = 'Actualizar Especialidad Médica' # Dejado al mixin o plantilla
        # context['submit_button_text'] = 'Actualizar Especialidad' # Si la plantilla base lo usa
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Especialidad '{self.object.nombre}' actualizada con éxito.")
        return response

class EspecialidadDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Especialidad
    template_name = 'core/delete_confirm.html' # Django buscará en templates/core/delete_confirm.html
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'delete_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Eliminar Especialidad Médica' # Dejado al mixin o plantilla

        # El related_name en Doctor.especialidad es "especialidades"
        # Por lo tanto, desde una instancia de Especialidad (self.object),
        # accedemos a los doctores relacionados con self.object.especialidades.count()
        doctores_con_especialidad_count = self.object.especialidades.count()

        if doctores_con_especialidad_count > 0:
            context['deletion_blocked'] = True
            context['description'] = (
                f"No se puede eliminar la especialidad '{self.object.nombre}' porque está asignada a "
                f"{doctores_con_especialidad_count} doctor(es). Primero debe desasignarla de los doctores o eliminarlos."
            )
        else:
            context['deletion_blocked'] = False # Asegurarse que esté presente para la plantilla
            context['description'] = f"¿Está seguro de eliminar la especialidad '{self.object.nombre}'?"
        context['back_url'] = self.success_url
        # context['confirm_button_text'] = 'Confirmar Eliminación' # Si la plantilla base lo usa
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        doctores_con_especialidad_count = self.object.especialidades.count()

        if doctores_con_especialidad_count > 0:
            messages.error(request, f"Acción bloqueada: No se puede eliminar la especialidad '{self.object.nombre}' porque está asignada a {doctores_con_especialidad_count} doctor(es).")
            return redirect(self.success_url)

        try:
            nombre_especialidad = self.object.nombre
            # super().form_valid(form) no es el método correcto aquí para DeleteView, es super().post() o super().delete()
            response = super().delete(request, *args, **kwargs) # Llama al método delete de la clase padre
            messages.success(self.request, f"Especialidad '{nombre_especialidad}' eliminada con éxito.")
            return response # response ya es la redirección a success_url
        except ProtectedError: # Aunque la lógica anterior debería prevenir esto para Doctores.
            messages.error(self.request, f"No se puede eliminar la especialidad '{self.object.nombre}' debido a otras restricciones de la base de datos.")
            return redirect(self.success_url)
