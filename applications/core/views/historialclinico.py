from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from applications.core.models import HistorialClinico
from applications.core.forms.historialclinico import HistorialClinicoForm

class HistorialClinicoListView(ListView):
    model=HistorialClinico
    template_name="clinica/historialclinico/list.html"
    context_object_name="historiales"
    
class HistorialClinicoCreateView(CreateView):
    model = HistorialClinico
    form_class= HistorialClinico
    template_name="clinica/historialclinico/historialclinico_form.html"
    success_url = reverse_lazy("historialclinico_form.html")
    
class HistorialClinicoUpdateView(UpdateView):
    model = HistorialClinico
    form_class= HistorialClinico
    template_name="clinica/historialclinico/historialclinico_form.html"
    success_url=reverse_lazy("historialclinico_form.html")
    
class HistorialClinicoDeleteView(DeleteView):
    model = HistorialClinico
    template_name="clinica/historialclinico/historialclinico_confirm_delete.html"
    success_url=reverse_lazy("historialclinico_confirm_delete.html")
    
class HistorialClinicoDetailView(DetailView):
    model = HistorialClinico
    template_name="clinica/historialclinico/historialclinico_detail.html"
    context_object_name="historiales"
   