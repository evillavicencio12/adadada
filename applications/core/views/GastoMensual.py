# aplicacion/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum , Count , F
from django.views.generic import ListView
from django.utils import timezone
from applications.core.models import TipoGasto, GastoMensual
from applications.core.forms.forms import TipoGastoForm, GastoMensualForm

# ==============================================
# VISTAS PARA TIPO DE GASTO
# ==============================================

def listar_tipos_gasto(request):
    """
    Lista todos los tipos de gasto, incluyendo los inactivos
    """
    tipos = TipoGasto.objects.all().order_by('nombre')
    context = {
        'tipos_gasto': tipos,
        'titulo': 'Listado de Tipos de Gasto'
    }
    return render(request, 'clinica/detalle_pago/gastos.html', context)

def crear_tipo_gasto(request):
    """
    Crea un nuevo tipo de gasto
    """
    if request.method == 'POST':
        form = TipoGastoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de gasto creado exitosamente.')
            return redirect('listar_tipos_gasto')
    else:
        form = TipoGastoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Tipo de Gasto',
        'boton_texto': 'Crear'
    }
    return render(request, 'clinica/detalle_pago/gastos.html', context)
def editar_tipo_gasto(request, id):
    """
    Edita un tipo de gasto existente
    """
    tipo_gasto = get_object_or_404(TipoGasto, pk=id)
    
    if request.method == 'POST':
        form = TipoGastoForm(request.POST, instance=tipo_gasto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de gasto actualizado exitosamente.')
            return redirect('core:listar_tipos_gasto')
    else:
        form = TipoGastoForm(instance=tipo_gasto)  # <- Solo se ejecuta en GET
    
    context = {
        'form': form,
        'titulo': f'Editar Tipo de Gasto: {tipo_gasto.nombre}',
        'boton_texto': 'Actualizar'
    }
    return render(request, 'clinica/detalle_pago/gastos.html', context)

def cambiar_estado_tipo_gasto(request, id):
    """
    Activa/Desactiva un tipo de gasto
    """
    tipo_gasto = get_object_or_404(TipoGasto, pk=id)
    tipo_gasto.activo = not tipo_gasto.activo
    tipo_gasto.save()
    
    estado = "activado" if tipo_gasto.activo else "desactivado"
    messages.success(request, f'Tipo de gasto {estado} exitosamente.')
    return redirect('core:listar_tipos_gasto')  # Cambiado aquíS
# ==============================================
# VISTAS PARA GASTO MENSUAL
# ==============================================

class ListarGastosMensuales(ListView):
    model = GastoMensual
    template_name =   'clinica/detalle_pago/gastos.html'
    context_object_name = 'gastos'
    ordering = ['-fecha']
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        tipo_gasto = self.request.GET.get('tipo_gasto')
        mes = self.request.GET.get('mes')
        anio = self.request.GET.get('anio')
        
        if tipo_gasto:
            queryset = queryset.filter(tipo_gasto__id=tipo_gasto)
        if mes:
            queryset = queryset.filter(fecha__month=mes)
        if anio:
            queryset = queryset.filter(fecha__year=anio)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Totales
        queryset = self.get_queryset()
        total_gastos = queryset.aggregate(total=Sum('valor'))['total'] or 0
        
        # Filtros disponibles
        context['total_gastos'] = total_gastos
        context['tipos_gasto'] = TipoGasto.objects.filter(activo=True)
        context['titulo'] = 'Registro de Gastos Mensuales'
        context['mes_actual'] = timezone.now().month
        context['anio_actual'] = timezone.now().year
        
        return context

def crear_gasto_mensual(request):
    """
    Crea un nuevo gasto mensual
    """
    if request.method == 'POST':
        form = GastoMensualForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto mensual registrado exitosamente.')
            return redirect('listar_gastos_mensuales')
    else:
        form = GastoMensualForm(initial={'fecha': timezone.now()})
    
    context = {
        'form': form,
        'titulo': 'Registrar Nuevo Gasto Mensual',
        'boton_texto': 'Registrar'
    }
    return render(request, 'clinica/detalle_pago/gastos.html', context)
def editar_gasto_mensual(request, id):
    """
    Edita un gasto mensual existente
    """
    gasto = get_object_or_404(GastoMensual, pk=id)
    
    if request.method == 'POST':
        form = GastoMensualForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto mensual actualizado exitosamente.')
            return redirect('listar_gastos_mensuales')
    else:
        form = GastoMensualForm(instance=gasto)
    
    context = {
        'form': form,
        'titulo': f'Editar Gasto Mensual: {gasto.tipo_gasto.nombre}',
        'boton_texto': 'Actualizar'
    }
    return render(request, 'clinica/detalle_pago/gastos.html', context)
def eliminar_gasto_mensual(request, id):
    """
    Elimina un gasto mensual
    """
    gasto = get_object_or_404(GastoMensual, pk=id)
    
    if request.method == 'POST':
        gasto.delete()
        messages.success(request, 'Gasto mensual eliminado exitosamente.')
        return redirect('listar_gastos_mensuales')
    
    context = {
        'gasto': gasto,
        'titulo': 'Confirmar Eliminación',
        'mensaje': f'¿Está seguro que desea eliminar el gasto de {gasto.tipo_gasto.nombre} por ${gasto.valor}?'
    }
    return render(request, 'clinica/detalle_pago/gastos.html', context)
# ==============================================
# REPORTES
# ==============================================

def reporte_gastos_por_tipo(request):
    """
    Muestra un reporte de gastos agrupados por tipo
    """
    # Obtener parámetros de filtro
    mes = request.GET.get('mes', timezone.now().month)
    anio = request.GET.get('anio', timezone.now().year)
    
    # Filtrar gastos
    gastos = GastoMensual.objects.filter(
        fecha__year=anio,
        fecha__month=mes
    )
    
    # Agrupar por tipo de gasto y calcular totales
    gastos_por_tipo = gastos.values('tipo_gasto__nombre').annotate(
        total=Sum('valor'),
        cantidad=Count('id')
    ).order_by('-total')
    
    # Total general
    total_general = gastos.aggregate(total=Sum('valor'))['total'] or 0

    # Calcular porcentaje para cada tipo de gasto
    for gasto in gastos_por_tipo:
        gasto['porcentaje'] = (gasto['total'] / total_general * 100) if total_general != 0 else 0  # Evitar división por cero
    
    context = {
        'gastos_por_tipo': gastos_por_tipo,
        'total_general': total_general,
        'mes': mes,
        'anio': anio,
        'titulo': f'Reporte de Gastos por Tipo - {mes}/{anio}',
        'meses': [(i, timezone.datetime(1900, i, 1).strftime('%B')) for i in range(1, 13)],
        'anios': range(timezone.now().year - 5, timezone.now().year + 1)
    }
    return render(request, 'clinica/detalle_pago/gastos.html', context)

