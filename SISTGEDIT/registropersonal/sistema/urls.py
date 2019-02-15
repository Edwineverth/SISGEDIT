# from django.contrib import admin
from django.urls import path
from .views import presentacion

urlpatterns = [
    path('sistema/', presentacion, name='sistema'),
]
