from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from applications.core.models import Diagnostico
from applications.core.forms import DiagnosticoForm # Asumiendo que este form exista
from proy_clinico.util import save_audit # Asumiendo utilidad de auditoría

class DiagnosticoListView(PermissionMixin, ListViewMixin, ListView):
    model = Diagnostico
    template_name = 'core/diagnostico/list.html'
    context_object_name = 'diagnosticos'
    permission_required = 'core.view_diagnostico' # Ajusta el permiso
    model_name_title = "Diagnóstico"

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(codigo__icontains=q1) | Q(descripcion__icontains=q1), Q.OR)

        # self.query.add(Q(activo=True), Q.AND) # Si solo quieres mostrar activos por defecto
        return self.model.objects.filter(self.query).order_by('codigo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:diagnostico_create')
        return context

class DiagnosticoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'core/diagnostico/form.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'core.add_diagnostico'
    model_name_title = "Diagnóstico"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ADICION")
        messages.success(self.request, f"Éxito al crear el {self.model_name_title.lower()} '{self.object.codigo} - {self.object.descripcion}'.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, f"Error al crear el {self.model_name_title.lower()}. Revise los campos.")
        return super().form_invalid(form)

class DiagnosticoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'core/diagnostico/form.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'core.change_diagnostico'
    model_name_title = "Diagnóstico"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "MODIFICACION")
        messages.success(self.request, f"Éxito al actualizar el {self.model_name_title.lower()} '{self.object.codigo} - {self.object.descripcion}'.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, f"Error al actualizar el {self.model_name_title.lower()}. Revise los campos.")
        return super().form_invalid(form)

class DiagnosticoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    template_name = 'core/delete_confirm.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'core.delete_diagnostico'
    model_name_title = "Diagnóstico"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = f"¿Está seguro de eliminar el {self.model_name_title.lower()}: {self.object.codigo} - {self.object.descripcion}?"
        return context

    def form_valid(self, form):
        object_repr = f"{self.object.codigo} - {self.object.descripcion}"
        # Si es soft delete (ej. campo 'activo'):
        # self.object.activo = False
        # self.object.save()
        # save_audit(self.request, self.object, "ELIMINACION_LOGICA")
        # messages.success(self.request, f"Éxito al eliminar lógicamente el {self.model_name_title.lower()} '{object_repr}'.")
        # return HttpResponseRedirect(self.success_url)

        response = super().form_valid(form) # Hard delete
        save_audit(self.request, self.object, "ELIMINACION_FISICA")
        messages.success(self.request, f"Éxito al eliminar el {self.model_name_title.lower()} '{object_repr}'.")
        return response
