# from django.shortcuts import render
from registropersonal.sistema.models import Persona, Usuario
import json
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.db import transaction
from django.contrib import messages

# Clase que se encarga de listar las personas y usuarios dentro del sistema


class listarPersonas(TemplateView):
    template_name = "persona/listarpersona.html"


class presentarFormularioPersonaView(TemplateView):
    template_name = "persona/crearpersona.html"


class personaListView(ListView):
    context_object_name='person_list' # noqa
    model = Persona
    template_name = "persona/listarpersona.html"


class insertarpersona(TemplateView):
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        datos = json.loads(request.GET['person'])
        _transaccion = transaction.savepoint()
        try:
            for person in datos["person"]:
                nombre = person["nombre"]
                apellidos = person["apellido"]
                usuario = person["usuario"]
                password = person["password"]
                puesto = person["puesto"]
            estado = True
            persona = Persona(
                nombre=nombre, apellidos=apellidos, puesto=puesto, estado=estado)# noqa
            persona.save()
            idpersona = Persona.objects.get(secuencial=persona.secuencial)
            usuarioObjetc = Usuario(usuario=usuario, password=password,
                                    estado=estado, secuencial_persona=idpersona)# noqa
            usuarioObjetc.save()
            transaction.savepoint_commit(_transaccion)
            datos['result'] = "OK"
            datos['message'] = "¡Registro de usuario  guardado correctamente!"
            messages.add_message(request, messages.SUCCESS, datos['message'])
            return HttpResponse(
                json.dumps(datos), content_type="application/json")
        except Exception as error:
            print("Error al guardar-->transaccion" + str(error))
            transaction.savepoint_rollback(_transaccion)
            datos['message'] = "¡Ha ocurrido un error al tratar de ingresar los datos de la persona!"# noqa
            datos['result'] = "X"
            return HttpResponse(
                json.dumps(datos), content_type="application/json")
