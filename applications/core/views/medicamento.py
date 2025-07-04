from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect


from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from applications.core.models import Medicamento, MarcaMedicamento, TipoMedicamento
from applications.core.forms import MedicamentoForm, MarcaMedicamentoForm, TipoMedicamentoForm
from proy_clinico.util import save_audit

# --- Vistas para Medicamento ---
class MedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = Medicamento
    template_name = 'core/medicamento/list.html'
    context_object_name = 'medicamentos'
    permission_required = 'core.view_medicamento'
    model_name_title = "Medicamento"

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(
                Q(nombre__icontains=q1) |
                Q(descripcion__icontains=q1) |
                Q(tipo__nombre__icontains=q1) |
                Q(marca_medicamento__nombre__icontains=q1), Q.OR
            )
        # self.query.add(Q(activo=True), Q.AND) # Opcional: filtrar por activos
        return self.model.objects.filter(self.query).select_related('tipo', 'marca_medicamento').order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:medicamento_create')
        return context

class MedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'core.add_medicamento'
    model_name_title = "Medicamento"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ADICION")
        messages.success(self.request, f"Éxito al crear el {self.model_name_title.lower()} '{self.object.nombre}'.")
        return response

class MedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'core.change_medicamento'
    model_name_title = "Medicamento"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "MODIFICACION")
        messages.success(self.request, f"Éxito al actualizar el {self.model_name_title.lower()} '{self.object.nombre}'.")
        return response

class MedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Medicamento
    template_name = 'core/delete_confirm.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'core.delete_medicamento'
    model_name_title = "Medicamento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = f"¿Está seguro de eliminar el {self.model_name_title.lower()}: {self.object.nombre}?"
        return context

    def form_valid(self, form):
        object_repr = str(self.object.nombre)
        # Soft delete si aplica (ej. self.object.activo = False; self.object.save())
        # O hard delete (default)
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ELIMINACION_FISICA") # o ELIMINACION_LOGICA
        messages.success(self.request, f"Éxito al eliminar el {self.model_name_title.lower()} '{object_repr}'.")
        return response

# --- Vistas para MarcaMedicamento ---
class MarcaMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/list.html' # Ajusta la ruta
    context_object_name = 'marcas'
    permission_required = 'core.view_marcamedicamento'
    model_name_title = "Marca de Medicamento"

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:marcamedicamento_create') # Ajusta el nombre de la URL
        return context

class MarcaMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'core/marca_medicamento/form.html' # Ajusta la ruta
    success_url = reverse_lazy('core:marcamedicamento_list')
    permission_required = 'core.add_marcamedicamento'
    model_name_title = "Marca de Medicamento"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ADICION")
        messages.success(self.request, f"Éxito al crear la {self.model_name_title.lower()} '{self.object.nombre}'.")
        return response

class MarcaMedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'core/marca_medicamento/form.html' # Ajusta la ruta
    success_url = reverse_lazy('core:marcamedicamento_list')
    permission_required = 'core.change_marcamedicamento'
    model_name_title = "Marca de Medicamento"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "MODIFICACION")
        messages.success(self.request, f"Éxito al actualizar la {self.model_name_title.lower()} '{self.object.nombre}'.")
        return response

class MarcaMedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = MarcaMedicamento
    template_name = 'core/delete_confirm.html'
    success_url = reverse_lazy('core:marcamedicamento_list')
    permission_required = 'core.delete_marcamedicamento'
    model_name_title = "Marca de Medicamento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = f"¿Está seguro de eliminar la {self.model_name_title.lower()}: {self.object.nombre}?"
        return context

    def form_valid(self, form):
        # Protección contra borrado si hay medicamentos asociados
        if Medicamento.objects.filter(marca_medicamento=self.object).exists():
            messages.error(self.request, f"No se puede eliminar la marca '{self.object.nombre}' porque está asociada a uno o más medicamentos.")
            return HttpResponseRedirect(self.success_url) # O a donde prefieras

        object_repr = str(self.object.nombre)
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ELIMINACION_FISICA")
        messages.success(self.request, f"Éxito al eliminar la {self.model_name_title.lower()} '{object_repr}'.")
        return response


# --- Vistas para TipoMedicamento ---
class TipoMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = TipoMedicamento
    template_name = 'core/tipo_medicamento/list.html' # Ajusta la ruta
    context_object_name = 'tipos'
    permission_required = 'core.view_tipomedicamento'
    model_name_title = "Tipo de Medicamento"

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipomedicamento_create') # Ajusta el nombre de la URL
        return context

class TipoMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'core/tipo_medicamento/form.html' # Ajusta la ruta
    success_url = reverse_lazy('core:tipomedicamento_list')
    permission_required = 'core.add_tipomedicamento'
    model_name_title = "Tipo de Medicamento"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ADICION")
        messages.success(self.request, f"Éxito al crear el {self.model_name_title.lower()} '{self.object.nombre}'.")
        return response

class TipoMedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'core/tipo_medicamento/form.html' # Ajusta la ruta
    success_url = reverse_lazy('core:tipomedicamento_list')
    permission_required = 'core.change_tipomedicamento'
    model_name_title = "Tipo de Medicamento"

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, "MODIFICACION")
        messages.success(self.request, f"Éxito al actualizar el {self.model_name_title.lower()} '{self.object.nombre}'.")
        return response

class TipoMedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoMedicamento
    template_name = 'core/delete_confirm.html'
    success_url = reverse_lazy('core:tipomedicamento_list')
    permission_required = 'core.delete_tipomedicamento'
    model_name_title = "Tipo de Medicamento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = f"¿Está seguro de eliminar el {self.model_name_title.lower()}: {self.object.nombre}?"
        return context

    def form_valid(self, form):
        # Protección contra borrado si hay medicamentos asociados
        if Medicamento.objects.filter(tipo=self.object).exists():
            messages.error(self.request, f"No se puede eliminar el tipo '{self.object.nombre}' porque está asociado a uno o más medicamentos.")
            return HttpResponseRedirect(self.success_url)

        object_repr = str(self.object.nombre)
        response = super().form_valid(form)
        save_audit(self.request, self.object, "ELIMINACION_FISICA")
        messages.success(self.request, f"Éxito al eliminar el {self.model_name_title.lower()} '{object_repr}'.")
        return response
