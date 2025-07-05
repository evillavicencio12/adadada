from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)
from applications.core.models import Cargo
from applications.core.forms.cargo_form import CargoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class CargoListView(LoginRequiredMixin, PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/cargo/list.html'
    model = Cargo
    context_object_name = 'cargos'
    permission_required = 'core.view_cargo' # Asegúrate de que este permiso exista o créalo

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        queryset = self.model.objects.all().order_by('id')
        if q1:
            queryset = queryset.filter(nombre__icontains=q1)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:cargo_create')
        context['title'] = 'Cargos'
        return context


class CargoCreateView(LoginRequiredMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Cargo
    template_name = 'core/cargo/form.html'
    form_class = CargoForm
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'core.add_cargo' # Asegúrate de que este permiso exista o créalo

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Cargo'
        context['back_url'] = self.success_url
        context['title'] = 'Nuevo Cargo'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        instance = self.object
        messages.success(self.request, f"Éxito al crear el cargo {instance.nombre}.")
        return response


class CargoUpdateView(LoginRequiredMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Cargo
    template_name = 'core/cargo/form.html'
    form_class = CargoForm
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'core.change_cargo' # Asegúrate de que este permiso exista o créalo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Cargo'
        context['back_url'] = self.success_url
        context['title'] = 'Actualizar Cargo'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        instance = self.object
        messages.success(self.request, f"Éxito al actualizar el cargo {instance.nombre}.")
        return response


class CargoDeleteView(LoginRequiredMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Cargo
    template_name = 'core/delete_confirm.html' # Usar una plantilla de confirmación genérica o crear una específica
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'core.delete_cargo' # Asegúrate de que este permiso exista o créalo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Cargo'
        context['description'] = f"¿Desea eliminar el cargo: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        instance_nombre = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el cargo {instance_nombre}.")
        return response
