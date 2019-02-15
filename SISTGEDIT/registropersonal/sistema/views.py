from django.shortcuts import render
from .models import Persona


def presentacion(request):
    person_list = Persona.objects.all()
    return render(request, 'sistema/index.html', {'person_list': person_list})
