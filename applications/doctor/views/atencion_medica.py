from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
# Modelos de la app doctor
from applications.doctor.models import Atencion, DetalleAtencion, Patient as DoctorPatient
# Modelos de la app core que se usan
from applications.core.models import Medicamento, Diagnostico, TipoMedicamento
# Formularios
from applications.doctor.forms.atencion import AtencionForm, DetalleAtencionFormSet, AtencionFilterForm
from proy_clinico.util import save_audit # Asumiendo que tienes esta utilidad


class AtencionListView(PermissionMixin, ListViewMixin, ListView):
    model = Atencion
    template_name = 'doctor/atencion/list.html' # Cambiado a la nueva ruta
    context_object_name = 'atenciones'
    permission_required = 'doctor.view_atencion'
    form_class = AtencionFilterForm

    def get_queryset(self):
        self.query = Q()
        # Atencion.paciente es ForeignKey a DoctorPatient.
        # DoctorPatient tiene: primer_nombre, apellido, dni
        queryset = self.model.objects.select_related('paciente').prefetch_related('diagnostico', 'detalles_doctor_app__medicamento').order_by('-fecha_atencion_real')

        self.filter_form = self.form_class(self.request.GET or None)
        if self.filter_form.is_valid():
            paciente_query = self.filter_form.cleaned_data.get('paciente') # Este es un CharField del filter form
            fecha_desde = self.filter_form.cleaned_data.get('fecha_desde')
            fecha_hasta = self.filter_form.cleaned_data.get('fecha_hasta')
            diagnostico_filter = self.filter_form.cleaned_data.get('diagnostico')

            if paciente_query:
                self.query.add(
                    Q(paciente__primer_nombre__icontains=paciente_query) |
                    Q(paciente__apellido__icontains=paciente_query) |
                    Q(paciente__dni__icontains=paciente_query), Q.AND
                )
            if fecha_desde:
                # Asumiendo que 'fecha_atencion_real' es el campo correcto en Atencion
                self.query.add(Q(fecha_atencion_real__date__gte=fecha_desde), Q.AND)
            if fecha_hasta:
                self.query.add(Q(fecha_atencion_real__date__lte=fecha_hasta), Q.AND)
            if diagnostico_filter:
                self.query.add(Q(diagnostico=diagnostico_filter), Q.AND)

        return queryset.filter(self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        context['create_url'] = reverse_lazy('doctor:atencion_create')
        return context

class AtencionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Atencion
    form_class = AtencionForm
    template_name = 'doctor/atencion/form.html'
    success_url = reverse_lazy('doctor:atencion_list')
    permission_required = 'doctor.add_atencion'
    model_name_title = "Atención Médica"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['detalle_formset'] = DetalleAtencionFormSet(self.request.POST, prefix='detalles')
        else:
            paciente_id = self.request.GET.get('paciente_id')
            initial_form_data = {}
            if paciente_id:
                # Usar DoctorPatient consistentemente
                paciente = get_object_or_404(DoctorPatient, pk=paciente_id) # Asumimos que DoctorPatient no tiene 'activo' o se filtra en el manager
                initial_form_data['paciente_nombre'] = f"{paciente.primer_nombre} {paciente.apellido}"
                initial_form_data['paciente'] = paciente.pk # El ID para el ModelChoiceField oculto
                context['selected_paciente'] = paciente

            # Pasar initial_form_data al constructor del formulario
            context['form'] = self.form_class(initial=initial_form_data)
            context['detalle_formset'] = DetalleAtencionFormSet(prefix='detalles')

        context['medicamentos_existentes'] = Medicamento.objects.filter(activo=True).order_by('nombre')
        context['tipos_medicamento_existentes'] = TipoMedicamento.objects.filter(activo=True).order_by('nombre') # Para el modal de creación rápida
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']

        with transaction.atomic():
            # Guardar el paciente_id si viene del campo oculto 'paciente'
            paciente_id = form.cleaned_data.get('paciente')
            if paciente_id:
                 form.instance.paciente = paciente_id # Asignar el objeto Paciente

            self.object = form.save()

            if detalle_formset.is_valid():
                detalle_formset.instance = self.object

                for detalle_form in detalle_formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        # Lógica para manejar medicamento_nombre y medicamento (ID)
                        medicamento_nombre = detalle_form.cleaned_data.get('medicamento_nombre')
                        medicamento_id = detalle_form.cleaned_data.get('medicamento')

                        if not medicamento_id and medicamento_nombre:
                            # Intento de crear nuevo medicamento "al vuelo" (requiere más campos)
                            # Esta es una simplificación. En un caso real, necesitarías un form para Medicamento
                            # y probablemente un modal para llenarlo.
                            # Por ahora, si no hay ID y hay nombre, intentamos buscarlo o fallamos si no es exacto.
                            try:
                                med = Medicamento.objects.get(nombre__iexact=medicamento_nombre, activo=True)
                                detalle_form.instance.medicamento = med
                            except Medicamento.DoesNotExist:
                                # Aquí podrías mostrar un error o redirigir a crear medicamento
                                messages.error(self.request, f"El medicamento '{medicamento_nombre}' no fue encontrado y no se pudo crear automáticamente.")
                                form.add_error(None, f"Medicamento '{medicamento_nombre}' no encontrado.")
                                return self.form_invalid(form) # Re-renderizar con error
                            except Medicamento.MultipleObjectsReturned:
                                messages.error(self.request, f"Múltiples medicamentos encontrados para '{medicamento_nombre}'. Por favor sea más específico o seleccione de la lista.")
                                form.add_error(None, f"Múltiples medicamentos para '{medicamento_nombre}'.")
                                return self.form_invalid(form) # Re-renderizar con error
                        elif medicamento_id:
                             detalle_form.instance.medicamento = medicamento_id


                detalle_formset.save()
                save_audit(self.request, self.object, "ADICION") # Auditoría
                messages.success(self.request, f"Éxito al registrar la {self.model_name_title.lower()} #{self.object.id}.")
                return HttpResponseRedirect(self.get_success_url())
            else:
                # Errores en el formset
                form.add_error(None, "Por favor corrija los errores en los detalles de la atención.")
                return self.form_invalid(form)

    def form_invalid(self, form):
        # Asegurarse de que el formset con errores también se pase al contexto
        context = self.get_context_data(form=form)
        if not context.get('detalle_formset'): # Si no se llenó en get_context_data porque no era POST
            context['detalle_formset'] = DetalleAtencionFormSet(self.request.POST or None, prefix='detalles')

        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{form.fields[field].label if field != '__all__' else ''}: {error}")
        for detalle_form in context['detalle_formset'].forms:
            for field, errors in detalle_form.errors.items():
                for error in errors:
                    error_messages.append(f"Detalle - {detalle_form.prefix} - {detalle_form.fields[field].label if field != '__all__' else ''}: {error}")

        messages.error(self.request, f"Error al guardar la {self.model_name_title.lower()}. Revise los campos: {'; '.join(error_messages)}")
        return self.render_to_response(context)


class AtencionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Atencion
    form_class = AtencionForm
    template_name = 'doctor/atencion/form.html' # Cambiado a la nueva ruta
    success_url = reverse_lazy('doctor:atencion_list')
    permission_required = 'doctor.change_atencion'
    model_name_title = "Atención Médica"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['detalle_formset'] = DetalleAtencionFormSet(self.request.POST, instance=self.object, prefix='detalles')
        else:
            context['detalle_formset'] = DetalleAtencionFormSet(instance=self.object, prefix='detalles')

        context['selected_paciente'] = self.object.paciente # Para mostrar info del paciente
        context['medicamentos_existentes'] = Medicamento.objects.filter(activo=True).order_by('nombre')
        context['tipos_medicamento_existentes'] = TipoMedicamento.objects.filter(activo=True).order_by('nombre') # Para el modal de creación rápida
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']

        with transaction.atomic():
            self.object = form.save()
            if detalle_formset.is_valid():
                detalle_formset.instance = self.object # Asegurar que la instancia se asigne al formset

                for detalle_form in detalle_formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        medicamento_nombre = detalle_form.cleaned_data.get('medicamento_nombre')
                        medicamento_id = detalle_form.cleaned_data.get('medicamento')

                        if not medicamento_id and medicamento_nombre:
                            try:
                                med = Medicamento.objects.get(nombre__iexact=medicamento_nombre, activo=True)
                                detalle_form.instance.medicamento = med
                            except Medicamento.DoesNotExist:
                                messages.error(self.request, f"El medicamento '{medicamento_nombre}' no fue encontrado.")
                                form.add_error(None, f"Medicamento '{medicamento_nombre}' no encontrado.")
                                return self.form_invalid(form)
                            except Medicamento.MultipleObjectsReturned:
                                messages.error(self.request, f"Múltiples medicamentos encontrados para '{medicamento_nombre}'.")
                                form.add_error(None, f"Múltiples medicamentos para '{medicamento_nombre}'.")
                                return self.form_invalid(form)
                        elif medicamento_id:
                             detalle_form.instance.medicamento = medicamento_id

                detalle_formset.save()
                save_audit(self.request, self.object, "MODIFICACION") # Auditoría
                messages.success(self.request, f"Éxito al actualizar la {self.model_name_title.lower()} #{self.object.id}.")
                return HttpResponseRedirect(self.get_success_url())
            else:
                form.add_error(None, "Por favor corrija los errores en los detalles de la atención.")
                return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        if not context.get('detalle_formset'):
             context['detalle_formset'] = DetalleAtencionFormSet(self.request.POST or None, instance=self.object, prefix='detalles')

        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{form.fields[field].label if field != '__all__' else ''}: {error}")
        for detalle_form in context['detalle_formset'].forms:
            for field, errors in detalle_form.errors.items():
                for error in errors:
                    error_messages.append(f"Detalle - {detalle_form.prefix} - {detalle_form.fields[field].label if field != '__all__' else ''}: {error}")

        messages.error(self.request, f"Error al actualizar la {self.model_name_title.lower()}. Revise los campos: {'; '.join(error_messages)}")
        return self.render_to_response(context)


class AtencionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Atencion
    template_name = 'core/delete_confirm.html'
    success_url = reverse_lazy('doctor:atencion_list')
    permission_required = 'doctor.delete_atencion'
    model_name_title = "Atención Médica"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'grabar', 'description', 'back_url' ya se manejan en DeleteViewMixin
        context['description'] = f"¿Está seguro de eliminar la {self.model_name_title.lower()} de {self.object.paciente} del {self.object.fecha_atencion_real.strftime('%d/%m/%Y')}?"
        return context

    def form_valid(self, form):
        object_repr = str(self.object) # Guardar representación antes de eliminar
        with transaction.atomic():
            # Si hay detalles, podrías querer eliminarlos explícitamente o manejarlo con on_delete=models.CASCADE
            # DetalleAtencion.objects.filter(atencion=self.object).delete() # Si no es CASCADE
            response = super().form_valid(form) # Esto llama a self.object.delete()

        save_audit(self.request, self.object, "ELIMINACION") # Auditoría
        messages.success(self.request, f"Éxito al eliminar la {self.model_name_title.lower()}: {object_repr}.")
        return response

# --- Vistas para búsqueda de Pacientes y Medicamentos (AJAX) ---

def buscar_paciente_ajax(request):
    term = request.GET.get('term', '')
    page = request.GET.get('page', 1)

    # Usar DoctorPatient
    # Asumimos que DoctorPatient no tiene un campo 'activo', si lo tuviera, añadir .filter(activo=True)
    pacientes_qs = DoctorPatient.objects.filter(
        Q(primer_nombre__icontains=term) |
        Q(apellido__icontains=term) |
        Q(dni__icontains=term)
    ).order_by('apellido', 'primer_nombre')

    # Paginación para Select2 (opcional pero bueno para rendimiento)
    # por ahora, limitamos a un número fijo de resultados como antes
    limit = 15
    # offset = (int(page) - 1) * limit
    # pacientes = pacientes_qs[offset:offset+limit]
    # total_count = pacientes_qs.count()
    pacientes = pacientes_qs[:limit]


    results = []
    for p in pacientes:
        # Construir el texto para Select2
        text = f"{p.primer_nombre} {p.apellido}"
        if p.dni:
            text += f" (DNI: {p.dni})"

        # Construir el objeto full_data para pasar más información al frontend si es necesario
        # Especialmente para actualizar la sección de info del paciente
        # Nota: 'edad_calculada' es una propiedad del modelo DoctorPatient, asegúrate que exista
        # o calcúlala aquí si es necesario.
        try:
            edad = p.edad_calculada # Asumiendo que existe esta propiedad
        except AttributeError:
            from datetime import date
            today = date.today()
            edad = today.year - p.birth_date.year - ((today.month, today.day) < (p.birth_date.month, p.birth_date.day)) if p.birth_date else "N/A"


        full_data = {
            'id': p.id,
            'primer_nombre': p.primer_nombre,
            'apellido': p.apellido,
            'dni': p.dni,
            'phone': p.phone,
            'email': p.email,
            'birth_date': p.birth_date.strftime('%Y-%m-%d') if p.birth_date else None,
            'edad_calculada': edad,
            # Añade otros campos que quieras mostrar en `infoPacienteSeleccionado`
        }
        results.append({
            "id": p.pk,
            "text": text,
            "full_data": full_data # Enviar datos completos para JS
        })

    # Para la paginación de Select2, necesitarías 'total_count' y un formato como:
    # return JsonResponse({'results': results, 'pagination': {'more': offset + limit < total_count}}, safe=False)
    return JsonResponse({'results': results, 'pagination': {'more': False}}, safe=False) # Simplificado sin paginación real Select2


def buscar_medicamento_ajax(request):
    query = request.GET.get('term', '')
    medicamentos = Medicamento.objects.filter(
        Q(nombre__icontains=query) |
        Q(descripcion__icontains=query),
        activo=True
    ).select_related('tipo', 'marca_medicamento').only(
        'id', 'nombre', 'concentracion', 'tipo__nombre', 'marca_medicamento__nombre', 'precio'
    )[:10]

    results = []
    for med in medicamentos:
        text = f"{med.nombre}"
        if med.concentracion: text += f" ({med.concentracion})"
        if med.tipo: text += f" T: {med.tipo.nombre}"
        if med.marca_medicamento: text += f" M: {med.marca_medicamento.nombre}"
        results.append({
            "id": med.pk,
            "text": text,
            "nombre": med.nombre,
            "concentracion": med.concentracion,
            "precio": str(med.precio) # Para el frontend
        })
    return JsonResponse(results, safe=False)


def previsualizar_atencion_ajax(request):
    if request.method == 'POST':
        # Esta función es un placeholder y necesitaría una implementación más robusta
        # para tomar todos los datos del formulario de atención vía AJAX
        # y renderizar una plantilla parcial con la previsualización.
        # Por ahora, solo devolvemos un mensaje.

        # Ejemplo simplificado de cómo podrías empezar a recolectar datos:
        # form_data = AtencionForm(request.POST or None) # Validar y limpiar
        # detalle_formset_data = DetalleAtencionFormSet(request.POST or None, prefix='detalles')

        # if form_data.is_valid() and detalle_formset_data.is_valid():
        #     # Aquí construirías el HTML de previsualización
        #     # html_preview = render_to_string('doctor/atencion/_preview_template.html',
        #     #                                 {'atencion_data': form_data.cleaned_data,
        #     #                                  'detalles_data': detalle_formset_data.cleaned_data})
        #     html_preview = "<p>Previsualización no implementada completamente. Datos recibidos.</p>"
        #     return JsonResponse({'status': 'success', 'html_preview': html_preview})
        # else:
        #     return JsonResponse({'status': 'error', 'message': 'Datos inválidos para previsualización.'})

        # return JsonResponse({'status': 'info', 'message': 'Previsualización no implementada.'})
        # --- INICIO IMPLEMENTACIÓN ---
        from django.template.loader import render_to_string
        from applications.doctor.forms.atencion import AtencionForm, DetalleAtencionFormSet
        from applications.core.models import Paciente as CorePaciente # Para obtener datos del paciente si es necesario
        from applications.doctor.models import Patient as DoctorPatient
        from applications.core.models import Medicamento, Diagnostico

        if request.method == 'POST':
            # Instanciar el formulario principal con los datos del POST
            form = AtencionForm(request.POST)
            # Instanciar el formset de detalles con los datos del POST
            # El prefijo 'detalles' debe coincidir con el usado en el template
            detalle_formset = DetalleAtencionFormSet(request.POST, prefix='detalles')

            atencion_data = {}
            detalles_data_list = []

            # No llamamos a form.is_valid() aquí a propósito para la previsualización,
            # ya que el objetivo es mostrar lo que el usuario ha ingresado, incluso si no es válido aún.
            # Sin embargo, para obtener algunos datos relacionados (como nombres de objetos ForeignKey),
            # podríamos necesitar IDs válidos.

            # Copiar datos del formulario principal
            for field_name, field in form.fields.items():
                atencion_data[field_name] = form.data.get(field_name) # Usar form.data para obtener el valor raw

            # Intentar obtener el objeto paciente para mostrar más detalles
            paciente_id = form.data.get('paciente')
            if paciente_id:
                try:
                    # Usamos DoctorPatient ya que AtencionForm ahora referencia a este
                    paciente_obj = DoctorPatient.objects.get(pk=paciente_id)
                    atencion_data['paciente_obj'] = paciente_obj
                    atencion_data['paciente_nombre'] = f"{paciente_obj.primer_nombre} {paciente_obj.apellido}"
                except DoctorPatient.DoesNotExist:
                    atencion_data['paciente_obj'] = None
                    atencion_data['paciente_nombre'] = form.data.get('paciente_nombre', 'Paciente no encontrado')


            # Intentar obtener los objetos de diagnóstico
            diagnostico_ids = request.POST.getlist('diagnostico') # form.data.getlist('diagnostico')
            if diagnostico_ids:
                try:
                    atencion_data['diagnostico_objs'] = Diagnostico.objects.filter(pk__in=diagnostico_ids)
                except Exception:
                    atencion_data['diagnostico_objs'] = None


            # Procesar datos del formset de detalles
            # Necesitamos el total_forms para iterar correctamente
            total_forms = int(form.data.get(f'{detalle_formset.prefix}-TOTAL_FORMS', 0))
            for i in range(total_forms):
                detalle_data = {}
                # No marcar para eliminar en la previsualización, solo mostrar si existe
                # if form.data.get(f'{detalle_formset.prefix}-{i}-DELETE'):
                #     continue # O marcarlo para no mostrarlo

                detalle_data['medicamento_nombre'] = form.data.get(f'{detalle_formset.prefix}-{i}-medicamento_nombre', '')
                detalle_data['cantidad'] = form.data.get(f'{detalle_formset.prefix}-{i}-cantidad', '')
                detalle_data['prescripcion'] = form.data.get(f'{detalle_formset.prefix}-{i}-prescripcion', '')
                detalle_data['DELETE'] = form.data.get(f'{detalle_formset.prefix}-{i}-DELETE', False)


                medicamento_id = form.data.get(f'{detalle_formset.prefix}-{i}-medicamento')
                if medicamento_id:
                    try:
                        med_obj = Medicamento.objects.get(pk=medicamento_id)
                        detalle_data['medicamento_obj'] = med_obj
                        # Si el nombre del medicamento no se pasó o se quiere el nombre "oficial":
                        detalle_data['medicamento_nombre_resolved'] = med_obj.nombre
                    except Medicamento.DoesNotExist:
                        detalle_data['medicamento_obj'] = None

                if detalle_data['medicamento_nombre'] or medicamento_id : # Solo añadir si hay algo
                     detalles_data_list.append(detalle_data)


            context_preview = {
                'atencion_data': atencion_data,
                'detalles_data': detalles_data_list
            }

            html_preview = render_to_string('doctor/atencion/_preview_template.html', context_preview)
            return JsonResponse({'status': 'success', 'html_preview': html_preview})
        else:
            return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
        # --- FIN IMPLEMENTACIÓN ---
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def crear_medicamento_ajax(request):
    if request.method == 'POST':
        # Aquí se necesitaría un formulario para Medicamento
        # from applications.core.forms import MedicamentoForm # Suponiendo que existe
        # form = MedicamentoForm(request.POST)
        # if form.is_valid():
        #     try:
        #         medicamento = form.save()
        #         return JsonResponse({
        #             'status': 'success',
        #             'medicamento_id': medicamento.pk,
        #             'medicamento_nombre': medicamento.nombre,
        #             'medicamento_text': f"{medicamento.nombre} ({medicamento.concentracion or ''})" # Texto para select2
        #         })
        #     except Exception as e:
        #         return JsonResponse({'status': 'error', 'message': f'Error al guardar: {str(e)}'})
        # else:
        #     return JsonResponse({'status': 'error', 'message': 'Datos inválidos.', 'errors': form.errors})

        # Placeholder hasta que se implemente el form
        nombre_medicamento = request.POST.get('nombre_medicamento_modal') # Asumiendo un campo del modal
        if nombre_medicamento:
            # Lógica muy simplificada (NO USAR EN PRODUCCIÓN SIN VALIDACIÓN COMPLETA Y MÁS CAMPOS)
            if Medicamento.objects.filter(nombre__iexact=nombre_medicamento).exists():
                 return JsonResponse({'status': 'error', 'message': 'El medicamento ya existe.'})

            # Necesitarías TipoMedicamento, cantidad, precio, etc.
            # tipo_default = TipoMedicamento.objects.first()
            # if not tipo_default:
            #     return JsonResponse({'status': 'error', 'message': 'No hay tipos de medicamento base.'})

            # med = Medicamento.objects.create(nombre=nombre_medicamento, tipo=tipo_default, cantidad=0, precio="0.00")
            # return JsonResponse({'status': 'success', 'medicamento_id': med.id, 'medicamento_nombre': med.nombre, 'medicamento_text': med.nombre})
            # return JsonResponse({'status': 'info', 'message': 'Creación rápida de medicamento no implementada (requiere más campos).'})
            # --- INICIO IMPLEMENTACIÓN ---
            from applications.core.forms.medicamento import MedicamentoForm # Importar el formulario

            # Crear un diccionario con los datos recibidos del POST que coinciden con los campos del form
            # Esto es una aproximación, idealmente el frontend enviaría nombres de campo que coincidan.
            # Por ahora, asumimos que el frontend envía 'nombre_medicamento_modal' y otros campos opcionales
            # que podrían mapear a los campos del MedicamentoForm.

            data_from_request = request.POST.copy() # Hacemos una copia para poder modificarla

            # Mapeo de nombres de campos del modal a nombres de campos del MedicamentoForm
            # Esto dependerá de cómo se nombren los campos en el modal HTML
            field_map = {
                'nombre_medicamento_modal': 'nombre',
                'tipo_medicamento_modal': 'tipo', # Asumiendo que envías el ID del TipoMedicamento
                'marca_medicamento_modal': 'marca_medicamento', # Asumiendo ID
                'concentracion_modal': 'concentracion',
                'via_administracion_modal': 'via_administracion', # Asumiendo el valor de la opción
                'cantidad_modal': 'cantidad',
                'precio_modal': 'precio',
                'descripcion_modal': 'descripcion',
            }

            form_data = {}
            for modal_field, form_field in field_map.items():
                if modal_field in data_from_request:
                    form_data[form_field] = data_from_request[modal_field]

            # Valores por defecto si no vienen del modal
            if 'nombre' not in form_data or not form_data['nombre']:
                 return JsonResponse({'status': 'error', 'message': 'El nombre del medicamento es requerido.'})

            if 'tipo' not in form_data:
                # Asignar un tipo por defecto o el primero que encuentre si no se provee
                default_tipo = TipoMedicamento.objects.filter(activo=True).first()
                if default_tipo:
                    form_data['tipo'] = default_tipo.pk
                else:
                    return JsonResponse({'status': 'error', 'message': 'No se encontró un tipo de medicamento por defecto. Por favor, cree tipos de medicamento en el sistema.'})

            form_data.setdefault('cantidad', 0) # Stock inicial
            form_data.setdefault('precio', "0.00")
            form_data.setdefault('activo', True)
            form_data.setdefault('via_administracion', 'oral') # Un valor común por defecto

            form = MedicamentoForm(form_data)
            if form.is_valid():
                try:
                    medicamento = form.save()
                    # Texto para mostrar en Select2, puede ser personalizado
                    select2_text = f"{medicamento.nombre}"
                    if medicamento.concentracion:
                        select2_text += f" ({medicamento.concentracion})"
                    if medicamento.tipo:
                        select2_text += f" - T: {medicamento.tipo.nombre}"

                    return JsonResponse({
                        'status': 'success',
                        'medicamento_id': medicamento.pk,
                        'medicamento_nombre': medicamento.nombre, # Nombre base
                        'medicamento_text': select2_text, # Texto completo para Select2
                        'medicamento_precio': str(medicamento.precio) # Para el frontend si es necesario
                    })
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': f'Error al guardar el medicamento: {str(e)}'})
            else:
                # Errores del formulario
                return JsonResponse({'status': 'error', 'message': 'Datos inválidos para el medicamento.', 'errors': form.errors.as_json()})
            # --- FIN IMPLEMENTACIÓN ---
        else: # Esto es si 'nombre_medicamento_modal' (o el campo principal) no viene en el POST
            return JsonResponse({'status': 'error', 'message': 'Nombre del medicamento es requerido (desde el else principal).'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)