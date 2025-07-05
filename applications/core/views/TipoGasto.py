from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import TipoGasto
from applications.core.forms import TipoGastoForm
from applications.security.components.mixin_crud import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin, PermissionMixin

class TipoGastoListView(LoginRequiredMixin, PermissionRequiredMixin, ListViewMixin, ListView):
    model = TipoGasto
    template_name = "core/tipogasto/tipogasto_list.html"
    context_object_name = "tipos_gasto"
    permission_required = "core.view_tipogasto"
    login_url = reverse_lazy('security:login')

    def get_queryset(self):
        return TipoGasto.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Tipos de Gasto"
        context['entity_name'] = "Tipo de Gasto"
        context['create_url'] = reverse_lazy('core:tipogasto_create')
        return context

class TipoGastoCreateView(LoginRequiredMixin, PermissionRequiredMixin, ListViewMixin, CreateView):
    model = TipoGasto
    form_class = TipoGastoForm
    template_name = "core/tipogasto/tipogasto_form.html"
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = "core.add_tipogasto"
    login_url = reverse_lazy('security:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Nuevo Tipo de Gasto"
        context['entity_name'] = "Tipo de Gasto"
        context['list_url'] = self.success_url
        return context

    def form_valid(self, form):
        # Lógica adicional si es necesaria antes de guardar
        return super().form_valid(form)

class TipoGastoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, ListViewMixin, UpdateView):
    model = TipoGasto
    form_class = TipoGastoForm
    template_name = "core/tipogasto/tipogasto_form.html"
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = "core.change_tipogasto"
    login_url = reverse_lazy('security:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Tipo de Gasto"
        context['entity_name'] = "Tipo de Gasto"
        context['list_url'] = self.success_url
        return context

    def form_valid(self, form):
        # Lógica adicional si es necesaria antes de guardar
        return super().form_valid(form)

class TipoGastoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ListViewMixin, DeleteView):
    model = TipoGasto
    template_name = "core/delete_confirm.html" # Usar una plantilla genérica para confirmación de borrado
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = "core.delete_tipogasto"
    login_url = reverse_lazy('security:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar Tipo de Gasto"
        context['entity_name'] = "Tipo de Gasto"
        context['list_url'] = self.success_url
        return context
