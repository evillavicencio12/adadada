from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect

from proy_clinico.util import save_audit
from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
)
from applications.core.models import Medicamento, MarcaMedicamento, TipoMedicamento
from applications.core.forms import MedicamentoForm, MarcaMedicamentoForm, TipoMedicamentoForm
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
# ---------------------- VISTAS PARA MEDICAMENTO ----------------------
class MedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = Medicamento
    template_name = 'core/medicamento/list.html'
    context_object_name = 'medicamentos'
    permission_required = 'core.view_medicamento'
    model_name_title = "Medicamento"

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query |= Q(nombre__icontains=q) | Q(descripcion__icontains=q) | Q(tipo__nombre__icontains=q) | Q(marca_medicamento__nombre__icontains=q)
        return self.model.objects.filter(query).select_related('tipo', 'marca_medicamento').order_by('nombre')

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
        context['back_url'] = self.success_url or self.request.META.get('HTTP_REFERER', '#')
        return context

    def form_valid(self, form):
        object_repr = str(self.object.nombre)
        save_audit(self.request, self.object, "ELIMINACION_FISICA")
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el {self.model_name_title.lower()} '{object_repr}'.")
        return response


# ---------------------- VISTAS PARA MARCA DE MEDICAMENTO ----------------------
class MarcaMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/list.html'
    context_object_name = 'marcas'
    permission_required = 'core.view_marcamedicamento'
    model_name_title = "Marca de Medicamento"

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query |= Q(nombre__icontains=q)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:marcamedicamento_create')
        return context


class MarcaMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'core/marca_medicamento/form.html'
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
    template_name = 'core/marca_medicamento/form.html'
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
        context['back_url'] = self.success_url or self.request.META.get('HTTP_REFERER', '#')
        return context

    def form_valid(self, form):
        if Medicamento.objects.filter(marca_medicamento=self.object).exists():
            messages.error(self.request, f"No se puede eliminar la marca '{self.object.nombre}' porque está asociada a uno o más medicamentos.")
            return HttpResponseRedirect(self.success_url)

        object_repr = str(self.object.nombre)
        save_audit(self.request, self.object, "ELIMINACION_FISICA")
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar la {self.model_name_title.lower()} '{object_repr}'.")
        return response


# ---------------------- VISTAS PARA TIPO DE MEDICAMENTO ----------------------
class TipoMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = TipoMedicamento
    template_name = 'core/tipo_medicamento/list.html'
    context_object_name = 'tipos'
    permission_required = 'core.view_tipomedicamento'
    model_name_title = "Tipo de Medicamento"

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query |= Q(nombre__icontains=q)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipomedicamento_create')
        return context


class TipoMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'core/tipo_medicamento/form.html'
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
    template_name = 'core/tipo_medicamento/form.html'
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
        context['back_url'] = self.success_url or self.request.META.get('HTTP_REFERER', '#')
        return context

    def form_valid(self, form):
        if Medicamento.objects.filter(tipo=self.object).exists():
            messages.error(self.request, f"No se puede eliminar el tipo '{self.object.nombre}' porque está asociado a uno o más medicamentos.")
            return HttpResponseRedirect(self.success_url)

        object_repr = str(self.object.nombre)
        save_audit(self.request, self.object, "ELIMINACION_FISICA")
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el {self.model_name_title.lower()} '{object_repr}'.")
        return response
#-----------------------AJAX MEDICAMENTOS------------------------
from django.core.paginator import Paginator

@require_POST
def ajax_create_medicamento(request):
    # Mapeo entre los nombres de campos en el modal y los del modelo
    field_map = {
        'nombre_medicamento_modal': 'nombre',
        'tipo_medicamento_modal': 'tipo',
        'marca_medicamento_modal': 'marca_medicamento',
        'concentracion_modal': 'concentracion',
        'via_administracion_modal': 'via_administracion',
        'cantidad_modal': 'cantidad',
        'precio_modal': 'precio',
        'descripcion_modal': 'descripcion',
        # Si tienes 'foto' y 'comercial', también deberías mapearlos
    }

    data = request.POST.copy()
    files = request.FILES or None

    # Creamos un nuevo diccionario con los nombres correctos
    translated_data = {}
    for modal_name, model_field in field_map.items():
        translated_data[model_field] = data.get(modal_name)

    # Pasamos el nuevo dict con nombres correctos al form
    form = MedicamentoForm(translated_data, request.FILES)


    if form.is_valid():
        try:
            medicamento = form.save()
            return JsonResponse({
                'status': 'success',
                'medicamento': {
                    'id': medicamento.pk,
                    'nombre': medicamento.nombre,
                }
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'errors': {
                    '__all__': [f'Error interno del servidor: {str(e)}']
                }
            }, status=500)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@require_GET
def ajax_search_medicamento(request):
    nombre = request.GET.get('nombre', '').strip()
    page_number = request.GET.get('page', 1)

    if not nombre:
        return JsonResponse({'medicamentos': [], 'total_count': 0})

    base_queryset = Medicamento.objects.filter(
        nombre__icontains=nombre,
        activo=True # Solo buscar medicamentos activos
    ).order_by('nombre')

    paginator = Paginator(base_queryset, 10) # 10 items per page
    try:
        page_obj = paginator.page(page_number)
    except Exception:
        page_obj = paginator.page(1)

    data_list = [{
        'id': m.pk,
        'text': m.nombre # Select2 espera 'text' por defecto
        # puedes añadir más datos si el template de Select2 los usa:
        # 'concentracion': m.concentracion,
        # 'tipo': m.tipo.nombre if m.tipo else ''
    } for m in page_obj.object_list]

    return JsonResponse({
        'results': data_list, # Select2 espera 'results' para la lista de items
        'pagination': { # Select2 espera 'pagination.more'
            'more': page_obj.has_next()
        },
        # Para compatibilidad con el JS anterior que esperaba 'medicamentos' y 'total_count'
        'medicamentos': data_list,
        'total_count': paginator.count
    })