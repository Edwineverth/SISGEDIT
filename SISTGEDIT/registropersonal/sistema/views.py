from django.shortcuts import render
from .models import Persona
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login')
def presentacion(request):
    person_list = Persona.objects.all()
    return render(request, 'sistema/index.html', {'person_list': person_list})


def home(request):
    # person_list = Persona.objects.all()
    return render(request, 'home.html', {})
