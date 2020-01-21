# from django.contrib import admin
from django.urls import path, include
from .views import presentacion, home, signup

urlpatterns = [
    path('sistema/', presentacion, name='sistema'),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
]
