# from django.shortcuts import render

from registropersonal.sistema.models import Feriados
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

# Clase que se encarga de listar las personas y usuarios dentro del sistema


class FeriadosCreate(CreateView):
    model = Feriados
    fields = ['nombre', 'descripcion', 'fechainicio', 'fechafin', 'estado']
    template_name='feriados/insertar.html'# noqa
    success_url= reverse_lazy('feriados_listar')# noqa


class FeriadosListar(ListView):
    context_object_name='feriados_list' # noqa
    model = Feriados
    template_name='feriados/listar.html'# noqa


class FeriadosUpdate(UpdateView):
    model = Feriados
    template_name='feriados/actualizar.html'# noqa
    fields = ['nombre', 'descripcion', 'fechainicio', 'fechafin', 'estado']
    success_url= reverse_lazy('feriados_listar')# noqa


class FeriadosDelete(DeleteView):
    model = Feriados
    context_object_name="feriados" # noqa
    template_name='feriados/eliminar.html'# noqa
    success_url= reverse_lazy('feriados_listar')# noqa
