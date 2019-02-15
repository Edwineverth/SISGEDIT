# from django.shortcuts import render

from registropersonal.sistema.models import Requerido
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

# Clase que se encarga de listar las personas y usuarios dentro del sistema


class RequeridoCreate(CreateView):
    model = Requerido
    fields = ['nombre', 'descripcion', 'estado']
    template_name='requerido/insertar.html'# noqa
    success_url= reverse_lazy('requerido_listar')# noqa


class RequeridoListar(ListView):
    context_object_name='requerido_list' # noqa
    model = Requerido
    template_name='requerido/listar.html'# noqa


class RequeridoUpdate(UpdateView):
    model = Requerido
    template_name='requerido/actualizar.html'# noqa
    fields = ['nombre', 'descripcion', 'estado']
    success_url= reverse_lazy('requerido_listar')# noqa


class RequeridoDelete(DeleteView):
    model = Requerido
    context_object_name="requerido" # noqa
    template_name='requerido/eliminar.html'# noqa
    success_url= reverse_lazy('requerido_listar')# noqa
