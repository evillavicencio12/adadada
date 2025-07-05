from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from applications.doctor.models import ServiciosAdicionales
from applications.doctor.forms import ServiciosAdicionalesForm # Asegúrate que este form exista
from proy_clinico.util import save_audit # Asumiendo utilidad de auditoría

class ServiciosAdicionalesListView(PermissionMixin, ListViewMixin, ListView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/list.html' # Ajusta la ruta de la plantilla
    context_object_name = 'servicios'
    permission_required = 'doctor.view_serviciosadicionales' # Ajusta el permiso
    model_name_title = "Servicio Adicional"

    def get_queryset(self):
        self.query = Q() # Inicializa Q object
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(nombre_servicio__icontains=q1) | Q(descripcion__icontains=q1), Q.OR)

        # Filtrar por estado activo si es necesario, o añadir más filtros
        # self.query.add(Q(activo=True), Q.AND)
        return self.model.objects.filter(self.query).order_by('nombre_servicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:servicio_adicional_create') # Ajusta el nombre de la URL
        return context

class ServiciosAdicionalesCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ServiciosAdicionales
    form_class = ServiciosAdicionalesForm
    template_name = 'doctor/servicios_adicionales/form.html' # Ajusta la ruta
    success_url = reverse_lazy('doctor:servicio_adicional_list') # Ajusta el nombre de la URL
    permission_required = 'doctor.add_serviciosadicionales' # Ajusta el permiso
    model_name_title = "Servicio Adicional"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ADICION")
        messages.success(self.request, f"Éxito al crear el {self.model_name_title.lower()} '{self.object.nombre_servicio}'.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, f"Error al crear el {self.model_name_title.lower()}. Revise los campos.")
        return super().form_invalid(form)

class ServiciosAdicionalesUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = ServiciosAdicionales
    form_class = ServiciosAdicionalesForm
    template_name = 'doctor/servicios_adicionales/form.html' # Ajusta la ruta
    success_url = reverse_lazy('doctor:servicio_adicional_list') # Ajusta el nombre de la URL
    permission_required = 'doctor.change_serviciosadicionales' # Ajusta el permiso
    model_name_title = "Servicio Adicional"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "MODIFICACION")
        messages.success(self.request, f"Éxito al actualizar el {self.model_name_title.lower()} '{self.object.nombre_servicio}'.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, f"Error al actualizar el {self.model_name_title.lower()}. Revise los campos.")
        return super().form_invalid(form)

class ServiciosAdicionalesDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = ServiciosAdicionales
    template_name = 'core/delete_confirm.html' # Plantilla global de confirmación
    success_url = reverse_lazy('doctor:servicio_adicional_list') # Ajusta el nombre de la URL
    permission_required = 'doctor.delete_serviciosadicionales' # Ajusta el permiso
    model_name_title = "Servicio Adicional"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = f"¿Está seguro de eliminar el {self.model_name_title.lower()}: {self.object.nombre_servicio}?"
        return context

    def form_valid(self, form):
        object_repr = str(self.object.nombre_servicio)
        # Lógica de eliminación (soft delete si 'activo' existe y se usa para eso)
        # Si es soft delete:
        # self.object.activo = False
        # self.object.save()
        # save_audit(self.request, self.object, "ELIMINACION_LOGICA")
        # messages.success(self.request, f"Éxito al eliminar lógicamente el {self.model_name_title.lower()} '{object_repr}'.")
        # return HttpResponseRedirect(self.success_url)
        # Si es hard delete (como lo hace DeleteView por defecto):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ELIMINACION_FISICA")
        messages.success(self.request, f"Éxito al eliminar físicamente el {self.model_name_title.lower()} '{object_repr}'.")
        return response
