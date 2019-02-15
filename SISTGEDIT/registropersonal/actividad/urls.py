from django.urls import path

from .views import (ActividadFormulario, ActividadLisView, GuardarActividad,
                    TipoactividadCreate, TipoactividadDelete,
                    TipoactividadListar, TipoactividadUpdate)

# from registropersonal.sistema.models import Persona, Usuario

urlpatterns = [
    path('listar/', ActividadLisView.as_view(), name='actividad_listar'),
    path('insertar/', ActividadFormulario.as_view(),
         name='actividad_insertar'),
    path('guardar/', GuardarActividad.as_view(), name='actividad_guardar'),
    path('tipoactividad/listar/', TipoactividadListar.as_view(),
         name='tipoactividad_listar'),
    path('tipoactividad/insertar/', TipoactividadCreate.as_view(),
         name='tipoactividad_insetar'),
    path('tipoactividad/actualizar/<int:pk>/', TipoactividadUpdate.as_view(),
         name='tipoactividad_editar'),
    path('tipoactividad/eliminar/<int:pk>/', TipoactividadDelete.as_view(),
         name='tipoactividad_eliminar'),
]
