from django.urls import path
from applications.core import views
from .views.historialclinico import HistorialClinicoCreateView, HistorialClinicoDeleteView, HistorialClinicoDetailView, HistorialClinicoListView, HistorialClinicoUpdateView
from applications.core.views.paciente import paciente_find, paciente_search_view
from applications.core.views.medicamento import ajax_create_medicamento, ajax_search_medicamento
# Se eliminan imports de GastoMensual que ya no se usan directamente aquí
# from applications.core.views.GastoMensual import listar_tipos_gasto , crear_tipo_gasto , editar_tipo_gasto , cambiar_estado_tipo_gasto , reporte_gastos_por_tipo , ListarGastosMensuales , crear_gasto_mensual
from applications.core.views import TipoGasto as TipoGastoViews
from applications.core.views import GastoMensual as GastoMensualViews


app_name = 'core'

urlpatterns = [
    # Rutas existentes para Pacientes, Doctores, Especialidades, HistorialClinico...
    path('paciente_find/', views.paciente_find, name='paciente_find'),
    path('pacientes/search/', views.paciente_search_view, name='paciente_search'),

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
    
    # Rutas para TipoGasto
    path('tipos-gasto/', TipoGastoViews.TipoGastoListView.as_view(), name='tipogasto_list'),
    path('tipos-gasto/crear/', TipoGastoViews.TipoGastoCreateView.as_view(), name='tipogasto_create'),
    path('tipos-gasto/editar/<int:pk>/', TipoGastoViews.TipoGastoUpdateView.as_view(), name='tipogasto_update'),
    path('tipos-gasto/eliminar/<int:pk>/', TipoGastoViews.TipoGastoDeleteView.as_view(), name='tipogasto_delete'),

    # Rutas para GastoMensual
    path('gastos-mensuales/', GastoMensualViews.GastoMensualListView.as_view(), name='gastomensual_list'),
    path('gastos-mensuales/crear/', GastoMensualViews.GastoMensualCreateView.as_view(), name='gastomensual_create'),
    path('gastos-mensuales/editar/<int:pk>/', GastoMensualViews.GastoMensualUpdateView.as_view(), name='gastomensual_update'),
    path('gastos-mensuales/eliminar/<int:pk>/', GastoMensualViews.GastoMensualDeleteView.as_view(), name='gastomensual_delete'),
]



