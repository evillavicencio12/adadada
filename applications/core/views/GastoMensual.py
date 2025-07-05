from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import GastoMensual
from applications.core.forms import GastoMensualForm
from applications.security.components.mixin_crud import MixinCRUD

class GastoMensualListView(LoginRequiredMixin, PermissionRequiredMixin, MixinCRUD, ListView):
    model = GastoMensual
    template_name = "core/gastomensual/gastomensual_list.html"
    context_object_name = "gastos_mensuales"
    permission_required = "core.view_gastomensual"
    login_url = reverse_lazy('security:login')

    def get_queryset(self):
        return GastoMensual.objects.all().order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Gastos Mensuales"
        context['entity_name'] = "Gasto Mensual"
        context['create_url'] = reverse_lazy('core:gastomensual_create')
        
        # Calcular la suma de los gastos en la página actual
        gastos_en_pagina = context.get(self.context_object_name) # self.context_object_name es 'gastos_mensuales'
        if gastos_en_pagina:
            context['total_gastos_pagina'] = sum(gasto.valor for gasto in gastos_en_pagina if gasto.valor is not None)
        else:
            context['total_gastos_pagina'] = 0
            
        return context

class GastoMensualCreateView(LoginRequiredMixin, PermissionRequiredMixin, MixinCRUD, CreateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = "core/gastomensual/gastomensual_form.html"
    success_url = reverse_lazy('core:gastomensual_list')
    permission_required = "core.add_gastomensual"
    login_url = reverse_lazy('security:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Nuevo Gasto Mensual"
        context['entity_name'] = "Gasto Mensual"
        context['list_url'] = self.success_url
        return context

    def form_valid(self, form):
        # Lógica adicional si es necesaria antes de guardar
        return super().form_valid(form)

class GastoMensualUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MixinCRUD, UpdateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = "core/gastomensual/gastomensual_form.html"
    success_url = reverse_lazy('core:gastomensual_list')
    permission_required = "core.change_gastomensual"
    login_url = reverse_lazy('security:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Gasto Mensual"
        context['entity_name'] = "Gasto Mensual"
        context['list_url'] = self.success_url
        return context

    def form_valid(self, form):
        # Lógica adicional si es necesaria antes de guardar
        return super().form_valid(form)

class GastoMensualDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MixinCRUD, DeleteView):
    model = GastoMensual
    template_name = "core/delete_confirm.html" # Usar una plantilla genérica para confirmación de borrado
    success_url = reverse_lazy('core:gastomensual_list')
    permission_required = "core.delete_gastomensual"
    login_url = reverse_lazy('security:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar Gasto Mensual"
        context['entity_name'] = "Gasto Mensual"
        context['list_url'] = self.success_url
        return context
