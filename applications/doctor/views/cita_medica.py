# applications/doctor/views/cita_medica_views.py
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, date
from ..models import CitaMedica
from applications.doctor.forms.forms import CitaMedicaForm  # Importar la clase form correctamente

def cita_medica_list(request):
    """Lista todas las citas médicas con filtros y paginación"""
    citas = CitaMedica.objects.select_related('paciente').all()
    
    # Filtros
    search = request.GET.get('search')
    estado = request.GET.get('estado')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if search:
        citas = citas.filter(
            Q(paciente__nombre_completo__icontains=search) |
            Q(observaciones__icontains=search)
        )
    
    if estado:
        citas = citas.filter(estado=estado)
    
    if fecha_desde:
        try:
            fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
            citas = citas.filter(fecha__gte=fecha_desde)
        except ValueError:
            pass
    
    if fecha_hasta:
        try:
            fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
            citas = citas.filter(fecha__lte=fecha_hasta)
        except ValueError:
            pass
    
    # Paginación
    paginator = Paginator(citas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estados_choices': CitaMedica._meta.get_field('estado').choices,
    }
    
    return render(request, 'doctor/cita_medica/citas.html', context)

def cita_medica_detail(request, pk):
    """Muestra el detalle de una cita médica"""
    cita = get_object_or_404(CitaMedica, pk=pk)
    
    context = {
        'cita': cita,
    }
    
    return render(request, 'doctor/cita_medica/citas.html', context)


def cita_medica_create(request):
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')

    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            try:
                cita = form.save()
                messages.success(request, 'Cita médica creada exitosamente')
                return redirect('doctor:cita_medica_detail', pk=cita.pk)
            except Exception as e:
                messages.error(request, f'Error al crear la cita: {str(e)}')
    else:
        initial_data = {}
        if fecha:
            try:
                initial_data['fecha'] = datetime.strptime(fecha, '%Y-%m-%d').date()
            except ValueError:
                pass
        if hora:
            try:
                initial_data['hora_cita'] = datetime.strptime(hora, '%H:%M').time()
            except ValueError:
                pass
        form = CitaMedicaForm(initial=initial_data)

    context = {
        'form': form,
        'title': 'Crear Cita Médica',
        'action': 'Crear'
    }

    return render(request, 'doctor/cita_medica/citas.html', context)



def cita_medica_update(request, pk):
    """Actualiza una cita médica existente"""
    cita = get_object_or_404(CitaMedica, pk=pk)
    
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST, instance=cita)
        if form.is_valid():
            try:
                cita = form.save()
                messages.success(request, 'Cita médica actualizada exitosamente')
                return redirect('doctor:cita_medica_detail', pk=cita.pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar la cita: {str(e)}')
    else:
        form = CitaMedicaForm(instance=cita)
    
    context = {
        'form': form,
        'cita': cita,
        'title': 'Editar Cita Médica',
        'action': 'Actualizar'
    }
    
    return render(request, 'doctor/cita_medica/citas.html', context)


def cita_medica_delete(request, pk):
    """Elimina una cita médica"""
    cita = get_object_or_404(CitaMedica, pk=pk)
    
    if request.method == 'POST':
        try:
            cita.delete()
            messages.success(request, 'Cita médica eliminada exitosamente')
            return redirect('doctor:cita_medica_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar la cita: {str(e)}')
    
    context = {
        'cita': cita,
    }
    
    return render(request, 'doctor/cita_medica/citas.html', context)


@require_http_methods(["POST"])
def cita_medica_change_estado(request, pk):
    """Cambia el estado de una cita médica via AJAX"""
    cita = get_object_or_404(CitaMedica, pk=pk)
    nuevo_estado = request.POST.get('estado')
    
    if nuevo_estado in dict(CitaMedica._meta.get_field('estado').choices):
        cita.estado = nuevo_estado
        cita.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Estado cambiado a {cita.get_estado_display()}',
            'nuevo_estado': nuevo_estado,
            'nuevo_estado_display': cita.get_estado_display()
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Estado no válido'
    })

def citas_hoy(request):
    """Muestra las citas de hoy"""
    hoy = date.today()
    citas = CitaMedica.objects.filter(fecha=hoy).select_related('paciente').order_by('hora_cita')
    
    context = {
        'citas': citas,
        'fecha': hoy,
        'title': 'Citas de Hoy'
    }
    
    return render(request, 'doctor/cita_medica/citas.html', context)


def citas_por_fecha(request, fecha):
    """Muestra las citas de una fecha específica"""
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, 'Formato de fecha inválido')
        return redirect('doctor:cita_medica_list')
    
    citas = CitaMedica.objects.filter(fecha=fecha_obj).select_related('paciente').order_by('hora_cita')
    
    context = {
        'citas': citas,
        'fecha': fecha_obj,
        'title': f'Citas del {fecha_obj.strftime("%d/%m/%Y")}'
    }
    
    return render(request, 'doctor/cita_medica/citas.html', context)

def vista_citas(request):
    citas = CitaMedica.objects.all()
    context = {
        'citas': citas,
    }
    return render(request, 'doctor/cita_medica/citas.html', context)
