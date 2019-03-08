# from django.shortcuts import render
import json
import time

from django.contrib import messages
from django.core import serializers # noqa
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from registropersonal.sistema.models import (Actividad, Cobertura,
                                             Detalleactividad,
                                             Detalleplanificacionactividad,
                                             Planificacion, Requerido,
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


class PlanificacionActividad(ListView):
    template_name = 'planificacion/listar.html'
    context_object_name = 'planificacion_listar'
    model = Detalleplanificacionactividad


class PlanificacionActividadFormulario(ListView):
    template_name = 'planificacion/insertar.html'
    context_object_name = 'planificacion_listar'
    model = Detalleplanificacionactividad

    def get_context_data(self, **kwargs):
        fechaactual = time.strftime("%Y-%m-%d")
        print(fechaactual)
        ctx = super(PlanificacionActividadFormulario,
                    self).get_context_data(**kwargs)
        ctx['actividad_list'] = Actividad.objects.all()
        ctx['planificacion_list'] = Planificacion.objects.all()
        ctx['semana'] = Planificacion.objects.filter(
            Q(fechainicio__lte=fechaactual) & Q(fechafin__gte=fechaactual))
        ctx['semana2'] = Actividad.objects.all()\
            .values('nombre',
                    'detalleactividad__numerosemana',
                    )\
            .filter(Q(
                detalleactividad__secuencial_tipoactividad=1) & Q(
                detalleactividad__numerosemana=2))
        return ctx


class ActividadLisView(ListView):
    template_name = 'actividad/listar.html'
    context_object_name = 'actividad_listar'
    model = Actividad

    def get_context_data(self, **kwargs):
        ctx = super(ActividadLisView, self).get_context_data(**kwargs)
        ctx['actividad_objeto'] = Actividad.objects.all().order_by('nombre')\
            .values('secuencial',
                    'nombre',
                    'descripcion',
                    'secuencial_usuario__usuario',
                    'secuencial_cobertura__nombre',
                    'secuencial_requerido__nombre',
                    'detalleactividad__numerosemana',
                    'detalleactividad__secuencial_tipoactividad')\
            .distinct('nombre')\
            .annotate(usuario=F('secuencial_usuario__usuario'),
                      cobertura=F('secuencial_cobertura__nombre'),
                      requerido=F('secuencial_requerido__nombre'), )
        ctx['actividad_detalle_tipo'] = Actividad.objects.all()\
            .values('nombre',
                    'descripcion',
                    'secuencial_usuario__usuario',
                    'secuencial_cobertura__nombre',
                    'secuencial_requerido__nombre',
                    'detalleactividad__numerosemana',
                    'detalleactividad__secuencial_tipoactividad')
        ctx['duracion_list'] = Tipoactividad.objects.all()
        ctx['detalleactividad_list'] = Detalleactividad.objects.all()
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

# Permite generar la tabla de actiidad mediante una
# consulta por el numero de semana correspondiente.


class GenerarTabla(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            datos = json.loads(request.GET['actividad_mes'])
            for actividad in datos['semana_mes']:
                numerosemanames = int(actividad)
            print(numerosemanames)
            numerosemana = int(datos['semana'])
            print('numero semana', numerosemana)
            # Declaración de variables del sistema
            datos_JSON = {}  # Arreglo de datos_JSON para solicitud
            semana = Actividad.objects.all()  # Conjunto de datos_JSON por semana mes # noqa
            semanaTipo = Actividad.objects.all()  # Conjunto de datos_JSON de actividades por semana tipo # noqa
            semanaUnica = Actividad.objects.all()  # Conjunto de datos_JSON de actibidades unicas # noqa
            fechaactual = time.strftime("%Y-%m-%d")
            fechasemana_JSON = {}
            fechasemana_queryset = Planificacion.objects.all().values('fechainicio','fechafin').filter(
                        Q(fechainicio__lte=fechaactual) & Q(fechafin__gte=fechaactual) & Q(numerosemana=numerosemana))
            for fecha in fechasemana_queryset:
                fechasemana_JSON = {
                    'fechainicio': str(fecha['fechainicio']),
                    'fechafin': str(fecha['fechafin'])
                }
            # ORM para extraer las actividades recurrentes por periodos Bimensuales, Trimestrales, Cuatrimestrales, Semestrales y Anuales. # noqa
            semanaTipo = Actividad.objects.all()\
                .values('nombre',
                        'secuencial_usuario__usuario',
                        'secuencial_cobertura__nombre',
                        'secuencial_requerido__nombre',
                        'detalleactividad__numerosemana',
                        )\
                .filter(detalleactividad__numerosemana=numerosemana).exclude(
                    detalleactividad__fechaproceso=fechaactual)
            print(semanaTipo)
            # ORM para exraer las actividades Unicas por periodos mensuales
            semanaUnica = Actividad.objects.all()\
                .values('nombre',
                        'secuencial_usuario__usuario',
                        'secuencial_cobertura__nombre',
                        'secuencial_requerido__nombre',
                        'detalleactividad__numerosemana',
                        )\
                .filter(Q(detalleactividad__numerosemana=numerosemana) & Q(
                    detalleactividad__fechaproceso=fechaactual))
            print(semanaUnica)
            # SECUENCIA DE IF PARA IDENTIFICAR EL NUMERO DE SEMANA DEL MES QUE
            # PERTENECE UNA ACTIVIDAD
            if numerosemanames == 1:
                # print("entra a if")
                semana = Actividad.objects.all()\
                    .values('nombre',
                            'secuencial_usuario__usuario',
                            'secuencial_cobertura__nombre',
                            'secuencial_requerido__nombre',
                            'detalleactividad__numerosemana',
                            )\
                    .filter(Q(
                        detalleactividad__secuencial_tipoactividad=1) & Q(
                        detalleactividad__numerosemana=1))
            elif numerosemanames == 2:
                semana = Actividad.objects.all()\
                    .values('nombre',
                            'secuencial_usuario__usuario',
                            'secuencial_cobertura__nombre',
                            'secuencial_requerido__nombre',     
                            'detalleactividad__numerosemana',
                            )\
                    .filter(Q(
                        detalleactividad__secuencial_tipoactividad=1) & Q(
                        detalleactividad__numerosemana=2))
            elif numerosemanames == 3:
                semana = Actividad.objects.all()\
                    .values('nombre',
                            'secuencial_usuario__usuario',
                            'secuencial_cobertura__nombre',
                            'secuencial_requerido__nombre',     
                            'detalleactividad__numerosemana',
                            )\
                    .filter(Q(
                        detalleactividad__secuencial_tipoactividad=1) & Q(
                        detalleactividad__numerosemana=3))
            elif numerosemanames == 4:
                semana = Actividad.objects.all()\
                    .values('nombre',
                            'secuencial_usuario__usuario',
                            'secuencial_cobertura__nombre',
                            'secuencial_requerido__nombre',     
                            'detalleactividad__numerosemana',
                            )\
                    .filter(Q(
                        detalleactividad__secuencial_tipoactividad=1) & Q(
                        detalleactividad__numerosemana=4))
            elif numerosemanames == 5:
                semana = Actividad.objects.all()\
                    .values('nombre',
                            'secuencial_usuario__usuario',
                            'secuencial_cobertura__nombre',
                            'secuencial_requerido__nombre',     
                            'detalleactividad__numerosemana',
                            )\
                    .filter(Q(
                        detalleactividad__secuencial_tipoactividad=1) & Q(
                        detalleactividad__numerosemana=5))
            # Guardar lista generada dentro de los datos_JSON
            datos_JSON['semana'] = list(semana) # Transformar a lista el ORM obtenido # noqa
            datos_JSON['semanatipo'] = list(semanaTipo)
            datos_JSON['semanaunica'] = list(semanaUnica)
            datos_JSON['semanames'] = fechasemana_JSON
            datos_JSON['result'] = "OK" # Establecer un mensaje en el caso de un correcto proceso # noqa
            datos_JSON['message'] = "¡Proecso Actividad Extracción \
                                guardado correctamente!"
            return HttpResponse(
                json.dumps(datos_JSON), content_type="application/json")

        except Exception as error:
            print("Error al guardar-->transaccion" + str(error))
            datos_JSON['message'] = "¡Ha ocurrido un error al procesar datos_JSON \
                de la actividd!"
            datos_JSON['result'] = "X"
            return HttpResponse(
                json.dumps(datos_JSON), content_type="application/json")


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


# Clase para guardar planificaciones dentro del sistema.

class GuardarPlanificacion(TemplateView):
    # Llamar al metodo para transacciones en base de datos
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        print("Entro a guardar planificación")
        datosplanificacion = {}
        _transaccion = transaction.savepoint()
        try:
            valor = request.POST.get('datosplaning', None)
            print(valor)
            datosplanificacion = json.loads(request.POST['datosplaning'])
            print(datosplanificacion)
            fechaactual = time.strftime("%Y-%m-%d")
            print(fechaactual)
            print('pasa')
            semanaactividad = int(datosplanificacion["semana"])
            print('pasa')
            for planifica in datosplanificacion['planificacion']:
                print('entra')
                # print(planifica['actividad'])
                actividad = planifica['actividad']
                fechainicio = planifica['fechainicio']
                fechafin = planifica['fechafin']
                detalleplanificacion = Detalleplanificacionactividad(
                    secuencial_actividad=Actividad.objects.get(
                        nombre=actividad),
                    secuencial_planificacion=Planificacion.objects.get(
                        Q(fechainicio__lte=fechaactual) & Q(fechafin__gte=fechaactual) & Q(numerosemana=semanaactividad)), # noqa
                    fechainicio=fechainicio, fechafin=fechafin)
                detalleplanificacion.save()
            transaction.savepoint_commit(_transaccion)
            datosplanificacion['result'] = "OK"
            datosplanificacion['message'] = "¡Registro de actividad \
                                guardado correctamente!"
            messages.add_message(request, messages.SUCCESS, datosplanificacion['message'])
            # Responder solicitud pedida por AJAX
            return HttpResponse(
                json.dumps(datosplanificacion), content_type="application/json")
        except Exception as error:
            print("Error al guardar-->transaccion: " + str(error))
            print(type(error))    # la instancia de excepción
            print(error.args)     # argumentos guardados en .args
            print(error) 
            transaction.savepoint_rollback(_transaccion)
            datosplanificacion['message'] = "¡Ha ocurrido un error al tratar de ingresar los datosplanificacion de la persona!"
            datosplanificacion['error'] = "Transacción: " + str(error)
            return HttpResponse(
                json.dumps(datosplanificacion), content_type="application/json")