from django.urls import path
from .views import FeriadosListar, FeriadosCreate, FeriadosUpdate, FeriadosDelete  # noqa
# from registropersonal.sistema.models import Persona, Usuario

urlpatterns = [
    path('listar/', FeriadosListar.as_view(), name='feriados_listar'),
    path('insertar/', FeriadosCreate.as_view(), name='feriados_insetar'),
    path('actualizar/<int:pk>/', FeriadosUpdate.as_view(), name='feriados_editar'), # noqa    path('actualizar/<int:pk>/', FeriadosUpdate.as_view(), name='Feriados_editar'), # noqa
    path('eliminar/<int:pk>/', FeriadosDelete.as_view(), name='feriados_eliminar'), # noqa
]
