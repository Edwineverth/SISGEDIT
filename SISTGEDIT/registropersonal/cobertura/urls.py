from django.urls import path
from .views import CoberturaCreate, CoberturaUpdate, CoberturaListar, CoberturaDelete # noqa
# from registropersonal.sistema.models import Persona, Usuario

urlpatterns = [
    path('listar/', CoberturaListar.as_view(), name='cobertura_listar'),
    path('insertar/', CoberturaCreate.as_view(), name='cobertura_insetar'),
    path('actualizar/<int:pk>/', CoberturaUpdate.as_view(), name='cobertura_editar'), # noqa    path('actualizar/<int:pk>/', CoberturaUpdate.as_view(), name='cobertura_editar'), # noqa
    path('eliminar/<int:pk>/', CoberturaDelete.as_view(), name='cobertura_eliminar'), # noqa
]
