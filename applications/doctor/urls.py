from django.urls import path
from applications.doctor import views

app_name = 'doctor'

urlpatterns = [
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
]