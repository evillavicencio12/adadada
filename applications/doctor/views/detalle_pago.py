from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from applications.doctor.models import DetallePago, Pago
from applications.doctor.forms.detalle_pago import DetallePagoForm

class DetallePagoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DetallePago
    form_class = DetallePagoForm
    template_name = 'clinica/detalle_pago/form.html' # Esta plantilla parece estar bien diseñada para un form
    # success_url se definirá en get_success_url para redirigir al detalle del Pago padre
    success_message = "Detalle de pago creado exitosamente."

    def get_initial(self):
        initial = super().get_initial()
        pago_id = self.request.GET.get('pago_id')
        if pago_id:
            pago = get_object_or_404(Pago, pk=pago_id)
            initial['pago'] = pago
        return initial

    def form_valid(self, form):
        form.instance.user_creation = self.request.user
        # El subtotal se calcula en el save() del modelo DetallePago
        # y el total del Pago padre también se actualiza allí.
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Nuevo Detalle de Pago'
        # Breadcrumbs y otros datos de contexto pueden permanecer o ajustarse
        pago_id = self.request.GET.get('pago_id')
        if pago_id:
             context['pago_obj'] = get_object_or_404(Pago, pk=pago_id) # Para mostrar info del pago
        context['breadcrumb'] = [
            {'name': 'Inicio', 'url': reverse_lazy('security:home')}, # Asumiendo una URL de inicio
            {'name': 'Pagos', 'url': reverse_lazy('doctor:pago_list')},
        ]
        if pago_id:
            context['breadcrumb'].append({'name': f'Pago #{pago_id}', 'url': reverse_lazy('doctor:pago_detail', kwargs={'pk': pago_id})})
        context['breadcrumb'].append({'name': 'Nuevo Detalle', 'active': True})
        return context

    def get_success_url(self):
        # Redirigir a la vista de detalle del Pago al que pertenece este detalle
        if self.object.pago:
            return reverse_lazy('doctor:pago_detail', kwargs={'pk': self.object.pago.pk})
        return reverse_lazy('doctor:detalle_pago_list') # Fallback

class DetallePagoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DetallePago
    form_class = DetallePagoForm
    template_name = 'clinica/detalle_pago/form.html' # Reutilizar la plantilla del formulario
    success_message = "Detalle de pago actualizado exitosamente."

    def form_valid(self, form):
        form.instance.user_updated = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Detalle de Pago #{self.object.id}'
        context['pago_obj'] = self.object.pago
        context['breadcrumb'] = [
            {'name': 'Inicio', 'url': reverse_lazy('security:home')},
            {'name': 'Pagos', 'url': reverse_lazy('doctor:pago_list')},
            {'name': f'Pago #{self.object.pago.id}', 'url': reverse_lazy('doctor:pago_detail', kwargs={'pk': self.object.pago.pk})},
            {'name': 'Editar Detalle', 'active': True}
        ]
        return context

    def get_success_url(self):
        if self.object.pago:
            return reverse_lazy('doctor:pago_detail', kwargs={'pk': self.object.pago.pk})
        return reverse_lazy('doctor:detalle_pago_list')

class DetallePagoListView(LoginRequiredMixin, ListView): # Aunque esta vista podría no ser tan necesaria si se gestionan desde el Pago
    model = DetallePago
    template_name = 'clinica/detalle_pago/list.html'
    context_object_name = 'detalles_pago'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('pago', 'servicio_adicional').order_by('-pago__date_creation', 'id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(pago__id__icontains=search_query) |
                Q(servicio_adicional__nombre_servicio__icontains=search_query) # Corregido: nombre_servicio
            )
        # Filtrar por pago_id si se proporciona en la URL
        pago_id = self.kwargs.get('pago_id')
        if pago_id:
            queryset = queryset.filter(pago_id=pago_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Detalles de Pago'
        context['search_query'] = self.request.GET.get('q', '')
        # Breadcrumbs y otros datos de contexto
        context['breadcrumb'] = [
            {'name': 'Inicio', 'url': reverse_lazy('security:home')},
            {'name': 'Pagos', 'url': reverse_lazy('doctor:pago_list')},
            {'name': 'Todos los Detalles de Pago', 'active': True}
        ]
        pago_id = self.kwargs.get('pago_id')
        if pago_id: # Si se está listando para un pago específico
            pago = get_object_or_404(Pago, pk=pago_id)
            context['title'] = f'Detalles del Pago #{pago.id}'
            context['pago_obj'] = pago
            context['breadcrumb'] = [
                {'name': 'Inicio', 'url': reverse_lazy('security:home')},
                {'name': 'Pagos', 'url': reverse_lazy('doctor:pago_list')},
                {'name': f'Pago #{pago.id}', 'url': reverse_lazy('doctor:pago_detail', kwargs={'pk': pago.id})},
                {'name': 'Detalles', 'active': True}
            ]
        return context

class DetallePagoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DetallePago
    template_name = 'clinica/detalle_pago/detallepago_confirm_delete.html' # Corregido
    success_message = "Detalle de pago eliminado exitosamente."
    # success_url se definirá en get_success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Detalle de Pago'
        # Breadcrumbs
        context['breadcrumb'] = [
            {'name': 'Inicio', 'url': reverse_lazy('security:home')},
            {'name': 'Pagos', 'url': reverse_lazy('doctor:pago_list')},
            {'name': f'Pago #{self.object.pago.id}', 'url': reverse_lazy('doctor:pago_detail', kwargs={'pk': self.object.pago.pk})},
            {'name': 'Eliminar Detalle', 'active': True}
        ]
        return context

    def delete(self, request, *args, **kwargs):
        # Guardar el pago_id antes de que el objeto se elimine
        self.pago_id_for_redirect = self.get_object().pago_id
        response = super().delete(request, *args, **kwargs)
        # Actualizar el monto_total del Pago padre después de eliminar un detalle
        if self.pago_id_for_redirect:
            try:
                pago = Pago.objects.get(id=self.pago_id_for_redirect)
                # La lógica de actualizar_total_pago_padre se invoca desde DetallePago.delete() si está sobreescrito
                # Si no, se debe llamar aquí explícitamente o mediante una señal.
                # Asumiendo que el modelo DetallePago.save() y .delete() actualizan el padre.
                # Si DetallePago.delete() no lo hace, hay que hacerlo manualmente:
                total = DetallePago.objects.filter(pago=pago).aggregate(total=models.Sum('subtotal'))['total'] or Decimal('0.00')
                pago.monto_total = total
                pago.save()
            except Pago.DoesNotExist:
                pass # El pago ya no existe, no hay nada que actualizar
        messages.success(self.request, self.success_message) # SuccessMessageMixin no funciona bien con delete sobreescrito sin HttpResponseRedirect
        return response

    def get_success_url(self):
        # Redirigir a la vista de detalle del Pago padre después de la eliminación
        if hasattr(self, 'pago_id_for_redirect') and self.pago_id_for_redirect:
            return reverse_lazy('doctor:pago_detail', kwargs={'pk': self.pago_id_for_redirect})
        # Fallback, aunque no debería ser necesario si el detalle siempre tiene un pago
        return reverse_lazy('doctor:pago_list')