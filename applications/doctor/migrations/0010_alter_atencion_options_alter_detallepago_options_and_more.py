# Generated by Django 5.2.1 on 2025-07-05 09:29

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_atencion_ecografia_examenlaboratorio_and_more'),
        ('doctor', '0009_alter_citamedica_paciente'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='atencion',
            options={'ordering': ['-fecha_atencion_real', '-date_creation'], 'verbose_name': 'Atención Médica', 'verbose_name_plural': 'Atenciones Médicas'},
        ),
        migrations.AlterModelOptions(
            name='detallepago',
            options={'verbose_name': 'Detalle de Pago', 'verbose_name_plural': 'Detalles de Pagos'},
        ),
        migrations.AlterModelOptions(
            name='diagnosis',
            options={'ordering': ['-diagnosis_date', '-date_creation'], 'verbose_name': 'Diagnóstico', 'verbose_name_plural': 'Diagnósticos'},
        ),
        migrations.AlterModelOptions(
            name='pago',
            options={'ordering': ['-date_creation'], 'verbose_name': 'Pago', 'verbose_name_plural': 'Pagos'},
        ),
        migrations.RenameIndex(
            model_name='citamedica',
            new_name='idx_fecha_hora_cita_doctor',
            old_name='idx_fecha_hora',
        ),
        migrations.RemoveField(
            model_name='atencion',
            name='fecha_atencion',
        ),
        migrations.RemoveField(
            model_name='diagnosis',
            name='date',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='created_at',
        ),
        migrations.AddField(
            model_name='atencion',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='atencion',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='atencion',
            name='fecha_atencion_real',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Fecha y hora real en que se realizó la atención.', verbose_name='Fecha y Hora de la Atención'),
        ),
        migrations.AddField(
            model_name='atencion',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='atencion',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AddField(
            model_name='citamedica',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='citamedica',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='citamedica',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='citamedica',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AddField(
            model_name='detalleatencion',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='detalleatencion',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='detalleatencion',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='detalleatencion',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AddField(
            model_name='detallepago',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='detallepago',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='detallepago',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='detallepago',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='diagnosis_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha del Diagnóstico'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AddField(
            model_name='horarioatencion',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='horarioatencion',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='horarioatencion',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='horarioatencion',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AddField(
            model_name='pago',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='pago',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='pago',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='pago',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AddField(
            model_name='patient',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='patient',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='patient',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='patient',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AddField(
            model_name='serviciosadicionales',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
        migrations.AddField(
            model_name='serviciosadicionales',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de Actualización'),
        ),
        migrations.AddField(
            model_name='serviciosadicionales',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_creations', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AddField(
            model_name='serviciosadicionales',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updates', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por'),
        ),
        migrations.AlterField(
            model_name='atencion',
            name='diagnostico',
            field=models.ManyToManyField(help_text='Diagnósticos clínicos asociados a esta atención.', related_name='atenciones_doctor_app', to='core.diagnostico', verbose_name='Diagnósticos'),
        ),
        migrations.AlterField(
            model_name='atencion',
            name='paciente',
            field=models.ForeignKey(help_text='Paciente que recibe esta atención médica (modelo doctor.Patient).', on_delete=django.db.models.deletion.PROTECT, related_name='atenciones_doctor_app', to='doctor.patient', verbose_name='Paciente'),
        ),
        migrations.AlterField(
            model_name='citamedica',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('ocupado', 'Ocupado'), ('atendido', 'Atendido')], default='pendiente', max_length=20, verbose_name='Estado de la Cita'),
        ),
        migrations.AlterField(
            model_name='citamedica',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas_doctor_app', to='doctor.patient', verbose_name='Paciente'),
        ),
        migrations.AlterField(
            model_name='detalleatencion',
            name='atencion',
            field=models.ForeignKey(help_text='Atención médica asociada a este detalle.', on_delete=django.db.models.deletion.CASCADE, related_name='detalles_doctor_app', to='doctor.atencion', verbose_name='Atención Médica'),
        ),
        migrations.AlterField(
            model_name='detalleatencion',
            name='medicamento',
            field=models.ForeignKey(help_text='Medicamento recetado al paciente.', on_delete=django.db.models.deletion.PROTECT, related_name='prescripciones_doctor_app', to='core.medicamento', verbose_name='Medicamento'),
        ),
        migrations.AlterField(
            model_name='detallepago',
            name='pago',
            field=models.ForeignKey(help_text='Pago al que corresponde este detalle de cobro.', on_delete=django.db.models.deletion.CASCADE, related_name='detalles_doctor_app', to='doctor.pago', verbose_name='Pago'),
        ),
        migrations.AlterField(
            model_name='detallepago',
            name='servicio_adicional',
            field=models.ForeignKey(help_text='Servicio adicional cobrado (ej. Radiografía, Laboratorio).', on_delete=django.db.models.deletion.PROTECT, related_name='detalles_pago_doctor_app', to='doctor.serviciosadicionales', verbose_name='Servicio'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnoses_doctor_app', to='doctor.patient', verbose_name='Paciente'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='atencion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pagos_doctor_app', to='doctor.atencion', verbose_name='Atención'),
        ),
    ]
