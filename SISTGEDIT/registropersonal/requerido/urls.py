from django.urls import path
from .views import RequeridoCreate, RequeridoListar, RequeridoUpdate, RequeridoDelete # noqa
# from registropersonal.sistema.models import Persona, Usuario

urlpatterns = [
    path('listar/', RequeridoListar.as_view(), name='requerido_listar'),
    path('insertar/', RequeridoCreate.as_view(), name='requerido_insetar'),
    path('actualizar/<int:pk>/', RequeridoUpdate.as_view(), name='requerido_editar'), # noqa    path('actualizar/<int:pk>/', RequeridoUpdate.as_view(), name='Requerido_editar'), # noqa
    path('eliminar/<int:pk>/', RequeridoDelete.as_view(), name='requerido_eliminar'), # noqa
]
