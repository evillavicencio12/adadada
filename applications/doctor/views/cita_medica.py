# applications/doctor/views/cita_medica_views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, date
from ..models import CitaMedica
from applications.doctor.forms.forms import CitaMedicaForm
from applications.doctor.utils.cita_medica import EstadoCitaChoices
def cita_medica_list(request):
    """Lista todas las citas médicas con filtros y paginación"""
    citas_qs = CitaMedica.objects.select_related('paciente').order_by('-fecha', '-hora_cita')

    search_query = request.GET.get('search')
    estado_filter = request.GET.get('estado')
    fecha_desde_filter = request.GET.get('fecha_desde')
    fecha_hasta_filter = request.GET.get('fecha_hasta')
    
    if search_query:
        citas_qs = citas_qs.filter(
            Q(paciente__primer_nombre__icontains=search_query) |
            Q(paciente__apellido__icontains=search_query) |
            Q(paciente__dni__icontains=search_query) |
            Q(observaciones__icontains=search_query)
        )
    
    if estado_filter:
        citas_qs = citas_qs.filter(estado=estado_filter)
    
    if fecha_desde_filter:
        try:
            fecha_desde_dt = datetime.strptime(fecha_desde_filter, '%Y-%m-%d').date()
            citas_qs = citas_qs.filter(fecha__gte=fecha_desde_dt)
        except ValueError:
            messages.error(request, "Formato de 'fecha desde' inválido.")
            fecha_desde_filter = None
    
    if fecha_hasta_filter:
        try:
            fecha_hasta_dt = datetime.strptime(fecha_hasta_filter, '%Y-%m-%d').date()
            citas_qs = citas_qs.filter(fecha__lte=fecha_hasta_dt)
        except ValueError:
            messages.error(request, "Formato de 'fecha hasta' inválido.")
            fecha_hasta_filter = None
    
    paginator = Paginator(citas_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Listado de Citas Médicas',
        'page_obj': page_obj,
        'search_query': search_query,
        'estado_filter': estado_filter,
        'fecha_desde_filter': fecha_desde_filter,
        'fecha_hasta_filter': fecha_hasta_filter,
        'estados_choices': EstadoCitaChoices.choices,
    }
    return render(request, 'doctor/cita_medica/cita_list.html', context)

def cita_medica_detail(request, pk):
    """Muestra el detalle de una cita médica"""
    cita = get_object_or_404(CitaMedica.objects.select_related('paciente', 'user_creation', 'user_updated'), pk=pk)
    context = {
        'title': f'Detalle Cita #{cita.pk}',
        'cita': cita,
    }
    return render(request, 'doctor/cita_medica/cita_detail.html', context)

def cita_medica_create(request):
    fecha_param = request.GET.get('fecha')
    hora_param = request.GET.get('hora')
    initial_data = {}
    campos_precargados = {
        'fecha': False,
        'hora_cita': False,
    }

    if fecha_param:
        try:
            initial_data['fecha'] = datetime.strptime(fecha_param, 'YYYY-MM-DD').date()
            campos_precargados['fecha'] = True
        except ValueError:
            messages.warning(request, 'Formato de fecha inválido para la nueva cita.')
    if hora_param:
        try:
            initial_data['hora_cita'] = datetime.strptime(hora_param, '%H:%M').time()
            campos_precargados['hora_cita'] = True
        except ValueError:
            messages.warning(request, 'Formato de hora inválido para la nueva cita.')

    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            try:
                cita = form.save(commit=False)
                if request.user.is_authenticated:
                    cita.user_creation = request.user
                cita.save()
                messages.success(request, f'Cita médica para {cita.paciente} creada exitosamente.')
                return redirect('doctor:cita_medica_detail', pk=cita.pk)
            except Exception as e:
                messages.error(request, f'Error al crear la cita: {str(e)}')
    else:
        form = CitaMedicaForm(initial=initial_data)

    context = {
        'title': 'Crear Nueva Cita Médica',
        'form': form,
        'action': 'Crear',
        'campos_precargados': campos_precargados,
    }
    return render(request, 'doctor/cita_medica/cita_form.html', context)

def cita_medica_update(request, pk):
    """Actualiza una cita médica existente"""
    cita = get_object_or_404(CitaMedica, pk=pk)
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST, instance=cita)
        if form.is_valid():
            try:
                updated_cita = form.save(commit=False)
                updated_cita.user_updated = request.user if request.user.is_authenticated else None
                updated_cita.save()
                messages.success(request, f'Cita médica para {updated_cita.paciente} actualizada exitosamente.')
                return redirect('doctor:cita_medica_detail', pk=updated_cita.pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar la cita: {str(e)}')
    else:
        form = CitaMedicaForm(instance=cita)
    
    context = {
        'title': f'Editar Cita Médica #{cita.pk}',
        'form': form,
        'cita': cita,
        'action': 'Actualizar'
    }
    return render(request, 'doctor/cita_medica/cita_form.html', context)

def cita_medica_delete(request, pk):
    """Muestra confirmación o elimina una cita médica"""
    cita = get_object_or_404(CitaMedica.objects.select_related('paciente'), pk=pk)
    if request.method == 'POST':
        try:
            nombre_paciente = f"{cita.paciente.primer_nombre} {cita.paciente.apellido}"
            cita.delete()
            messages.success(request, f'Cita médica para {nombre_paciente} eliminada exitosamente.')
            return redirect('doctor:cita_medica_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar la cita: {str(e)}')
            return redirect('doctor:cita_medica_detail', pk=cita.pk)
    
    context = {
        'title': f'Confirmar Eliminación de Cita #{cita.pk}',
        'cita': cita,
    }
    return render(request, 'doctor/cita_medica/cita_confirm_delete.html', context)

@require_http_methods(["POST"])
def cita_medica_change_estado(request, pk):
    """Cambia el estado de una cita médica via AJAX"""
    cita = get_object_or_404(CitaMedica, pk=pk)
    nuevo_estado = request.POST.get('estado')
    
    valid_estados = [choice[0] for choice in EstadoCitaChoices.choices]

    if nuevo_estado in valid_estados:
        cita.estado = nuevo_estado
        cita.user_updated = request.user if request.user.is_authenticated else None
        cita.save()
        return JsonResponse({
            'success': True,
            'message': f'Estado cambiado a {cita.get_estado_display()}',
            'nuevo_estado': nuevo_estado,
            'nuevo_estado_display': cita.get_estado_display()
        })
    
    return JsonResponse({'success': False, 'message': 'Estado no válido'}, status=400)

def citas_hoy(request):
    """Muestra las citas de hoy en el formato de lista"""
    hoy = date.today()
    citas_qs = CitaMedica.objects.filter(fecha=hoy).select_related('paciente').order_by('hora_cita')
    
    paginator = Paginator(citas_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': f'Citas de Hoy ({hoy.strftime("%d/%m/%Y")})',
        'page_obj': page_obj,
        'estados_choices': EstadoCitaChoices.choices,
        'search_query': None,
        'estado_filter': None,
        'fecha_desde_filter': hoy.strftime('%Y-%m-%d'),
        'fecha_hasta_filter': hoy.strftime('%Y-%m-%d'),
    }
    return render(request, 'doctor/cita_medica/cita_list.html', context)

def citas_por_fecha(request, fecha_str):
    """Muestra las citas de una fecha específica en el formato de lista"""
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, 'Formato de fecha inválido. Use YYYY-MM-DD.')
        return redirect('doctor:cita_medica_list')
    
    citas_qs = CitaMedica.objects.filter(fecha=fecha_obj).select_related('paciente').order_by('hora_cita')
    
    paginator = Paginator(citas_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': f'Citas del {fecha_obj.strftime("%d/%m/%Y")}',
        'page_obj': page_obj,
        'estados_choices': EstadoCitaChoices.choices,
        'search_query': None,
        'estado_filter': None,
        'fecha_desde_filter': fecha_obj.strftime('%Y-%m-%d'),
        'fecha_hasta_filter': fecha_obj.strftime('%Y-%m-%d'),
    }
    return render(request, 'doctor/cita_medica/cita_list.html', context)


def cita_medica_create_ajax(request):
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')
    if request.method == 'GET':
        form = CitaMedicaForm(initial={'fecha': fecha, 'hora_cita': hora})
        return render(request, 'doctor/cita_medica/form_ajax.html', {'form': form})
    elif request.method == 'POST' and request.is_ajax():
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            return JsonResponse({'success': True, 'cita_id': cita.id, 'mensaje': 'Cita agendada exitosamente'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'error': 'Método no soportado'}, status=405)