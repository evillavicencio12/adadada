# views.py - Sistema de Calendario Automático
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
from calendar import monthrange
import json

from ..models import HorarioAtencion, CitaMedica
from applications.doctor.utils.doctor import DiaSemanaChoices

class CalendarioMedicoService:
    """Servicio para generar calendarios médicos automáticamente"""
    
    INTERVALOS_CITA = 30  # minutos por cita
    
    @classmethod
    def obtener_nombre_dia_espanol(cls, fecha):
        """Convierte el día de la semana a español para matching con modelo"""
        dias_semana = {
            0: DiaSemanaChoices.LUNES,
            1: DiaSemanaChoices.MARTES, 
            2: DiaSemanaChoices.MIERCOLES,
            3: DiaSemanaChoices.JUEVES,
            4: DiaSemanaChoices.VIERNES,
            5: DiaSemanaChoices.SABADO,
            6: DiaSemanaChoices.DOMINGO
        }
        return dias_semana.get(fecha.weekday())
    
    @classmethod
    def generar_slots_horarios(cls, horario_atencion):
        """Genera slots de tiempo disponibles basado en horario de atención"""
        slots = []
        
        # Primer bloque: desde hora_inicio hasta intervalo_desde
        if horario_atencion.intervalo_desde:
            slots.extend(cls._crear_slots_bloque(
                horario_atencion.hora_inicio, 
                horario_atencion.intervalo_desde
            ))
            
            # Segundo bloque: desde intervalo_hasta hasta hora_fin
            slots.extend(cls._crear_slots_bloque(
                horario_atencion.intervalo_hasta, 
                horario_atencion.hora_fin
            ))
        else:
            # Sin pausa de almuerzo
            slots.extend(cls._crear_slots_bloque(
                horario_atencion.hora_inicio, 
                horario_atencion.hora_fin
            ))
        
        return slots
    
    @classmethod
    def _crear_slots_bloque(cls, hora_inicio, hora_fin):
        """Crea slots de tiempo para un bloque específico"""
        slots = []
        hora_actual = datetime.combine(datetime.today(), hora_inicio)
        hora_limite = datetime.combine(datetime.today(), hora_fin)
        
        while hora_actual < hora_limite:
            slots.append(hora_actual.time())
            hora_actual += timedelta(minutes=cls.INTERVALOS_CITA)
        
        return slots
    
    @classmethod
    def obtener_citas_ocupadas(cls, fecha):
        """Obtiene las horas ocupadas para una fecha específica"""
        citas_ocupadas = CitaMedica.objects.filter(
            fecha=fecha
        ).values_list('hora_cita', flat=True)
        
        return list(citas_ocupadas)
    
    @classmethod
    def generar_calendario_mes(cls, year, month):
        """Genera calendario completo para un mes específico"""
        # Obtener días del mes
        primer_dia, dias_mes = monthrange(year, month)
        
        calendario_datos = {
            'year': year,
            'month': month,
            'dias': []
        }
        
        for dia in range(1, dias_mes + 1):
            fecha = datetime(year, month, dia).date()
            dia_semana = cls.obtener_nombre_dia_espanol(fecha)
            
            # Buscar horario de atención para este día
            try:
                horario = HorarioAtencion.objects.get(
                    dia_semana=dia_semana, 
                    activo=True
                )
                slots_disponibles = cls.generar_slots_horarios(horario)
                citas_ocupadas = cls.obtener_citas_ocupadas(fecha)
                
                # Calcular disponibilidad
                slots_libres = [
                    slot for slot in slots_disponibles 
                    if slot not in citas_ocupadas
                ]
                
                estado_dia = 'disponible' if slots_libres else 'ocupado'
                color = 'yellow' if slots_libres else 'red'
                
            except HorarioAtencion.DoesNotExist:
                # No hay atención este día
                slots_disponibles = []
                slots_libres = []
                estado_dia = 'sin_atencion'
                color = 'gray'
            
            calendario_datos['dias'].append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'dia': dia,
                'dia_semana': dia_semana,
                'estado': estado_dia,
                'color': color,
                'slots_totales': len(slots_disponibles) if slots_disponibles else 0,
                'slots_libres': len(slots_libres),
                'slots_ocupados': len(slots_disponibles) - len(slots_libres) if slots_disponibles else 0
            })
        
        return calendario_datos

# VIEWS
def generar_calendario_automatico(request):
    """Vista principal para generar calendario automáticamente"""
    try:
        # Obtener parámetros
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
        
        # Validar parámetros
        if month < 1 or month > 12:
            return JsonResponse({
                'error': 'Mes inválido. Debe ser entre 1 y 12.'
            }, status=400)
        
        # Generar calendario
        calendario = CalendarioMedicoService.generar_calendario_mes(year, month)
        
        return JsonResponse({
            'success': True,
            'calendario': calendario,
            'resumen': {
                'total_dias': len(calendario['dias']),
                'dias_disponibles': len([d for d in calendario['dias'] if d['estado'] == 'disponible']),
                'dias_ocupados': len([d for d in calendario['dias'] if d['estado'] == 'ocupado']),
                'dias_sin_atencion': len([d for d in calendario['dias'] if d['estado'] == 'sin_atencion'])
            }
        })
        
    except ValueError as e:
        return JsonResponse({
            'error': f'Parámetros inválidos: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error interno: {str(e)}'
        }, status=500)

def obtener_slots_dia_especifico(request):
    """Obtiene slots detallados para un día específico"""
    try:
        fecha_str = request.GET.get('fecha')
        if not fecha_str:
            return JsonResponse({'error': 'Fecha requerida'}, status=400)
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        dia_semana = CalendarioMedicoService.obtener_nombre_dia_espanol(fecha)
        
        try:
            horario = HorarioAtencion.objects.get(dia_semana=dia_semana, activo=True)
            slots_disponibles = CalendarioMedicoService.generar_slots_horarios(horario)
            citas_ocupadas = CalendarioMedicoService.obtener_citas_ocupadas(fecha)
            
            slots_detalle = []
            for slot in slots_disponibles:
                ocupado = slot in citas_ocupadas
                slots_detalle.append({
                    'hora': slot.strftime('%H:%M'),
                    'disponible': not ocupado,
                    'color': 'red' if ocupado else 'yellow',
                    'estado': 'ocupado' if ocupado else 'disponible'
                })
            
            return JsonResponse({
                'success': True,
                'fecha': fecha_str,
                'dia_semana': dia_semana,
                'horario_atencion': {
                    'inicio': horario.hora_inicio.strftime('%H:%M'),
                    'fin': horario.hora_fin.strftime('%H:%M'),
                    'intervalo_desde': horario.intervalo_desde.strftime('%H:%M') if horario.intervalo_desde else None,
                    'intervalo_hasta': horario.intervalo_hasta.strftime('%H:%M') if horario.intervalo_hasta else None,
                },
                'slots': slots_detalle
            })
            
        except HorarioAtencion.DoesNotExist:
            return JsonResponse({
                'success': True,
                'fecha': fecha_str,
                'dia_semana': dia_semana,
                'mensaje': 'No hay atención médica este día',
                'slots': []
            })
            
    except ValueError:
        return JsonResponse({
            'error': 'Formato de fecha inválido. Use YYYY-MM-DD'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error interno: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def agendar_cita_automatica(request):
    """Agenda una cita automáticamente verificando disponibilidad"""
    try:
        data = json.loads(request.body)
        
        # Validar datos requeridos
        campos_requeridos = ['paciente_id', 'fecha', 'hora_cita', 'estado']
        for campo in campos_requeridos:
            if campo not in data:
                return JsonResponse({
                    'error': f'Campo requerido: {campo}'
                }, status=400)
        
        fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        hora_cita = datetime.strptime(data['hora_cita'], '%H:%M').time()
        
        # Verificar si ya existe una cita en esa fecha/hora
        if CitaMedica.objects.filter(fecha=fecha, hora_cita=hora_cita).exists():
            return JsonResponse({
                'error': 'Ya existe una cita agendada para esa fecha y hora',
                'disponible': False,
                'color': 'red'
            }, status=400)
        
        # Verificar que esté dentro del horario de atención
        dia_semana = CalendarioMedicoService.obtener_nombre_dia_espanol(fecha)
        try:
            horario = HorarioAtencion.objects.get(dia_semana=dia_semana, activo=True)
            slots_disponibles = CalendarioMedicoService.generar_slots_horarios(horario)
            
            if hora_cita not in slots_disponibles:
                return JsonResponse({
                    'error': 'La hora solicitada no está dentro del horario de atención',
                    'horario_disponible': [slot.strftime('%H:%M') for slot in slots_disponibles]
                }, status=400)
                
        except HorarioAtencion.DoesNotExist:
            return JsonResponse({
                'error': 'No hay atención médica en este día de la semana'
            }, status=400)
        
        # Crear la cita
        nueva_cita = CitaMedica.objects.create(
            paciente_id=data['paciente_id'],
            fecha=fecha,
            hora_cita=hora_cita,
            estado=data['estado'],
            observaciones=data.get('observaciones', '')
        )
        
        return JsonResponse({
            'success': True,
            'cita_id': nueva_cita.id,
            'mensaje': 'Cita agendada exitosamente',
            'detalles': {
                'fecha': nueva_cita.fecha.strftime('%Y-%m-%d'),
                'hora': nueva_cita.hora_cita.strftime('%H:%M'),
                'estado': nueva_cita.estado,
                'paciente': str(nueva_cita.paciente)
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'JSON inválido'
        }, status=400)
    except ValueError as e:
        return JsonResponse({
            'error': f'Error en formato de datos: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error interno: {str(e)}'
        }, status=500)

def calendario_dashboard(request):
    """Vista para renderizar el dashboard del calendario"""
    return render(request, 'doctor/cita_medica/calendario_dashboard.html')

