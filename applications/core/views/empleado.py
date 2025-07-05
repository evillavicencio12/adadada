from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Empleado

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'clinica/empleados/list.html'
    context_object_name = 'empleados'

class EmpleadoCreateView(CreateView):
    model = Empleado
    fields = '__all__'  # <-- Aquí
    template_name = 'clinica/empleados/list.html'
    success_url = reverse_lazy('core:empleado_list')

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    fields = '__all__'  # <-- Aquí también
    template_name = 'clinica/empleados/list.html'
    success_url = reverse_lazy('core:empleado_list')

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'clinica/empleados/list.html'  # Recomiendo usar un template distinto para confirm delete, pero si quieres puedes reutilizar este
    success_url = reverse_lazy('core:empleado_list')
