from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)
from applications.core.models import TipoSangre
from applications.core.forms.tiposangre_form import TipoSangreForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class TipoSangreListView(LoginRequiredMixin, PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tiposangre/list.html'
    model = TipoSangre
    context_object_name = 'tipos_sangre'
    permission_required = 'core.view_tiposangre' # Asegúrate de que este permiso exista o créalo

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        queryset = self.model.objects.all().order_by('id')
        if q1:
            queryset = queryset.filter(tipo__icontains=q1)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tiposangre_create')
        context['title'] = 'Tipos de Sangre'
        return context


class TipoSangreCreateView(LoginRequiredMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = TipoSangre
    template_name = 'core/tiposangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tiposangre_list')
    permission_required = 'core.add_tiposangre' # Asegúrate de que este permiso exista o créalo

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo de Sangre'
        context['back_url'] = self.success_url
        context['title'] = 'Nuevo Tipo de Sangre'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        instance = self.object
        messages.success(self.request, f"Éxito al crear el tipo de sangre {instance.tipo}.")
        return response


class TipoSangreUpdateView(LoginRequiredMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoSangre
    template_name = 'core/tiposangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tiposangre_list')
    permission_required = 'core.change_tiposangre' # Asegúrate de que este permiso exista o créalo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Tipo de Sangre'
        context['back_url'] = self.success_url
        context['title'] = 'Actualizar Tipo de Sangre'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        instance = self.object
        messages.success(self.request, f"Éxito al actualizar el tipo de sangre {instance.tipo}.")
        return response


class TipoSangreDeleteView(LoginRequiredMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoSangre
    template_name = 'core/delete_confirm.html' # Usar una plantilla de confirmación genérica o crear una específica
    success_url = reverse_lazy('core:tiposangre_list')
    permission_required = 'core.delete_tiposangre' # Asegúrate de que este permiso exista o créalo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tipo de Sangre'
        context['description'] = f"¿Desea eliminar el tipo de sangre: {self.object.tipo}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        instance_tipo = self.object.tipo
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el tipo de sangre {instance_tipo}.")
        return response
