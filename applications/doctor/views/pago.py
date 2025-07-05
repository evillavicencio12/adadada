from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from applications.doctor.models import Pago

class PagoListView(ListView):
    model = Pago
    template_name = 'clinica/pago/form.html'
    context_object_name = 'pagos'

class PagoCreateView(CreateView):
    model = Pago
    fields = '__all__'
    template_name = 'clinica/pago/form.html'
    success_url = reverse_lazy('doctor:pago_list')

class PagoUpdateView(UpdateView):
    model = Pago
    fields = '__all__'
    template_name = 'clinica/pago/form.html'
    success_url = reverse_lazy('doctor:pago_list')

class PagoDetailView(DetailView):
    model = Pago
    template_name = 'clinica/pago/form.html'
    context_object_name = 'pago'

class PagoDeleteView(DeleteView):
    model = Pago
    template_name = 'clinica/pago/form.html'
    success_url = reverse_lazy('doctor:pago_list')
