from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin # Asegurar que el usuario esté logueado

from applications.doctor.models import Pago
from applications.doctor.forms.pago import PagoForm

class PagoListView(LoginRequiredMixin, ListView):
    model = Pago
    template_name = 'clinica/pago/list.html' # Corregido: Usar la plantilla de lista
    context_object_name = 'pagos'
    paginate_by = 10 # Opcional: añadir paginación

    def get_queryset(self):
        # Opcional: Pre-cargar datos relacionados para optimizar queries
        return Pago.objects.select_related('atencion', 'atencion__paciente').order_by('-date_creation')

class PagoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pago
    form_class = PagoForm # Corregido: Usar el formulario personalizado
    template_name = 'clinica/pago/form.html' # Se usará una nueva plantilla para el form
    success_url = reverse_lazy('doctor:pago_list')
    success_message = "Pago registrado exitosamente."

    def form_valid(self, form):
        form.instance.user_creation = self.request.user
        return super().form_valid(form)

class PagoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pago
    form_class = PagoForm # Corregido: Usar el formulario personalizado
    template_name = 'clinica/pago/form.html' # Se usará la misma plantilla de form que create
    success_url = reverse_lazy('doctor:pago_list')
    success_message = "Pago actualizado exitosamente."

    def form_valid(self, form):
        form.instance.user_updated = self.request.user
        return super().form_valid(form)

class PagoDetailView(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = 'clinica/pago/detail.html' # Se creará una plantilla de detalle
    context_object_name = 'pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se podrían cargar los DetallePago asociados si se quieren mostrar en la vista de detalle del Pago
        # context['detalles_pago'] = self.object.detalles_doctor_app.all()
        return context

class PagoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Pago
    template_name = 'clinica/pago/pago_confirm_delete.html' # Corregido: Usar plantilla de confirmación
    success_url = reverse_lazy('doctor:pago_list')
    success_message = "Pago eliminado exitosamente."

    # No es necesario sobreescribir delete() solo para el mensaje si se usa SuccessMessageMixin
    # def delete(self, request, *args, **kwargs):
    #     messages.success(self.request, self.success_message)
    #     return super(PagoDeleteView, self).delete(request, *args, **kwargs)
