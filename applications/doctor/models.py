from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from django.db import models
from applications.doctor.utils.cita_medica import EstadoCitaChoices
from applications.doctor.utils.doctor import DiaSemanaChoices
from applications.doctor.utils.pago import MetodoPagoChoices, EstadoPagoChoices


# Campos comunes de auditoría
class AuditModel(models.Model):
    user_creation = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='%(app_label)s_%(class)s_creations',
        verbose_name="Creado por"
    )
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Fecha de Creación")
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='%(app_label)s_%(class)s_updates',
        verbose_name="Actualizado por"
    )
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Fecha de Actualización")

    class Meta:
        abstract = True

class HorarioAtencion(AuditModel):
    dia_semana = models.CharField(
        max_length=10,
        choices=DiaSemanaChoices.choices,
        verbose_name="Día de la Semana"
    )
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    intervalo_desde = models.TimeField(verbose_name="Intervalo desde", null=True, blank=True)
    intervalo_hasta = models.TimeField(verbose_name="Intervalo hasta", null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.get_dia_semana_display()} ({self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')})"

    class Meta:
        verbose_name = "Horario de Atención"
        verbose_name_plural = "Horarios de Atención"
        unique_together = ('dia_semana', 'hora_inicio', 'hora_fin')

class CitaMedica(AuditModel):
    paciente = models.ForeignKey('Patient', on_delete=models.CASCADE, verbose_name="Paciente", related_name="citas_doctor_app") # related_name ajustado
    fecha = models.DateField(verbose_name="Fecha de la Cita")
    hora_cita = models.TimeField(verbose_name="Hora de la Cita")
    estado = models.CharField(
        max_length=20, # Ajustado por si los choices son más largos
        choices=EstadoCitaChoices.choices,
        default=EstadoCitaChoices.PENDIENTE,
        verbose_name="Estado de la Cita"
    )
    observaciones = models.TextField(verbose_name="Observaciones", blank=True, null=True)

    def __str__(self):
        paciente_nombre = "Paciente Desconocido"
        if self.paciente:
            # Intenta obtener un nombre completo, si no, usa el ID.
            primer_nombre = getattr(self.paciente, 'primer_nombre', '')
            apellido = getattr(self.paciente, 'apellido', '')
            if primer_nombre or apellido:
                paciente_nombre = f"{primer_nombre} {apellido}".strip()
            else:
                paciente_nombre = f"ID: {self.paciente.id}"
        return f"{paciente_nombre} - {self.fecha.strftime('%d/%m/%Y')} {self.hora_cita.strftime('%H:%M')}"


    class Meta:
        ordering = ['fecha', 'hora_cita']
        indexes = [
            models.Index(fields=['fecha', 'hora_cita'], name='idx_fecha_hora_cita_doctor'), # Nombre de índice específico
        ]
        verbose_name = "Cita Médica"
        verbose_name_plural = "Citas Médicas"
        unique_together = ('fecha', 'hora_cita')

class Atencion(AuditModel):
    paciente = models.ForeignKey(
        'Patient',
        on_delete=models.PROTECT,
        verbose_name="Paciente",
        related_name="atenciones_doctor_app",
        help_text="Paciente que recibe esta atención médica (modelo doctor.Patient)."
    )
    # fecha_atencion se maneja con date_creation de AuditModel si es creación, o un campo específico si es diferente
    # Si fecha_atencion es la fecha REAL de la atención y no de registro, se mantiene
    fecha_atencion_real = models.DateTimeField(
        default=timezone.now, # Opcional, para que se pueda editar si es necesario
        verbose_name="Fecha y Hora de la Atención",
        help_text="Fecha y hora real en que se realizó la atención."
    )
    presion_arterial = models.CharField(max_length=20, null=True, blank=True, verbose_name="Presión Arterial", help_text="Ejemplo: 120/80 mmHg.")
    pulso = models.PositiveIntegerField(null=True, blank=True, verbose_name="Pulso (ppm)", help_text="Pulsaciones por minuto.")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura (°C)", help_text="Temperatura corporal en grados Celsius.")
    frecuencia_respiratoria = models.PositiveIntegerField(null=True, blank=True, verbose_name="Frecuencia Respiratoria (rpm)", help_text="Respiraciones por minuto.")
    saturacion_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Saturación de Oxígeno (%)", help_text="Porcentaje de oxígeno en sangre.")
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)", help_text="Peso del paciente en kilogramos.")
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Altura (m)", help_text="Altura del paciente en metros.")
    motivo_consulta = models.TextField(verbose_name="Motivo de Consulta", help_text="Razón principal por la que el paciente acude a consulta.")
    sintomas = models.TextField(verbose_name="Síntomas", help_text="Síntomas que presenta el paciente.")
    tratamiento = models.TextField(verbose_name="Plan de Tratamiento", help_text="Indicaciones o receta entregada al paciente.")
    diagnostico = models.ManyToManyField('core.Diagnostico', verbose_name="Diagnósticos", related_name="atenciones_doctor_app", help_text="Diagnósticos clínicos asociados a esta atención.")
    examen_fisico = models.TextField(null=True, blank=True, verbose_name="Examen Físico", help_text="Descripción de hallazgos del examen físico.")
    examenes_enviados = models.TextField(null=True, blank=True, verbose_name="Exámenes Solicitados", help_text="Exámenes que se han solicitado al paciente.")
    comentario_adicional = models.TextField(null=True, blank=True, verbose_name="Comentario Adicional", help_text="Observaciones adicionales del profesional de salud.")
    es_control = models.BooleanField(default=False, verbose_name="¿Es consulta de control?", help_text="Marca si esta atención es parte de un seguimiento.")

    class Meta:
        ordering = ['-fecha_atencion_real', '-date_creation'] # Priorizar fecha real de atención
        verbose_name = "Atención Médica"
        verbose_name_plural = "Atenciones Médicas"

    def __str__(self):
        return f"Atención de {self.paciente} el {self.fecha_atencion_real.strftime('%Y-%m-%d %H:%M')}"

    @property
    def calcular_imc(self):
        if self.peso and self.altura and self.altura > 0:
            return round(float(self.peso) / (float(self.altura) ** 2), 2)
        return None

    @property
    def get_diagnosticos(self):
        return " - ".join([d.descripcion for d in self.diagnostico.all().order_by('descripcion')])

class DetalleAtencion(AuditModel):
    atencion = models.ForeignKey(Atencion, on_delete=models.CASCADE, verbose_name="Atención Médica", related_name="detalles_doctor_app", help_text="Atención médica asociada a este detalle.")
    medicamento = models.ForeignKey('core.Medicamento', on_delete=models.PROTECT, verbose_name="Medicamento", related_name="prescripciones_doctor_app", help_text="Medicamento recetado al paciente.")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad", help_text="Unidades del medicamento recetadas.")
    prescripcion = models.TextField(verbose_name="Prescripción", help_text="Instrucciones para tomar el medicamento.")
    duracion_tratamiento = models.PositiveIntegerField(verbose_name="Duración del Tratamiento (días)", null=True, blank=True, help_text="Cantidad de días de tratamiento estimado.")
    frecuencia_diaria = models.PositiveIntegerField(verbose_name="Frecuencia Diaria (veces por día)", null=True, blank=True, help_text="Cuántas veces al día debe tomar el medicamento.")

    class Meta:
        ordering = ['atencion']
        verbose_name = "Detalle de Atención"
        verbose_name_plural = "Detalles de Atención"

    def __str__(self):
        return f"{self.medicamento} para {self.atencion.paciente}"

class ServiciosAdicionales(AuditModel):
    nombre_servicio = models.CharField(max_length=255, verbose_name="Nombre del Servicio", help_text="Ejemplo: Radiografía, Laboratorio clínico, Procedimiento menor.")
    costo_servicio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del Servicio", help_text="Costo unitario del servicio en dólares. Ejemplo: 25.00")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción del Servicio", help_text="Descripción opcional del servicio. Ejemplo: Examen de sangre de rutina.")
    activo = models.BooleanField(default=True, verbose_name="Activo", help_text="Marca si el servicio adicional está disponible para agendar o prescribir.")

    class Meta:
        ordering = ['nombre_servicio']
        verbose_name = "Servicio Adicional"
        verbose_name_plural = "Servicios Adicionales"

    def __str__(self):
        return self.nombre_servicio

class Pago(AuditModel):
    atencion = models.ForeignKey(Atencion, on_delete=models.PROTECT, verbose_name="Atención", related_name="pagos_doctor_app", null=True, blank=True)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPagoChoices.choices, verbose_name="Método de Pago")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total")
    estado = models.CharField(max_length=20, choices=EstadoPagoChoices.choices, default=EstadoPagoChoices.PENDIENTE, verbose_name="Estado")
    fecha_pago = models.DateTimeField(verbose_name="Fecha de Pago", null=True, blank=True)
    # fecha_creacion es date_creation de AuditModel
    nombre_pagador = models.CharField(max_length=100, verbose_name="Nombre del Pagador", blank=True, null=True)
    referencia_externa = models.CharField(max_length=100, verbose_name="Referencia Externa", blank=True, null=True, help_text="ID de transacción PayPal, etc.")
    evidencia_pago = models.ImageField(upload_to='doctor/evidencia_pagos/', verbose_name="Evidencia de Pago", blank=True, null=True, help_text="Captura de pantalla o comprobante del pago")
    observaciones = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    activo = models.BooleanField(default=True, verbose_name="Activo") # Este 'activo' es del pago en sí, no de la entidad auditada.

    def __str__(self):
        return f"Pago {self.id} - {self.atencion} - {self.monto_total}"

    def save(self, *args, **kwargs):
        if self.estado == EstadoPagoChoices.PAGADO and not self.fecha_pago: # Usar el enum
            self.fecha_pago = timezone.now()
        # self.clean() # clean no está definido en este modelo. Si es necesario, debe implementarse.
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

class DetallePago(AuditModel):
    pago = models.ForeignKey('Pago', on_delete=models.CASCADE, verbose_name="Pago", related_name="detalles_doctor_app", help_text="Pago al que corresponde este detalle de cobro.")
    servicio_adicional = models.ForeignKey('ServiciosAdicionales', on_delete=models.PROTECT, verbose_name="Servicio", related_name="detalles_pago_doctor_app", help_text="Servicio adicional cobrado (ej. Radiografía, Laboratorio).")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad", help_text="Cantidad del servicio facturado (ej. 1 examen, 2 procedimientos, etc.).")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario", help_text="Precio normal por unidad del servicio, sin considerar seguros.")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal", editable=False, help_text="Subtotal calculado automáticamente, considerando seguro y descuento.")
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Descuento %", help_text="Descuento aplicado sobre el precio base. Ejemplo: 10 para 10%.")
    aplica_seguro = models.BooleanField(default=False, verbose_name="Aplica Seguro", help_text="Marca si el servicio tiene cobertura por seguro médico.")
    valor_seguro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Cubierto por Seguro", help_text="Valor real cubierto por el seguro. Se usará en lugar del precio normal si se aplica seguro.")
    descripcion_seguro = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descripción del Seguro", help_text="Nombre del seguro utilizado. Ejemplo: Saludsa Nivel 2.")

    def save(self, *args, **kwargs):
        precio_base = self.valor_seguro if self.aplica_seguro and self.valor_seguro is not None else self.precio_unitario
        descuento = (self.descuento_porcentaje / Decimal(100)) * precio_base
        precio_con_descuento = precio_base - descuento
        self.subtotal = round(precio_con_descuento * self.cantidad, 2)
        super().save(*args, **kwargs)
        self.actualizar_total_pago_padre()


    def __str__(self):
        return f"{self.servicio_adicional} - Cantidad: {self.cantidad} - Subtotal: {self.subtotal}"

    def actualizar_total_pago_padre(self): # Renombrado para claridad
        if self.pago_id: # Asegurarse que el pago existe
            try:
                pago_obj = Pago.objects.get(id=self.pago_id) # Obtener la instancia del pago
                total = DetallePago.objects.filter(pago=pago_obj).aggregate(
                    total_calculado=models.Sum('subtotal')
                )['total_calculado'] or Decimal('0.00')

                if pago_obj.monto_total != total:
                    pago_obj.monto_total = total
                    pago_obj.save(update_fields=['monto_total', 'date_updated', 'user_updated']) # Especificar campos para evitar recursión y actualizar user_updated
            except Pago.DoesNotExist:
                # Manejar el caso donde el pago no existe, aunque es improbable si self.pago_id está seteado.
                pass # O loggear un error

    def delete(self, *args, **kwargs):
        pago_afectado_id = self.pago_id
        super().delete(*args, **kwargs)
        if pago_afectado_id:
            try:
                pago_obj = Pago.objects.get(id=pago_afectado_id)
                total = DetallePago.objects.filter(pago=pago_obj).aggregate(
                    total_calculado=models.Sum('subtotal')
                )['total_calculado'] or Decimal('0.00')

                if pago_obj.monto_total != total:
                    pago_obj.monto_total = total
                    # Quién es user_updated aquí? Si es parte de un request, debería pasarse.
                    # Por ahora, se actualizará solo el monto y date_updated.
                    pago_obj.save(update_fields=['monto_total', 'date_updated'])
            except Pago.DoesNotExist:
                pass


    class Meta:
        verbose_name = "Detalle de Pago"
        verbose_name_plural = "Detalles de Pagos"
        
class Patient (AuditModel): # Hereda de AuditModel
    primer_nombre= models.CharField(verbose_name='Nombres', max_length=150)
    apellido=models.CharField(verbose_name='Apellidos', max_length=150)
    dni = models.CharField(verbose_name='Cédula', max_length=13, unique=True)
    birth_date = models.DateField(verbose_name='Fecha de Nacimiento')
    gender = models.CharField(
        verbose_name='Género', 
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    )
    phone = models.CharField(verbose_name='Teléfono', max_length=15, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    address = models.CharField(verbose_name='Dirección', max_length=200, null=True, blank=True)
    blood_type = models.CharField(
        verbose_name='Tipo de Sangre',
        max_length=3,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        null=True, blank=True
    )
    # created_at es ahora date_creation de AuditModel
    
    @property
    def nombre_completo(self):
        return f"{self.primer_nombre} {self.apellido}"

    def __str__(self):
        return f"{self.nombre_completo} ({self.dni})"
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellido', 'primer_nombre']

class Diagnosis(AuditModel): # Hereda de AuditModel
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Paciente', related_name='diagnoses_doctor_app') # related_name ajustado
    # date es ahora date_creation de AuditModel, o si es fecha de diagnóstico específica, mantener y renombrar
    diagnosis_date = models.DateTimeField(default=timezone.now, verbose_name="Fecha del Diagnóstico")
    description = models.TextField(verbose_name='Descripción')
    icd_code = models.CharField(verbose_name='Código CIE', max_length=10, null=True, blank=True)
    notes = models.TextField(verbose_name='Notas Adicionales', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Activo', default=True) # Este 'is_active' es del diagnóstico en sí.
    
    def __str__(self):
        return f"Diagnóstico de {self.patient} - {self.diagnosis_date.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ['-diagnosis_date', '-date_creation']
