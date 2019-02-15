
# -*- coding: utf-8 -*e
from __future__ import unicode_literals
from django.db import models


class Actividad(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    duracion = models.IntegerField(blank=True, null=True)
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)
    secuencial_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='secuencial_usuario')  # noqa
    secuencial_covertura = models.ForeignKey('Cobertura', models.DO_NOTHING, db_column='secuencial_covertura')  # noqa
    secuencial_requerido = models.ForeignKey('Requerido', models.DO_NOTHING, db_column='secuencial_requerido')  # noqa

    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Actividad: ' + self.nombre


class Cobertura(models.Model):
    secuencial = models.AutoField(primary_key=True)
    estadot = True
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.NullBooleanField(default=estadot)   # noqa

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
    secuencial_listacontrol = models.ForeignKey('Listacontrol', models.DO_NOTHING, db_column='secuencial_listacontrol')  # noqa
    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Cobertura: ' + self.nombre


class Feriados(models.Model):
    secuencial = models.AutoField(primary_key=True)
    estadot = True
    nombre = models.CharField(max_length=80, blank=True, null=True)
    descripcion = models.CharField(max_length=120, blank=True, null=True)
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)
    estado = models.NullBooleanField(default=estadot)
    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Cobertura: ' + self.nombre


class Horario(models.Model):
    secuencial = models.AutoField(primary_key=True)
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)
    estado = models.NullBooleanField()


class Listacontrol(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    estado = models.NullBooleanField()
    secuencial_tipocontrol = models.ForeignKey('Tipoturno', models.DO_NOTHING, db_column='secuencial_tipocontrol', blank=True, null=True)  # noqa
    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Cobertura: ' + self.nombre


class Persona(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellidos = models.CharField(max_length=50, blank=True, null=True)
    puesto = models.CharField(max_length=100, blank=True, null=True)
    estado = models.NullBooleanField()

    def __str__(self):  # noqa
        return 'Persona: ' + self.nombre  # noqa


class Requerido(models.Model):
    secuencial = models.AutoField(primary_key=True)
    estadot = True
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.NullBooleanField(default=estadot)
    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Cobertura: ' + self.nombre # noqa


class Tipoturno(models.Model):
    secuencial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    estado = models.NullBooleanField()
    descripcion = models.CharField(max_length=100, blank=True, null=True)  
    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Cobertura: ' + self.nombre


class Turno(models.Model):
    secuencial = models.AutoField(primary_key=True)
    secuencial_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='secuencial_usuario')  # noqa
    secuencial_tipoturno = models.ForeignKey(Tipoturno, models.DO_NOTHING, db_column='secuencial_tipoturno')  # noqa
    secuencial_horario = models.ForeignKey(Horario, models.DO_NOTHING, db_column='secuencial_horario')  # noqa


class Turnoferiado(models.Model):
    secuencial_tipoturno = models.ForeignKey(Tipoturno, models.DO_NOTHING, db_column='secuencial_tipoturno')  # noqa
    secuencial_feriado = models.ForeignKey(Feriados, models.DO_NOTHING, db_column='secuencial_feriado')  # noqa


class Usuario(models.Model):
    secuencial = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    estado = models.NullBooleanField()
    secuencial_persona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='secuencial_persona', blank=True, null=True)  # noqa
    class Meta:  # noqa
        ordering = ["secuencial"]

    def __str__(self):
        return 'Cobertura: ' + self.usuario # noqa