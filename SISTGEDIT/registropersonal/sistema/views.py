from django.shortcuts import render, redirect
from .models import Persona
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from registropersonal.sistema.forms import SignUpForm


@login_required(login_url='/accounts/login')
def presentacion(request):
    person_list = Persona.objects.all()
    return render(request, 'sistema/index.html', {'person_list': person_list})


@login_required(login_url='/accounts/login')
def home(request):
    # person_list = Persona.objects.all()
    return render(request, 'home.html', {})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.cargo = form.cleaned_data.get('cargo')
            user.profile.numerotelefono = form.cleaned_data.get('numerotelefono')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/registro.html', {'form': form})
