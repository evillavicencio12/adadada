from .paciente import (
        paciente_find, paciente_search_view
)
from .doctores import DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView
from .especialidades import EspecialidadListView, EspecialidadCreateView, EspecialidadUpdateView, EspecialidadDeleteView
from .historialclinico import HistorialClinicoListView, HistorialClinicoCreateView, HistorialClinicoUpdateView, HistorialClinicoDeleteView
from .diagnostico import (
    DiagnosticoListView, DiagnosticoCreateView, DiagnosticoUpdateView, DiagnosticoDeleteView
)
from .medicamento import (
    MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView,
    MarcaMedicamentoListView, MarcaMedicamentoCreateView, MarcaMedicamentoUpdateView, MarcaMedicamentoDeleteView,
    TipoMedicamentoListView, TipoMedicamentoCreateView, TipoMedicamentoUpdateView, TipoMedicamentoDeleteView
)
from .TipoGasto import (
    TipoGastoListView, TipoGastoCreateView, TipoGastoUpdateView, TipoGastoDeleteView
)
from .GastoMensual import (
    GastoMensualListView, GastoMensualCreateView, GastoMensualUpdateView, GastoMensualDeleteView
)
from .tiposangre_views import (
    TipoSangreListView, TipoSangreCreateView, TipoSangreUpdateView, TipoSangreDeleteView
)
from .cargo_views import (
    CargoListView, CargoCreateView, CargoUpdateView, CargoDeleteView
)
