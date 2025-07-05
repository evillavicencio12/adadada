from django.urls import path
from applications.doctor import views # Esto ya importa las vistas de atencion_medica y servicios_adicionales
from applications.doctor.views import patient as patient_views
from applications.doctor.views import calendario as calendario_views # Importar vistas de calendario
from applications.doctor.views.cita_medica import (
    cita_medica_list,
    cita_medica_create,
    cita_medica_detail,
    cita_medica_update,
    cita_medica_delete,
    cita_medica_change_estado,
    citas_hoy,
    citas_por_fecha
)
from applications.doctor.views.pago import PagoCreateView, PagoDeleteView, PagoDetailView, PagoListView, PagoUpdateView
app_name = 'doctor'
from applications.doctor.views.detalle_pago import DetallePagoCreateView, DetallePagoDeleteView, DetallePagoListView

urlpatterns = [
    # Rutas para Patient
    path('patients/', patient_views.PatientListView.as_view(), name='patient_list'),
    path('patients/crear/', patient_views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/editar/<int:pk>/', patient_views.PatientUpdateView.as_view(), name='patient_update'),
    path('patients/eliminar/<int:pk>/', patient_views.PatientDeleteView.as_view(), name='patient_delete'),
    # Rutas AJAX para Patient (usadas en el formulario de Atencion)
    path('ajax/patient/crear/', patient_views.ajax_create_patient, name='ajax_create_patient'),
    path('ajax/patient/buscar/dni/', patient_views.ajax_search_patient_dni, name='ajax_search_patient_dni'),
    path('ajax/patient/search_by_name/', patient_views.ajax_search_patient_by_name, name='ajax_search_patient_by_name'),

    # Rutas para Atencion y DetalleAtencion (manejadas juntas)
    path('atenciones/', views.AtencionListView.as_view(), name='atencion_list'),
    path('atenciones/crear/', views.AtencionCreateView.as_view(), name='atencion_create'),
    path('atenciones/editar/<int:pk>/', views.AtencionUpdateView.as_view(), name='atencion_update'),
    path('atenciones/eliminar/<int:pk>/', views.AtencionDeleteView.as_view(), name='atencion_delete'),

    # Rutas AJAX para Atencion
    path('ajax/buscar-paciente/', views.buscar_paciente_ajax, name='ajax_buscar_paciente'),
    path('ajax/buscar-medicamento/', views.buscar_medicamento_ajax, name='ajax_buscar_medicamento'),
    path('ajax/previsualizar-atencion/', views.previsualizar_atencion_ajax, name='ajax_previsualizar_atencion'),
    path('ajax/crear-medicamento/', views.crear_medicamento_ajax, name='ajax_crear_medicamento'),

    # Rutas para ServiciosAdicionales
    path('servicios-adicionales/', views.ServiciosAdicionalesListView.as_view(), name='servicio_adicional_list'),
    path('servicios-adicionales/crear/', views.ServiciosAdicionalesCreateView.as_view(), name='servicio_adicional_create'),
    path('servicios-adicionales/editar/<int:pk>/', views.ServiciosAdicionalesUpdateView.as_view(), name='servicio_adicional_update'),
    path('servicios-adicionales/eliminar/<int:pk>/', views.ServiciosAdicionalesDeleteView.as_view(), name='servicio_adicional_delete'),
    
    
    # Rutas para citas médicas
    path('citas/', cita_medica_list, name='cita_medica_list'),
    path('citas/crear/', cita_medica_create, name='cita_medica_create'), # Usada para crear desde fuera del calendario
    path('citas/<int:pk>/', cita_medica_detail, name='cita_medica_detail'),
    path('citas/<int:pk>/editar/', cita_medica_update, name='cita_medica_update'),
    path('citas/<int:pk>/eliminar/', cita_medica_delete, name='cita_medica_delete'),
    
    # URLs adicionales para citas
    path('citas/<int:pk>/cambiar-estado/', cita_medica_change_estado, name='cita_medica_change_estado'),
    path('citas/hoy/', citas_hoy, name='citas_hoy'),
    path('citas/fecha/<str:fecha>/', citas_por_fecha, name='citas_por_fecha'),

    # URLs para el Calendario Automático y gestión de citas desde el calendario
    path('calendario/', calendario_views.calendario_dashboard, name='calendario_dashboard'),
    path('calendario/api/generar-mes/', calendario_views.generar_calendario_automatico, name='calendario_api_generar_mes'),
    path('calendario/api/slots-dia/', calendario_views.obtener_slots_dia_especifico, name='calendario_api_slots_dia'),
    path('calendario/api/agendar-cita/', calendario_views.agendar_cita_automatica, name='calendario_api_agendar_cita'),
    # La URL para crear citas desde el calendario (`cita_medica_create` con parámetros GET o `agendar_cita_automatica` POST)
    # ya está cubierta. Si se va a usar `cita_medica_create` desde el calendario, se puede llamar con ?fecha=YYYY-MM-DD&hora=HH:MM
    # Si se usa `agendar_cita_automatica`, es una API POST.
    
    path('pago/', PagoListView.as_view(), name='pago_list'),
    path('pago/create/', PagoCreateView.as_view(), name='pago_create'),
    path('pago/<int:pk>/', PagoDetailView.as_view(), name='pago_detail'),
    path('pago/<int:pk>/edit/', PagoUpdateView.as_view(), name='pago_update'),
    path('pago/<int:pk>/delete/', PagoDeleteView.as_view(), name='pago_delete'),
    
    path('detalle_pago/', DetallePagoListView.as_view(), name='detalle_pago_list'),
    path('detalle_pago/nuevo/', DetallePagoCreateView.as_view(), name='detalle_pago_create'),
    path('detalle_pago/<int:pk>/eliminar/', DetallePagoDeleteView.as_view(), name='detalle_pago_delete'),
]