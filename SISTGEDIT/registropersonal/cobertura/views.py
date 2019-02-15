# from django.shortcuts import render

from registropersonal.sistema.models import Cobertura
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

# Clase que se encarga de listar las personas y usuarios dentro del sistema


class CoberturaCreate(CreateView):
    model = Cobertura
    fields = ['nombre', 'descripcion', 'estado']
    template_name='cobertura/insertar.html'# noqa
    success_url= reverse_lazy('cobertura_listar')# noqa


class CoberturaListar(ListView):
    context_object_name='cobertura_list' # noqa
    model = Cobertura
    template_name='cobertura/listar.html'# noqa


class CoberturaUpdate(UpdateView):
    model = Cobertura
    template_name='cobertura/actualizar.html'# noqa
    fields = ['nombre', 'descripcion', 'estado']
    success_url= reverse_lazy('cobertura_listar')# noqa


class CoberturaDelete(DeleteView):
    model = Cobertura
    context_object_name="cobertura" # noqa
    template_name='cobertura/eliminar.html'# noqa
    success_url= reverse_lazy('cobertura_listar')# noqa
