# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create,
# modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field
# names.
from django.db import models


class Actividad(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    secuencial_requerido = models.ForeignKey(
        'Requerido', models.DO_NOTHING,
        db_column='secuencial_requerido', default=1)
    secuencial_cobertura = models.ForeignKey(
        'Cobertura', models.DO_NOTHING,
        db_column='secuencial_cobertura', default=1)
    secuencial_usuario = models.ForeignKey(
        'Usuario', models.DO_NOTHING,
        db_column='secuencial_usuario', default=1)

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Actividad: ' + self.nombre


class Cobertura(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.NullBooleanField()

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Cobertura: ' + self.nombre


class Controlactivdad(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    proceso = models.CharField(max_length=1, blank=True, null=True)
    estado = models.NullBooleanField()
    secuencial_listacontrol = models.ForeignKey(
        'Listacontrol', models.DO_NOTHING, db_column='secuencial_listacontrol')

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Control Actividad: ' + self.nombre


class Detalleactividad(models.Model):
    secuencial = models.AutoField(primary_key=True)
    numerosemana = models.IntegerField()
    fechaproceso = models.DateField(blank=True, null=True)
    secuencial_actividad = models.ForeignKey(
        Actividad, models.DO_NOTHING,
        db_column='secuencial_actividad', default=1)
    secuencial_tipoactividad = models.ForeignKey(
        'Tipoactividad', models.DO_NOTHING,
        db_column='secuencial_tipoactividad', default=1)

    class Meta:  # noqa
        ordering = ["secuencial"]


class Detalleplanificacionactividad(models.Model):
    secuencial = models.AutoField(primary_key=True)
    secuencial_actividad = models.ForeignKey(
        Actividad, models.DO_NOTHING, db_column='secuencial_actividad',
        default=1)
    secuencial_planificacion = models.ForeignKey(
        'Planificacion', models.DO_NOTHING,
        db_column='secuencial_planificacion', default=1)
    fechainicio = models.DateField()
    fechafin = models.DateField()
    INICIADO = 'I'
    EJECUTADO = 'E'
    TERMINADO = 'T'
    PROCESO = (
        (INICIADO, 'Iniciado'),
        (EJECUTADO, 'Ejecutando'),
        (TERMINADO, 'Terminado'),
        )
    estado = models.CharField(max_length=1, choices=PROCESO, default=INICIADO,)
    class Meta:  # noqa
        ordering = ["secuencial"]


class Feriados(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    descripcion = models.CharField(max_length=120, blank=True, null=True)
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)
    estado = models.NullBooleanField()

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Feriados: ' + self.nombre


class Horario(models.Model):
    secuencial = models.AutoField(primary_key=True)
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)
    estado = models.NullBooleanField()

    class Meta:  # noqa
        ordering = ["secuencial"]


class Listacontrol(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    estado = models.NullBooleanField()
    secuencial_tipocontrol = models.ForeignKey(
        'Tipoturno', models.DO_NOTHING, db_column='secuencial_tipocontrol',
        blank=True, null=True)

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Feriados: ' + self.nombre


class Persona(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellidos = models.CharField(max_length=50, blank=True, null=True)
    puesto = models.CharField(max_length=100, blank=True, null=True)
    estado = models.NullBooleanField()

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Persona: ' + self.nombre


class Planificacion(models.Model):
    secuencial = models.AutoField(primary_key=True)
    numerosemana = models.IntegerField(blank=True, null=True)
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)

    class Meta:  # noqa
        ordering = ["secuencial"]


class Notasplanificacion(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nota = models.TextField(null=True)
    secuencial_planificacion = models.ForeignKey(
        'Planificacion', models.DO_NOTHING,
        db_column='secuencial_planificacion', default=1)
    fechaproceso = models.DateField(blank=True, null=True)

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Nota: ' + self.nota


class Requerido(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.NullBooleanField()

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Requerido: ' + self.nombre


class Tipoactividad(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=80)

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Tipo Actividad: ' + self.nombre


class Tipoturno(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.NullBooleanField()

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Tipo Turno: ' + self.nombre


class Turno(models.Model):
    secuencial = models.AutoField(primary_key=True)
    secuencial_usuario = models.ForeignKey(
        'Usuario', models.DO_NOTHING, db_column='secuencial_usuario')
    secuencial_tipoturno = models.ForeignKey(
        Tipoturno, models.DO_NOTHING, db_column='secuencial_tipoturno')
    secuencial_horario = models.ForeignKey(
        Horario, models.DO_NOTHING, db_column='secuencial_horario')

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Turno: ' + self.nombre


class Turnoferiado(models.Model):
    secuencial_tipoturno = models.ForeignKey(
        Tipoturno, models.DO_NOTHING, db_column='secuencial_tipoturno')
    secuencial_feriado = models.ForeignKey(
        Feriados, models.DO_NOTHING, db_column='secuencial_feriado')


class Usuario(models.Model):
    secuencial = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    estado = models.NullBooleanField()
    secuencial_persona = models.ForeignKey(
        Persona, models.DO_NOTHING,
        db_column='secuencial_persona', blank=True, null=True)

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Usuario: ' + self.usuario
