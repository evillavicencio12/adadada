from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages

from applications.core import models
from applications.doctor.models import DetallePago
from applications.doctor.forms.detalle_pago import DetallePagoForm

class DetallePagoCreateView(CreateView):
    model = DetallePago
    form_class = DetallePagoForm
    template_name = 'clinica/detalle_pago/form.html'
    success_url = reverse_lazy('doctor:detalle_pago_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Nuevo Detalle de Pago'
        context['breadcrumb'] = [
            {'name': 'Inicio', 'url': '/'},
            {'name': 'Pagos', 'url': '#'},
            {'name': 'Detalles de Pago', 'url': reverse_lazy('doctor:detalle_pago_list')},
            {'name': 'Nuevo Detalle', 'active': True}
        ]
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Detalle de pago creado exitosamente.')
        return super().form_valid(form)

class DetallePagoListView(ListView):
    model = DetallePago
    template_name = 'clinica/detalle_pago/list.html'
    context_object_name = 'detalles_pago'  # Cambiado para coincidir con el template
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(pago__id__icontains=search_query) |
                Q(servicio_adicional__nombre__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Detalles de Pago'
        context['search_query'] = self.request.GET.get('q', '')
        context['breadcrumb'] = [
            {'name': 'Inicio', 'url': '/'},
            {'name': 'Pagos', 'url': '#'},
            {'name': 'Detalles de Pago', 'active': True}
        ]
        return context

class DetallePagoDeleteView(DeleteView):
    model = DetallePago
    template_name = 'clinica/detalle_pago/list.html'
    success_url = reverse_lazy('doctor:detalle_pago_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Detalle de Pago'
        context['breadcrumb'] = [
            {'name': 'Inicio', 'url': '/'},
            {'name': 'Pagos', 'url': '#'},
            {'name': 'Detalles de Pago', 'url': reverse_lazy('doctor:detalle_pago_list')},
            {'name': 'Eliminar', 'active': True}
        ]
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Detalle de pago eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)