from django.urls import path
from applications.core import views
from .views.historialclinico import HistorialClinicoCreateView, HistorialClinicoDeleteView, HistorialClinicoDetailView, HistorialClinicoListView, HistorialClinicoUpdateView
from applications.core.views.paciente import paciente_find, paciente_search_view
from applications.core.views.medicamento import ajax_create_medicamento, ajax_search_medicamento
from applications.core.views.GastoMensual import listar_tipos_gasto , crear_tipo_gasto , editar_tipo_gasto , cambiar_estado_tipo_gasto , reporte_gastos_por_tipo , ListarGastosMensuales , crear_gasto_mensual 
app_name = 'core'

urlpatterns = [
    # Rutas existentes para Pacientes, Doctores, Especialidades, HistorialClinico...
    path('paciente_find/', views.paciente_find, name='paciente_find'),
    path('pacientes/search/', views.paciente_search_view, name='paciente_search'),
    # path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    # path('pacientes/crear/', views.PacienteCreateView.as_view(), name='paciente_create'),
    # path('pacientes/editar/<int:pk>/', views.PacienteUpdateView.as_view(), name='paciente_update'),
    # path('pacientes/eliminar/<int:pk>/', views.PacienteDeleteView.as_view(), name='paciente_delete'),
    # path('ajax/buscar-paciente-dni/', views.buscar_paciente_dni_ajax, name='ajax_buscar_paciente_dni'),
    # path('ajax/buscar-paciente-id/', views.buscar_paciente_id_ajax, name='ajax_buscar_paciente_id'),


    path('historialclinico/', HistorialClinicoListView.as_view(), name='historialclinico_list'),
    path('historialclinico/create/', HistorialClinicoCreateView.as_view(), name='historialclinico_create'),
    path('historialclinico/<int:pk>/update/', HistorialClinicoUpdateView.as_view(), name='historialclinico_update'),
    path('historialclinico/<int:pk>/delete/', HistorialClinicoDeleteView.as_view(), name='historialclinico_delete'),
    path('historialclinico/<int:pk>/', HistorialClinicoDetailView.as_view(), name='historialclinico_detail'),

    path('doctores/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctores/nuevo/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('doctores/editar/<int:pk>/', views.DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctores/eliminar/<int:pk>/', views.DoctorDeleteView.as_view(), name='doctor_delete'),

    path('especialidades/', views.EspecialidadListView.as_view(), name='especialidad_list'),
    path('especialidades/nueva/', views.EspecialidadCreateView.as_view(), name='especialidad_create'),
    path('especialidades/editar/<int:pk>/', views.EspecialidadUpdateView.as_view(), name='especialidad_update'),
    path('especialidades/eliminar/<int:pk>/', views.EspecialidadDeleteView.as_view(), name='especialidad_delete'),

    # Nuevas rutas para Diagnostico
    path('diagnosticos/', views.DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('diagnosticos/crear/', views.DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('diagnosticos/editar/<int:pk>/', views.DiagnosticoUpdateView.as_view(), name='diagnostico_update'),
    path('diagnosticos/eliminar/<int:pk>/', views.DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),

    # Nuevas rutas para Medicamento
    path('medicamentos/', views.MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamentos/crear/', views.MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamentos/editar/<int:pk>/', views.MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('medicamentos/eliminar/<int:pk>/', views.MedicamentoDeleteView.as_view(), name='medicamento_delete'),
    path('ajax/medicamento/crear/', ajax_create_medicamento, name='ajax_create_medicamento'),
    path('ajax/medicamento/buscar/', ajax_search_medicamento, name='ajax_search_medicamento'),

    # Nuevas rutas para MarcaMedicamento
    path('marcas-medicamentos/', views.MarcaMedicamentoListView.as_view(), name='marcamedicamento_list'),
    path('marcas-medicamentos/crear/', views.MarcaMedicamentoCreateView.as_view(), name='marcamedicamento_create'),
    path('marcas-medicamentos/editar/<int:pk>/', views.MarcaMedicamentoUpdateView.as_view(), name='marcamedicamento_update'),
    path('marcas-medicamentos/eliminar/<int:pk>/', views.MarcaMedicamentoDeleteView.as_view(), name='marcamedicamento_delete'),

    # Nuevas rutas para TipoMedicamento
    path('tipos-medicamentos/', views.TipoMedicamentoListView.as_view(), name='tipomedicamento_list'),
    path('tipos-medicamentos/crear/', views.TipoMedicamentoCreateView.as_view(), name='tipomedicamento_create'),
    path('tipos-medicamentos/editar/<int:pk>/', views.TipoMedicamentoUpdateView.as_view(), name='tipomedicamento_update'),
    path('tipos-medicamentos/eliminar/<int:pk>/', views.TipoMedicamentoDeleteView.as_view(), name='tipomedicamento_delete'),
    
    path('gastos/', ListarGastosMensuales.as_view(), name='listar_gastos_mensuales'),
    path('gastos/crear/', crear_gasto_mensual, name='crear_gasto_mensual'),
    path('gastos/tipos/', listar_tipos_gasto, name='listar_tipos_gasto'),
    path('gastos/tipos/crear/', crear_tipo_gasto, name='crear_tipo_gasto'),
    path('gastos/tipos/<int:id>/editar/', editar_tipo_gasto, name='editar_tipo_gasto'),
    path('gastos/tipos/<int:id>/cambiar_estado/', cambiar_estado_tipo_gasto, name='cambiar_estado_tipo_gasto'),
    path('gastos/reportes/', reporte_gastos_por_tipo, name='reporte_gastos_por_tipo'),
]



