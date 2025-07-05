from .atencion_medica import (
    AtencionListView, AtencionCreateView, AtencionUpdateView, AtencionDeleteView,
    buscar_paciente_ajax, buscar_medicamento_ajax,
    previsualizar_atencion_ajax, crear_medicamento_ajax
)
from .servicios_adicionales import (
    ServiciosAdicionalesListView, ServiciosAdicionalesCreateView,
    ServiciosAdicionalesUpdateView, ServiciosAdicionalesDeleteView
)
from .patient import (
    PatientListView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
    ajax_create_patient,
    ajax_search_patient_dni,
)