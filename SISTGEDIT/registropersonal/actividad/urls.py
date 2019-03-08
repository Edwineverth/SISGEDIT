from django.urls import path

from .views import (ActividadFormulario, ActividadLisView, GenerarTabla,
                    GuardarActividad, PlanificacionActividad,
                    PlanificacionActividadFormulario, TipoactividadCreate,
                    TipoactividadDelete, TipoactividadListar,
                    TipoactividadUpdate, GuardarPlanificacion)

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
    path('planificacion/listar/', PlanificacionActividad.as_view(),
         name='planificacion_listar'),
    path('planificacion/insertar/', PlanificacionActividadFormulario.as_view(),
         name='planificacion_insertar'),
    path('planificacion/datostabla/', GenerarTabla.as_view(),
         name='planificacion_generartabla'),
    path('planificacion/guardarplanificacion/', GuardarPlanificacion.as_view(),
         name='planificacion_guardar'),
]
