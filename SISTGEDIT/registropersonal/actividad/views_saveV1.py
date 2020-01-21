"""
# from django.shortcuts import render
import json
from datetime import datetime

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from registropersonal.sistema.models import (Actividad, Requerido,
                                             Tipoactividad, Usuario, Cobertura)

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
        return ctx


class ActividadFormulario(ListView):
    template_name = "actividad/insertar.html"
    context_object_name = "usuario_list"
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super(ActividadFormulario, self).get_context_data(**kwargs)
        context['cobertura_list'] = Cobertura.objects.all()
        context['requerido_list'] = Requerido.objects.all()
        return context


class GuardarActividad(TemplateView):
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        datos = json.loads(request.GET['actividad'])
        _transaccion = transaction.savepoint()
        try:
            for actividad in datos["actividad"]:
                nombre = actividad["nombre"]
                descripcion = actividad["descripcion"]
                fechainicio = actividad["fechainicio"]
                fechafin = actividad["fechafin"]
                usuario = int(actividad["usuario"])
                cobertura = int(actividad["cobertura"])
                requerido = int(actividad["requerido"])
            fechainicio_array = fechainicio.split("/")
            fechafin_array = fechafin.split("/")
            diferencia = (datetime(int(fechafin_array[2]),
                                   int(fechafin_array[0]),
                                   int(fechafin_array[1]))) - (datetime(int(
                                       fechainicio_array[2]),
                                       int(
                                       fechainicio_array[0]),
                                       int(fechainicio_array[1])))

            fi = datetime.strptime(fechainicio, '%m/%d/%Y')
            ff = datetime.strptime(fechafin, '%m/%d/%Y')
            actividad = Actividad(nombre=nombre, descripcion=descripcion,
                                  duracion=int(diferencia.days),
                                  fechainicio=fi.strftime("%Y-%m-%d"),
                                  fechafin=ff.strftime("%Y-%m-%d"),
                                  secuencial_usuario=Usuario.objects.get(
                                      secuencial=usuario),
                                  secuencial_covertura=Cobertura.objects.get(
                                      secuencial=cobertura),
                                  secuencial_requerido=Requerido.objects.get(
                                      secuencial=requerido))
            actividad.save()
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
"""
