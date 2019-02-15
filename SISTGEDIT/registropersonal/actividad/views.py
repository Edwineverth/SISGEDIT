# from django.shortcuts import render
import json
import time

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from registropersonal.sistema.models import (Actividad, Cobertura,
                                             Detalleactividad, Requerido,
                                             Tipoactividad, Usuario)

# Creaciòn de una actividad basada en 3 entidades de relaciòn

# METODOS PARA LA GESTIÓN DE TIPO ACTIVIDADES


class TipoactividadCreate(CreateView):
    model = Tipoactividad
    fields = ['nombre', 'descripcion']
    template_name = 'actividad/tipoactividad/insertar.html'
    success_url = reverse_lazy('tipoactividad_listar')


class TipoactividadListar(ListView):
    context_object_name = 'tipoactividad_list'
    model = Tipoactividad
    template_name = 'actividad/tipoactividad/listar.html'


class TipoactividadUpdate(UpdateView):
    model = Tipoactividad
    template_name = 'actividad/tipoactividad/actualizar.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('tipoactividad_listar')


class TipoactividadDelete(DeleteView):
    model = Tipoactividad
    context_object_name = "tipoactividad"
    template_name = 'actividad/tipoactividad/eliminar.html'
    success_url = reverse_lazy('tipoactividad_listar')


# METODOS PARA LA GESTIÓN DE ACTIVIDADES


class ActividadLisView(ListView):
    template_name = 'actividad/listar.html'  # noqa
    context_object_name = 'actividad_listar'  # noqa
    model = Actividad  # noqa

    def get_context_data(self, **kwargs):
        ctx = super(ActividadLisView, self).get_context_data(**kwargs)
        ctx['actividad_objeto'] = Actividad.objects.all()\
            .values('nombre',
                    'descripcion',
                    'secuencial_usuario__usuario',
                    'secuencial_cobertura__nombre',
                    'secuencial_requerido__nombre')\
            .annotate(usuario=F('secuencial_usuario__usuario'),
                      cobertura=F('secuencial_cobertura__nombre'),
                      requerido=F('secuencial_requerido__nombre'), )
        ctx['detalle_actividad'] = Detalleactividad.objects.all().values(
            'numerosemana', 'secuencial_actividad__nombre',
            'secuencial_tipoactividad__nombre').annotate(
            actividadp=F('secuencial_actividad__nombre'), tipoactividad=F(
                'secuencial_tipoactividad__nombre'),)
        ctx['actividad_detalle_tipo'] = Actividad.objects.all()\
            .values('nombre',
                    'descripcion',
                    'secuencial_usuario__usuario',
                    'secuencial_cobertura__nombre',
                    'secuencial_requerido__nombre',
                    'detalleactividad__numerosemana',
                    'detalleactividad__secuencial_tipoactividad')
        ctx['duracion_list'] = Tipoactividad.objects.all()
        return ctx


class ActividadFormulario(ListView):
    template_name = "actividad/insertar.html"
    context_object_name = "usuario_list"
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super(ActividadFormulario, self).get_context_data(**kwargs)
        context['cobertura_list'] = Cobertura.objects.all()
        context['requerido_list'] = Requerido.objects.all()
        context['tipoactividad_list'] = Tipoactividad.objects.all()
        return context


class GuardarActividad(TemplateView):
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        _transaccion = transaction.savepoint()
        try:
            # Obtener cojunto de datos GET y establecer carga en formato JSON
            datos = json.loads(request.GET['actividad'])
            # Creación de la variable fecha actual para el ingreso de DETALLE
            # ACTIVIDAD
            fechaproceso = time.strftime("%Y-%m-%d")
            # Establecer un punto de guardado en la base en el caso de que no
            # exista un problema
            for proceso in datos["proceso"]:
                procesoactividad = int(proceso["proceso"])
            # En el caso de que, el proceso sea 1 se corre la actividad por
            # mes (Mensuales)
            if procesoactividad == 1:
                for semana in datos["semana"]:
                    # Guarda el numero de la semana del objeto en la variable
                    # semana
                    semanaactividad = int(semana["semana"])

                for actividad in datos["actividad"]:
                    nombre = actividad["nombre"]
                    descripcion = actividad["descripcion"]
                    usuario = int(actividad["usuario"])
                    cobertura = int(actividad["cobertura"])
                    requerido = int(actividad["requerido"])
                    recurrencia = int(actividad["recurrencia"])

                    actividad = Actividad(
                        nombre=nombre,
                        descripcion=descripcion,
                        secuencial_usuario=Usuario.objects.get(
                            secuencial=usuario),
                        secuencial_cobertura=Cobertura.objects.get(
                            secuencial=cobertura),
                        secuencial_requerido=Requerido.objects.get(
                            secuencial=requerido))
                    actividad.save()
                    detalleactividad = Detalleactividad(
                        numerosemana=semanaactividad,
                        secuencial_actividad=Actividad.objects.get(
                            nombre=nombre),
                        secuencial_tipoactividad=Tipoactividad.objects.get(
                            secuencial=recurrencia),
                        fechaproceso=fechaproceso)
                    detalleactividad.save()
            # En el caso de ser 2 proceso se corre actividad por Las demas
            # duraciones (Bimestral, Trimestral, Cuatrimestral, Semestral y
            # Anual)
            else:
                # Obtener los datos del objeto actividad para almacenar en las
                # variables
                for actividad in datos["actividad"]:
                    nombre = actividad["nombre"]
                    descripcion = actividad["descripcion"]
                    usuario = int(actividad["usuario"])
                    cobertura = int(actividad["cobertura"])
                    requerido = int(actividad["requerido"])
                    recurrencia = int(actividad["recurrencia"])
                # Creación del objeto actividad e introducción de valores
                actividad = Actividad(
                    nombre=nombre, descripcion=descripcion,
                    secuencial_usuario=Usuario.objects.get(
                        secuencial=usuario),
                    secuencial_cobertura=Cobertura.objects.get(
                        secuencial=cobertura),
                    secuencial_requerido=Requerido.objects.get(
                        secuencial=requerido))
                actividad.save()  # Guarda el objeto en el modelo actividad
                # Ciclo paa contar los numeros de semana registrados
                for semana in datos["semana"]:
                    # Guarda el numero de semana en la variable
                    semanaactividad = int(semana["semana"])
                    detalleactividad = Detalleactividad(
                        numerosemana=semanaactividad,
                        secuencial_actividad=Actividad.objects.get(
                            nombre=nombre),
                        secuencial_tipoactividad=Tipoactividad.objects.get(
                            secuencial=recurrencia),
                        fechaproceso=fechaproceso)
                    detalleactividad.save()
            # TERMINACIÓN DE PROCESO DE GUARDADO DE DATOS
            # PROCEDIMIENTO PARA REALIZAR UN COMIT A LA BASE DE DATOS
            transaction.savepoint_commit(_transaccion)
            datos['result'] = "OK"
            datos['message'] = "¡Registro de actividad \
                                guardado correctamente!"
            messages.add_message(request, messages.SUCCESS, datos['message'])
            return HttpResponse(
                json.dumps(datos), content_type="application/json")
        except Exception as error:
            print("Error al guardar-->transaccion" + str(error))
            transaction.savepoint_rollback(_transaccion)
            datos['message'] = "¡Ha ocurrido un error al tratar de ingresar \
                los datos de la persona!"
            datos['result'] = "X"
            return HttpResponse(
                json.dumps(datos), content_type="application/json")
