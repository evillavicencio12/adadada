from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)
from applications.doctor.models import Patient
from applications.doctor.forms.patient import PatientForm
from datetime import date

class PatientListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/patient/list.html'
    model = Patient
    context_object_name = 'patients'
    permission_required = 'doctor.view_patient' # Assuming you have this permission

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        queryset = self.model.objects.all().order_by('apellido', 'primer_nombre')
        if q1:
            queryset = queryset.filter(
                Q(Primer_nombre__icontains=q1) |
                Q(apellido__icontains=q1) |
                Q(dni__icontains=q1) |
                Q(email__icontains=q1)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:patient_create')
        context['title'] = 'Listado de Pacientes'
        # print(context.get('permissions')) # For debugging permissions
        return context


class PatientCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Patient
    template_name = 'doctor/patient/form.html'
    form_class = PatientForm
    success_url = reverse_lazy('doctor:patient_list')
    permission_required = 'doctor.add_patient' # Assuming you have this permission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Registrar Paciente'
        context['back_url'] = self.success_url
        context['title'] = 'Nuevo Paciente'
        return context

    def form_valid(self, form):
        patient = form.save()
        messages.success(self.request, f"Éxito al crear el paciente {patient.primer_nombre} {patient.apellido}.")
        return super().form_valid(form)


class PatientUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Patient
    template_name = 'doctor/patient/form.html'
    form_class = PatientForm
    success_url = reverse_lazy('doctor:patient_list')
    permission_required = 'doctor.change_patient' # Assuming you have this permission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Paciente'
        context['back_url'] = self.success_url
        context['title'] = 'Actualizar Paciente'
        return context

    def form_valid(self, form):
        patient = self.object
        messages.success(self.request, f"Éxito al actualizar el paciente {patient.primer_nombre} {patient.apellido}.")
        return super().form_valid(form)


class PatientDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Patient
    template_name = 'core/delete_confirm.html' # Using a generic delete confirmation
    success_url = reverse_lazy('doctor:patient_list')
    permission_required = 'doctor.delete_patient' # Assuming you have this permission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Paciente'
        context['description'] = f"¿Desea eliminar el paciente: {self.object.primer_nombre} {self.object.apellido}?"
        context['back_url'] = self.success_url
        context['title'] = 'Eliminar Paciente'
        return context

    def form_valid(self, form):
        patient_name = f"{self.object.primer_nombre} {self.object.apellido}"
        # Instead of super().form_valid(form) which calls delete(),
        # we can implement soft delete if the model supports it (e.g., an 'activo' field)
        # For now, we'll proceed with hard delete as per DeleteView's default.
        # If soft delete is needed, the model should be updated and this method overridden.
        # self.object.activo = False
        # self.object.save()
        # messages.success(self.request, f"Éxito al eliminar lógicamente el paciente {patient_name}.")
        # return HttpResponseRedirect(self.success_url)

        # Hard delete:
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el paciente {patient_name}.")
        return response

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # Consider CSRF implications for AJAX POST
from django.views.decorators.http import require_POST, require_GET
import json

@require_POST
# @csrf_exempt # Temporarily, for simplicity. For production, ensure proper CSRF handling for AJAX.
# It's better to include CSRF token in AJAX request rather than exempting. The JS already includes it.
def ajax_create_patient(request):
    # For simplicity, this directly uses request.POST.
    # A more robust way would be to instantiate PatientForm with request.POST
    # and call form.is_valid() and form.save().
    form = PatientForm(request.POST)
    if form.is_valid():
        try:
            patient = form.save()
            # Assuming 'edad' is a property on the Patient model that calculates age
            # or a method. Let's try calling it if it's a method, or accessing if property.
            edad_calculada = None
            if hasattr(patient, 'get_edad_display') and callable(patient.get_edad_display):
                 edad_calculada = patient.get_edad_display()
            elif hasattr(patient, 'edad'):
                if callable(patient.edad):
                    edad_calculada = patient.edad()
                else:
                    edad_calculada = patient.edad

            if edad_calculada is None and patient.birth_date: # Fallback calculation
                today = date.today()
                born = patient.birth_date
                edad_calculada = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

            return JsonResponse({
                'status': 'success',
                'paciente': {
                    'id': patient.pk,
                    'primer_nombre': patient.primer_nombre,
                    'apellido': patient.apellido,
                    'dni': patient.dni or "",
                    'birth_date': patient.birth_date.strftime('%Y-%m-%d') if patient.birth_date else None,
                    'phone': patient.phone or "",
                    'email': patient.email or "",
                    'edad': edad_calculada
                }
            })
        except Exception as e:
            # Log the full error for debugging
            print(f"Error saving patient: {e}") # Consider proper logging
            return JsonResponse({'status': 'error', 'errors': f'Error interno del servidor: {str(e)}'}, status=500)
    else:
        # Convert form.errors (which is an ErrorDict) to a more AJAX-friendly format
        # The JS expects something like: {'field_name': [{'message': 'error text', 'code': '...'}], ...}
        # form.errors.as_json() converts it to a JSON string, which then needs to be parsed by JS.
        # A better way is to return a dict directly.
        error_dict = {}
        for field, error_list in form.errors.items():
            error_dict[field] = [{'message': str(error)} for error in error_list]


        return JsonResponse({'status': 'error', 'errors': error_dict}, status=400)


@require_GET
def ajax_search_patient_dni(request):
    dni = request.GET.get('dni', None)
    if dni:
        try:
            patient = Patient.objects.get(dni__iexact=dni) # DNI should be unique
            edad_calculada = None
            if hasattr(patient, 'get_edad_display') and callable(patient.get_edad_display):
                 edad_calculada = patient.get_edad_display()
            elif hasattr(patient, 'edad'):
                if callable(patient.edad):
                    edad_calculada = patient.edad()
                else:
                    edad_calculada = patient.edad
            if edad_calculada is None and patient.birth_date:
                today = date.today()
                born = patient.birth_date
                edad_calculada = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

            data = {
                'id': patient.pk,
                'primer_nombre': patient.primer_nombre,
                'apellido': patient.apellido,
                'dni': patient.dni or "",
                'birth_date': patient.birth_date.strftime('%Y-%m-%d') if patient.birth_date else None,
                'phone': patient.phone or "",
                'email': patient.email or "",
                'edad': edad_calculada,
                # Add any other fields needed
            }
            # The JS expects a list, even if it's one patient for DNI search
            return JsonResponse({'pacientes': [data]})
        except Patient.DoesNotExist:
            return JsonResponse({'error': 'Paciente no encontrado con este DNI.', 'pacientes': []}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}', 'pacientes': []}, status=500)
    return JsonResponse({'error': 'DNI no proporcionado.', 'pacientes': []}, status=400)

from django.core.paginator import Paginator

@require_GET
def ajax_search_patient_by_name(request):
    nombre = request.GET.get('nombre', '').strip()
    page_number = request.GET.get('page', 1)

    if not nombre:
        return JsonResponse({'pacientes': [], 'total_count': 0})

    base_queryset = Patient.objects.filter(
        Q(primer_nombre__icontains=nombre) | Q(apellido__icontains=nombre)
    ).order_by('apellido', 'primer_nombre')

    paginator = Paginator(base_queryset, 10) # 10 items per page, adjust as needed
    try:
        page_obj = paginator.page(page_number)
    except Exception: # E.g., PageNotAnInteger, EmptyPage
        page_obj = paginator.page(1)

    data_list = []
    for p in page_obj.object_list:
        edad_calculada = None
        # Intentar obtener la edad de una propiedad o método del modelo
        if hasattr(p, 'edad_calculada'): # Si 'edad_calculada' es una propiedad
            edad_calculada = p.edad_calculada
        elif hasattr(p, 'get_edad_display') and callable(p.get_edad_display): # Si es un método
            edad_calculada = p.get_edad_display()
        elif hasattr(p, 'edad'): # Otro posible nombre de propiedad/método
            if callable(p.edad):
                edad_calculada = p.edad()
            else:
                edad_calculada = p.edad

        # Fallback si no se pudo obtener la edad del modelo y hay fecha de nacimiento
        if edad_calculada is None and p.birth_date:
            today = date.today()
            born = p.birth_date
            edad_calculada = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        text_display = f"{p.primer_nombre} {p.apellido}"
        if p.dni:
            text_display += f" (DNI: {p.dni})"

        data_list.append({
            'id': p.pk, # Para el valor del Select2
            'text': text_display, # Para la visualización en Select2
            'full_data': { # Datos adicionales para usar en el frontend
                'id': p.pk,
                'primer_nombre': p.primer_nombre,
                'apellido': p.apellido,
                'dni': p.dni or '',
                'phone': p.phone or '',
                'email': p.email or '',
                'birth_date': p.birth_date.strftime('%Y-%m-%d') if p.birth_date else None,
                'edad_calculada': edad_calculada if edad_calculada is not None else "N/A",
            }
        })

    return JsonResponse({
        'results': data_list, # Cambiado de 'pacientes' a 'results'
        'pagination': {
            'more': page_obj.has_next() # Select2 espera 'more'
        }
    })
