# from django.shortcuts import render
# import datetime
import json
import time

from braces.views import GroupRequiredMixin, LoginRequiredMixin
# pip install django-braces
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.core import serializers  # noqa
# from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import F, Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)
from django.contrib.auth.models import User
from registropersonal.sistema.models import (Actividad, Cobertura,
                                             Detalleactividad,
                                             Detalleplanificacionactividad,
                                             Notasplanificacion, Planificacion,
                                             Requerido, Tipoactividad)

# @login_required(login_url='/accounts/login')
# Creaciòn de una actividad basada en 3 entidades de relaciòn

# METODOS PARA LA GESTIÓN DE TIPO ACTIVIDADES
"""
from django.contrib.auth.mixins import LoginRequiredMixin

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
"""


class TipoactividadCreate(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    model = Tipoactividad
    fields = ['nombre', 'descripcion']
    template_name = 'actividad/tipoactividad/insertar.html'
    success_url = reverse_lazy('tipoactividad_listar')

    @method_decorator(permission_required('sistema.add_tipoactividad', reverse_lazy('home'))) # noqa
    def dispatch(self, *args, **kwargs):
        return super(TipoactividadCreate, self).dispatch(*args, **kwargs)


class TipoactividadListar(LoginRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    context_object_name = 'tipoactividad_list'
    model = Tipoactividad
    template_name = 'actividad/tipoactividad/listar.html'


class TipoactividadUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    model = Tipoactividad
    template_name = 'actividad/tipoactividad/actualizar.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('tipoactividad_listar')
    @method_decorator(permission_required('sistema.change_tipoactividad', reverse_lazy('home'))) # noqa
    def dispatch(self, *args, **kwargs):
        return super(TipoactividadUpdate, self).dispatch(*args, **kwargs)


class TipoactividadDelete(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    model = Tipoactividad
    context_object_name = "tipoactividad"
    template_name = 'actividad/tipoactividad/eliminar.html'
    success_url = reverse_lazy('tipoactividad_listar')

    @method_decorator(permission_required('sistema.delete_tipoactividad', reverse_lazy('home')))# noqa
    def dispatch(self, *args, **kwargs):
        return super(TipoactividadDelete, self).dispatch(*args, **kwargs)

# METODOS PARA LA GESTIÓN DE ACTIVIDADES
""" # noqa
***********************************************************************
***********************************************************************
GESTIÓN DE ACTIVIDADES - PLANIFICACIÓN
***********************************************************************
"""


# PRESENTACIÓN DE "GENERAR PLANIFICACIÓN"
class PlanificacionActividadFormulario(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'
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
        ctx['usuario_list'] = User.objects.all()
        ctx['cobertura_list'] = Cobertura.objects.all()
        ctx['requerido_list'] = Requerido.objects.all()
        ctx['tipoactividad_list'] = Tipoactividad.objects.all()
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


# Genera la tabla de actividades mediante petición AJAX--
class GenerarTabla(LoginRequiredMixin, GroupRequiredMixin,  TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'

    def get(self, request, *args, **kwargs):
        try:
            datos = json.loads(request.GET['actividad_mes'])
            for actividad in datos['semana_mes']:
                numerosemanames = int(actividad)
            # print(numerosemanames)
            numerosemana = int(datos['semana'])
            # print('numero semana', numerosemana)
            # Declaración de variables del sistema
            datos_JSON = {}  # Arreglo de datos_JSON para solicitud
            semana = Actividad.objects.all()  # Conjunto de datos_JSON por semana mes # noqa
            semanaTipo = Actividad.objects.all()  # Conjunto de datos_JSON de actividades por semana tipo # noqa
            semanaUnica = Actividad.objects.all()  # Conjunto de datos_JSON de actibidades unicas # noqa
            fechaactual = time.strftime("%Y-%m-%d")
            fechasemana_JSON = {}
            fechasemana_queryset = Planificacion.objects.all().values('fechainicio','fechafin').filter( # noqa
                        Q(fechainicio__lte=fechaactual) & Q(fechafin__gte=fechaactual) & Q(numerosemana=numerosemana)) # noqa
            for fecha in fechasemana_queryset:
                fechasemana_JSON = {
                    'fechainicio': str(fecha['fechainicio']),
                    'fechafin': str(fecha['fechafin'])
                }
            # ORM para extraer las actividades recurrentes por periodos Bimensuales, Trimestrales, Cuatrimestrales, Semestrales y Anuales. # noqa
            numeroActividad = Detalleactividad.objects.all().filter(Q(numerosemana=numerosemana) & ~Q(secuencial_tipoactividad=7)).values_list('secuencial_actividad', flat=True)  # noqa
            existePlanificacion = Detalleplanificacionactividad.objects.filter(secuencial_planificacion=Planificacion.objects.get( # noqa
                Q(fechainicio__lte=fechaactual) & Q(fechafin__gte=fechaactual) & Q(numerosemana=numerosemana))).count() # noqa
            semanaTipo = Actividad.objects.all()\
                .values('nombre',
                        'user_id__first_name',
                        'user_id__last_name',
                        'secuencial_cobertura__nombre',
                        'secuencial_requerido__nombre',
                        ).filter(secuencial__in=list(numeroActividad))

            # ORM para exraer las actividades Unicas por periodos mensuales
            semanaUnica = Actividad.objects.all()\
                .values('nombre',
                        'user_id__first_name',
                        'user_id__last_name',
                        'secuencial_cobertura__nombre',
                        'secuencial_requerido__nombre',
                        'detalleactividad__numerosemana',
                        )\
                .filter(Q(detalleactividad__numerosemana=numerosemana) & Q(
                    detalleactividad__fechaproceso=fechaactual) & Q(
                    detalleactividad__secuencial_tipoactividad=7))
            # SECUENCIA DE IF PARA IDENTIFICAR EL NUMERO DE SEMANA DEL MES QUE
            # PERTENECE UNA ACTIVIDAD
            if numerosemanames == 1:
                # print("entra a if")
                semana = Actividad.objects.all()\
                    .values('nombre',
                            'user_id__first_name',
                            'user_id__last_name',
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
                            'user_id__first_name',
                            'user_id__last_name',
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
                            'user_id__first_name',
                            'user_id__last_name',
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
                            'user_id__first_name',
                            'user_id__last_name',
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
                            'user_id__first_name',
                            'user_id__last_name',
                            'secuencial_cobertura__nombre',
                            'secuencial_requerido__nombre',
                            'detalleactividad__numerosemana',
                            )\
                    .filter(Q(
                        detalleactividad__secuencial_tipoactividad=1) & Q(
                        detalleactividad__numerosemana=5))
            # Guardar lista generada dentro de los datos_JSON
            datos_JSON['existeplanificacion'] = existePlanificacion
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

# MUESTRA LA GENERACIÓN DEL CRONOGRAMA


class PlanificacionActividad(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'
    template_name = 'planificacion/listar.html'
    context_object_name = 'planificacion_listar'
    model = Planificacion


# GENERACION DE CRONOGRAMA DE ACTIVIDADES PARA REPORTES


class CronogramaActividad(LoginRequiredMixin, GroupRequiredMixin, TemplateView): # noqa
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'

    def get(self, request, *args, **kwargs):
        try:
            datos_JSON = {}
            planificacion_List = []
            fechas_List = []
            datos = json.loads(request.GET['planificacion'])
            print(datos)
            secuencialDetallePlanificaicon = datos
            fechas_QuerySet = Planificacion.objects.all().values('numerosemana', 'fechainicio', 'fechafin').filter(secuencial=secuencialDetallePlanificaicon)  # noqa
            for fechas in fechas_QuerySet:
                fechas_List.append({
                    'numerosemana': str(fechas['numerosemana']),
                    'fechainicio': str(fechas['fechainicio']),
                    'fechafin': str(fechas['fechafin'])
                })
            planificación_QuerySet = Actividad.objects.all()\
                .values('nombre',
                        'user_id__first_name',
                        'user_id__last_name',
                        'secuencial_cobertura__nombre',
                        'secuencial_requerido__nombre',
                        'detalleplanificacionactividad__fechainicio',
                        'detalleplanificacionactividad__fechafin',
                        'detalleplanificacionactividad__secuencial_planificacion',  # noqa
                        )\
                .filter(Q(detalleplanificacionactividad__fechainicio__range=(str(fechas['fechainicio']),  # noqa
                 str(fechas['fechafin']))) & Q(detalleplanificacionactividad__secuencial_planificacion=int(secuencialDetallePlanificaicon))).order_by('nombre').distinct('nombre')  # noqa
            for planificacion in planificación_QuerySet:
                planificacion_List.append({
                    'nombre': str(planificacion['nombre']),
                    'cobertura': str(planificacion['secuencial_cobertura__nombre']),  # noqa
                    'responsable': str(planificacion['user_id__first_name']) + " " +str(planificacion['user_id__last_name']),  # noqa
                    'requerido': str(planificacion['secuencial_requerido__nombre']),  # noqa
                    'fechainicio': str(planificacion['detalleplanificacionactividad__fechainicio']),  # noqa
                    'fechafin': str(planificacion['detalleplanificacionactividad__fechafin'])  # noqa
                })
            print(planificacion_List)
            notap = Notasplanificacion.objects.filter(
                secuencial_planificacion=secuencialDetallePlanificaicon).count() # noqa
            print('Notas planificacion', notap)
            if notap == 1:
                print("entra")
                notaplanificar = Notasplanificacion.objects.all().values('nota').filter(
                    secuencial_planificacion=secuencialDetallePlanificaicon)
                datos_JSON['notaarea'] = list(notaplanificar)

            datos_JSON['existenota'] = notap
            datos_JSON['cronograma'] = planificacion_List
            datos_JSON['fechas'] = fechas_List
            datos_JSON['result'] = "OK"  # Establecer un mensaje en el caso de un correcto proceso # noqa
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


class CronogramaGuardar(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        _transaccion = transaction.savepoint()
        try:
            datos_JSON = {}
            datos = json.loads(request.GET['cronograma'])
            fechaactual = time.strftime("%Y-%m-%d")
            idPlan = int(datos['idplanificacion'])
            notasPlanificacion = Notasplanificacion(
                nota=datos['notas'],
                secuencial_planificacion=Planificacion.objects.get(pk=idPlan),
                fechaproceso=fechaactual)
            notasPlanificacion.save()
            transaction.savepoint_commit(_transaccion)
            datos_JSON['result'] = "OK"  # Establecer un mensaje en el caso de un correcto proceso # noqa
            datos_JSON['message'] = "¡Proecso Nota guardado correctamente!"
            return HttpResponse(
                json.dumps(datos_JSON), content_type="application/json")
        except Exception as error:
            print("Error al guardar-->transaccion" + str(error))
            transaction.savepoint_rollback(_transaccion)
            datos_JSON['message'] = "¡Ha ocurrido un error al procesar datos_JSON \
                de la actividd!"
            datos_JSON['result'] = "X"
            return HttpResponse(
                json.dumps(datos_JSON), content_type="application/json")


class ActividadLisView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'
    template_name = 'actividad/listar.html'
    context_object_name = 'actividad_listar'
    model = Actividad

    def get_context_data(self, **kwargs):
        ctx = super(ActividadLisView, self).get_context_data(**kwargs)
        ctx['actividad_objeto'] = Actividad.objects.all().order_by('nombre')\
            .values('secuencial',
                    'nombre',
                    'descripcion',
                    'user_id__first_name',
                    'user_id__last_name',
                    'secuencial_cobertura__nombre',
                    'secuencial_requerido__nombre',
                    'detalleactividad__numerosemana',
                    'detalleactividad__secuencial_tipoactividad')\
            .distinct('nombre')\
            .annotate(cobertura=F('secuencial_cobertura__nombre'),
                      requerido=F('secuencial_requerido__nombre'), )
        ctx['actividad_detalle_tipo'] = Actividad.objects.all()\
            .values('nombre',
                    'descripcion',
                    'user_id__first_name',
                    'user_id__last_name',
                    'secuencial_cobertura__nombre',
                    'secuencial_requerido__nombre',
                    'detalleactividad__numerosemana',
                    'detalleactividad__secuencial_tipoactividad')
        ctx['duracion_list'] = Tipoactividad.objects.all()
        ctx['detalleactividad_list'] = Detalleactividad.objects.all()
        return ctx


class ActividadFormulario(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'
    template_name = "actividad/insertar.html"
    context_object_name = "usuario_list"
    model = User

    def get_context_data(self, **kwargs):
        context = super(ActividadFormulario, self).get_context_data(**kwargs)
        context['cobertura_list'] = Cobertura.objects.all()
        context['requerido_list'] = Requerido.objects.all()
        context['tipoactividad_list'] = Tipoactividad.objects.all()
        return context

# Permite generar la tabla de actiidad mediante una
# consulta por el numero de semana correspondiente.


class GuardarActividad(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'
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
                        user_id=(User.objects.get(id=usuario)).id,
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
                    user_id=(User.objects.get(id=usuario)).id,
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

class GuardarPlanificacion(LoginRequiredMixin, GroupRequiredMixin, TemplateView): # noqa
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'
    # Llamar al metodo para transacciones en base de datos
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        print("Entro a guardar planificación")
        datosplanificacion = {}
        _transaccion = transaction.savepoint()
        try:
            datosplanificacion = json.loads(request.POST['datosplaning'])
            fechaactual = time.strftime("%Y-%m-%d")
            semanaactividad = int(datosplanificacion["semana"])

            for planifica in datosplanificacion['planificacion']:
                print('entra')
                # print(planifica['actividad'])
                actividad_nombre = planifica['actividad']
                fechainicio = planifica['fechainicio']
                fechafin = planifica['fechafin']

                if(Actividad.objects.filter(nombre=actividad_nombre).exists()):
                    print("El elemento existe")
                    # print(Actividad.objects.get(nombre=actividad))
                    detalleplanificacion = Detalleplanificacionactividad(
                    secuencial_actividad=Actividad.objects.get(
                        nombre=actividad_nombre), # noqa
                    secuencial_planificacion=Planificacion.objects.get(
                        Q(fechainicio__lte=fechaactual) & Q(fechafin__gte=fechaactual) & Q(numerosemana=semanaactividad)), # noqa
                    fechainicio=fechainicio, fechafin=fechafin)
                    detalleplanificacion.save()
                else:
                    responsablearray = planifica["responsable"].split()
                    if(len(responsablearray) == 2):
                        usuario_GET = User.objects.get(Q(first_name=responsablearray[0])and Q(last_name=responsablearray[1]))
                    else:
                        usuario_GET = User.objects.get(Q(first_name=responsablearray[0]+" "+responsablearray[1])and Q(last_name=responsablearray[2]+" "+responsablearray[3])) # noqa
                    print(responsablearray)
                    print("El elemento no existe")
                    #usuario_GET = User.objects.get(Q(first_name=responsablearray[0])and Q(last_name=responsablearray[1])) # noqa
                    cobertura_GET = Cobertura.objects.get(nombre=planifica["cobertura"]) # noqa
                    requerido_GET = Requerido.objects.get(nombre=planifica["requerido"]) # noqa
                    recurrencia_GET = Tipoactividad.objects.get(secuencial=7)

                    actividad = Actividad(
                        nombre=actividad_nombre,
                        descripcion="Programación de TI",
                        user_id=usuario_GET.id,
                        secuencial_cobertura=cobertura_GET,
                        secuencial_requerido=requerido_GET)
                    actividad.save()

                    print("la actividad unica se llama ", actividad_nombre)
                    detalleactividad = Detalleactividad(
                        numerosemana=semanaactividad,
                        secuencial_actividad=Actividad.objects.get(
                            nombre=actividad_nombre),
                        secuencial_tipoactividad=recurrencia_GET,
                        fechaproceso=fechaactual)
                    detalleactividad.save()
                    detalleplanificacion = Detalleplanificacionactividad(
                        secuencial_actividad=Actividad.objects.get(
                            nombre=actividad_nombre),
                        secuencial_planificacion=Planificacion.objects.get(
                            Q(fechainicio__lte=fechaactual) & Q(fechafin__gte=fechaactual) & Q(numerosemana=semanaactividad)), # noqa
                        fechainicio=fechainicio, fechafin=fechafin)
                    detalleplanificacion.save()
            transaction.savepoint_commit(_transaccion)
            datosplanificacion['result'] = "OK"
            datosplanificacion['message'] = "¡Registro de actividad \
                                guardado correctamente!"
            messages.add_message(request, messages.SUCCESS, datosplanificacion['message']) # noqa
            # Responder solicitud pedida por AJAX
            return HttpResponse(
                json.dumps(datosplanificacion), content_type="application/json") # noqa
        except Exception as error:
            print("Error al guardar-->transaccion: " + str(error))
            print(type(error))    # la instancia de excepción
            print(error.args)     # argumentos guardados en .args
            print(error)
            transaction.savepoint_rollback(_transaccion)
            datosplanificacion['message'] = "¡Ha ocurrido un error al tratar de ingresar los datosplanificacion de la persona!" # noqa
            datosplanificacion['error'] = "Transacción: " + str(error)
            return HttpResponse(
                json.dumps(datosplanificacion), content_type="application/json") # noqa


class ObtenerActividad(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'
    # Metodo para obtener las actividades
    def get(self, request, *args, **kwargs): # noqa
        datos_JSON = {}
        try:
            secTipoActividad = json.loads(request.GET['tipoactividad'])
            print("secttipocuenta", secTipoActividad)
            actividad_QuerySet = Actividad.objects.all().values('secuencial', 'nombre',  # noqa
             'user_id__first_name',
             'user_id__last_name',
              'secuencial_cobertura__nombre', 'secuencial_requerido__nombre').filter(detalleactividad__secuencial_tipoactividad=secTipoActividad).order_by('nombre').distinct('nombre') # noqa
            print("el query set es", actividad_QuerySet)
            datos_JSON['actividades'] = list(actividad_QuerySet)
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

# Clase para solicitud get en donde debuelve un JSON de respuesta


"""
class NombredelMetodo(TemplateView):
    def get(self, request, *args, **kwargs):
        datos_JSON = {}
        try:
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
"""


"""
-********************EJECUCIÓN DE ACTIVIDADES ****************************
"""


class EjecutarActividad(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'
    template_name = 'actividad/ejecutar.html'
    context_object_name = 'planificacion_listar'
    model = Detalleplanificacionactividad

    def get_context_data(self, **kwargs):
        ctx = super(EjecutarActividad, self).get_context_data(**kwargs)
        ctx['actividad_list'] = Actividad.objects.all()
        return ctx

    def post(self, request, *args, **kwargs):
        datos_JSON = {}
        planificacion_List = []
        try:
            usuario = json.loads(request.POST['usuario'])
            print("el usuario es: ", usuario)
            actividad_QuerySet = Actividad.objects.values('detalleplanificacionactividad__secuencial', 'nombre',  # noqa
                                                                'user_id__first_name',  # noqa
                                                                'user_id__last_name',  # noqa
                                                                'detalleplanificacionactividad__estado',  # noqa
                                                                'detalleplanificacionactividad__fechainicio',  # noqa
                                                                'detalleplanificacionactividad__fechafin').exclude(detalleplanificacionactividad__estado=None)  # noqa
            # print(actividad_QuerySet)

            for planificacion in actividad_QuerySet:
                planificacion_List.append({
                    'secuencial': str(planificacion['detalleplanificacionactividad__secuencial']),  # noqa
                    'usuario': str(planificacion['user_id__first_name'])+" " + str(planificacion['user_id__last_name']),  # noqa
                    'actividad': str(planificacion['nombre']),
                    'estado': str(planificacion['detalleplanificacionactividad__estado']),  # noqa
                    'fechainicio': str(planificacion['detalleplanificacionactividad__fechainicio']),
                    'fechafin': str(planificacion['detalleplanificacionactividad__fechafin'])  # noqa
                })

            for p in planificacion_List:
                print(p)

            datos_JSON['actividades'] = planificacion_List
            datos_JSON['result'] = "OK"  # Establecer un mensaje en el caso de un correcto proceso # noqa
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


class CambiarEstadoActividad(LoginRequiredMixin, GroupRequiredMixin, ListView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    group_required = 'jefesistemas'

    def post(self, request, *args, **kwargs):
        datos_JSON = {}
        requestData = {}

        try:
            requestData = json.loads(request.POST['estado'])
            actividadId = int(requestData["actividad"])
            estadoActividad = requestData["estadoactividad"]
            print(actividadId)
            print(estadoActividad)
            
            detalleAct = Detalleplanificacionactividad.objects.get(secuencial=actividadId)
            detalleAct.estado = estadoActividad
            
            print(detalleAct)
            detalleAct.save()
            
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
            
    def get(self, request, **kwargs):
        datos_JSON = {}
        requestData = {}
        
        try:
            requestData = json.loads(request.GET['actividad'])
            print(requestData)
            detalleAct = Detalleplanificacionactividad.objects.get(secuencial=requestData)
            
            
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
            